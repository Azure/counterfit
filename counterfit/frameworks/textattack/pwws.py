from textattack.attack_recipes.pwws_ren_2019 import PWWSRen2019
from counterfit.core.state import Attack


class PWWSAttackWrapper(Attack):
    attack_cls = PWWSRen2019
    attack_name = "pwws_ren_2019"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}