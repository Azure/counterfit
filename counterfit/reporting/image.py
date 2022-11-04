import numpy as np
import hashlib

from counterfit.core.reporting import CFReportGenerator
from counterfit.data.image import ImageDataType
from PIL import Image
from rich.table import Table
from azure.storage.blob import BlobClient, ContentSettings
from counterfit.core.output import CFPrint
from counterfit.core.utils import (get_azure_storage_sas_uri,
                                   get_image_in_bytes, get_mime_type,
                                   get_predict_folder,
                                   is_img_save_in_azure_storage,
                                   transform_numpy_to_bytes)


class ImageReportGenerator(CFReportGenerator):
    is_img_save_in_azure_storage: bool = is_img_save_in_azure_storage()

    def __init__(self):
        super().__init__()

    @classmethod
    def printable(cls, target, batch, prefix=''):
        result = []
        i = 0
        for img_arr in batch:
            target_name = target.target_name
            _id = hashlib.md5(transform_numpy_to_bytes(
                img_arr)).hexdigest()[:8]
            basename = prefix + f"-{target_name}-{_id}-sample-{i}"
            predict_folder = get_predict_folder(target)
            filename = ImageReportGenerator.save(
                target, img_arr, results_path=predict_folder, filename=basename)
            result.append(filename)
            i += 1
        return result

    @classmethod
    def save(cls, target, array, suffix='', extension='png', results_path=None, filename=None, save_output=True):
        model_name = target.target_name
        if filename is None:
            filename = f"{model_name}-{target.target_id}"
        if suffix:
            filename += f'-{suffix}'
        filename += f'.{extension}'
        array = np.array(array)
        array[np.isnan(array)] = 0  # change NaNs to 0s
        if np.max(array) > 1.0:
            array = ImageDataType.convert_to_uint8(array)
        elif np.max(array) <= 1.0:
            array = ImageDataType.convert_to_uint8(array, 255.)
        else:
            raise ValueError("Cannot determine image type from clip_values.  Expecting: (0,1) or (0,255)")
        if len(target.input_shape) == 3:  # color channel?
            if not ImageDataType.is_channels_last(target.input_shape):
                # If channels are last. Convert to channels first
                # Squeezing the numpy array ensures that the dimensions for the array are correct.
                # E.g., an array of shape (1, 1, 28, 28) turns to shape (1, 28, 28)
                try:
                    # NOTE. This is needed for "digits_mlp> predict -i 0"
                    array = array.transpose(1, 2, 0)
                except ValueError:
                    # NOTE. This is neede for "digits_mlp>HopSkipJump:xxxx> show results"
                    array = array.squeeze(1).transpose(1, 2, 0)
            # save mode is "L" or "RGB"
            save_mode = ImageDataType.get_channels(target.input_shape)
            new_image = Image.fromarray(array.squeeze(), mode=f"{save_mode}")

        elif len(target.input_shape) == 2:  # grayscale
            new_image = Image.fromarray(array, 'L')

        else:
            raise ValueError("Expecting at least 2-dimensional image in input_shape")
        if results_path:
            filename = results_path + f'/{filename}'

        if ImageReportGenerator.is_img_save_in_azure_storage:
            try:
                content_type = get_mime_type(filename)
                content_settings = ContentSettings(content_type=f"{content_type}")
                filename = get_azure_storage_sas_uri(filename)
                blob_client = BlobClient.from_blob_url(filename)
                new_image_bytes = get_image_in_bytes(new_image)
                blob_client.upload_blob(new_image_bytes, overwrite=True, content_settings=content_settings)
            except Exception as ex:
                raise ValueError(f"Upload blob failed with exception. {ex}")
        elif save_output:
            new_image.save(filename)
        CFPrint.info(f'Image has been saved in the location {filename}')

        return filename
    
    @classmethod
    def get_run_summary(cls, cfattack):
        # count successes
        success_indicator = cfattack.success
        batch_size = len(success_indicator)
        successes = sum(success_indicator)

        # initial scores/labels
        i_0 = np.atleast_2d(cfattack.samples)
        o_0 = np.atleast_2d(cfattack.initial_outputs)
        l_0 = np.array(cfattack.initial_labels)

        # final scores/labels
        if cfattack.results is None:
            # failed attack? adopt originals
            i_f, o_f, l_f = i_0, o_0, l_0
        else:
            i_f = np.array(cfattack.results)
            o_f = np.atleast_2d(cfattack.final_outputs)
            l_f = np.array(cfattack.final_labels)

        # l2 norm
        i_0 = i_0.reshape(batch_size, -1).astype(float)
        i_f = i_f.reshape(batch_size, -1).astype(float)
        metric = "Max Abs Chg."

        max_abs_change = np.atleast_1d(abs(i_f - i_0).max(axis=-1))

        conf_0 = np.array([o_0[i][cfattack.target.output_classes.index(lab)]
                           for i, lab in enumerate(l_0)])

        conf_f = np.array([o_f[i][cfattack.target.output_classes.index(lab)]
                           for i, lab in enumerate(l_f)])

        degenerate = np.logical_and(l_0 != l_f, success_indicator == True)
        run_summary = {
            'batch_size': batch_size,
            'successes': successes,
            'input_change': max_abs_change,
            'input_change_metric': metric,
            'initial_confidence': conf_0,
            'final_confidence': conf_f,
            'initial_label': l_0,
            'final_label': l_f,
            'sample_index': np.atleast_1d(cfattack.options.cf_options["sample_index"]["current"]),
            'type': cfattack.target.data_type,
            'result': '',
            # 'result': filename,
            'elapsed_time': cfattack.elapsed_time,
            'queries': cfattack.logger.num_queries,
            'attack_name': cfattack.name,
            'attack_id': cfattack.attack_id,
            'parameters': cfattack.options.attack_parameters,
            'targeted': cfattack.options.attack_parameters['targeted'] if 'targeted' in cfattack.options.attack_parameters.keys() else False,
            'target_label': cfattack.options.attack_parameters['target_labels'] if 'targeted' in cfattack.options.attack_parameters.keys() else "",
            'degenerate': degenerate
        }
        return run_summary

    @classmethod
    def print_run_summary(cls, summary):
        stats_table = Table(header_style="bold magenta")
        stats_table.add_column("Success", no_wrap=True)
        stats_table.add_column("Elapsed time", no_wrap=True)
        stats_table.add_column("Total Queries", no_wrap=True)

        if summary['elapsed_time'] > summary['queries']:
            query_rate = summary['elapsed_time'] / summary['queries']
            units = 'sec/query'
        else:
            query_rate = summary["queries"] / summary["elapsed_time"]
            units = "query/sec"

        stats_table.add_row(f"{summary['successes']}/{summary['batch_size']}",
                            f"{summary['elapsed_time']:.1f}", f"{summary['queries']:.0f} ({query_rate:.1f} {units})")

        CFPrint.output(stats_table)

        table = Table(header_style="bold magenta")
        metric = summary["input_change_metric"]
        table.add_column("Sample Index")
        table.add_column("Input Label (conf)")
        table.add_column("Adversarial Label (conf)")
        table.add_column(f"{metric}")
        table.add_column("Adversarial Input", width=110)
        table.add_column("Success")

        # si = summary
        si = 0
        li = int(summary["initial_label"].tolist()[0])
        conf_0 = float(summary["initial_confidence"].tolist()[0])
        lf = int(summary["final_label"].tolist()[0])
        conf_f = float(summary["final_confidence"].tolist()[0])
        change = float(summary["input_change"].tolist()[0])
        res = summary["result"]
        d = summary["degenerate"]

        label_confidence = f"{li} ({conf_0:.4f})"
        final_confidence = f"{lf} ({conf_f:.4f})"
        table.add_row(
            str(si),
            str(label_confidence),
            str(final_confidence),
            str(round(change, 4)),
            str(res),
            str(d)
        )

        CFPrint.output(table)