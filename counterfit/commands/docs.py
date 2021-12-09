import argparse
from cmd2 import with_category
from cmd2 import with_argparser
import subprocess
from subprocess import DEVNULL, STDOUT
from counterfit.core.output import CFPrint

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", default="2718")
parser.add_argument("-a", "--address", default="127.0.0.1")

@with_argparser(parser)
@with_category("Counterfit Commands")
def do_docs(self, args: argparse.Namespace):
    """Start a local web server that hosts the documentation

    Args:
        port (str): the port to open.
        address (str): the ip address to host on.
    """
    try:
        subprocess.Popen(["python", f"docs/server.py --port {args.port} --address {args.address}"],
                         stdout=DEVNULL, stderr=STDOUT)

        CFPrint.success("started server on http://127.0.0.1:5000/index.html")
    except Exception as e:
        CFPrint.error(f"Failed to start server: {e}")
