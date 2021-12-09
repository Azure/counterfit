import argparse
from cmd2 import with_argparser
from cmd2 import with_category
from counterfit.core.state import CFState
from counterfit.core.output import CFPrint


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--commands", action="store_true",
                    help="Reload commands")
parser.add_argument("-t", "--target", action="store_true",
                    help="Reload the active target")
parser.add_argument("-f", "--framework", help="Reload a framework",
                    choices=list(CFState.state().get_frameworks().keys()))


@with_argparser(parser)
@with_category("Counterfit Commands")
def do_reload(self, args: argparse.Namespace) -> None:
    """Reload a Counterfit object
    """

    if args.target:
        if not CFState.state().get_active_target():
            CFPrint.warn("Not interacting with a target.")
        else:
            CFState.state().reload_target()
            CFPrint.success("Successfully reloaded target")

    elif args.commands:
        self.load_commands()
        CFPrint.success("Successfully reloaded commands")

    elif args.framework:
        CFState.state().reload_framework(args.framework)
        CFPrint.success(f"Successfully reloaded {args.framework}")

    else:
        CFPrint.failed("Argument not recognized")
