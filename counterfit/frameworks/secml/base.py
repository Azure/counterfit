from abc import ABC

from secml_malware.attack.blackbox.c_blackbox_header_problem import CBlackBoxHeaderEvasionProblem

from counterfit.core.attacks import Attack
from counterfit.core.enums import AttackStatus


class ByteBasedBlackBox(Attack, ABC):
	# attack_cls = CBlackBoxHeaderEvasionProblem
	attack_name = "byte_based"
	attack_type = "evasion"
	tags = ["exe", "CArray"]
	category = "blackbox"
	framework = "secml"
