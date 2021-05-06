import argparse
import cmd2
from counterfit.core.run_scan_utils import get_run_summary, get_printable_run_summary
from counterfit.core.state import CFState

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--log", action="store_true", help="log all actions")


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_run(self, args):
    """run an active attack against an active target, using parameters set by "set".
    Requires
    *  "interact <target>"
    *  "use <attack>"
    Default parameters may be override via "set param1=val1 param2=val2"
    """
    if CFState.get_instance().active_target is None:
        self.pwarning("\n [!] Not interacting with a target. Set the active target with `interact`.\n")
        return

    if CFState.get_instance().active_target.active_attack is None:
        self.pwarning("\n [!] No attack specified. Set the active attack with 'use'.\n")
        return

    if (
        CFState.get_instance().active_target.model_data_type
        not in CFState.get_instance().active_target.active_attack.tags
    ):
        self.pwarning(
            f"Error: innappropriate attack for target {CFState.get_instance().active_target.model_name}"
        )
        print()
        self.pwarning(
            f"{CFState.get_instance().active_target.model_name} is of data type {CFState.get_instance().active_target.model_data_type}"
        )
        self.pwarning(
            f"but, {CFState.get_instance().active_target.active_attack.attack_name} is for models with:"
        )
        for tag in CFState.get_instance().active_target.active_attack.tags:
            self.pwarning(f"\t{tag}")

        return

    self.poutput(
        f"\n[+] Running {CFState.get_instance().active_target.active_attack.attack_name} on {CFState.get_instance().active_target.model_name}\n"
    )

    CFState.get_instance().active_target.set_attack_samples(
        CFState.get_instance().active_target.active_attack.sample_index
    )
    # Run init_attack followed by run_attack
    CFState.get_instance().active_target.init_run_attack()
    CFState.get_instance().active_target.run_attack(logging=args.log)

    summary = get_run_summary(CFState.get_instance().active_target)
    self.poutput(get_printable_run_summary(summary))    
