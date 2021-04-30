from counterfit.core.state import Attack

from textattack.attack_recipes.deepwordbug_gao_2018 import DeepWordBugGao2018


class DeepWordBugWrapper(Attack):
    attack_cls = DeepWordBugGao2018
    attack_name = "deepwordbug"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}
