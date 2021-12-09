import argparse
from cmd2 import with_category
from cmd2 import with_argparser
from counterfit.core.state import CFState

def get_targets():
    return CFState.state().list_targets()

parser = argparse.ArgumentParser()
parser.add_argument("target", choices=get_targets())

@with_argparser(parser)
@with_category("Counterfit Commands")
def do_interact(self, args: argparse.Namespace) -> None:
    """Sets the the active target. 

    Args:
        target (str): The target to interact with.
    """

    # Load the target
    target = CFState.state().load_target(args.target)

    # Set it as the active target
    CFState.state().set_active_target(target)
