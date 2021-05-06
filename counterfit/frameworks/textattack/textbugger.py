from textattack.attack_recipes.textbugger_li_2018 import TextBuggerLi2018
from counterfit.core.state import Attack


class TextBuggerAttackWrapper(Attack):
    attack_cls = TextBuggerLi2018
    attack_name = "textbugger_li_2018"
    attack_type = "evasion"
    tags = ["text"]
    category = "blackbox"
    framework = "textattack"

    default = {}
    random = {}