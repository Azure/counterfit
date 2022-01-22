import argparse
import random

from cmd2 import with_argparser
from cmd2 import with_category
from rich.table import Table

from counterfit.core.output import CFPrint
from counterfit.core.state import CFState
from counterfit.report.report_generator import get_target_data_type_obj
from counterfit.report import report_generator

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--index", type=str, default=None,
                    help="Send the selected samples to the target model. Python list and range accepted.  Examples: 0, [0,1,2,3], range(5)")
parser.add_argument("-r", "--random", action="store_true",
                    help="Send a randomly selected sample to the target model")
parser.add_argument("-a", "--attack_result", action="store_true",
                    help="Send the result of the active_attack to the target model")


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


@with_category("Counterfit Commands")
@with_argparser(parser)
def do_predict(self, args: argparse.Namespace) -> None:
    """Predict a single sample for the active target.
    """

    target = CFState.state().get_active_target()
    if not target:
        CFPrint.warn(
            "No active target. Try 'interact' <target>")
        return
    heading1 = "Sample Index"
    if args.index is not None:  # default behavior
        sample_index = eval(args.index)
        samples = target.get_samples(sample_index)
        prefix = 'initial'
    elif args.attack_result:
        active_attack = target.active_attack
        if not active_attack:
            CFPrint.warn("No active attack. Try 'use' <attack>")
            return

        elif active_attack.attack_status == "complete":
            heading1 = "Attack ID"
            samples = active_attack.results
            sample_index = [target.active_attack.attack_id] * len(samples)
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
    
    result = target.predict(samples)  # results is list of probability scores
    labels = target.outputs_to_labels(result)
    target_datatype = target.target_data_type
    target_data_type_obj = get_target_data_type_obj(target_datatype)
    samples = target_data_type_obj.printable(target, samples, prefix)
    results = report_generator.printable_numpy(result)
    if not hasattr(sample_index, "__iter__"):
        sample_index = [sample_index]

    predict_table(heading1,
                  sample_index=sample_index,
                  samples=samples,
                  results=results,
                  labels=labels
                  )
