import os
import argparse
from rich.prompt import Prompt
from cmd2 import with_argparser
from cmd2 import with_category
from counterfit.core.state import CFState
from counterfit.core.output import CFPrint

parser = argparse.ArgumentParser()
parser.add_argument("option", choices=["counterfit", "target", "attack"])

@with_argparser(parser)
@with_category("Counterfit Commands")
def do_exit(self, args: str) -> None:
    """Exit Counterfit

    Args:
        option (str): the object to exit.
    """
    if args.option == "target":
        CFState.state().active_target = None
        return

    elif args.option == "attack":
        CFState.state().active_target.active_attack = None
        return

    elif args.option == "counterfit":
        while True:
            answer = Prompt.ask("[yellow][*][/yellow] Are you sure?", choices=["y", "n"])

            print()
            if answer == "y":
                CFPrint.success("Come again soon!\n")
                os._exit(0)
            elif answer == "n":
                return False
            else:
                return True

    else:
        CFPrint.info("Argument not recognized")
