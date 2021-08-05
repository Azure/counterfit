from art.attacks.evasion import PixelAttack
from counterfit.core.attacks import Attack
from hyperopt import hp


class PixelAttackWrapper(Attack):
    attack_cls = PixelAttack
    attack_name = "pixel"
    attack_type = "evasion"
    tags = ["image"]
    category = "blackbox"
    framework = "art"

    random = {
        "targeted": hp.choice("pxl_targ", [False, True]),
        "th": hp.choice("pxl_th", [1, 127]),
        "es": hp.choice("pxl_es", [1]),
    }

    default = {"targeted": False, "th": 1, "es": 1}
