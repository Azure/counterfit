import argparse
import sys

import cmd2
from examples.terminal.core.state import CFState
from counterfit.core.output import CFPrint
from rich.prompt import Prompt


def exit_cmd(args: argparse.Namespace) -> None:
    """Exit Counterfit

    Args:
        option (str): the object to exit.
    """
    option = args.option
    if option == "target":
        CFState.state().active_target = None
        return
    if option == "attack":
        CFState.state().active_target.active_attack = None
        return
    if option == "counterfit":
        while True:
            prompt = "[yellow][*][/yellow] Are you sure?"
            answer = Prompt.ask(prompt, choices=["y", "n"])
            if answer == "y":
                CFPrint.success("Come again soon!\n")
                sys.exit(0)
            else:
                break
    else:
        CFPrint.info("Argument not recognized")


exit_args = cmd2.Cmd2ArgumentParser()
exit_args.add_argument("option", choices=["counterfit", "target", "attack"])
