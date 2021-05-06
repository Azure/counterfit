from art.attacks.evasion import BoundaryAttack
from hyperopt import hp
from counterfit.core.attacks import Attack


class BoundaryAttackWrapper(Attack):
    attack_cls = BoundaryAttack
    attack_name = "boundary"
    attack_type = "evasion"
    tags = ["image", "numpy"]
    category = "blackbox"
    framework = "art"

    random = {
        "targeted": hp.choice("bound_targ", [False, True]),
        "delta": hp.uniform("bound_delta", 0.005, 0.05),
        "epsilon": hp.uniform("bound_uniform", 0.005, 0.05),
        "step_adapt": hp.uniform("bound_adapt", 0.5, 0.75),
        "max_iter": hp.quniform("bound_maxiter", 200, 2000, 1),
        "num_trial": hp.quniform("bound_trial", 10, 50, 1),
        "sample_size": hp.quniform("bound_ssize", 10, 50, 1),
        "init_size": hp.quniform("bound_isize", 10, 200, 1),
    }

    default = {
        "targeted": False,
        "delta": 0.01,
        "epsilon": 0.01,
        "step_adapt": 0.667,
        "max_iter": 5000,
        "num_trial": 25,
        "sample_size": 20,
        "init_size": 100,
    }
