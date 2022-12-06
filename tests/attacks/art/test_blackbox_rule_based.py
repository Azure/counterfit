import pytest
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from counterfit.targets import CreditFraud, Digits, DigitKeras, SatelliteImages

from counterfit import Counterfit

@pytest.fixture(params=[CreditFraud, Digits, DigitKeras, SatelliteImages])
def target(request):
    yield request.param

# Evasion
@pytest.fixture(params=['hop_skip_jump'])
def attack(request):
    yield request.param


def build_attack(target_obj: 'CFTarget', attack: str):
    target = target_obj()
    target.load()
    return Counterfit.build_attack(target, attack)


def test_attack(target, attack):
    cfattack = build_attack(target, attack)
    assert cfattack

    clip_values = (0., 1.)
    cfattack.options.update({"clip_values": clip_values})
    Counterfit.run_attack(cfattack)
    print(cfattack.results)
    assert cfattack.results is not None