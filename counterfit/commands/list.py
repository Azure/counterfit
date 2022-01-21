import argparse
from rich.table import Table
from cmd2 import with_argparser
from cmd2 import with_category

from counterfit.core.output import CFPrint
from counterfit.core.state import CFState


def list_frameworks() -> Table:
    """
    List the frameworks with the number of attacks loaded. 

    Returns:
        Table: table of frameworks.
    """
    table = Table(header_style="bold magenta")
    table.add_column("Framework")
    table.add_column("# Attacks")
    #table.add_column("Loaded Attacks", justify="center")

    for framework, framework_cls in sorted(CFState.state().frameworks.items()):
        table.add_row(framework, str(len(framework_cls.attacks)))

    return table


def list_targets() -> Table:
    """
    List the available targets and their loaded status.

    Returns:
        Table: table of targets.
    """
    table = Table(header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Input Shape")
    table.add_column("Endpoint")
    table.add_column("Loaded")

    for target_name, target_obj in sorted(CFState.state().targets.items()):
        if target_obj == CFState.state().active_target:
            target_name = f"*{target_name}"
            row_style = "cyan"
        else:
            row_style = None

        target_input_shape = str(target_obj.target_input_shape)
        table.add_row(
            target_name,
            target_obj.target_data_type,
            target_input_shape,
            target_obj.target_endpoint,
            str(target_obj.loaded_status),
            style=row_style
        )

    return table


def list_attacks() -> Table:
    """List the available attack from all frameworks.

    Returns:
        Table: table of attacks
    """
    table = Table(header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Type")
    table.add_column("Tags")
    table.add_column("Framework")

    frameworks = CFState.state().get_frameworks()
    for framework_name, framework in frameworks.items():
        for k, v in sorted(framework.attacks.items()):
            table.add_row(
                k,                             # Name
                v.attack_category,             # Category
                v.attack_type,                 # Type
                ", ".join(v.attack_data_tags), # Tags
                framework_name                 # Framework
            )
    return table


parser = argparse.ArgumentParser()
parser.add_argument("option", choices=["targets", "attacks", "frameworks"])


@with_argparser(parser)
@with_category("Counterfit Commands")
def do_list(self, args: argparse.Namespace) -> None:
    """List the available targets, frameworks, or attacks.

    Args:
        option (str): One of targets, attacks, or frameworks.
    """

    if args.option.lower() == "targets":
        CFPrint.output(list_targets())
    elif args.option.lower() == "attacks":
        CFPrint.output(list_attacks())
    elif args.option.lower() == "frameworks":
        CFPrint.output(list_frameworks())
    else:
        CFPrint.warn(
            "Argument not recognized: expecting 'targets', 'attacks', or 'frameworks'.\n")
