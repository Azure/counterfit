import numpy as np
from art.attacks.evasion import SquareAttack
from hyperopt import hp
from counterfit.core.attacks import Attack


class SquareAttackWrapper(Attack):
    attack_cls = SquareAttack
    attack_name = "square"
    attack_type = "evasion"
    tags = ["image"]
    category = "blackbox"
    framework = "art"

    random = {
        "norm": hp.choice("sqr_norm", [2, np.inf]),
        "max_iter": hp.quniform("sqr_maxiter", 5, 500, 1),
        "eps": hp.uniform("sqr_eps", 0.1, 0.8),
        "p_init": hp.uniform("sqr_p_init", 0.5, 0.95),
        "nb_restarts": hp.quniform("sqr_restarts", 1, 5, 1),
    }

    default = {"norm": 1, "max_iter": 100, "eps": 0.3, "p_init": 0.8, "nb_restarts": 1}
