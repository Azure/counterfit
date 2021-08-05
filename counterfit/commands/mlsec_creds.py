import argparse
import cmd2
from cmd2 import ansi
import os
from counterfit.core.state import CFState
import functools

bold_yellow = functools.partial(ansi.style, fg=ansi.fg.bright_yellow, bold=True)


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", type=str, help="Username")
parser.add_argument("-k", "--apitoken", type=str, help='API token inside double quotes, e.g., "0123456789abcdef0123456789abcdef"')


@cmd2.with_argparser(parser)
@cmd2.with_category("ML Security Evasion Competition Commands")
def do_mlsec_creds(self, args):
    """Sets the username and API key
    """
    if args.user is None or args.apitoken is None:
        self.poutput("Login to \t" + bold_yellow("https://mlsec.io/myuser/"))
        self.poutput("and enter the following information")

    username = input(bold_yellow("Nickname: ")) if args.user is None else args.user
    api_token = input(bold_yellow("API Token: ")) if args.user is None else args.apitoken

    os.environ["API_TOKEN"] = api_token
    os.environ["USERNAME"] = username

    # also, append these to the .counterfit startup script
    with open('.counterfit', 'a') as f:
        f.write(f'mlsec_creds -u {username} -k "{api_token}"\n')