import argparse
import cmd2

from counterfit.core.state import CFState


parser = argparse.ArgumentParser()
parser.add_argument("framework", choices=CFState.get_instance().loaded_frameworks, default="art")


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_load(self, args):
    """Loads a framework.

    :param framework name: the framework to load.
    """
    CFState.get_instance().load_framework(args.framework)
