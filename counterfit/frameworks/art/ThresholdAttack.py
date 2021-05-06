from art.attacks.evasion import ThresholdAttack
from hyperopt import hp
from counterfit.core.attacks import Attack


class ThresholdAttackWrapper(Attack):
    attack_cls = ThresholdAttack
    attack_name = "threshold"
    attack_type = "evasion"
    tags = ["image"]
    category = "blackbox"
    framework = "art"

    random = {
        "targeted": hp.choice("thld_targ", [False, True]),
        "th": hp.choice("thld_th", [None, 1, 127]),
        "es": hp.choice("thld_es", [1]),
    }

    default = {"targeted": False, "th": 1, "es": 1}
