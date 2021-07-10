import datetime
import functools
import os
import time
from collections import namedtuple

import numpy as np
import shutil
import tempfile
import pyminizip
from counterfit.core import enums, wrappers
from counterfit.core.interfaces import AbstractTarget
from PIL import Image
from secml.array import CArray
from secml_malware.attack.blackbox.ga.c_base_genetic_engine import \
    CGeneticAlgorithm
from tqdm import tqdm

PE_MALWARE_FOLDER = 'pe_malware'

Query = namedtuple('Query', ['input', 'output', 'label'])


class Target(AbstractTarget):
    """Parent class for all targets"""
    # member variables expected
    active_attack = None
    model = None
    clip_values = None
    channels_first = True
    attacks = {}

    # for metrics
    num_evaluations = 0
    actual_evaluations = 0

    # optional cache
    cache = {}

    # Attack management
    def get_attacks(self, status=None):
        if not status:
            return self.attacks

        if status not in enums.AttackStatus:
            print(f"[!] {status} not understood")
            return False

        else:
            return {k: v for (k, v) in self.attacks.items() if v.status == status}

    def set_attack_samples(self, index=0):
        if hasattr(index, "__iter__"):
            # (unused) multiple index
            out = np.array([self.X[i] for i in index])
            batch_shape = (-1,) + self.model_input_shape
        elif type(self.X[index]) is str:
            # array of strings (textattack)
            out = np.array(self.X[index])
            batch_shape = (-1,)
        else:
            # array of arrays (art)
            out = np.atleast_2d(self.X[index])
            batch_shape = (-1,) + self.model_input_shape

        self.active_attack.sample_index = index
        self.active_attack.samples = out.reshape(batch_shape)

    def check_attack_success(self):
        new_labels = np.atleast_1d(
            self.active_attack.results['final']['label'])
        old_labels = np.atleast_1d(
            self.active_attack.results['initial']['label'])

        # successful
        if self.active_attack.parameters.get("targeted", False):
            # compare all new labels to all target classes (both as np arrays)
            return new_labels == np.array(self.model_output_classes)[self.active_attack.target_class]
        else:
            return new_labels != np.array(old_labels)

    def outputs_to_labels(self, output):
        # default multiclass label selector via argmax
        # user can override this function if, for example, one wants to choose a specific threshold
        output = np.atleast_2d(output)
        return [self.model_output_classes[i] for i in np.argmax(output, axis=1)]

    @staticmethod
    def _key(array):
        return np.array(array).data.tobytes()

    def _submit_with_cache(self, batch_input):
        # submit to model, with caching
        self.num_evaluations += len(batch_input)
        submit_batch, index, output = [], [], []
        for i, array in enumerate(batch_input):
            key = self._key(array)
            if key in self.cache:
                output.append(self.cache[key])
            else:
                output.append(None)
                submit_batch.append(array)
                index.append(i)

        # submit an entire batch at once for potential API efficiency
        if len(submit_batch) > 0:
            self.actual_evaluations += len(submit_batch)
            results = self.__call__(np.array(submit_batch))

            # merge new results with cached results
            for i, inp, outp in zip(index, submit_batch, results):
                key = self._key(inp)
                self.cache[key] = outp
                output[i] = outp

        return output

    def _submit(self, batch_input):
        # submit to model, without caching
        self.num_evaluations += len(batch_input)
        self.actual_evaluations += len(batch_input)
        return self.__call__(np.array(batch_input))

    def _submit_with_logging(self, batch_input, attack_name="", attack_id=""):
        timestamp = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        output = self._submit(batch_input)  # call the model predict function
        # get labels based on output(probabilities)
        label = self.outputs_to_labels(output)

        for _inp, _outp, _lab in zip(batch_input, output, label):
            log_entry = {
                "timestamp": timestamp,
                "model_id": self.model_name,
                "attack_name": attack_name,
                "attack_id": attack_id,
                "input": np.array(_inp).flatten().reshape(-1).tolist(),
                "output": _outp,
                "label": _lab,
            }

            self.active_attack.append_log(log_entry)

        return output

    def _get_query(self, batch):
        inp = batch
        outp = self._submit(inp)
        # call the model predict function and send perturbed text
        labels = np.atleast_1d(self.outputs_to_labels(outp))
        # convert to named-tuple in raw list format (JSON compatibility)
        return Query(np.array(inp).tolist(),
                     np.array(outp).tolist(),
                     np.array(labels).tolist())

    def _save_image(self, array, suffix='', extension='png', filename=None):
        assert self.model_data_type == "image", "Saving non-'image' types as an image is not supported"
        module_path = "/".join(self.__module__.split(".")[:-1])
        if filename is None:
            filename = f"{module_path}/results/{self.model_name}-{self.active_attack.attack_id}"
            if "results" not in os.listdir(module_path):
                os.mkdir(f"{module_path}/results")
        if suffix:
            filename += f'-{suffix}'
        filename += f'.{extension}'

        array = np.array(array)
        array[np.isnan(array)] = 0  # change NaNs to 0s

        if self.clip_values[1] == 255:
            array = np.uint8(array)
        elif self.clip_values[1] == 1:
            array = np.uint8(array * 255.)
        else:
            raise ValueError(
                "Cannot determine image type from clip_values.  Expecting: (0,1) or (0,255)")

        if len(self.model_input_shape) == 3:  # color channel?
            if self.channels_first:
                # convert (C, H, W) to (H, W, C)
                array = array.transpose(1, 2, 0)
                C = self.model_input_shape[0]
            else:
                C = self.model_input_shape[-1]

            im = Image.fromarray(
                array.squeeze(), mode='L' if C == 1 else 'RGB')

        elif len(self.model_input_shape) == 2:  # grayscale
            im = Image.fromarray(array, 'L')

        else:
            raise ValueError(
                "Expecting at least 2-dimensional image in model_input_shape")

        im.save(filename)
        return filename

    def init_run_attack(self):
        # get initial query input/output/label
        initial = self._get_query(self.active_attack.samples)
        self.active_attack.results = {'initial': initial._asdict()}

    def run_attack(self, logging=False):
        t0 = time.time()
        queries0 = self.num_evaluations
        actual_queries0 = self.actual_evaluations

        # run the attack
        resulting_samples = self._run_attack(logging)  # call the specific method

        # get result input/output/label
        final = self._get_query(resulting_samples)

        self.active_attack.results['final'] = final._asdict()

        # add timing statistics
        elapsed = time.time() - t0
        queries = self.num_evaluations - queries0
        actual_queries = self.actual_evaluations - actual_queries0
        self.active_attack.results['elapsed_time'] = elapsed
        self.active_attack.results['queries'] = queries
        self.active_attack.results['cache_hits'] = queries - actual_queries
        if self.model_data_type == 'image':
            filenames = []
            # loop over initial images
            for i, array in enumerate(self.active_attack.results['initial']['input']):
                initial_label = self.active_attack.results["initial"]["label"][i]
                filenames.append(self._save_image(
                    array, suffix=f'initial-{i}-label-{initial_label}'))
                self.active_attack.results['initial']['images'] = filenames

            filenames = []
            for i, array in enumerate(final[0]):  # loop over final images
                final_label = self.active_attack.results["final"]["label"][i]
                filenames.append(self._save_image(
                    array, suffix=f'final-{i}-label-{final_label}'))
                self.active_attack.results['final']['images'] = filenames
        elif self.model_data_type == 'PE':
            module_path = "/".join(self.__module__.split(".")[:-1])
            if "results" in os.listdir(module_path):
                shutil.rmtree(module_path+"/results", ignore_errors=True)
            filenames = []
            with tempfile.TemporaryDirectory() as tmpdirname:
                for i, array in enumerate(final[0]):  # loop over final PEs
                    final_label = self.active_attack.results["final"]["label"][i]
                    filenames.append(self._save_exe(
					array, suffix=f'final-{i}-label-{final_label}', temp_dir=tmpdirname))
                self.active_attack.results['final']['images'] = filenames
                zip_path = f"{module_path}/results/{self.model_name}.zip"
                self._create_zip_password_protected(tmpdirname, zip_path)

    def _run_attack(self, logging):
        raise NotImplementedError()

    def dump(self):
        return {"model_name": self.model_name, "attacks": [v.dump() for k, v in self.attacks.items()]}


class ArtTarget(Target):
    """Art attacks specific implementation inherits Target class"""

    def __init__(self) -> None:
        super().__init__()

    def _as_blackbox_art_target(self, logging, attack_name="", attack_id=""):
        func = functools.partial(
            self._submit_with_logging, attack_name=attack_name, attack_id=attack_id)
        return wrappers.BlackBoxClassifierWrapper(
            submit_sample=func if logging else self._submit,
            model_input_shape=self.model_input_shape,
            nb_output_classes=len(self.model_output_classes),
            clip_values=self.clip_values,
            channels_first=self.channels_first,
        )

    def _run_art_attack(self, logging):
        # Adversarial Robustness Toolkit

        # initialize attack
        attack_cls = self.active_attack.attack_cls(
            self._as_blackbox_art_target(
                logging,
                attack_name=self.active_attack.attack_name,
                attack_id=self.active_attack.attack_id,
            ),
            **self.active_attack.parameters,
        )
        if self.active_attack.parameters.get("targeted", False):
            adv_examples = attack_cls.generate(
                self.active_attack.samples, [
                    self.active_attack.target_class] * len(self.active_attack.samples)
            ).tolist()

        else:
            adv_examples = attack_cls.generate(
                self.active_attack.samples).tolist()

        self.active_attack.status = enums.AttackStatus.completed
        return adv_examples

    def _run_attack(self, logging):
        return self._run_art_attack(logging)


class TextTarget(Target):
    def __init__(self) -> None:
        super().__init__()

    def _as_blackbox_textattack_target(self, logging, attack_name="", attack_id=""):
        if logging:
            # return wrapper object with __call__ doing the logging
            func = functools.partial(
                self._submit_with_logging, attack_name=attack_name, attack_id=attack_id)
        else:
            func = self._submit

        class TextAttackWrapperObject(object):
            def __init__(self, model, logging_func):
                self.logging_func = logging_func
                self.model = model

            def __call__(self, x):
                return self.logging_func(x)

        # use wrapped __call__
        return TextAttackWrapperObject(self.model, func)

    def _run_textattack_attack(self, logging):
        # TextAttack

        # initialize attack
        attack_cls = self.active_attack.attack_cls.build(
            self._as_blackbox_textattack_target(
                logging, attack_name=self.active_attack.attack_name, attack_id=self.active_attack.attack_id
            )
        )
        # use the appropriate batch of samples
        results_iter = attack_cls.attack_dataset(
            list(zip(self.active_attack.samples.tolist(),
                     self.active_attack.results['initial']['label']))
        )

        results = [r.perturbed_text() for r in tqdm(results_iter)]

        self.active_attack.status = enums.AttackStatus.completed
        return results

    def _run_attack(self, logging):
        return self._run_textattack_attack(logging)


class SecMLMalwareTarget(Target):

    def __init__(self) -> None:
        super().__init__()

    def _save_exe(self, exe, suffix='', extension='', filename=None, temp_dir=None):
        assert self.model_data_type == "PE", "Saving non-'PE' types as an PE is not supported"
        module_path = "/".join(self.__module__.split(".")[:-1])
        if filename is None:
            filename = f"{temp_dir}/{self.model_name}-{self.active_attack.attack_id}"
            if "results" not in os.listdir(module_path):
                os.mkdir(f"{module_path}/results")
        if suffix:
            filename += f'-{suffix}'
        # filename += f'.{extension}'
        exe = exe.tondarray()[0]
        with open(filename, 'wb') as h:
            x_real = exe.astype(np.uint8).tolist()
            x_real_adv = b''.join([bytes([i]) for i in x_real])
            h.write(x_real_adv)
        return filename
    
    def _create_zip_password_protected(self, folder_path, output_path, password='infected'):
        """
        Zip the contents of an entire folder and encrypt with the password.
        """
        contents = os.walk(folder_path)
        try:
            compression_lvl = 5
            file_paths = []
            for root, folders, files in contents:
                for file_name in files:
                    abs_path = os.path.join(root, file_name)
                    file_paths.append(abs_path)
            pyminizip.compress_multiple(file_paths, [], output_path, password, compression_lvl)
        except (IOError, OSError) as io_error:
            print(io_error)

    def _submit(self, batch):
    # 'batch' can be a list of bytes or a CArray        # submit to model, without caching
        n = batch.shape[0] if hasattr(batch, 'shape') else len(batch)
        self.num_evaluations += n
        self.actual_evaluations += n
        return self.__call__(batch)

    def set_attack_samples(self, index=0):
        out = np.array([self.X[i] for i in index]) if hasattr(index, '__iter__') else [self.X[index]]
        self.active_attack.sample_index = index
        self.active_attack.samples = out

    def _create_blackbox_wrapper(self, logging):
        func = functools.partial(self._submit_with_logging, attack_name=self.active_attack.attack_name,
                                 attack_id=self.active_attack.attack_id)
        prediction_function = func if logging else self._submit

        model = wrappers.SecMLBlackBoxClassifierWrapper(
            self.model, prediction_function)
        return model

    def _run_attack(self, logging):
        model = self._create_blackbox_wrapper(logging)
        try:
            problem = self.active_attack.attack_cls(model_wrapper=model, **self.active_attack.parameters)
        except:
            from IPython import embed
            embed()
        engine = CGeneticAlgorithm(problem)

        # run Genetic Algorithm on
        adv_examples = []
        max_length = 0

        for x_i in self.active_attack.samples:
            xx = CArray(np.frombuffer(x_i, dtype='uint8'))
            y_pred, scores, adv_ds, f_opt = engine.run(xx.atleast_2d(), CArray([1]))
            adv_x = adv_ds.X[0, :]
            adv_examples.append(adv_x)
        self.active_attack.status = enums.AttackStatus.completed
        return adv_examples

    def _get_query(self, batch):
        inp = batch
        _, outp = self._submit(inp)
        try:
            labels = np.atleast_1d(self.outputs_to_labels(outp))
        except ValueError:
            from IPython import embed
            embed()

        return Query(np.array(inp).tolist(),
                     np.array(outp).tolist(),
                     np.array(labels).tolist())
