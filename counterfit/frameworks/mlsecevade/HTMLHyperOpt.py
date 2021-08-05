import numpy as np
from counterfit.core.attacks import Attack
from hyperopt import hp
from .HTMLutils.html_render_preserving import HTMLHyperoptAttack


class HTMLHyperOptWrapper(Attack):
    attack_cls = HTMLHyperoptAttack
    attack_name = "hyperopt-html"
    attack_type = "evasion"
    tags = ["html"]
    category = "blackbox"
    framework = "mlsecevade"

    random = {
        "max_evals": hp.quniform("hyp_maxeval", 10, 200, 1),
    }

    default = {
        "max_evals": 20,
    }
