from json.decoder import JSONDecodeError
import numpy as np
import tqdm
from zipfile import ZipFile
from counterfit.core.targets import ArtTarget
from counterfit.core import config
import requests
import os

MLSEC_API = 'https://api.mlsec.io/api/phish'
MLSEC_SUBMIT_API = f'{MLSEC_API}/submit_sample' + '?api_token={api_token}' + '&model={models}'  # POST
ALL_MODELS = ["00", "01", "02", "03", "04", "05", "06"]

ZIP_END_POINT = 'https://mlsec.io/static/phishing_samples_2021.zip'

def download_samples_to(filename):
    r = requests.get(ZIP_END_POINT)
    if r.ok:
        print(f"\n[+] Successfully downloaded malware samples to the location {filename}\n")
        # open method to open a file on your system and write the contents to the file location specified
        with open(filename, "wb") as code:
            code.write(r.content)
    else:
        print(r.status_code)

class MlsecPhish(ArtTarget):
    model_name = "mlsecphish"
    model_data_type = "html"
    model_endpoint = MLSEC_API
    model_input_shape = (1, )
    model_output_classes = [0, 1]

    sample_input_path = f"{config.targets_path}/mlsecphish/mlsec_phish_samples.zip"
    encryption_password = b'infected'

    X = []
    zip_info = []

    target_models = ALL_MODELS


    def __init__(self):
        if not os.path.exists(self.sample_input_path):
            download_samples_to(self.sample_input_path)

        print(f"scanning malware sample info from {self.sample_input_path}")
        with ZipFile(self.sample_input_path) as thezip:
            thezip.setpassword(self.encryption_password)
            for zipinfo in tqdm.tqdm(thezip.infolist()):
                self.zip_info.append(zipinfo)

        self.X = self.read_input_data()
    
    def read_input_data(self):
        out = []
        with ZipFile(self.sample_input_path) as thezip:
            for i in range(len(self.zip_info)):
                with thezip.open(self.zip_info[i], pwd=self.encryption_password) as thefile:
                    out.append(thefile.read())
        return out

    def set_attack_samples(self, index=0):
        # JIT loading of samples
        if hasattr(index, "__iter__"):
            # list of indices
            to_fetch = index
        else:
            to_fetch = [index]

        out = []
        
        for i in to_fetch:
            out.append(self.X[i])
        self.active_attack.sample_index = index
        self.active_attack.samples = out

    def submit_single(self, html):
        if type(html) is np.ndarray or type(html) is np.bytes_:
            html = html.item()
        query = MLSEC_SUBMIT_API.format(models=",".join(self.target_models), api_token=os.getenv('API_TOKEN'))
        resp = requests.post(url=query, data=html, headers={'Content-Type': 'application/octet-stream'})
        try:
            res = resp.json()
        except JSONDecodeError:
            raise Exception(resp.text)
        # results for model 0 are stored as res['p_mod_00'], etc.
        scores = [res[f'p_mod_{m}'] for m in self.target_models]
        return scores

    def __call__(self, x):
        scores = []

        for sample in x:
            s = np.mean(self.submit_single(sample))
            scores.append([1-s, s])

        return np.array(scores)
