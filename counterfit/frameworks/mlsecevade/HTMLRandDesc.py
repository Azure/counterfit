import numpy as np
from counterfit.core.attacks import Attack
from .HTMLutils.html_render_preserving import HTMLRandomizedDescentAttack


class HTMLRandDescWrapper(Attack):
    attack_cls = HTMLRandomizedDescentAttack
    attack_name = "randdescent-html"
    attack_type = "evasion"
    tags = ["html"]
    category = "blackbox"
    framework = "mlsecevade"

    random = {
        "n_iters": np.random.choice(100),
        "n_times": np.random.choice(5),
    }
    default = {
        "n_iters": 100,
	"n_times": 1,
    }

