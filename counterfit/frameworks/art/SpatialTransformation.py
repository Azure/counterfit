from art.attacks.evasion import SpatialTransformation
from hyperopt import hp
from counterfit.core.attacks import Attack


class SpatialTransformationWrapper(Attack):
    attack_cls = SpatialTransformation
    attack_name = "spatial_transformation"
    attack_type = "evasion"
    tags = ["image"]
    category = "blackbox"
    framework = "art"

    random = {
        "max_translation": hp.quniform("sptf_maxtrans", 0, 10, 1),
        "num_translations": hp.quniform("sptf_maxnumtrans", 1, 10, 1),
        "max_rotation": hp.uniform("sptf_maxrot", 0, 30),
        "num_rotations": hp.quniform("sptf_maxnumrot", 1, 10, 1),
    }

    default = {"max_translation": 0.0, "num_translations": 1, "max_rotation": 0.0, "num_rotations": 1}
