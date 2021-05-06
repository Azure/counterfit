from textattack.attack_recipes.input_reduction_feng_2018 import InputReductionFeng2018
from counterfit.core.state import Attack


class InputReductionAttackWrapper(Attack):
    attack_cls = InputReductionFeng2018
    attack_name = "ir_feng_2018"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}