import argparse

import cmd2
from examples.terminal.core.state import CFState
from counterfit.core.output import CFPrint


def save_cmd(args: argparse.Namespace) -> None:
    """Save results or parameters to disk.
    
    Args:
        results (bool): save the results from `cfattack.results`.
        parameters (bool): Save the parameters used for the attack.
    """
    if not CFState.state().active_target:
        CFPrint.warn("Not interacting with a target. Set the active target with `set_target`.")
        return
    if not CFState.state().active_attack:
        CFPrint.warn("No active attack. Set the active attack with `set_attack`.")
        return
    if not args.parameters and not args.results:
        CFPrint.warn(f"Specify the --parameters or --results flag.")
        return
    results_folder = CFState.state().active_attack.get_results_folder()
    if args.parameters:
        CFState.state().active_attack.options.save_options(f"{results_folder}/params.json")
        CFPrint.success(f"Successfully wrote {results_folder}/params.json")

    if args.results:
        CFState.state().active_attack.save_run_summary(f"{results_folder}/run_summary.json")
        CFPrint.success(f"Successfully wrote {results_folder}/run_summary.json")


save_args = cmd2.Cmd2ArgumentParser()
save_args.add_argument("-p", "--parameters", action="store_true",
                    help="Save the parameters for an attack")
save_args.add_argument("-r", "--results", action="store_true",
                    help="Save the results and metadata for an attack")

