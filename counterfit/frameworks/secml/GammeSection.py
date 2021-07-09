import numpy as np
from counterfit.core.attacks import Attack
from secml_malware.attack.blackbox.c_gamma_sections_evasion import CGammaSectionsEvasionProblem


class GammaSectionInjectionAttack(Attack):
    attack_cls = CGammaSectionsEvasionProblem
    attack_name = "gamma-section-injection"
    attack_type = "evasion"
    tags = ["PE", "CArray"]
    category = "blackbox"
    framework = "secml"
    default = {
        #'how_many_sections': 75,
        'section_population': ['.rdata'],
        # 'goodware_folder': None,
        'population_size': 10,
        'penalty_regularizer': 1e-7,
        'iterations': 100,
        'seed': None,
        'is_debug': False,
        'hard_label': False,
        'threshold': 0.0,
        'loss': 'l1',
        'random_names': True
    }

    random = {
        #'how_many_sections': np.random.randint(10, 100),
        'section_population': np.random.choice(['.rdata', '.text', '.reloc', '.data']),
        # 'goodware_folder': None,
        'population_size': np.random.randint(5, 20),
        'penalty_regularizer': pow(10, -np.random.randint(4, 8)),
        'iterations': np.random.randint(50, 500),
        'seed': None,
        'is_debug': False,
        'hard_label': False,
        'threshold': 0.0,
        'loss': 'l1',
        'random_names': True
    }
