import pytest
from counterfit.core.attacks import CFAttack
from counterfit.core.attacks import CFAttackOptions


def test_cfattack_options():
    sample_options = {
        "option_int": 1,
        "option_float": 1.0,
        "option_str": "hello"
    }

    cfattack_options = {
        "sample_index": 0,
        "logger": "default"
    }

    default_options_list = list(sample_options.keys())
    cfattack_options_list = list(cfattack_options.keys())
    all_options = {**sample_options, **cfattack_options}

    attack_options = CFAttackOptions(
        **all_options,
        default_options_list=default_options_list,
        cfattack_options_list=cfattack_options_list
    )

    assert attack_options is not None


def test_cfattack_get_default_options():
    sample_options = {
        "option_int": 1,
        "option_float": 1.0,
        "option_str": "hello"
    }

    cfattack_options = {
        "sample_index": 0,
        "logger": "default"
    }

    default_options_list = list(sample_options.keys())
    cfattack_options_list = list(cfattack_options.keys())
    all_options = {**sample_options, **cfattack_options}

    attack_options = CFAttackOptions(
        **all_options,
        default_options_list=default_options_list,
        cfattack_options_list=cfattack_options_list
    )

    default_options = attack_options.get_default_options()

    assert sample_options == default_options


def test_cfattack_get_current_options():
    sample_options = {
        "option_int": 1,
        "option_float": 1.0,
        "option_str": "hello"
    }

    cfattack_options = {
        "sample_index": 0,
        "logger": "default"
    }

    default_options_list = list(sample_options.keys())
    cfattack_options_list = list(cfattack_options.keys())
    all_options = {**sample_options, **cfattack_options}

    attack_options = CFAttackOptions(
        **all_options,
        default_options_list=default_options_list,
        cfattack_options_list=cfattack_options_list
    )

    attack_options.set_options({"option_int": 5})
    current_options = attack_options.get_current_options()

    assert current_options["option_int"] == 5


def test_cfattack_get_all_options():
    sample_options = {
        "option_int": 1,
        "option_float": 1.0,
        "option_str": "hello"
    }

    cfattack_options = {
        "sample_index": 0,
        "logger": "default"
    }

    default_options_list = list(sample_options.keys())
    cfattack_options_list = list(cfattack_options.keys())
    all_options = {**sample_options, **cfattack_options}

    attack_options = CFAttackOptions(
        **all_options,
        default_options_list=default_options_list,
        cfattack_options_list=cfattack_options_list
    )

    all_options = attack_options.get_all_options()

    assert all_options == {**sample_options, **cfattack_options}


def test_cfattack_save_previous_options():
    sample_options = {
        "option_int": 1,
        "option_float": 1.0,
        "option_str": "hello"
    }

    cfattack_options = {
        "sample_index": 0,
        "logger": "default"
    }

    default_options_list = list(sample_options.keys())
    cfattack_options_list = list(cfattack_options.keys())
    all_options = {**sample_options, **cfattack_options}

    attack_options = CFAttackOptions(
        **all_options,
        default_options_list=default_options_list,
        cfattack_options_list=cfattack_options_list
    )

    attack_options.save_previous_options()

    assert len(attack_options.previous_options) > 1
