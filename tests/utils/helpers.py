from collections import OrderedDict, namedtuple
from tests.mocks.targets import CreditFraud
from tests.mocks.targets import Digits
from tests.mocks.targets import DigitKeras
from tests.mocks.targets import SatelliteImages

def get_target_class(target: str):
    """loads attack-target combinations from json as dictionary"""
    target_classes = {
        "CreditFraud": CreditFraud(),
        "Digits": Digits(),
        "DigitKeras": DigitKeras(),
        "SatelliteImages": SatelliteImages()
    }
    return target_classes[target]

def extract_test_data(key: str, load_module_test_data):
    """gets only required portion from module test data dictionary as test object"""
    if key not in load_module_test_data:
        return
    return create_namedtuple_from_dict(load_module_test_data[key])


def create_namedtuple_from_dict(obj):
    """converts given list or dict to named tuples, generic alternative to dataclass"""
    if isinstance(obj, dict):
        fields = sorted(obj.keys())
        namedtuple_type = namedtuple(
            typename='test_data',
            field_names=fields,
            rename=True,
        )
        field_value_pairs = OrderedDict(
            (str(field), create_namedtuple_from_dict(obj[field]))
            for field in fields
        )
        try:
            return namedtuple_type(**field_value_pairs)
        except TypeError:
            # Cannot create namedtuple instance so fallback to dict (invalid attribute names)
            return dict(**field_value_pairs)
    elif isinstance(obj, (list, set, tuple, frozenset)):
        return [create_namedtuple_from_dict(item) for item in obj]
    else:
        return obj

