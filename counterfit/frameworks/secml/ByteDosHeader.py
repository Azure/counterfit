import numpy as np
from counterfit.core.attacks import Attack
from secml_malware.attack.blackbox.c_blackbox_header_problem import CBlackBoxHeaderEvasionProblem


class DOSHeaderAttack(Attack):
    attack_cls = CBlackBoxHeaderEvasionProblem
    attack_name = "byte-pe-header"
    attack_type = "evasion"
    tags = ["PE", "CArray"]
    category = "blackbox"
    framework = "secml"

    default = {
        'population_size': 10,
        'optimize_all_dos': False,
        'iterations': 100,
        'is_debug': False,
    }

    random = {
        'population_size': np.random.randint(5, 25),
        'optimize_all_dos': np.random.choice([True, False]),
        'iterations': np.random.randint(100, 300),
        'is_debug': False,
    }
