import os
import numpy as np
from counterfit.core.attacks import Attack
from secml_malware.attack.blackbox.c_gamma_evasion import CGammaEvasionProblem


class GammaPaddingAttack(Attack):
    attack_cls = CGammaEvasionProblem
    attack_name = "gamma-padding"
    attack_type = "evasion"
    tags = ["PE", "CArray"]
    category = "blackbox"
    framework = "secml"

    default = {
        'section_population': ['.rdata'],
        # 'goodware_folder': None,
        'population_size': 10,
        'penalty_regularizer': 1e-7,
        'iterations': 100,
        'seed': None,
        'is_debug': False,
        'hard_label': False,
        'threshold': 0.0,
        'loss': 'l1'
    }

    random = {
        'section_population': np.random.choice(['.rdata', '.text', '.reloc', '.data']),
        # 'goodware_folder': None,
        'population_size': np.random.randint(5, 20),
        'penalty_regularizer': pow(10, -np.random.randint(4, 8)),
        'iterations': np.random.randint(50, 500),
        'seed': None,
        'is_debug': False,
        'hard_label': False,
        'threshold': 0.0,
        'loss': 'l1'
    }
