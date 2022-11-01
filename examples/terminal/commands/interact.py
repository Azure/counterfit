import argparse

import cmd2
from examples.terminal.core.state import CFState
from counterfit.core.output import CFPrint
from counterfit.core.targets import CFTarget


def get_targets():
    targets = []
    for target_name, target_obj in sorted(CFState.state().get_targets().items()):
        targets.append(target_name)
    return targets


def interact_cmd(args: argparse.Namespace) -> None:
    target_name = args.target
    try:
        target: CFTarget = CFState.state().get_targets().get(target_name, None)
        if not target:
            CFPrint.failed(f"Could not load target {target_name}")
        target.load()
        CFState.state().set_active_target(target)
    except RuntimeError as e:
        CFPrint.failed(f"Could not load {target_name}: {e}\n")


interact_args = cmd2.Cmd2ArgumentParser()
interact_args.add_argument("target", choices=get_targets())
