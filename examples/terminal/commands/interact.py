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
    # Load the target
    target: CFTarget = CFState.state().get_targets().get(args.target, None)
    if not target:
        CFPrint.failed(f"Could not load target {args.target}")
    # try:
    #     new_target = CFState.state().build_new_target(target)
    #     CFPrint.success(f"{target.target_name} successfully loaded!")
    # except Exception as e:
    #     CFPrint.failed(f"Could not load {target.target_name}: {e}\n")
    # # Set it as the active target
    try:
        target.load()
        CFState.state().set_active_target(target)
    except RuntimeError as e:
        CFPrint.failed(str(e))


interact_args = cmd2.Cmd2ArgumentParser()
interact_args.add_argument("target", choices=get_targets())
