import argparse
import json
import os
import cmd2
from counterfit.core.state import CFState

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str, help="Output file")


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_save(self, args):
    """save parameters and results (if available) of current target
    Requires
    *  "interact <target>"
    """
    if not CFState.get_instance().active_target:
        self.pwarning("\n [!] Not interacting with a target. Set the active target with `interact`.\n")
        return
    module_path = "/".join(CFState.get_instance().active_target.__module__.split(".")[:-1])
    if "results" not in os.listdir(module_path):
        os.mkdir(f"{module_path}/results")

    filename = f"{module_path}/results/{CFState.get_instance().active_target.model_name}_{CFState.get_instance().active_target.target_id}.json"
    with open(filename, "w") as outfile:
        json.dump(CFState.get_instance().active_target.dump(), outfile, indent=1)

    self.poutput(f"\n[+] Successfully wrote {filename}\n")
