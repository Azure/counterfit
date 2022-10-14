import argparse

import cmd2
from examples.terminal.core.state import CFState
from counterfit.core.output import CFPrint


def run_cmd(args: argparse.Namespace) -> None:
    """Run an attack
    """

    target_to_scan = CFState.state().get_active_target()
    if not target_to_scan:
        CFPrint.warn("Active target not set. Try 'interact <target>''")
        return

    active_attack = CFState.state().get_active_attack()
    CFState.state().run_attack(active_attack)



run_args = cmd2.Cmd2ArgumentParser()
run_args.add_argument("-v", "--verbose", action="store_true", help="print a summary ", default=False)
