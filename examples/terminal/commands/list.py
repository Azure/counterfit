import argparse

import cmd2
from examples.terminal.core.state import CFState
from counterfit.core.output import CFPrint
from rich.table import Table


def list_frameworks() -> Table:
    """
    List the frameworks with the number of attacks loaded. 

    Returns:
        Table: table of frameworks.
    """
    table = Table(header_style="bold magenta")
    table.add_column("Framework")
    table.add_column("# Attacks")

    for framework, framework_cls in sorted(CFState.state().get_frameworks().items()):
        table.add_row(framework, f"{len(framework_cls['attacks'])}")

    return table


def list_targets() -> Table:
    """
    List the available targets and their loaded status.

    Returns:
        Table: table of targets.
    """
    table = Table(header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Model Type")
    table.add_column("Data Type")
    table.add_column("Input Shape")
    table.add_column("# Samples")
    table.add_column("Endpoint")
    # table.add_column("Loaded")
    for target_name, target_obj in sorted(CFState.state().get_targets().items()):
        active_target_class = CFState.state().active_target.__class__
        if isinstance(target_obj, active_target_class):
            target_name = f"*{target_name}"
            row_style = "cyan"
        else:
            row_style = None
        input_shape = str(target_obj.input_shape)
        table.add_row(
            target_name,
            target_obj.classifier,
            target_obj.data_type,
            input_shape,
            f"{len(target_obj.X)}",
            target_obj.endpoint,
            style=row_style
        )

    return table


def list_attacks() -> Table:
    """List the available attack from all frameworks.

    Returns:
        Table: table of attacks
    """
    frameworks = CFState.state().get_frameworks()

    table = Table(header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Category")
    table.add_column("Type")
    table.add_column("Tags")
    # table.add_column("Docs")
    table.add_column("Framework")

    for framework_name, framework in frameworks.items():
        for k, v in sorted(framework["attacks"].items()):
            table.add_row(
                k,                                 # Name
                v["attack_category"],              # Category
                v["attack_type"],                  # Type
                ", ".join(v["attack_data_tags"]),  # Tags
                # v["attack_docs"].strip(),          # Docs
                framework_name                     # Framework
            )
    return table


def list_cmd(args: argparse.Namespace) -> None:
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
        CFPrint.warn("Argument not recognized: expecting 'targets', 'attacks', or 'frameworks'.\n")


list_args = cmd2.Cmd2ArgumentParser()
list_args.add_argument("option", choices=["targets", "attacks", "frameworks"])
