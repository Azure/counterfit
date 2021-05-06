from textattack.attack_recipes.genetic_algorithm_alzantot_2018 import GeneticAlgorithmAlzantot2018
from counterfit.core.state import Attack


class GAAttackWrapper(Attack):
    attack_cls = GeneticAlgorithmAlzantot2018
    attack_name = "ga_alzantot_2018"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}
