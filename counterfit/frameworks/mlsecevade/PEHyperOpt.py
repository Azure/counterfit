import numpy as np
from counterfit.core.attacks import Attack
from hyperopt import hp
from .PEutils.pe_function_preserving import PEHyperoptAttack

class PEHyperoptWrapper(Attack):
    attack_cls = PEHyperoptAttack
    attack_name = "hyperopt-pe"
    attack_type = "evasion"
    tags = ["pe"]
    category = "blackbox"
    framework = "mlsecevade"

    random = {
        "max_evals": hp.quniform("hyp_maxeval", 10, 200, 1),
    }

    default = {
        "max_evals": 10,
    }
