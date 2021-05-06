import cmd2
import argparse

from counterfit.core.state import CFState, Target
from counterfit.core import state


parser = argparse.ArgumentParser()
# including this print the correct help message


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_reload(self, args):
    """Reload the active target. Helpful when making changes to a target class."""
    if not CFState.get_instance().active_target:
        self.poutput("\n[!] Not interacting with a target. \n")
        return
    else:
        CFState.get_instance().reload_target()
