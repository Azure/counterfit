from numpy.core.numeric import count_nonzero
from counterfit.core.state import CFState
import argparse
import cmd2
import random
import numpy as np
from cmd2.table_creator import Column, SimpleTable, HorizontalAlignment
from typing import Any, List

from counterfit.core.run_scan_utils import get_printable_batch, printable_numpy

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--index", type=int, default=None, help="Send the selected sample to the target model")
parser.add_argument("-s", "--surprise", action="store_true", help="Send a randomly selected sample to the target model")
parser.add_argument("-r", "--result", action="store_true", help="Send the result of the active_attack to the target model")
parser.add_argument("-v", "--verbose", action="store_true")


def set_attack_samples(target, sample_index=0):
    # This function helps to directly set sample_index and samples for a target not depending on attack 
    if hasattr(sample_index, "__iter__"):
        # (unused) multiple index
        out = np.array([target.X[i] for i in sample_index])
        batch_shape = (-1,) + target.model_input_shape
    elif type(target.X[sample_index]) is str:
        # array of strings (textattack)
        out = np.array(target.X[sample_index])
        batch_shape = (-1,)
    else:
        # array of arrays (art)
        out = np.atleast_2d(target.X[sample_index])
        batch_shape = (-1,) + target.model_input_shape

    return out.reshape(batch_shape)


@cmd2.with_category("Counterfit Commands")
@cmd2.with_argparser(parser)
def do_predict(self, args):
    """Predict a single sample for the active target"""
    if CFState.get_instance().active_target is None:
        self.pwarning("\n [!] must first `interact` with a target.\n")
        return
    else:
        target = CFState.get_instance().active_target

    if sum([args.surprise, args.index is not None, args.result]) > 1:
        self.pwarning("\n [!] must specify only one of {surprise, index, result}.\n")
        return

    heading1 = "Sample Index"
    if args.surprise:
        sample_index = random.randint(0, len(target.X) - 1)
        samples = set_attack_samples(target, sample_index)

    elif args.index is not None:  # default behavior
        sample_index = args.index
        samples = set_attack_samples(target, sample_index)

    elif args.result:
        try:
            samples = target.active_attack.results['final']['input']
            sample_index = [target.active_attack.attack_id] * len(samples)
            heading1 = "Attack ID"
        except (KeyError, AttributeError):
            self.pwarning("\n [!] No results found. First 'run' an attack.\n")
            return

    elif target.active_attack is not None and target.active_attack.sample_index is not None:
        sample_index = target.active_attack.sample_index
        samples = set_attack_samples(target, sample_index)

    else:
        self.pwarning("\n [!] No index sample, setting random index.\n")
        sample_index = random.randint(0, len(target.X) - 1)
        samples = set_attack_samples(target, sample_index)
    result = target._submit(samples)

    columns: List[Column] = list()
    columns.append(
        Column(
            heading1,
            width=8,
            header_horiz_align=HorizontalAlignment.LEFT,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )

    columns.append(
        Column(
            "Sample",
            width=60,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.CENTER,
        )
    )

    columns.append(
        Column(
            "Output Scores\n" +
            str(target.model_output_classes).replace(',', ''),
            width=30,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.CENTER,
        )
    )

    if not hasattr(sample_index, "__iter__"):
        sample_index = [sample_index]

    samples_str = get_printable_batch(target, samples, sample_index, args.result)
    results_str = printable_numpy(result)

    data_list: List[List[Any]] = list()
    for idx, samp, res in zip(sample_index, samples_str, results_str):
        data_list.append([idx, samp, res])

    st = SimpleTable(columns)
    self.poutput("\n" + st.generate_table(data_list, row_spacing=0) + "\n")
