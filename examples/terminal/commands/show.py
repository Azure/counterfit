import argparse
from pprint import pprint

import cmd2
from counterfit.core.output import CFPrint
from counterfit.reporting import ImageReportGenerator, TabularReportGenerator, TextReportGenerator
from examples.terminal.core.state import CFState
from rich.table import Table
from pprint import pprint

def show_results():
    # default to the active attack
    if not CFState.state().active_target:
        CFPrint.warn("No active target.")
        return
    if not CFState.state().active_attack:
        CFPrint.warn("No active acttack.")
        return
    cfattack = CFState.state().active_attack
    if cfattack.attack_status != 'complete':
        CFPrint.warn("No completed attacks.  Try 'run'.")
        return
    results_table = Table(header_style="bold magenta")
    results_table.add_column("Success")
    # results_table.add_column("Accuracy")
    results_table.add_column("Elapsed time")
    results_table.add_column("Total Queries")
    success = str(cfattack.success[0])
    # accuracy = str(cfattack.results)
    elapse_time = str(cfattack.elapsed_time)
    num_queries = str(cfattack.logger.num_queries)
    results_table.add_row(
        success,
        # accuracy,
        elapse_time,
        num_queries)
    CFPrint.output(results_table)

    active_target = CFState.state().active_target
    active_target_type = active_target.get_data_type_obj()

    results_folder = cfattack.get_results_folder()
    cfattack.save_run_summary(f"{results_folder}/run_summary.json")

    if active_target_type == 'TextReportGenerator':
        summary = TextReportGenerator.get_run_summary(cfattack)
        TextReportGenerator.print_run_summary(summary)
    elif active_target_type == 'ImageReportGenerator':
        summary = ImageReportGenerator.get_run_summary(cfattack)
        summary['result'] = ImageReportGenerator.save(cfattack.target, cfattack.results, results_path=results_folder)
        ImageReportGenerator.print_run_summary(summary)
    elif active_target_type == 'TabularReportGenerator':
        summary = TabularReportGenerator.get_run_summary(cfattack)
        TabularReportGenerator.print_run_summary(summary)
    else:
        raise RuntimeError(f'Counterfit does not support displaying result for data type "{active_target_type}"')

def show_options():
    # default to the active attack
    if not CFState.state().active_target:
        CFPrint.warn("No active target.")
        return

    if not CFState.state().active_attack:
        CFPrint.warn("No active acttack.")
        return   
    
    table = Table(header_style="bold magenta")
    table.add_column("Attack Options (type)")
    table.add_column("Default")
    table.add_column("Current")
    table.add_column("Docs")

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

def show_info():
    table = Table(header_style="bold magenta")
    table.add_column("Attack Field")
    table.add_column("Description")

    if not CFState.state().active_attack:
        CFPrint.warn("No active attack")
        return
    active_attack = CFState.state().active_attack
    framework_attack_info = None
    all_framework = CFState.state().get_frameworks()
    for framework_name, framework_info in all_framework.items():
        for attack_name, attack_info in framework_info['attacks'].items():
            if attack_info['attack_class'] == active_attack.name:
                framework_attack_info = attack_info
                framework_attack_info['framework_name'] = framework_name
    if not framework_attack_info:
        CFPrint.warn("Unable to find attack in the frameworks.")
        return
    # pprint(framework_attack_info)
    attack_name = framework_attack_info['attack_name']
    attack_type = framework_attack_info['attack_type']
    attack_category = framework_attack_info['attack_category']
    attack_tags = framework_attack_info['attack_data_tags']
    attack_docs = ' '.join(framework_attack_info['attack_docs'].split())
    attack_framework_name = framework_attack_info['framework_name']
    table.add_row("Name", attack_name)
    table.add_row("Type", attack_type)
    table.add_row("Category", attack_category)
    table.add_row("Tags", ", ".join(attack_tags))
    table.add_row("Framework", str(attack_framework_name))
    table.add_row("Docs", str(attack_docs))
    CFPrint.output(table)


def show_attacks():
    # Active attacks
    table = Table(header_style="bold magenta")
    table.add_column("Attack id")
    table.add_column("Target Name")
    table.add_column("Attack Name")
    table.add_column("Status")
    table.add_column("Success")

    # The target to attacks dic contains the mapping of each target to all the
    # attacks that were used against it.
    for target_obj, (attack_name2object) in CFState.state().target2attacks.items():
        target_name = target_obj.target_name
        for attack_name, attack in attack_name2object.items():
            if attack.attack_id == CFState.state().active_attack.attack_id:
                # Is current active attack
                row_style = "cyan"
                id = "*" + attack.attack_id
            else:
                row_style = None
                id = attack.attack_id
            if attack.success is None:
                attack_did_succeed = "N/A"
            else:
                sample_index = attack.options.cf_options['sample_index']
                if type(sample_index) is int:
                    sample_index = [sample_index]
                attack_did_succeed = str(dict(zip(list(sample_index), attack.success)))
            # The attack.name has the following example format e.g., "art.attacks.evasion.hop_skip_jump.HopSkipJump"
            attack_name = attack.name.split('.')[-1]
            table.add_row(
                id,
                target_name,
                attack_name,
                str(attack.attack_status),
                attack_did_succeed, style=row_style)
    CFPrint.output(table)



def show_cmd(args: argparse.Namespace) -> None:
    """
    'show info' describes the active attack.
    'show options' lists attack parameters.
    'show sample' displays the target data
    """
    option = args.option
    if option == "info":
        show_info()
    elif option == "options":
        show_options()
    elif option == "results":
        show_results()
    elif option == "attacks":
        show_attacks()
    else:
        pass

# show
show_args = cmd2.Cmd2ArgumentParser()
show_args.add_argument(
    "option",
    help="Show specific information about `info`, `options`, `results`, and `attacks`",
    choices=["info", "options", "results", "attacks"])
