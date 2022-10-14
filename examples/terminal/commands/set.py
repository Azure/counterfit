import argparse
from typing import Union

import cmd2
from examples.terminal.core.state import CFState
from counterfit.core.output import CFPrint
from rich.table import Table


def set_table():
    table = Table(header_style="bold magenta")
    table.add_column("Parameter (type)")
    table.add_column("Default")
    table.add_column("Current")
    table.add_column("New")

    # print attack params first
     # print attack params first
    attack_parameters = CFState.state().active_attack.options.attack_parameters
    table.add_row("Algo Parameters")
    table.add_row("--------------------", "--", "--", "--")
    for k, v in attack_parameters.items():
        table.add_row(
            f"{k} ({str(type(v['default']).__name__)})",
            str(v["default"]),
            str(v["current"]),
            str(v["docs"])
        )

    # print cfspecific options next
    cf_options = CFState.state().active_attack.options.cf_options
    table.add_row()
    table.add_row("CFAttack Options")
    table.add_row("--------------------", "--", "--", "--")
    for k, v in cf_options.items():
        table.add_row(
            f"{k} ({str(type(v['default']).__name__)})",
            str(v["default"]),
            str(v["current"]),
            str(v["docs"])
        )

    CFPrint.output(table)


def get_sample_index(sample_index: str) -> Union[list, int, range, None]:
    try:
        sample_index = eval(sample_index)
    except Exception as e:
        CFPrint.failed(f"Error parsing '--sample_index {sample_index}: {e}")
        return None

    if type(sample_index) is tuple:
        sample_index = list(sample_index)

    if type(sample_index) not in (range, int, list):
        CFPrint.failed(f"Error parsing '--sample_index {sample_index}: expression must result in a 'list', 'range' or 'int'")
        return None

    if type(sample_index) is list:
        if any([type(el) is not int for el in sample_index]):
            CFPrint.failed(f"Error parsing '--sample_index {sample_index}': list must only contain integers")
            return None
    
    return sample_index


NoneType = type(None)
def get_clip_values(clip_values: str) -> Union[tuple,NoneType]:
    try:
        clip_values = tuple(eval(clip_values))
    except Exception as e:
        CFPrint.failed(f"Error parsing '--clip_values {clip_values}': {e}")
        return None

    if clip_values is None:
        return "None"

    if type(clip_values) not in (tuple,):
        CFPrint.failed(f"Error parsing '--clip_values {clip_values}: expression must result in a 'tuple' or 'None'")
        return None

    return clip_values


def parse_numeric(argname: str, val_str: str) -> Union[int, float, None]:
    # simple check for "inf" as a shortcut to float('inf)
    if type(val_str) is str and val_str == "inf":
        return float('inf')
    try:
        val = eval(val_str)
    except Exception as e:
        CFPrint.failed(f"Error parsing --'{argname} {val_str}': {e}")
        return None

    if type(val) not in (int, float):
        CFPrint.failed(f"Error parsing '--{argname} {val_str}': expression must result in a 'int' or 'float'")
        return None

    return val


def parse_boolean(argname: str, val_str: str) -> Union[bool, None]:
    if val_str.lower() in ("true", "t", "yes", "y", "1"):
        return True
    elif val_str.lower() in ("false", "f", "no", "n", "0"):
        return False
    else:
        CFPrint.failed(f"Error parsing '--{argname} {val_str}': must be 'true' or 'false'")
        return None

def get_options() -> dict:
    # dynamically get the list of options
    if not CFState.state().active_target:
        options = {}
    elif not CFState.state().active_attack:
        options = {}
    elif CFState.state().active_attack and hasattr(CFState.state().active_attack, 'options'):
        options = CFState.state().active_attack.options.get_all()
    else:
        options = {}
    return options


def set_cmd(args: argparse.Namespace) -> None:
    """Set parameters of the active attack on the active target using

    For infinity, use 'inf' or 'float("inf")'.

    This command replaces built-in "set" command, which is renamed to "setg".
    """
    if not CFState.state().active_target:
        CFPrint.warn('No active target. Try "set_target <target>"')
        return
    if not CFState.state().active_attack:
        CFPrint.warn('No active attack. Try "set_attack <attack>"')
        return

    new_params = {}
    options = get_options()

    for parameter, value in args.__dict__.items():
        if options.get(parameter):
            if parameter == 'clip_values':
                clip_values = get_clip_values(args.clip_values)
                if clip_values is None:
                    return
                if clip_values=="None":  # None is a valid type we handle separately
                    clip_values = None
                new_params[parameter] = clip_values

            elif parameter == 'sample_index':
                sample_index = get_sample_index(args.sample_index)
                if sample_index is None:
                    return
                new_params[parameter] = sample_index
            elif type(options.get(parameter)["default"]) in (float, int) and type(value) is str:
                # parse numeric type
                value = parse_numeric(parameter, value)
                if value is None:
                    return
                new_params[parameter] = value
            elif type(options.get(parameter)) is bool:
                # parse boolean type
                value = parse_boolean(parameter, value)
                if value is None:
                    return
                new_params[parameter] = value
    CFState.state().active_attack.options.update(new_params)
    set_table()

# dynamic option add
set_args = cmd2.Cmd2ArgumentParser()

for k, v in get_options().items():
    set_args.add_argument(f"--{k}", type=str, default=str(v["default"]))

