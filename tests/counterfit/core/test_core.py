from counterfit import Counterfit
from counterfit.core.attacks import CFAttack
from counterfit.core.targets import CFTarget

import warnings
warnings.filterwarnings('ignore')

def load():
    pass

def predict():
    return [1]

def test_frameworks():
    frameworks = Counterfit.get_frameworks()
    assert dict(frameworks)

def test_build_target(test_data):
    target = Counterfit.build_target(
        data_type=test_data.data_type,
        endpoint=test_data.endpoint,
        output_classes=test_data.output_classes,
        classifier=test_data.classifier,
        input_shape=(1,),
        load_func=load,
        predict_func=predict,
        X = test_data.X
    )
    assert isinstance(target, CFTarget)


def test_build_attack(test_data):
    target = Counterfit.build_target(
        data_type=test_data.data_type,
        endpoint=test_data.endpoint,
        output_classes=test_data.output_classes,
        classifier=test_data.classifier,
        input_shape=(1,),
        load_func=load,
        predict_func=predict,
        X = test_data.X
    )

    cfattack = Counterfit.build_attack(
        target=target,
        attack=test_data.attack
    )

    assert isinstance(cfattack, CFAttack)

