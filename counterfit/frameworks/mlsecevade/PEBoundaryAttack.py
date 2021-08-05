from art.attacks.evasion import BoundaryAttack
from counterfit.core.attacks import Attack
from hyperopt import hp
from .PEutils.pe_function_preserving import PE_wrap_ART_attack


class PEBoundaryAttackWrapper(Attack):
    attack_cls = PE_wrap_ART_attack(BoundaryAttack)
    attack_name = "boundary-pe"
    attack_type = "evasion"
    tags = ["pe"]
    category = "blackbox"
    framework = "mlsecevade"

    random = {
        "targeted": hp.choice("bound_targ", [False, True]),
        "delta": hp.uniform("bound_delta", 0.005, 0.05),
        "epsilon": hp.uniform("bound_uniform", 0.005, 0.05),
        "step_adapt": hp.uniform("bound_adapt", 0.5, 0.75),
        "max_iter": hp.quniform("bound_maxiter", 100, 500, 1),
        "num_trial": hp.quniform("bound_trial", 10, 40, 1),
        "sample_size": hp.quniform("bound_ssize", 10, 50, 1),
        "init_size": hp.quniform("bound_isize", 10, 200, 1),
    }

    default = {
        "targeted": False,
        "delta": 0.01,
        "epsilon": 0.01,
        "step_adapt": 0.667,
        "max_iter": 50,
        "num_trial": 25,
        "sample_size": 20,
        "init_size": 50,
    }
