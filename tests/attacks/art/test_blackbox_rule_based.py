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
@pytest.fixture(params=['boundary', 'hop_skip_jump'])
def attack(request):
    yield request.param


def build_attack(target_obj: 'CFTarget', attack: str):
    target = target_obj()
    target.load()
    return Counterfit.build_attack(target, attack)


def test_boundary_credit():
    attack = build_attack(CreditFraud, 'boundary')
    # attack = build_attack(CreditFraud, 'hop_skip_jump')
    # >>>> run() attack estimator: BlackBoxClassifier(model=None, clip_values=None, preprocessing=StandardisationMeanStd(mean=0.0, std=1.0, apply_fit=True, apply_predict=True), preprocessing_defences=None, postprocessing_defences=None, preprocessing_operations=[StandardisationMeanStd(mean=0.0, std=1.0, apply_fit=True, apply_predict=True)], nb_classes=2, predict_fn=<bound method CFTarget.predict_wrapper of <counterfit.targets.creditfraud.CreditFraud object at 0x7f75f3fc22e0>>, input_shape=(30,))
    attack_did_succeed = Counterfit.run_attack(attack)

    assert attack
    assert attack_did_succeed


def test_attack(target, attack):
    cfattack = build_attack(target, attack)
    assert cfattack

    clip_values = (0., 1.)
    cfattack.options.update({"clip_values": clip_values})
    Counterfit.run_attack(cfattack)
    print(cfattack.results)
    assert cfattack.results is not None