from counterfit.core.state import Attack

from textattack.attack_recipes.textfooler_jin_2019 import TextFoolerJin2019


class TextFoolerAttackWrapper(Attack):
    attack_cls = TextFoolerJin2019
    attack_name = "textfooler_jin_2019"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}
    