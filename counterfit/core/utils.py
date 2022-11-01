# Utility functions should live here so can be used across codebase...
import datetime
import importlib
import inspect
import io
import mimetypes
import os
import uuid
import numpy as np
import pathlib
from PIL import Image

def param_floats_to_ints(parameters: dict) -> dict:
    """Convert floats to integers

    Args:
        parameters (dict): The dictionary of parameters

    Returns:
        [type]: [description]
    """
    new_parameters = {}
    for k, v in parameters.items():
        if isinstance(v, float) and v < np.inf:
            if int(v) == v:
                v = int(v)
        new_parameters[k] = v
    return new_parameters


def set_id() -> str:
    """Generate a random 8 char id

    Returns:
        str: A random 8 char id.
    """
    return uuid.uuid4().hex[:8]


def import_subclass(import_path:str, subcls: object) -> dict:
    """Import core modules based on path and subclass.

    Args:
        import_path (str): path of where the modules a
        subcls (object): The parent class to load.

    Returns:
        dict: Dictionaary of class paths. 
    """
    modules = {}

    for module in os.listdir(import_path):
        if not os.path.isdir(f"{import_path}/{module}"):
            continue

        for target in os.listdir(f"{import_path}/{module}"):
            if target == "__init__.py" or target[-3:] != ".py":
                continue
            else:
                target_module = ".".join(
                    f"{import_path}/{module}/{target[:-3]}".split("/"))
                targetcls = importlib.import_module(target_module)
                for _, obj in inspect.getmembers(targetcls):
                    if inspect.isclass(obj):
                        if issubclass(obj, subcls) and obj is not subcls:
                            modules[target[:-3]] = obj
    return modules


def get_subclasses(class_name):
    """Find all the subclasses of a class given its name"""
    return class_name.__subclasses__()


def get_timestamp():
    return datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")


def transform_numpy_to_bytes(arr):
    return np.array(arr).data.tobytes()


def get_predict_folder(target):
    module_path = "/".join(target.__module__.split(".")[:-1])

    if "results" not in os.listdir(module_path):
        os.mkdir(f"{module_path}/results")
    if 'predict' not in os.listdir(f"{module_path}/results"):
        os.mkdir(f"{module_path}/results/predict")

    results_folder = f"{module_path}/results/predict"
    return results_folder


def install_path(path) -> pathlib.Path:
    return pathlib.Path(os.path.join("counterfit", path)).resolve()


def is_img_save_in_azure_storage() -> bool:
    """Checks if Azure environment variables are set.

    Returns:
        bool: Returns True if Azure environment variables are set, otherwise False
    """
    return True if "AzureStorageAccountName" and "AzureStorageContainerName" in os.environ else False


def get_azure_storage_sas_uri(filename: str) -> str:
    """Generate Azure Storage SAS URI based on Azure Storage Account, Azure Storage SAS token, and file path

    Args:
        filename (str): relative path of the file

    Returns:
        str uri: Azure Storage SAS URI
    """
    if filename == "":
        raise ValueError("filename should not be empty.")
    azure_storage_account_name = os.environ["AzureStorageAccountName"]
    azure_storage_sas_token = os.environ["AzureStorageContainerAccessToken"]
    azure_storage_sas_uri = f"https://{azure_storage_account_name}.blob.core.windows.net/{filename}?{azure_storage_sas_token}"
    return azure_storage_sas_uri


def get_image_in_bytes(image:Image, format: str='png') -> bytes:
    """ Convert a PIL.Image to bytes

    Args:
        image (PIL.Image): The input image.
        format (str): The input file format (default 'png').

    Returns:
        bytes: the image as raw bytes.
    """
    buf = io.BytesIO()
    image.save(buf, format=format)  # In the above code, we save the image Image object into BytesIO object buffer
    im = buf.getvalue()
    return im


def get_mime_type(url: str) -> str:
    """ Get MIME type based on a given url name

    Example:
        "input_example.json" -> application/json, image/jpeg, image/png
    """
    content_type = mimetypes.guess_type(url)
    if not content_type[0]:
        raise ValueError(f'Invalid MIME type detected for the URL {url}. \
            Please provide a valid URL with valid extension.')
    return content_type[0]
