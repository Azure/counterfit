import argparse
from typing import List
from cmd2 import with_argparser
from cmd2 import with_category
from counterfit.core.output import CFPrint
from counterfit.core import utils
from counterfit.core.state import CFState


# return a list of attack names
def list_attacks() -> List[str]:
    # dynamically get the list of attacks
    attack_names = list(CFState.state().get_attacks().keys())  # new attack

    # add existing attack if there's an active target
    if CFState.state().active_target and hasattr(CFState.state().active_target, 'attacks'):
        # existing attack
        attack_names += list(CFState.state().active_target.attacks.keys())
    return attack_names


parser = argparse.ArgumentParser()
parser.add_argument("attack", choices=list_attacks(),
                    help="The attack to use, either <attack name> or <attack id>")


@with_argparser(parser)
@with_category("Counterfit Commands")
def do_use(self, args: argparse.Namespace) -> None:
    """Select an attack to use on the active target.
    Use 'interact' to select a target first.
    """

    if not CFState.state().active_target:
        CFPrint.warn(
            "Not interacting with any targets. Try interacting with a target.")
        return

    if args.attack in CFState.state().active_target.attacks:  # existing attack
        attack_id = args.attack
    else:
        scan_id = utils.set_id()
        attack_id = CFState.state().build_new_attack(
            target_name=CFState.state().active_target.target_name,
            attack_name=args.attack,
            scan_id=scan_id
        )

    if attack_id is None:
        CFPrint.warn("Attack not found: {}".format(args.attack))
    else:
        CFState.state().active_target.set_active_attack(attack_id)
