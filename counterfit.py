import sys
import os
import warnings
import argparse

from counterfit.core.config import Config
from counterfit.core.state import CFState
from counterfit.core.terminal import Terminal

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # make tensorflow quiet
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

if sys.version_info < (3, 7):
    sys.exit("[!] Python 3.7+ is required")


def main(args):
    # create the terminal
    terminal = Terminal()

    # import targets and frameworks
    CFState.state()._init_state()

    # load commands last. Choices depend on targets and attacks.
    terminal.load_commands()

    print(Config.start_banner)

    # run the terminal loop
    sys.exit(terminal.cmdloop())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", action="store_true", help="enable debug messages")
    args = parser.parse_args()
    main(args)
