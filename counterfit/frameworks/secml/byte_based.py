from abc import ABC

import numpy as np
from secml_malware.attack.blackbox.c_black_box_format_exploit_evasion import CBlackBoxFormatExploitEvasionProblem, \
	CBlackBoxContentShiftingEvasionProblem
from secml_malware.attack.blackbox.c_black_box_padding_evasion import CBlackBoxPaddingEvasionProblem
from secml_malware.attack.blackbox.c_blackbox_header_problem import CBlackBoxHeaderEvasionProblem

from counterfit.core.attacks import Attack


class ByteBasedBlackBox(ABC):
	attack_type = "evasion"
	tags = ["PE", "CArray"]
	category = "blackbox"
	framework = "secml"


class DOSHeaderAttack(ByteBasedBlackBox, Attack):
	attack_cls = CBlackBoxHeaderEvasionProblem
	attack_name = "header"
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


class PaddingAttack(ByteBasedBlackBox, Attack):
	attack_cls = CBlackBoxPaddingEvasionProblem
	attack_name = "padding"
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


class ContentShiftingAttack(ByteBasedBlackBox, Attack):
	attack_cls = CBlackBoxContentShiftingEvasionProblem
	attack_name = "content-shifting"
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
