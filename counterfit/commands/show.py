import cmd2
import argparse
from rich.table import Table
from counterfit.core.state import CFState
from counterfit.core.output import CFPrint

# show
base_parser = argparse.ArgumentParser()
base_subparsers = base_parser.add_subparsers(title="subcommands", help="show information about models and targets")

# show info
parser_info = base_subparsers.add_parser("info", help="show information about the model and active attack")
parser_info.add_argument("--attack", default=None, help="attack to show info (defaults to active attack)")

# show options
parser_options = base_subparsers.add_parser("options", help="show configuration options for the active attack")
parser_options.add_argument("--attack", default=None, help="attack to show info (defaults to active attack)")

# show results
parser_results = base_subparsers.add_parser("results", help="show results from the active attack")

# show attacks
parser_attacks = base_subparsers.add_parser("attacks", help="show the list of attacks run against this target")


def show_results(self, args):
    # default to the active attack
    if not CFState.state().active_target:
        CFPrint.warn("No active target.")
        return

    if not CFState.state().active_target.active_attack:
        CFPrint.warn("No active acttack.")
        return

    cfattack = CFState.state().active_target.active_attack
    if cfattack.attack_status != 'complete':
        CFPrint.warn("No completed attacks.  Try 'run'.")
        return

    # Get the framework responsible for the attack
    framework = CFState.state().frameworks.get(cfattack.framework_name)

    # Give the framework an opportunity to process the results, generate reports, etc
    framework.post_attack_processing(cfattack)


def show_options(self, args):
    # default to the active attack
    if not CFState.state().active_target:
        CFPrint.warn("No active target.")
        return

    if not CFState.state().active_target.active_attack:
        CFPrint.warn("No active acttack.")
        return

    current_options = CFState.state().active_target.active_attack.options.get_all_options()
    default_options = CFState.state(
    ).active_target.active_attack.options.previous_options[0]

    default_options_list = CFState.state(
    ).active_target.active_attack.options.default_options_list

    cfattack_options_list = CFState.state(
    ).active_target.active_attack.options.cfattack_options_list

    table = Table(header_style="bold magenta")
    table.add_column("Attack Options (type)")
    table.add_column("Default")
    table.add_column("Current")

    # print attack params first
    table.add_row("Algo Parameters")
    table.add_row("--------------------", "--", "--")
    for option in default_options_list:
        default_value = default_options.get(option)
        current_value = current_options.get(option)
        table.add_row(f"{option} ({str(type(default_value).__name__)})",
                      str(default_value), str(current_value))

    # print cfspecific options next
    table.add_row()
    table.add_row("CFAttack Options")
    table.add_row("--------------------", "--", "--")
    for option in cfattack_options_list:
        default_value = default_options.get(option)
        current_value = current_options.get(option)
        table.add_row(f"{option} ({str(type(default_value).__name__)})",
                      str(default_value), str(current_value))

    CFPrint.output(table)

def show_info(self, args):
    table = Table(header_style="bold magenta")
    table.add_column("Attack Info")
    table.add_column("-----------")

    if CFState.state().active_target and hasattr(CFState.state().active_target, 'active_attack'):
        cfattack = CFState.state().active_target.active_attack
        if cfattack is None:
            CFPrint.warn("No active attack")
            return
        framework = CFState.state().frameworks.get(cfattack.framework_name)
        attack = framework.attacks.get(cfattack.attack_name)
    else:
        CFPrint.warn("No active attack")
        return
 
    table.add_row("Attack name", str(attack.attack_name))
    table.add_row("Attack type", str(attack.attack_type))
    table.add_row("Attack category", str(attack.attack_category))
    table.add_row("Attack tags", ", ".join(attack.attack_data_tags))
    table.add_row("Attack framework", str(attack.framework_name))
    table.add_row("Docs", str(attack.attack_class.__doc__))
    CFPrint.output(table)


def show_attacks(self, args):
    # Active attacks
    table = Table(header_style="bold magenta")
    table.add_column("Attack id")
    table.add_column("Name")
    table.add_column("Status")
    table.add_column("Success")

    if CFState.state().active_target:
        for k, v in CFState.state().active_target.attacks.items():
            if k == CFState.state().active_target.active_attack.attack_id:
                row_style = "cyan"
                id = "*" + k
            else:
                row_style = None
                id = k

            if v.success is None:
                success = "N/A"
            else:
                sample_index = v.options.sample_index
                if type(sample_index) is int:
                    sample_index = [sample_index]
                success = str(dict(zip(list(sample_index), v.success)))

            table.add_row(
                id,
                v.attack_name,
                str(v.attack_status),
                success,
                style=row_style

            )

    CFPrint.output(table)


parser_options.set_defaults(func=show_options)
parser_attacks.set_defaults(func=show_attacks)
parser_info.set_defaults(func=show_info)
parser_results.set_defaults(func=show_results)


@cmd2.with_argparser(base_parser)
@cmd2.with_category("Counterfit Commands")
def do_show(self, args):
    """'show info' describes the active attack.
    'show options' lists attack parameters.
    'show sample' displays the target data
    """

    func = getattr(args, "func", None)

    if func is not None:
        func(self, args)
    else:
        self.do_help("show")
