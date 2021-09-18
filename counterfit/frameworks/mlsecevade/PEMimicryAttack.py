import numpy as np
from counterfit.core.attacks import Attack
from hyperopt import hp
from .PEutils.pe_mimicry import PEMimicryAttack

class PEMimicryAttackWrapper(Attack):
    attack_cls = PEMimicryAttack
    attack_name = "mimicry-pe"
    attack_type = "evasion"
    tags = ["pe"]
    category = "blackbox"
    framework = "mlsecevade"

    random = {
    }

    default = {
    }
