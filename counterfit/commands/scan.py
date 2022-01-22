import argparse
from cmd2 import with_argparser
from cmd2 import with_category

from collections import defaultdict

from counterfit.core.output import CFPrint
from counterfit.core.utils import set_id
from counterfit.core.state import CFState
from counterfit.report.report_generator import get_target_data_type_obj, get_scan_summary, printable_scan_summary
from counterfit.commands.use import list_attacks
from counterfit.commands.set import get_sample_index


parser = argparse.ArgumentParser()
parser.add_argument("-a", "--attacks", nargs='+', required=True, choices=list_attacks())
parser.add_argument("-o", "--options",
                    choices=["default", "random", "optimize"], default="default")
parser.add_argument("-n", "--num_iters", type=int, default=1)
parser.add_argument("-i", "--sample_index", type=str, default="0")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-s", "--summary", action="store_true", help="also summarize scans by class label")

# TODO Decouple setting options from build such that options are passed in at build time rather than during build time.


@with_argparser(parser)
@with_category("Counterfit Commands")
def do_scan(self, args):
    """[summary]

    Args:
        args.attacks (str): The list of attacks to run
        args.options (str): How attack parameters are selected
    """

    target_to_scan = CFState.state().get_active_target()
    if not target_to_scan:
        CFPrint.warn("Active target not set. Try 'interact <target>")
        return
    else:
        CFPrint.success(
            f"Scanning Target: {target_to_scan.target_name} ({target_to_scan.target_id})")

        sample_index = get_sample_index(args.sample_index)
        if sample_index is None:
            return

        scan_id = set_id()
        # loop over loaded attacks
        scans_by_attack = defaultdict(list)
        scans_by_label = defaultdict(list)
        for attack in args.attacks:
            for run in range(args.num_iters):
                attack_id = CFState.state().build_new_attack(
                    target_name=CFState.state().active_target.target_name,
                    attack_name=attack,
                    scan_id=scan_id
                )
                if attack_id is None:
                    CFPrint.warn(f"Attack not found: {attack}. Load <Framework>")
                    return
                else:
                    # create an attack
                    CFState.state().active_target.set_active_attack(attack_id)
                    # set options for this attack
                    active_attack = CFState.state().active_target.active_attack                    
                    active_attack.options.set_options({'sample_index': sample_index})
                    # run the attack
                    CFState.state().run_attack(target_to_scan.target_name, attack_id)

                    # display intermediate results
                    if args.verbose:
                        current_datatype = target_to_scan.target_data_type

                        current_dt_report_gen = get_target_data_type_obj(current_datatype)

                        summary = current_dt_report_gen.get_run_summary(active_attack)
                        current_dt_report_gen.print_run_summary(summary)
                
                # update the status and show success
                current_datatype = target_to_scan.target_data_type

                current_dt_report_gen = get_target_data_type_obj(current_datatype)

                summary = current_dt_report_gen.get_run_summary(active_attack)
                scans_by_attack[attack].append(summary)
                for lab in summary['initial_label']:
                    scans_by_label[lab].append(summary)

        # print scan summary
        summary_by_attack = {k : get_scan_summary(v) for k, v in scans_by_attack.items()}
        summary_by_label = {k : get_scan_summary(v) for k, v in scans_by_label.items()}
        
        printable_scan_summary(summary_by_attack, summary_by_label if args.summary else None)
        
