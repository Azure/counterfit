import os
import sys
import warnings
# make tensorflow quiet
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from examples.terminal.core.config import Config
from examples.terminal.core.terminal import Terminal

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

if sys.version_info < (3, 8):
    sys.exit("[!] Python 3.8+ is required")


def main():
    terminal = Terminal()
    print(Config.start_banner)
    sys.exit(terminal.cmdloop())


if __name__ == "__main__":
    main()
