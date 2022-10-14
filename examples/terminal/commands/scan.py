import argparse
import uuid
from typing import List
from unittest import result

import cmd2
from examples.terminal.core.state import CFState
from counterfit import CFPrint, Counterfit
from counterfit.core.optimize import optimize


# return a list of attack names
def get_attacks():
    frameworks = CFState.state().get_frameworks()
    attacks = []
    for framework_name, framework in frameworks.items():
        for temp_attack in list(framework["attacks"].keys()):
            attacks.append(temp_attack)
    return attacks



def scan_cmd(args: argparse.Namespace) -> None:
    target = CFState.state().get_active_target()
    if not target:
        CFPrint.warn("Active target not set. Try 'set_attack <target>")
        return

    CFPrint.success(f"Scanning Target: {target.target_name} ({target.target_id})")
    scan_id = uuid.uuid4().hex[:8]
    for attack in args.attacks:
        if args.optimize:
            optimize(scan_id=scan_id, target=target, attack=attack, num_iters=args.num_iters)
        else:
            results = {}
            for attack in args.attacks:
                cfattack = Counterfit.build_attack(target, attack)
                Counterfit.run_attack(cfattack)
                results[cfattack.attack_id] = cfattack.final_outputs



description = " Run multiple attack for the current target."
scan_args = cmd2.Cmd2ArgumentParser(description=description)
scan_args.add_argument(
    "-a", "--attacks",
    nargs='+',
    required=True,
    choices=get_attacks(),
    help="The list of attacks to run")
scan_args.add_argument(
    "-o", "--optimize",
    action="store_true",
    help="How attack parameters are selected")
scan_args.add_argument(
    "-i", "--num_iters",
    type=int,
    default=1)
scan_args.add_argument(
    "-v", "--verbose",
    action="store_true")
scan_args.add_argument(
    "-s", "--summary",
    action="store_true",
    help="also summarize scans by class label")

