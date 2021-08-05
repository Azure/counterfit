from art.attacks.evasion import ZooAttack
from counterfit.core.attacks import Attack
from hyperopt import hp
from .HTMLutils.html_render_preserving import HTML_wrap_ART_attack


class HTMLZooAttackWrapper(Attack):
    attack_cls = HTML_wrap_ART_attack(ZooAttack)
    attack_name = "zoo-html"
    attack_type = "evasion"
    tags = ["html"]
    category = "blackbox"
    framework = "mlsecevade"

    random = {
        "confidence": hp.uniform("zoo_conf", 0.0, 0.2),
        "targeted": hp.choice("zoo_targ", [False, True]),
        "learning_rate": hp.uniform("zoo_lr", 1e-3, 1e-1),
        "max_iter": hp.quniform("zoo_maxiter", 5, 10, 1),
        "binary_search_steps": hp.quniform("zoo_steps", 1, 5, 1),
        "initial_const": hp.uniform("zoo_init", 1e-4, 1e-2),
        "abort_early": hp.choice("zoo_abort", [False, True]),
        "use_resize": hp.choice("zoo_resize", [False]),
        "use_importance": hp.choice("zoo_importance", [False, True]),
        "nb_parallel": 1,
        "batch_size": 1,
        "variable_h": hp.uniform("zoo_h", 1e-5, 1e-3),
    }

    default = {
        "confidence": 0.0,
        "targeted": False,
        "learning_rate": 0.01,
        "max_iter": 10,
        "binary_search_steps": 1,
        "initial_const": 0.001,
        "abort_early": True,
        "use_resize": True,
        "use_importance": True,
        "nb_parallel": 1,
        "batch_size": 1,
        "variable_h": 0.0001,
    }
