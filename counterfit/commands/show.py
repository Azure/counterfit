import argparse
from collections import namedtuple
from typing import Any, List
import cmd2
from cmd2.table_creator import Column, SimpleTable, HorizontalAlignment
from counterfit.core.run_scan_utils import get_printable_batch, get_run_summary, get_printable_run_summary
from counterfit.core.state import CFState

# show
base_parser = argparse.ArgumentParser()
base_subparsers = base_parser.add_subparsers(title="subcommands", help="show information about models and targets")

# show info
parser_info = base_subparsers.add_parser("info", help="show information about the model and active attack")
parser_info.add_argument(
    "--attack",
    choices=CFState.get_instance().loaded_attacks.keys(),
    default=None,
    help="attack to show info (defaults to active attack)",
)
parser_info.add_argument(
    "--target",
    choices=CFState.get_instance().loaded_targets.keys(),
    default=None,
    help="target to show info (defaults to active target)",
)

# show options
parser_options = base_subparsers.add_parser("options", help="show configuration options for the active attack")
parser_options.add_argument(
    "--attack",
    choices=CFState.get_instance().loaded_attacks.keys(),
    default=None,
    help="attack to show info (defaults to active attack)",
)


# show sample
parser_sample = base_subparsers.add_parser("sample", help="show specified sample")
parser_sample.add_argument(
    "-i",
    "--index",
    default=None,
    type=int,
    help="sample index to show (defaults to the sample_index set in the active attack)",
)
parser_sample.add_argument("-r", "--result", action="store_true", help="show the result of the active attack")

# show results
parser_results = base_subparsers.add_parser("results", help="show results from the active attack")


def show_current_sample(target, samples, heading1=None, sample_index=None):
    columns: List[Column] = list()
    data_list: List[List[Any]] = list()

    if sample_index is None:
        sample_index = target.active_attack.sample_index

    if heading1 is None:
        heading1 = "Sample Index"

    # future support for multiple indices
    if not hasattr(sample_index, "__iter__"):
        sample_index = [sample_index]

    columns.append(
        Column(
            heading1,
            width=20,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Value",
            width=80,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.LEFT,
        )
    )

    for index, value in zip(sample_index, samples):
        data_list.append([index, value])

    st = SimpleTable(columns)
    output = "\n" + st.generate_table(data_list, row_spacing=0) + "\n"
    return output


def show_attack_info(attack):
    columns: List[Column] = list()
    data_list: List[List[Any]] = list()

    columns.append(
        Column(
            "",
            width=25,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column("", width=80, header_horiz_align=HorizontalAlignment.CENTER, data_horiz_align=HorizontalAlignment.LEFT)
    )

    st = SimpleTable(columns)

    data_list.append(["attack name", attack.attack_name])
    data_list.append(["attack type", attack.attack_type])
    data_list.append(["attack category", attack.category])
    data_list.append(["attack tags", attack.tags])
    data_list.append(["attack framework", attack.framework])
    if attack.attack_cls.__doc__:
        data_list.append(["attack docs", attack.attack_cls.__doc__.replace('\n',' ').replace('\t', '').replace('  ', ' ')])

    output = '\nAttack Information' + st.generate_table(data_list, row_spacing=0) + "\n"

    output += "\n" + show_attack_options(attack)

    return output


def show_attack_options(attack):
    columns: List[Column] = list()
    data_list: List[List[Any]] = list()

    # create structure to ensure all params are present
    params_struct = namedtuple(
        "params",
        [i for i in attack.default.keys()] + ["sample_index", "target_class"],
        defaults=list(attack.default.values()) + [0, 0],
    )

    # get default parameters
    default_params = params_struct()

    if hasattr(attack, 'parameters'):
        # get current parameters
        current_params = {k: v for k, v in attack.parameters.items()}
        current_params["sample_index"] = attack.sample_index
        current_params["target_class"] = attack.target_class

        # ensure everything exists and is ordered correctly
        current_params = params_struct(**current_params)._asdict()

    columns.append(
        Column(
            "Attack Parameter (type)",
            width=25,
            header_horiz_align=HorizontalAlignment.LEFT,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Default",
            width=12,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.LEFT,
        )
    )
    if hasattr(attack, 'parameters'):
        columns.append(
            Column(
                "Current",
                width=12,
                header_horiz_align=HorizontalAlignment.CENTER,
                data_horiz_align=HorizontalAlignment.LEFT,
            )
        )
    st = SimpleTable(columns)

    for k, v in zip(default_params._fields, default_params):
        param = f"{k} ({str(type(v).__name__)})"
        default_value = v
        if hasattr(attack, 'parameters'): # active attack with current parameters?
            current_value = current_params.get(k, "")
            data_list.append([param, default_value, current_value])
        else:
            data_list.append([param, default_value])

    return st.generate_table(data_list, row_spacing=0) + "\n"
    # not returning a header, because this is used in two places


def show_target_info(target):
    columns: List[Column] = list()
    data_list: List[List[Any]] = list()

    columns.append(
        Column("", width=25, header_horiz_align=HorizontalAlignment.CENTER, data_horiz_align=HorizontalAlignment.RIGHT)
    )
    columns.append(
        Column("", width=80, header_horiz_align=HorizontalAlignment.CENTER, data_horiz_align=HorizontalAlignment.LEFT)
    )

    st = SimpleTable(columns)
    output = "\nTarget Information"

    data_list.append(["model name", target.model_name])
    data_list.append(["model data type", target.model_data_type])
    data_list.append(["model endpoint", target.model_endpoint])
    data_list.append(["model input shape", target.model_input_shape])
    data_list.append([f"model output classes ({len(target.model_output_classes)})", target.model_output_classes])
    if target.__doc__:
        data_list.append(["model docs", target.__doc__])

    output += st.generate_table(data_list, row_spacing=0) + "\n"

    if target.active_attack:
        output += show_attack_info(target.active_attack)
        
    return output


def show_info(self, args):
    if args.target:
        target = CFState.get_instance().loaded_targets.get(args.target, None)
        if not target:
            self.pwarning(f"\n [!] Invalid target '{args.target}'.\n")
            return
        else:
            self.poutput(show_target_info(target))

    if not args.target and not args.attack:
        target = CFState.get_instance().active_target
        if not target:
            self.pwarning("\n [!] No active target.\n")
            return
        else:
            self.poutput(show_target_info(target))
            return

    if args.attack:
        attack = CFState.get_instance().loaded_attacks.get(args.attack, None)
        if not attack:
            self.pwarning(f"\n [!] Invalid attack '{args.attack}'.\n")
            return
        else:
            self.poutput(show_attack_info(attack))
            return

def show_options(self, args):
    if args.attack:
        try:
            attack = CFState.get_instance().loaded_attacks.get(args.attack, None)
        except AttributeError:
            self.pwarning("\n [!] Attack not found.\n")
    else:
        # default to the active attack
        try:
            attack = CFState.get_instance().active_target.active_attack
        except AttributeError:
            self.pwarning("\n [!] Interact with a target and set an active target first.\n")
            return

    if attack is None:
        self.pwarning("\n [!] No active attack. Try 'use'.\n")
        return

    self.poutput("\n" + show_attack_options(attack))


def show_sample(self, args):
    try:
        target = CFState.get_instance().active_target
        attack = target.active_attack
    except AttributeError:
        self.pwarning("\n [!] Interact with a target and set an active target first.\n")
        return

    if attack is None:
        self.pwarning("\n [!] No active attack. Try 'use'.\n")
        return

    if args.index is not None and args.result:
        self.pwarning("\n [!] Cannot specify both an index and a result.\n")
        return

    if args.result:
        try:
            samples = target.active_attack.results["final"]["input"]
            sample_index = [target.active_attack.attack_id] * len(samples)
            heading1 = "attack id"
        except (KeyError, AttributeError):
            self.p("\n [!] No results found. First 'run' an attack.\n")
            return
    elif args.index is None:
        restore_index = attack.sample_index
        target.set_attack_samples(attack.sample_index)
        samples = attack.samples
        target.set_attack_samples(restore_index)
        sample_index = attack.sample_index
        heading1 = None
    else:
        restore_index = attack.sample_index
        target.set_attack_samples(args.index)
        samples = attack.samples
        target.set_attack_samples(restore_index)
        sample_index = args.index
        heading1 = None

    self.poutput(show_current_sample(target, get_printable_batch(target, samples), heading1, sample_index))


def show_results(self, args):
    try:
        summary = get_run_summary(CFState.get_instance().active_target)
    except (KeyError, AttributeError, TypeError):
        self.pwarning("\n [!] No results found. First 'run' an attack.\n")
        return

    self.poutput(get_printable_run_summary(summary))


# Set handler functions for the subcommands
parser_info.set_defaults(func=show_info)
parser_options.set_defaults(func=show_options)
parser_sample.set_defaults(func=show_sample)
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
