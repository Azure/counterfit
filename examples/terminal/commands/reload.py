# import argparse
#
# import cmd2
# from examples.terminal.core.state import CFState
# from counterfit.core.output import CFPrint
#
#
# def reload_cmd(args: argparse.Namespace) -> None:
#     """Reload a Counterfit object
#     """
#     if args.target:
#         if not CFState.state().get_active_target():
#             CFPrint.warn("Not interacting with a target.")
#         else:
#             CFState.state().reload_target()
#             CFPrint.success("Successfully reloaded target")
#     elif args.commands:
#         self.load_commands()
#         CFPrint.success("Successfully reloaded commands")
#     else:
#         CFPrint.failed("Argument not recognized")
#
#
# reload_args = cmd2.Cmd2ArgumentParser()
# reload_args.add_argument(
#     "-c", "--commands", action="store_true", help="Reload commands")
# reload_args.add_argument(
#     "-t", "--target", action="store_true", help="Reload the active target")
# reload_args.add_argument(
#     "-f", "--framework", help="Reload a framework", choices=list(CFState.state().get_frameworks().keys()))
