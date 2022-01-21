import argparse
from cmd2 import with_argparser
from cmd2 import with_category
from rich.table import Table
from counterfit.core.state import CFState
from counterfit.core.output import CFPrint


def set_table(default_options, current_options, new_options):
    default_options_list = CFState.state(
    ).active_target.active_attack.options.default_options_list

    cfattack_options_list = CFState.state(
    ).active_target.active_attack.options.cfattack_options_list

    table = Table(header_style="bold magenta")
    table.add_column("Algo Parameter (type)")
    table.add_column("Default")
    table.add_column("Current")
    table.add_column("New")

    # print attack params first
    table.add_row("Algo Parameters")
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
    table.add_row("CFAttack Options")
    table.add_row("--------------------", "--", "--", "--")
    for option in cfattack_options_list:
        default_value = default_options.get(option)
        current_value = current_options.get(option)
        new_value = new_options.get(option, "-")

        if new_value != current_value:
            table.add_row(f"{option} ({str(type(default_value).__name__)})",
                          str(default_value), str(current_value), str(new_value))
        else:
            table.add_row(f"{option} ({str(type(default_value).__name__)})",
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


# dynamic option add
parser = argparse.ArgumentParser()
for option, value in get_options().items():
    if type(value) == bool:
        parser.add_argument(f"--{option}", default=value, action="store_true")
    else:
        parser.add_argument(
            f"--{option}", type=type(value), default=value)


@with_argparser(parser)
@with_category("Counterfit Commands")
def do_set(self, args: argparse.Namespace) -> None:
    """Set parameters of the active attack on the active target using param1=val1 param2=val2 notation.
    This command replaces built-in "set" command, which is renamed to "setg".

    """
    
    from IPython.core.debugger import set_trace
    set_trace()
    
    if not args.__dict__.get('clip_values'):
        pass
    else:
        clip_values = []
        for value in args.clip_values:
            try:
                clip_values.append(float(value))
            except:
                continue
        args.clip_values = tuple(clip_values)

    target = CFState.state().get_active_target()
    if not target:
        CFPrint.warn("No active target. Try 'interact <target>'")
        return

    if not target.get_active_attack():
        CFPrint.warn("No active attack. Try 'use <attack>'")
        return

    default_options = target.active_attack.options.previous_options[0]
    current_options = target.active_attack.options.get_all_options()

    new_options = {}
    for option in target.active_attack.options.get_all_options().keys():
        new_options[option] = args.__dict__.get(option)

    target.active_attack.options.set_options(new_options)

    set_table(default_options, current_options, new_options)
