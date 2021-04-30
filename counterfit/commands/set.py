import cmd2
import argparse
import re

from typing import Any, List
from cmd2.table_creator import Column, SimpleTable, HorizontalAlignment

from collections import namedtuple
from counterfit.core.state import CFState

parser = argparse.ArgumentParser()
parser.add_argument("what", nargs="*", help="param1=val1 param2=val2")


@cmd2.with_argparser(parser)
@cmd2.with_category("Counterfit Commands")
def do_set(self, args):
    """Set parameters of the active attack on the active target using param1=val1 param2=val2 notation.
    This command replaces built-in "set" command, which is renamed to "setg".
    """

    if not CFState.get_instance().active_target:
        self.pwarning('\n [!] No active target. Try "setg" for setting global arguments.\n')
        return

    if not CFState.get_instance().active_target.active_attack:
        self.pwarning('\n [!] No active attack. Try "use <attack>".\n')
        return

    # 'set' with no options shows current variables, similar to "show options"
    if not args.what:
        self.pwarning('\n [!] No arguments specified.  Try "set <param>=<value>".\n')

    # create structure to ensure all params are present and ordered properly. Defaults to current params to prevent over writing with default values
    params_struct = namedtuple(
        "params",
        [i for i in CFState.get_instance().active_target.active_attack.parameters.keys()]
        + ["sample_index", "target_class"],
        defaults=list(CFState.get_instance().active_target.active_attack.parameters.values())
        + [
            CFState.get_instance().active_target.active_attack.sample_index,
            CFState.get_instance().active_target.active_attack.target_class,
        ],
    )

    # parse parameters and new values from the args
    try:
        params_to_update = re.findall(r"(\w+)\s?=\s?([\w\.]+)", " ".join(args.what))
    except:
        self.pwarning("\n [!] Failed to parse arguments.\n")
        return

    # create default params struct
    default_params = {k: v for k, v in CFState.get_instance().active_target.active_attack.default.items()}
    default_params["sample_index"] = CFState.get_instance().active_target.active_attack.sample_index
    default_params["target_class"] = CFState.get_instance().active_target.active_attack.target_class

    # ensure all current params exist and are ordered correctly
    default_params = params_struct(**default_params)._asdict()

    # convert string "True"/"true" and "False"/"false" to boolean
    for i, v in enumerate(params_to_update):
        if type(default_params.get(v[0], None)) is bool:
            if v[1].lower() == "true" or int(v[1]) == 1:
                params_to_update[i] = (v[0], True)
            elif v[1].lower() == "false" or int(v[1]) == 0:
                params_to_update[i] = (v[0], False)

    # create new params struct using default values where no new values are spec'd
    new_params = params_struct(**{i[0]: type(default_params.get(i[0], ""))(i[1]) for i in params_to_update})

    # create current params struct
    current_params = {k: v for k, v in CFState.get_instance().active_target.active_attack.parameters.items()}
    current_params["sample_index"] = CFState.get_instance().active_target.active_attack.sample_index
    current_params["target_class"] = CFState.get_instance().active_target.active_attack.target_class

    # ensure all current params exist and are ordered correctly
    current_params = params_struct(**current_params)._asdict()

    # separate target_class and sample_index from struct and update the relevant values
    CFState.get_instance().active_target.active_attack.parameters = {
        k: v for k, v in zip(new_params._fields[:-2], new_params[:-2])
    }
    CFState.get_instance().active_target.active_attack.sample_index = new_params.sample_index
    CFState.get_instance().active_target.active_attack.target_class = new_params.target_class

    # print info
    print_new_params = new_params._asdict() 

    columns: List[Column] = list()
    data_list: List[List[Any]] = list()
    columns.append(Column("Attack Parameter (type)", width=25, header_horiz_align=HorizontalAlignment.LEFT,data_horiz_align=HorizontalAlignment.RIGHT))
    columns.append(Column("Default", width=12, header_horiz_align=HorizontalAlignment.CENTER,data_horiz_align=HorizontalAlignment.LEFT))
    columns.append(Column("Previous", width=12, header_horiz_align=HorizontalAlignment.CENTER,data_horiz_align=HorizontalAlignment.LEFT))
    columns.append(Column("New", width=12, header_horiz_align=HorizontalAlignment.CENTER,data_horiz_align=HorizontalAlignment.LEFT))

    for k, default_value in default_params.items():
        param = f"{k} ({str(type(default_value).__name__)})"
        previous_value = current_params.get(k, "")
        new_value = print_new_params.get(k, "")
        if new_value != previous_value:
            data_list.append([param, str(default_value), str(previous_value), str(new_value)])

        else:
            data_list.append([param, str(default_value)[:11], str(previous_value)[:11], ""])

    st = SimpleTable(columns)
    print()
    print(st.generate_table(data_list, row_spacing=0))
    print()
