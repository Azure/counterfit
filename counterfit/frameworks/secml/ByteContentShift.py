import numpy as np
from counterfit.core.attacks import Attack
from secml_malware.attack.blackbox.c_black_box_format_exploit_evasion import CBlackBoxContentShiftingEvasionProblem


class ContentShiftingAttack(Attack):
    attack_cls = CBlackBoxContentShiftingEvasionProblem
    attack_name = "byte-content-shifting"
    attack_type = "evasion"
    tags = ["PE", "CArray"]
    category = "blackbox"
    framework = "secml"
    default = {
        'population_size': 10,
        'bytes_to_inject': 0x200,
        'iterations': 100,
        'is_debug': False,
    }
    random = {
        'population_size': np.random.randint(5, 25),
        'bytes_to_inject': np.random.choice([0x100, 0x200, 0x300, 0x400, 0x500]),
        'iterations': np.random.randint(100, 300),
        'is_debug': False,
    }
