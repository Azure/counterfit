import argparse
import json
import os
import sys
import cmd2
import requests
from counterfit.core.state import CFState
import os

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", type=str, help="Username")
parser.add_argument("-k", "--apitoken", type=str, help='API token inside double quotes, e.g., "0123456789abcdef0123456789abcdef"')

@cmd2.with_argparser(parser)
@cmd2.with_category("ML Security Evasion Competition Commands")
def do_phish_upload(self, args):
    """Upload password protected zipfile of html files to mlsec.io/api/one_zip
    Requires
    *  "interact <target>"
    """
    api_token = args.apitoken or os.getenv('API_TOKEN')
    user = args.user or os.getenv('USERNAME')

    ZIP_END_POINT = 'https://api.mlsec.io/api/phish/post_one_zip/new/'
    if api_token is None or user is None:
        self.perror("\n [!] Please set api_token and user parameter to upload the zip file using `upload -u 'USERNAME' -k 'APITOKEN'`  Alternatively, use `mlsec_creds` to set `USERNAME` and `API_TOKEN` environmental variables.  This information can be found at https://mlsec.io/myuser/.\n")
        return
    if not CFState.get_instance().active_target:
        self.pwarning("\n [!] Not interacting with a target. Set the active target with `interact`.\n")
        return
    module_path = "/".join(CFState.get_instance().active_target.__module__.split(".")[:-1])
    if "results" not in os.listdir(module_path):
        self.pwarning("\n [!] Load the `mlsecevade` framework and run the attack using `run`.\n")
        return

    filename = f"{module_path}/results/{CFState.get_instance().active_target.model_name}.zip"
    # form_dict = create_form_object(user, filename)
    params = (
    ('url', '/zipfile/'),
    ('api_token', api_token),
    )
    data = {'name': user}
    
    files = {'path': open(filename, 'rb')}
    r = requests.post(ZIP_END_POINT, params=params, data=data, files=files)
    if r.ok:
        self.poutput(f"\n[+] Successfully uploaded {filename}\n")
    else:
        self.poutput(r.status_code)
