import os

import numpy as np
from secml_malware.attack.blackbox.c_gamma_evasion import CGammaEvasionProblem
from secml_malware.attack.blackbox.c_gamma_sections_evasion import CGammaSectionsEvasionProblem
from secml_malware.attack.blackbox.c_wrapper_phi import CWrapperPhi

from counterfit.core import config
from counterfit.core.attacks import Attack
from counterfit.frameworks.secml.byte_based import ByteBasedBlackBox

GOODWARE_FOLDER = os.path.join(config.targets_path, 'pe_malware', 'samples', 'goodware')


def real_constructor(*args, **kw):
	sp = CGammaEvasionProblem.create_section_population_from_folder(kw['goodware_folder'],
																	kw['how_many_sections'],
																	kw['which_sections'])
	del kw['goodware_folder']
	del kw['how_many_sections']
	del kw['which_sections']

	return CGammaEvasionProblem(sp, args[0], **kw)


class PaddingGammaWrapper(CGammaEvasionProblem):
	def __init__(self, model_wrapper: CWrapperPhi, how_many_sections: int, which_sections: list, goodware_folder: str,
				 population_size: int,
				 penalty_regularizer: float, iterations: int, seed: int = None,
				 is_debug: bool = False,
				 hard_label: bool = False,
				 threshold: float = 0.5,
				 loss: str = 'l1'):
		section_population, _ = self.create_section_population_from_folder(goodware_folder, how_many_sections,
																		which_sections)
		super().__init__(section_population,
						 model_wrapper,
						 population_size,
						 penalty_regularizer,
						 iterations,
						 seed,
						 is_debug,
						 hard_label,
						 threshold,
						 loss)


class SectionsGammaWrapper(CGammaSectionsEvasionProblem):
	def __init__(self, model_wrapper: CWrapperPhi, how_many_sections: int, which_sections: list, goodware_folder: str,
				 population_size: int,
				 penalty_regularizer: float, iterations: int, seed: int = None,
				 is_debug: bool = False,
				 hard_label: bool = False,
				 threshold: float = 0.5,
				 loss: str = 'l1',
				 random_names: bool = True):
		section_population, _ = self.create_section_population_from_folder(goodware_folder, how_many_sections,
																		which_sections)
		super().__init__(section_population,
						 model_wrapper,
						 population_size,
						 penalty_regularizer,
						 iterations,
						 seed,
						 is_debug,
						 hard_label,
						 threshold,
						 loss,
						 random_names)


class GammaPaddingAttack(ByteBasedBlackBox, Attack):
	attack_cls = PaddingGammaWrapper
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


class GammaSectionInjectionAttack(ByteBasedBlackBox, Attack):
	attack_cls = SectionsGammaWrapper
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
