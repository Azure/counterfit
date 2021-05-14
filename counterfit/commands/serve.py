from counterfit.core.state import CFState
from counterfit.core.server import Server

import argparse
import cmd2


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=13337, help="The port to run the server on.")
parser.add_argument("-s", "--start", action="store_true", help="Start the REST API server.")
parser.add_argument("-t", "--terminate", action="store_true", help="Stop the REST API server.")




@cmd2.with_category("Counterfit Commands")
@cmd2.with_argparser(parser)
def do_serve(self, args):
    """Servepredictions with a REST API"""
    if args.start:
        port = args.port
        self.pwarning("\n Starting the server on port {}.".format(port))
        try:
            server = Server.get_instance(port=port)
        except Server.ServerRunningException as e:
            self.pwarning("\n [!] Another server instance is already running on port {}. \n [!] Please first stop that instance with the serve -t command.".format(e))
            return
        server.serve()

    if args.terminate:
        try:
            server =Server.get_instance()
        except Server.ServerNotRunningException:
           self.pwarning("\n [!] You must launch the server before invoking the termination command.") 
           return
        self.pwarning("\n Stoping the server.")
        server.shutdown()

