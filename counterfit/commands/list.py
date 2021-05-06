import argparse
from typing import Any, List
from cmd2.table_creator import Column, SimpleTable
from counterfit.core.state import CFState
import cmd2

parser = argparse.ArgumentParser()
parser.add_argument("type", choices=["targets", "attacks", "frameworks"])


def list_frameworks():
    columns: List[Column] = list()
    data_list: List[List[Any]] = list()
    columns.append(Column("Framework", width=20))
    columns.append(Column("# of Attacks", width=30))
    for framework, list_of_attacks in CFState.get_instance().loaded_frameworks.items():
        data_list.append([framework, len(list_of_attacks)])
    st = SimpleTable(columns)
    print()
    print(st.generate_table(data_list, row_spacing=0))
    print()


def list_targets():
    columns: List[Column] = list()
    data_list: List[List[Any]] = list()
    columns.append(Column("Name", width=15))
    columns.append(Column("Type", width=15))
    columns.append(Column("Input Shape", width=15))
    columns.append(Column("Location", width=85))
    for _, target_obj in CFState.get_instance().loaded_targets.items():
        shp = str(target_obj.model_input_shape)
        data_list.append([target_obj.model_name, target_obj.model_data_type, shp, target_obj.model_endpoint])
    st = SimpleTable(columns)
    print()
    print(
        st.generate_table(
            data_list,
            row_spacing=0,
        )
    )
    print()


def list_attacks():
    columns: List[Column] = list()
    data_list: List[List[Any]] = list()
    columns.append(Column("Name", width=25))
    columns.append(Column("Type", width=15))
    columns.append(Column("Category", width=15))
    columns.append(Column("Tags", width=15))
    columns.append(Column("Framework", width=10))
    for _, attack_obj in CFState.get_instance().loaded_attacks.items():
        tags = ", ".join(attack_obj.tags)
        data_list.append(
            [attack_obj.attack_name, attack_obj.attack_type, attack_obj.category, tags, attack_obj.framework]
        )
    st = SimpleTable(columns)
    print()
    print(st.generate_table(data_list, row_spacing=0))
    print()


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_list(self, args):
    """List the available targets, frameworks, or attacks."""

    if args.type.lower() == "targets":
        list_targets()

    elif args.type.lower() == "attacks":
        if not CFState.get_instance().loaded_attacks:
            self.pwarning("\n [!] No frameworks have been loaded. Try 'load <framework>'.\n")
        else:
            list_attacks()

    elif args.type.lower() == "frameworks":
        list_frameworks()

    else:
        self.pwarning("\n [!] Argument not recognized: expecting 'targets', 'attacks', or 'frameworks'.\n")
