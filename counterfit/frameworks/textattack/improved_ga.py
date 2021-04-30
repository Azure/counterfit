from counterfit.core.state import Attack

from textattack.attack_recipes.iga_wang_2019 import IGAWang2019


class ImprovedGAAttackWrapper(Attack):
    attack_cls = IGAWang2019
    attack_name = "iga_wang_2019"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}