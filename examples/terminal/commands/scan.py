import argparse
import uuid
from collections import defaultdict
from typing import Dict
import cmd2
from examples.terminal.core.state import CFState
from counterfit import CFPrint, Counterfit
from counterfit.core.optimize import optimize
from counterfit.reporting import TextReportGenerator, ImageReportGenerator, TabularReportGenerator
from counterfit.core.reporting import CFReportGenerator


attack_datatype_2_report_generator: Dict[str, CFReportGenerator] = {
    'text': TextReportGenerator,
    'image': ImageReportGenerator,
    'tabular': TabularReportGenerator
 }

# return a list of attack names
def get_attacks():
    frameworks = CFState.state().get_frameworks()
    attacks = []
    for framework_name, framework in frameworks.items():
        for temp_attack in list(framework["attacks"].keys()):
            attacks.append(temp_attack)
    return attacks


def scan_cmd(args: argparse.Namespace) -> None:
    is_verbose = args.verbose
    sample_index = args.sample_index
    num_iters = args.num_iters
    selected_attacks = args.attacks
    should_run_optimize = args.optimize
    should_summarize_by_label = args.summary
    target = CFState.state().get_active_target()
    if not target:
        CFPrint.warn("Active target not set. Try 'set_attack <target>")
        return
    CFPrint.success(f"Scanning Target: {target.target_name} ({target.target_id})")
    new_scan_id = uuid.uuid4().hex[:8]
    attack_2_summaries = defaultdict(list)
    scans_by_label = defaultdict(list)
    for attack in args.attacks:
        if should_run_optimize:
            # TODO. Move this functionality to be based on the CFOptions
            optimize(scan_id=new_scan_id, target=target, attack=attack, num_iters=num_iters, verbose=is_verbose)
            return
        else:
            if is_verbose and (num_iters > 1):
                CFPrint.warn('Argument "num_iters" ignored because it is only applied during optimization.')
            results = {}
            for curr_attack in selected_attacks:
                # TODO. Add number of iterations
                cfattack = Counterfit.build_attack(target, curr_attack)
                cfattack.options.cf_options['sample_index']['default'] = sample_index
                Counterfit.run_attack(cfattack)
                results[cfattack.attack_id] = cfattack.final_outputs
                target_data_type = target.data_type
                report_generator = attack_datatype_2_report_generator[target_data_type]
                summary = report_generator.get_run_summary(cfattack)
                attack_2_summaries[cfattack.name].append(summary)
                if is_verbose:
                    # Print the current attack summary
                    report_generator.print_run_summary(summary)
                for label in summary['initial_label']:
                    scans_by_label[label].append(summary)
    # summary_by_attack = {attack_name: CFReportGenerator.get_scan_summary(summaries) for attack_name, summaries in attack_2_summaries.items()}
    summary_by_attack = {}
    for attack_name, summaries in attack_2_summaries.items():
        summary_by_attack[attack_name] = CFReportGenerator.get_scan_summary(summaries)
    summary_by_label = {}
    for label, summaries in scans_by_label.items():
        summary_by_label[label] = CFReportGenerator.get_scan_summary(summaries)
    if should_summarize_by_label:
        CFReportGenerator.printable_scan_summary(summary_by_attack, summary_by_label)
    else:
        CFReportGenerator.printable_scan_summary(summary_by_attack)


scan_args = cmd2.Cmd2ArgumentParser(description="Run multiple attack for the current target.")
scan_args.add_argument(
    "-a", "--attacks", nargs='+', required=True, choices=get_attacks(), help="The list of attacks to run")
scan_args.add_argument(
    "-o", "--optimize", action="store_true", help="How attack parameters are selected")
scan_args.add_argument(
    "-n", "--num_iters", type=int, default=1, help="Number of iterations for the attack run.")
scan_args.add_argument(
    "-v", "--verbose", action="store_true", help="Be verbose in the output.")
scan_args.add_argument(
    "-s", "--summary", action="store_true", help="Summarize scans by class label.")
scan_args.add_argument(
    "-i", "--sample_index", type=int, default=0, help="The index for for sample to use.")
