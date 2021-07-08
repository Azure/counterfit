import numpy as np
from counterfit.core.attacks import Attack
from secml_malware.attack.blackbox.c_black_box_padding_evasion import CBlackBoxPaddingEvasionProblem


class PaddingAttack(Attack):
    attack_cls = CBlackBoxPaddingEvasionProblem
    attack_name = "byte-padding"
    attack_type = "evasion"
    tags = ["PE", "CArray"]
    category = "blackbox"
    framework = "secml"
    default = {
        'population_size': 10,
        'how_many_padding_bytes': 102400,
        'iterations': 100,
        'is_debug': False,
    }
    random = {
        'population_size': np.random.randint(5, 25),
        'how_many_padding_bytes': np.random.randint(5000, 20000),
        'iterations': np.random.randint(100, 300),
        'is_debug': False,
    }
