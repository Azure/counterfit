import argparse
import random

import cmd2
import counterfit.reporting as reporting
import numpy as np
from examples.terminal.core.state import CFState
from counterfit.core.output import CFPrint
from rich.table import Table

target2target_reporting = {
    'text': reporting.TextReportGenerator,
    'image': reporting.ImageReportGenerator,
    'tabular': reporting.TabularReportGenerator
}


def printable_numpy(batch):
    o = np.get_printoptions()
    np.set_printoptions(
        threshold=30,
        precision=2,
        floatmode="maxprec_equal",
        formatter=dict(float=lambda x: f"{x:4.2f}"))
    result = [str(np.array(row)).replace("\n", " ") for row in batch]
    np.set_printoptions(
        threshold=o["threshold"],
        precision=o["precision"],
        floatmode=o["floatmode"],
        formatter=o["formatter"])
    return result



def predict_table(heading1, sample_index, samples, results, labels=None):
    table = Table(header_style="bold magenta")
    table.add_column(heading1)
    table.add_column("Sample")
    if labels is not None:
        table.add_column("Label")
    table.add_column("Output Scores")

    if labels is None:
        for idx, sample, result in zip(sample_index, samples, results):
            table.add_row(str(idx), str(sample), result)
    else:
        for idx, sample, label, result in zip(sample_index, samples, labels, results):
            table.add_row(str(idx), str(sample), str(label), result)
    
    CFPrint.output(table)


def predict_cmd(args: argparse.Namespace) -> None:
    """Predict a single sample for the active target.
    """

    target = CFState.state().get_active_target()
    if not target:
        CFPrint.warn("No active target. Try 'interact' <target>")
        return
    heading1 = "Sample Index"
    # default behavior
    if args.index is not None:
        sample_index = eval(args.index)
        samples = target.get_samples(sample_index)
        prefix = 'initial'
    elif args.attack_result:
        active_attack = CFState.state().get_active_attack()
        if not active_attack:
            CFPrint.warn("No active attack. Try 'use' <attack>")
            return

        elif active_attack.attack_status == "complete":
            heading1 = "Attack ID"
            samples = active_attack.results
            sample_index = [active_attack.attack_id] * len(samples)
            prefix = 'adversarial'
        else:
            CFPrint.warn(
                "Attack not complete or no results. Please run attack using 'run'")
            return

    elif args.random:
        sample_index = random.randint(0, len(target.X) - 1)
        samples = target.get_samples(sample_index)
        prefix = "random"

    else:
        CFPrint.warn("No index sample.")
        return

    # results is list of probability scores
    result = target.predict(samples)
    labels = target.outputs_to_labels(result)
    try:
        target_reporting = target2target_reporting[target.data_type]
    except KeyError:
        dt = target.data_type
        CFPrint.warn(f'Counterfit does not support target type "{dt}"')
        return

    # return a path when image target but text when text target.
    printable_sample = target_reporting.printable(target, samples, prefix)
    results = printable_numpy(result)
    if not hasattr(sample_index, "__iter__"):
        sample_index = [sample_index]

    predict_table(
        heading1,
        sample_index=sample_index,
        samples=printable_sample,
        results=results,
        labels=labels)




predict_args = cmd2.Cmd2ArgumentParser()
predict_args.add_argument(
    "-i", "--index", type=str, default=None,
    help="Send the selected samples to the target model. Python list and range accepted.  Examples: 0, [0,1,2,3], range(5)")
predict_args.add_argument(
    "-r", "--random", action="store_true",
    help="Send a randomly selected sample to the target model")
predict_args.add_argument(
    "-a", "--attack_result", action="store_true",
    help="Send the result of the active_attack to the target model")
