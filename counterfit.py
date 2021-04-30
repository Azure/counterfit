import sys
import os
import warnings
from counterfit.core import config
from counterfit.core.state import CFState
from counterfit.core.terminal import Terminal

if sys.version_info < (3, 7):
    print("[!] Python 3.7+ is required")
    sys.exit(1)


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # make tensorflow quiet
warnings.filterwarnings("ignore", category=FutureWarning)

if __name__ == "__main__":
    terminal = Terminal()
    num_attacks = CFState.get_instance().import_frameworks()
    num_targets = CFState.get_instance().import_targets()
    terminal.load_commands()  # load commands last. Choices depend on targets and attacks.

    print(config.start_banner)
    print(
        f"""
        [+] {num_attacks} attacks
        [+] {num_targets} targets
    """
    )

    sys.exit(terminal.cmdloop())
