import argparse
from typing import List

import cmd2
from examples.terminal.core.state import CFState
from counterfit.core import utils
from counterfit.core.output import CFPrint


# return a list of attack names
def get_attacks():
    frameworks = frameworks = CFState.state().get_frameworks()
    attacks = []
    for framework_name, framework in frameworks.items():
        for temp_attack in list(framework["attacks"].keys()):
            attacks.append(temp_attack)
    return attacks


def set_attack_cmd(args: argparse.Namespace) -> None:
    """Select an attack to use on the active target.
    Use 'set_attack' to select a target first.
    """

    if not CFState.state().active_target:
        CFPrint.warn("Not interacting with any targets. Try interacting with a target.")
        return False

    if args.attack in CFState.state().active_target.attacks:  # existing attack
        attack = CFState.state().active_target.attacks[args.attack]
    else:
        try:
            scan_id = utils.set_id()
            new_attack = CFState.state().build_new_attack(
                target=CFState.state().active_target,
                attack=args.attack,
                scan_id=scan_id
            )
            CFState.state().set_active_attack(new_attack)

        except Exception as error:
            CFPrint.warn(f"Failed to build {args.attack}: {error}")


set_attack_args = cmd2.Cmd2ArgumentParser()
set_attack_args.add_argument(
    "attack", choices=get_attacks(), help="The attack to use, either <attack name> or <attack id>")


