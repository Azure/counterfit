from collections import OrderedDict, namedtuple
import json
import os
import pytest
import tests.utils.helpers as hp

@pytest.fixture(scope='function', autouse=True)
def test_data(request, load_module_test_data):
    """gets only required portion from module test data dictionary as test object"""
    return hp.extract_test_data(request.node.originalname, load_module_test_data)

@pytest.fixture(scope='module', autouse=True)
def load_module_test_data(request, load_session_test_data):
    """gets only required portion from session test data dictionary"""
    key = request.module.__name__
    if key not in load_session_test_data:
        return {}
    return load_session_test_data[request.module.__name__]

@pytest.fixture(scope='session', autouse=True)
def load_session_test_data():
    """loads test data from json as dictionary"""
    folder_path = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(folder_path, *["tests", "test_data"])
    file = os.path.join(folder, "config.json")
    with open(file) as fp:
        data = json.load(fp)
    return data