import argparse
import cmd2

from counterfit.core.state import CFState

parser = argparse.ArgumentParser()
parser.add_argument("target", choices=CFState.get_instance().loaded_targets.keys())


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_interact(self, args):
    """Sets the active target."""

    CFState.get_instance().set_active_target(args.target)
