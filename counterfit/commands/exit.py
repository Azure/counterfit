import argparse
import os
import cmd2

parser = argparse.ArgumentParser()
# including this print the correct help message


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_exit(self, command):
    """
    exit counterfit
    """
    self.poutput("\n[+] Come again soon!\n")
    os._exit(0)
