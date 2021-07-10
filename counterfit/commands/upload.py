import argparse
import json
import os
import cmd2
import requests
from counterfit.core.state import CFState

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", type=str, help="Username")
parser.add_argument("-k", "--apitoken", type=str, help="API token")


# def create_form_object(username, zip_path):
#     return {'name': username, 'path': zip_path}

@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_upload(self, args):
    """Upload password protected zipfile to mlsec.io/api/one_zip
    Requires
    *  "interact <target>"
    """
    api_token = args.apitoken
    user = args.user
    # UPLOAD_API_ENDPOINT = 'https://api.mlsec.io/api/post_one_zip/new/?url=%2Fzipfile%2F&api_token={0}'.format(api_token)
    ZIP_END_POINT = 'https://api.mlsec.io/api/post_one_zip/new/'
    if not CFState.get_instance().active_target:
        self.pwarning("\n [!] Not interacting with a target. Set the active target with `interact`.\n")
        return
    module_path = "/".join(CFState.get_instance().active_target.__module__.split(".")[:-1])
    if "results" not in os.listdir(module_path):
        self.pwarning("\n [!] Run the attack using `scan`.\n")
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
