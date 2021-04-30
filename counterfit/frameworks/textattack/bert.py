from counterfit.core.state import Attack

from textattack.attack_recipes.bert_attack_li_2020 import BERTAttackLi2020


class BERTAttackWrapper(Attack):
    attack_cls = BERTAttackLi2020
    attack_name = "bert_attack_li_2020"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}