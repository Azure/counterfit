import pytest

from counterfit.core.targets import Target

from counterfit.targets.digits_blackbox.digits_blackbox import Digits
from counterfit.targets.digits_keras.digits_keras import DigitKeras
from counterfit.targets.creditfraud.creditfraud import CreditFraud
from counterfit.targets.satellite.satellite import SatelliteImagesTarget


@pytest.fixture(params=[CreditFraud, SatelliteImagesTarget])
def target(request):
    yield request.param


def test_target_init(target):
    new_target = target()
    assert new_target is not None


def test_target_load(target):
    new_target = target()
    new_target.load()
    new_target.set_loaded_status(status=True)
    assert new_target.loaded_status == True


def test_target_get_samples(target):
    new_target = target()
    new_target.load()
    new_target.set_loaded_status(status=True)
    samples = new_target.get_samples(1)
    assert samples is not None


def test_target_predict(target):
    new_target = target()
    new_target.load()
    new_target.set_loaded_status(status=True)
    samples = new_target.get_samples(1)
    output = new_target.predict(samples)
    assert output is not None


def test_target_outputs_to_labels(target):
    new_target = target()
    new_target.load()
    new_target.set_loaded_status(status=True)
    samples = new_target.get_samples(1)
    output = new_target.predict(samples)
    labels = new_target.outputs_to_labels(output)
    assert labels is not None
