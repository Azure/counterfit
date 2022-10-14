import pytest
import warnings
import sys, os
warnings.filterwarnings('ignore')

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from targets import Digits
from targets import DigitKeras
from counterfit import Counterfit


@pytest.fixture(params=[Digits, DigitKeras])
def target(request):
    yield request.param

# Evasion
@pytest.fixture(params=["Blur"])
def attack(request):
    yield request.param


def test_attack(target, attack):
    cftarget = target()
    cftarget.load()

    cfattack = Counterfit.build_attack(cftarget, attack)

    print(cfattack.options.get_all())

    Counterfit.run_attack(cfattack)    