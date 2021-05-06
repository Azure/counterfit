import cmd2
import argparse
from counterfit.core.state import CFState

parser = argparse.ArgumentParser()
# including this print the correct help message


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_back(self, args):
    """
    Exits the active attack or target.
    """

    if not CFState.get_instance().active_target.active_attack:
        self.poutput(f"\n[+] Exiting {CFState.get_instance().active_target.model_name}\n")
        CFState.get_instance().active_target = None
    else:
        self.poutput(f"\n[+] Exiting {CFState.get_instance().active_target.active_attack.attack_id}\n")
        CFState.get_instance().active_target.active_attack = None
