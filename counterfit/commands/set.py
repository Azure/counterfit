import argparse
from cmd2 import with_argparser
from cmd2 import with_category
from rich.table import Table
from counterfit.core.state import CFState
from counterfit.core.output import CFPrint
from typing import Union


def set_table(default_options, current_options, new_options):
    default_options_list = CFState.state(
    ).active_target.active_attack.options.default_options_list

    cfattack_options_list = CFState.state(
    ).active_target.active_attack.options.cfattack_options_list

    table = Table(header_style="bold magenta")
    table.add_column("Parameter (type)")
    table.add_column("Default")
    table.add_column("Current")
    table.add_column("New")

    # print attack params first
    table.add_row("Algorithm Parameters")
    table.add_row("--------------------", "--", "--", "--")
    for option in default_options_list:
        default_value = default_options.get(option)
        current_value = current_options.get(option)
        new_value = new_options.get(option, "-")

        if new_value != current_value:
            table.add_row(f"{option} ({str(type(default_value).__name__)})",
                          str(default_value), str(current_value), str(new_value))
        else:
            table.add_row(f"{option} ({str(type(default_value).__name__)})",
                          str(default_value), str(current_value), " ")

    # print cfspecific options next
    table.add_row()
    table.add_row("Attack Options")
    table.add_row("--------------------", "--", "--", "--")
    for option in cfattack_options_list:
        default_value = default_options.get(option)
        current_value = current_options.get(option)
        new_value = new_options.get(option, "-")

        if "sample_index" == option:
            parameter_type = "int or expr"
        else:
            parameter_type = str(type(default_value).__name__)

        if new_value != current_value:
            table.add_row(f"{option} ({parameter_type})",
                          str(default_value), str(current_value), str(new_value))
        else:
            table.add_row(f"{option} ({parameter_type})",
                          str(default_value), str(current_value), " ")

    CFPrint.output(table)


def get_options() -> list:
    # dynamically get the list of options
    if not CFState.state().active_target:
        options = {}
    elif not CFState.state().active_target.active_attack:
        options = {}
    elif CFState.state().active_target.active_attack and hasattr(CFState.state().active_target.active_attack, 'options'):
        options = CFState.state().active_target.active_attack.options.get_all_options()
    else:
        options = {}
    return options

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
        clip_values = eval(clip_values)
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


# dynamic option add
parser = argparse.ArgumentParser()
for option, value in get_options().items():
    if "sample_index" == option or "clip_values" == option:
        parser.add_argument(f"--{option}", type=str, default=str(value))
    elif type(value) in (float, int):
        parser.add_argument(f"--{option}", type=str, default=str(value))
    elif type(value) == bool:
        parser.add_argument(f"--{option}", type=str, default=str(value))
    else:
        parser.add_argument(
            f"--{option}", type=type(value), default=value)


def update_options(target, partial_options):
    default_options = target.active_attack.options.previous_options[0]
    current_options = target.active_attack.options.get_all_options()
    new_options = current_options.copy()

    new_options = {}
    for option, val in partial_options.items():
        if type(val) is bool and val:  # toggle boolean values
            val = not current_options.get(option)
        new_options[option] = val

    target.active_attack.options.set_options(new_options)

    return default_options, current_options, new_options


@with_argparser(parser)
@with_category("Counterfit Commands")
def do_set(self, args: argparse.Namespace) -> None:
    """Set parameters of the active attack on the active target using 
    --param1 val1  --param2 val2.

    For infinity, use 'inf' or 'float("inf")'.

    This command replaces built-in "set" command, which is renamed to "setg".
    """
    target = CFState.state().get_active_target()
    if not target:
        CFPrint.warn("No active target. Try 'interact <target>'")
        return

    if not target.get_active_attack():
        CFPrint.warn("No active attack. Try 'use <attack>'")
        return

    default_options = target.active_attack.options.previous_options[0]

    for argname, argval in args.__dict__.items():
        if argname == 'clip_values':
            clip_values = get_clip_values(args.clip_values)
            if clip_values is None:
                return
            if clip_values=="None":  # None is a valid type we handle separately
                clip_values = None
            args.clip_values = clip_values
        elif argname == 'sample_index':
            sample_index = get_sample_index(args.sample_index)
            if sample_index is None:
                return
            args.sample_index = sample_index
        elif type(default_options.get(argname)) in (float, int) and type(argval) is str:
            # parse numeric type
            argval = parse_numeric(argname, argval)
            if argval is None:
                return
            args.__dict__[argname] = argval
        elif type(default_options.get(argname)) is bool:
            # parse boolean type
            argval = parse_boolean(argname, argval)
            if argval is None:
                return
            args.__dict__[argname] = argval

    default_options, current_options, new_options = update_options(target, args.__dict__)

    set_table(default_options, current_options, new_options)
