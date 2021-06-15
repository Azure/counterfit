import os

import numpy as np
from secml_malware.attack.blackbox.c_gamma_evasion import CGammaEvasionProblem
from secml_malware.attack.blackbox.c_gamma_sections_evasion import CGammaSectionsEvasionProblem

from counterfit.core import config
from counterfit.core.enums import AttackStatus
from counterfit.frameworks.secml.base import ByteBasedBlackBox

GOODWARE_FOLDER = os.path.join(config.targets_path, 'malware', 'samples', 'goodware')


class GammaPaddingAttack(ByteBasedBlackBox):
	attack_cls = CGammaEvasionProblem
	attack_name = "gamma-padding"
	default = {
		'how_many_sections': 75,
		'which_sections': ['.rdata'],
		'goodware_folder': GOODWARE_FOLDER,
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
		'how_many_sections': np.random.randint(10, 100),
		'which_sections': np.random.choice(['.rdata', '.text', '.reloc', '.data']),
		'goodware_folder': GOODWARE_FOLDER,
		'population_size': np.random.randint(5, 20),
		'penalty_regularizer': pow(10, -np.random.randint(4, 8)),
		'iterations': np.random.randint(50, 500),
		'seed': None,
		'is_debug': False,
		'hard_label': False,
		'threshold': 0.0,
		'loss': 'l1'
	}

	def __init__(self, how_many_sections, which_sections, goodware_folder):
		super().__init__(AttackStatus.pending.value)
		section_population = CGammaEvasionProblem.create_section_population_from_folder(goodware_folder,
																						how_many_sections,
																						which_sections)
		self.attack_cls.__init__ = lambda mw, **kw: CGammaEvasionProblem(section_population, mw, **kw)


class GammaSectionInjectionAttack(ByteBasedBlackBox):
	attack_cls = CGammaSectionsEvasionProblem
	attack_name = "gamma-section-injection"
	default = {
		'how_many_sections': 75,
		'which_sections': ['.rdata'],
		'goodware_folder': GOODWARE_FOLDER,
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
		'how_many_sections': np.random.randint(10, 100),
		'which_sections': np.random.choice(['.rdata', '.text', '.reloc', '.data']),
		'goodware_folder': GOODWARE_FOLDER,
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

	def __init__(self, how_many_sections, which_sections, goodware_folder):
		super().__init__(AttackStatus.pending.value)
		section_population = CGammaSectionsEvasionProblem.create_section_population_from_folder(goodware_folder,
																								how_many_sections,
																								which_sections)
		self.attack_cls.__init__ = lambda mw, **kw: CGammaSectionsEvasionProblem(section_population, mw, **kw)
