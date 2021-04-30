import random
import json

import argparse
import cmd2
from collections import defaultdict

from counterfit.core.state import CFState
from counterfit.core.run_scan_utils import get_run_summary, get_printable_run_summary, get_scan_summary, get_printable_scan_summary


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--iterations", default=1, type=int, help="number of iterations of each algorithm")
parser.add_argument(
    "-a",
    "--attack",
    default=None,
    type=str,
    nargs='+',
    choices=CFState.get_instance().loaded_attacks.keys(),
    help="choose a specific set of attacks (default: all applicable)",
)
parser.add_argument("-c", "--class-summary", action="store_true", help="also summarize scans by class label")
parser.add_argument("-l", "--log", action="store_true", help="log all actions")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose")


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_scan(self, args):
    """scan over all attacks against an active target, using random parameters
    Requires
    *  "interact <target>"
    """

    def perform_attacks_on_target(attacks, num_iters, has_logging_enabled, has_verbose_enabled):
        # loop over loaded attacks
        scans_by_attack = defaultdict(list)
        scans_by_label = defaultdict(list)
        for attack_name in attacks:
            for n in range(num_iters):
                if has_verbose_enabled:
                    self.poutput(f"\n[+] Running {attack_name} iteration {n+1} of {num_iters}")
                # set random attack algorithm parameters
                CFState.get_instance().add_attack_to_active_target(attack_name, "random")

                parameters = CFState.get_instance().active_target.active_attack.parameters
                if has_verbose_enabled:
                    self.poutput(
                        f"Parameters: {json.dumps(parameters)}"
                    )

                # set random attack sample
                CFState.get_instance().active_target.set_attack_samples(
                    random.randint(0, len(CFState.get_instance().active_target.X) - 1)
                )
                
                # Initialize the attack to obtain initail labels
                CFState.get_instance().active_target.init_run_attack()
                
                # set random target class depends on targeted or untargeted attack
                is_targeted = CFState.get_instance().active_target.active_attack.parameters.get("targeted", False)
                if is_targeted:
                    initial_labels = CFState.get_instance().active_target.active_attack.results['initial']['label']
                    target_class = random.choice(list(set(CFState.get_instance().active_target.model_output_classes).difference(set(initial_labels))))
                    target_class_idx = CFState.get_instance().active_target.model_output_classes.index(target_class)
                else:
                    target_class_idx = random.randint(
                    0, len(CFState.get_instance().active_target.model_output_classes) - 1
                )
                CFState.get_instance().active_target.active_attack.target_class = target_class_idx 

                # run the attack
                CFState.get_instance().active_target.run_attack(logging=has_logging_enabled)

                # update the status and show success
                summary = get_run_summary(CFState.get_instance().active_target)
                scans_by_attack[attack_name].append(summary)
                for lab in summary['initial_label']:
                    scans_by_label[lab].append(summary)

                if has_verbose_enabled:
                    self.poutput(get_printable_run_summary(summary))    

        # print scan summary
        summary_by_attack = {k : get_scan_summary(v) for k, v in scans_by_attack.items()}
        summary_by_label = {k : get_scan_summary(v) for k, v in scans_by_label.items()}
        printable = get_printable_scan_summary(summary_by_attack, summary_by_label if args.class_summary else None)
        self.poutput(printable)

    if CFState.get_instance().active_target is None:
        self.pwarning("\n [!] Not interacting with a target. Set the active target with `interact`.\n")
        return

    input_attack = args.attack
    num_iters = args.iterations
    has_logging_enabled = args.log
    has_verbose_enabled = args.verbose

    try:
        attacks = [get_attacks(a)[0] for a in input_attack]
    except ValueError as e:
        self.pwarning(f'\n [!] {e}\n')
        return

    # prefilter for valid attacks
    attacks = filter_valid_attacks(attacks)
    if len(attacks) == 0:
        self.pwarning("\n [!] No matching attacks found for target.  Did you load a framework?\n")
        return
    self.poutput(f'\n[+] Running these attacks {num_iters}x each:\n\t{", ".join(attacks)}\n')
    perform_attacks_on_target(attacks, num_iters, has_logging_enabled, has_verbose_enabled)


def filter_valid_attacks(attacks):
    valid_attacks = [
        attack_name
        for attack_name in attacks
        if CFState.get_instance().active_target.model_data_type
        in CFState.get_instance().loaded_attacks[attack_name].tags
    ]
    return valid_attacks


def get_attacks(input_attack):
    # Takes input attack name and returns respective attack class object
    if not input_attack:
        attacks = list(CFState.get_instance().loaded_attacks.keys())
    else:
        try:
            attack_cls = CFState.get_instance().loaded_attacks[input_attack]
        except KeyError:
            raise ValueError(f"Attack Not Found: {input_attack}")
        if CFState.get_instance().active_target.model_data_type not in attack_cls.tags:
            raise ValueError(f"Inappropriate attack for target: {input_attack}")
        attacks = [input_attack]
    return attacks
