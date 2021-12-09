import argparse
from cmd2 import Cmd2ArgumentParser, with_argparser, with_category

from counterfit.core.state import CFState

parser = Cmd2ArgumentParser()
parser.add_argument("framework", nargs='+',
                    choices=CFState.state().get_frameworks().keys())
parser.add_argument("-f", "--force-no-config", action="store_true",
                    help="Force loading framework without using config")


@with_argparser(parser)
@with_category("Counterfit Commands")
def do_load(self, args: argparse.Namespace) -> None:
    """Loads a framework.

    """

    for framework in args.framework:
        CFState.state().load_framework(framework, args.force_no_config)
