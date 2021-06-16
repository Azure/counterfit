from counterfit.core.state import Attack

from textattack.attack_recipes.kuleshov_2017 import Kuleshov2017


class KuleshovAttackWrapper(Attack):
    attack_cls = Kuleshov2017
    attack_name = "kuleshov_2017"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}