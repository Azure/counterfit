import pytest
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from tests.mocks.targets import DigitKeras

from counterfit import Counterfit


@pytest.fixture(params=[DigitKeras])
def target(request):
    yield request.param

# Evasion
@pytest.fixture(params=["mi_face"])
def attack(request):
    yield request.param


def test_attack(target, attack):
    cftarget = target()
    cftarget.load()

    cfattack = Counterfit.build_attack(cftarget, attack)
    if not cfattack:
        assert cfattack == False
    clip_values = (0., 1.)

    cfattack.options.update({"clip_values": clip_values})

    Counterfit.run_attack(cfattack)   
    assert cfattack.results is not None 