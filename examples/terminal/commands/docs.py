import argparse
import cmd2
import subprocess
from subprocess import DEVNULL, STDOUT
from counterfit.core.output import CFPrint


def docs_cmd(args: argparse.Namespace) -> None:
    """Start a local web server that hosts the documentation

    Args:
        port (str): the port to open.
        address (str): the ip address to host on.
    """
    port = args.port
    addr = args.address
    cmd = ["python", f"docs/server.py --port {port} --address {addr}"]
    try:
        subprocess.Popen(cmd, stdout=DEVNULL, stderr=STDOUT)
    except Exception as e:
        CFPrint.error(f"Failed to start server: {e}")
    CFPrint.success("started server on http://127.0.0.1:5000/index.html")


docs_args = cmd2.Cmd2ArgumentParser()
docs_args.add_argument("-p", "--port", default="5000")
docs_args.add_argument("-a", "--address", default="127.0.0.1")
