import cmd2
import argparse

from counterfit.core.state import CFState


parser = argparse.ArgumentParser()
parser.add_argument("attack", choices=CFState.get_instance().loaded_attacks.keys())
parser.add_argument("-p", "--parameters", choices=["default", "random"], default="default")


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_use(self, args):
    """Select an attack to use on the active target.
    Use 'interact' to select a target first.
    """

    if not CFState.get_instance().active_target:
        self.pwarning("\n [!] Not interacting with any targets. Try interacting with a target.\n")
        return

    CFState.get_instance().add_attack_to_active_target(args.attack, args.parameters)
