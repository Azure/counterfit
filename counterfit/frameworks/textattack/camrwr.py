from counterfit.core.state import Attack

from textattack.attack_recipes.pruthi_2019 import Pruthi2019


class CAMRWRAttackWrapper(Attack):
    attack_cls = Pruthi2019
    attack_name = "pruthi_2019"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}