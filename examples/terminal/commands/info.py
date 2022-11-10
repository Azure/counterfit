import argparse

import cmd2
from counterfit.core.output import CFPrint
from examples.terminal.core.state import CFState


def info_cmd() -> None:
    """
    """
    # active_attack = CFState.state().active_attack
    active_attack = CFState.state().active_attack
    active_target = CFState.state().active_target
    # if active_target:
    #     active_attack = active_target.active_attack

    CFPrint.output(f'Active target: {active_target}')
    CFPrint.output(f'Active attack: {active_attack}')