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

def test_build_target():
    target = Counterfit.build_target(
        data_type="images",
        endpoint="http://locahost/score",
        output_classes=["Cat", "NotACat"],
        classifier="blackbox",
        input_shape=(1,),
        load_func=load,
        predict_func=predict,
        X = [[1,0]]
    )

    assert isinstance(target, CFTarget)


def test_build_attack():
    target = Counterfit.build_target(
        data_type="image",
        endpoint="http://locahost/score",
        output_classes=["Cat", "NotACat"],
        classifier="blackbox",
        input_shape=(1,),
        load_func=load,
        predict_func=predict,
        X = [[1,0]]
    )

    cfattack = Counterfit.build_attack(
        target=target,
        attack="hop_skip_jump"
    )

    assert isinstance(cfattack, CFAttack)

