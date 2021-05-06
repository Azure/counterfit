from textattack.attack_recipes.kuleshov_2017 import Kuleshov2017
from counterfit.core.state import Attack


class KuleshovAttackWrapper(Attack):
    attack_cls = Kuleshov2017
    attack_name = "kuleshov_2017"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}