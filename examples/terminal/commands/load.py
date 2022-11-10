# import argparse

# import cmd2
# from counterfit.core.state import CFState


# def load_cmd(args: argparse.Namespace) -> None:
#     """Loads a framework.

#     """
#     for framework in args.framework:
#         CFState.state().load_framework(framework, args.force_no_config)


# load_args = cmd2.Cmd2ArgumentParser()
# load_args.add_argument(
#     "framework", nargs='+', choices=CFState.state().get_frameworks().keys())
# load_args.add_argument(
#     "-f", "--force-no-config", action="store_true", help="Force loading framework without using config")
