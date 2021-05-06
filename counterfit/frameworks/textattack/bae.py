from counterfit.core.state import Attack

from textattack.attack_recipes.bae_garg_2019 import BAEGarg2019


class BAEAttackWrapper(Attack):
    attack_cls = BAEGarg2019
    attack_name = "bae_garg"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}
