import argparse
from cmd2 import with_argparser
from cmd2 import with_category

from counterfit.core.state import CFState
from counterfit.core.output import CFPrint

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", help="print a summary ", default=False)


@with_argparser(parser)
@with_category("Counterfit Commands")
def do_run(self, args: argparse.Namespace) -> None:
    """Run an attack
    """

    target_to_scan = CFState.state().get_active_target()
    if not target_to_scan:
        CFPrint.warn("Active target not set. Try 'interact <target>''")
        return

    active_attack = CFState.state().active_target.active_attack
    if not active_attack:
        CFPrint.warn("No attack specified. Try 'use <attack>''")
        return

    attack_id = CFState.state().active_target.get_active_attack()
    attack_name = active_attack.attack_name
    CFPrint.info(
        f"Running attack {attack_name} with id {attack_id} on {target_to_scan.target_name})\n")

    CFState.state().run_attack(target_to_scan.target_name, attack_id)
