import numpy as np
from art.attacks.evasion import HopSkipJump
from counterfit.core.attacks import Attack
from hyperopt import hp


class HopSkipJumpWrapper(Attack):
    attack_cls = HopSkipJump
    attack_name = "hop_skip_jump"
    attack_type = "evasion"
    tags = ["image", "numpy"]
    category = "blackbox"
    framework = "art"

    random = {
        "targeted": hp.choice("hsj_targeted", [False, True]),
        "norm": hp.choice("hsj_norm", [2, np.inf]),
        "max_iter": hp.quniform("hsj_maxiter", 10, 100, 1),
        "max_eval": hp.quniform("hsj_maxeval", 300, 1000, 1),
        "init_eval": hp.quniform("hsj_initeval", 10, 200, 1),
        "init_size": hp.quniform("hsj_initsize", 10, 200, 1),
    }

    default = {
        "targeted": False,
        "norm": 2.,  # float, so that we can optionally set it to math.inf
        "max_iter": 50,
        "max_eval": 1000,
        "init_eval": 100,
        "init_size": 100,
    }
