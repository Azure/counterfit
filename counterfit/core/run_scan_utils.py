import numpy as np
import Levenshtein  # pip install python-Levenshtein
from cmd2.table_creator import Column, SimpleTable, HorizontalAlignment
from cmd2 import ansi
from typing import Any, List
import json
import os
import functools
import hashlib


bold_yellow = functools.partial(ansi.style, fg=ansi.fg.bright_yellow, bold=True)


def shallow_dict_to_fixed_width(d):
    return {k: f"{v:.4f}" if isinstance(v, float) else v for k, v in d.items()}


def printable_numpy(batch):
    o = np.get_printoptions()
    np.set_printoptions(
        threshold=30, precision=3, floatmode="maxprec_equal", formatter=dict(float=lambda x: f"{x:4.3f}")
    )
    result = [str(np.array(row)).replace("\n", " ") for row in batch]
    np.set_printoptions(
        threshold=o["threshold"], precision=o["precision"], floatmode=o["floatmode"], formatter=o["formatter"]
    )
    return result


def get_printable_batch(target, samples):
    if target.model_data_type == "text":
        result = samples

    if target.model_data_type == "image":
        result = []
        for image in samples:
            _id = hashlib.md5(target._key(image)).hexdigest()[:8]
            basename = f"{target.model_name}-sample-{_id}"
            filename = target._save_image(image, filename=basename)
            result.append(filename)

    else:  # numpy
        result = printable_numpy(samples)

    return result


def get_run_summary(target, attack=None):
    """ this function gathers statistics about a run and returns a dict """
    if attack is None:
        attack = target.active_attack

    # count successes
    success_indicator = target.check_attack_success()
    batch_size = len(success_indicator)
    successes = sum(success_indicator)

    # initial scores/labels
    i_0 = np.array(attack.results["initial"]["input"])
    o_0 = np.array(attack.results["initial"]["output"])
    l_0 = np.array(attack.results["initial"]["label"])

    # final scores/labels
    i_f = np.array(attack.results['final']['input'])
    o_f = np.array(attack.results['final']['output'])
    l_f = np.array(attack.results['final']['label'])

    # handle degenerate cases in which target_class is the true class
    targeted = attack.parameters.get("targeted", False)
    degenerate = np.logical_and(l_0 == l_f, success_indicator == True)

    # compute distance, depending on target
    if target.model_data_type == "text":
        # Levenshtein distance
        metric = "% edit dist."
        distances = [Levenshtein.distance(iif, ii0) for iif, ii0 in zip(i_f, i_0)]
        rel_distance = [d / len(ii0) for d, ii0 in zip(distances, i_0)]
    elif target.model_data_type == "numpy" or target.model_data_type == "image":
        # l2 norm
        i_0 = i_0.reshape(batch_size, -1).astype(float)
        i_f = i_f.reshape(batch_size, -1).astype(float)
        metric = "% Eucl. dist."
        eps = np.finfo("float32").eps
        rel_distance = np.sqrt(np.nansum(np.square(i_f - i_0), axis=1)) / (np.linalg.norm(i_0, axis=1) + eps)
    else:
        raise ValueError("Unexpected model_data_type")

    result = (
        attack.results["final"]["images"]
        if target.model_data_type == "image"
        else get_printable_batch(target, samples=i_f)
    )

    conf_0 = np.array([o_0[i, target.model_output_classes.index(lab)] for i, lab in enumerate(l_0)])
    conf_f = np.array([o_f[i, target.model_output_classes.index(lab)] for i, lab in enumerate(l_f)])

    params = attack.parameters.copy()
    params.update([("sample_index", attack.sample_index), ("target_class", attack.target_class)])

    return {
        'batch_size': batch_size,
        'successes': successes,
        'input_change': rel_distance,
        'input_change_metric': metric,
        'initial_confidence': conf_0,
        'final_confidence': conf_f,
        'initial_label': l_0,
        'final_label': l_f,
        'sample_index': np.atleast_1d(attack.sample_index),
        'type': target.model_data_type,
        'result': result,
        'elapsed_time': attack.results['elapsed_time'],
        'queries': attack.results['queries'],
        'attack_name': attack.attack_name,
        'attack_id': attack.attack_id,
        'parameters': params,
        'targeted': targeted,
        'target_class': attack.target_class,
        'degenerate': degenerate
    }


def get_printable_run_summary(summary):
    output = ""
    output += f"\n[+] {summary['successes']}/{summary['batch_size']} succeeded\n\n"
    if summary['elapsed_time'] > summary['queries']:
        query_rate = summary['elapsed_time'] / summary['queries']
        units = 'sec/query'
    else:
        query_rate = summary["queries"] / summary["elapsed_time"]
        units = "query/sec"

    metric = summary["input_change_metric"]
    terminal_cols = os.get_terminal_size().columns
    results_width = terminal_cols - 125  # default Windows is 120x30

    columns: List[Column] = list()
    columns.append(Column("", width=3))  # number
    columns.append(
        Column(
            "Sample Index",
            width=13,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Label (conf)",
            width=18,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Attack Label (conf)",
            width=19,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            metric,
            width=len(metric),
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Elapsed Time [sec]",
            width=18,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Queries (rate)",
            width=18,
            header_horiz_align=HorizontalAlignment.CENTER,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    if results_width > 0:
        columns.append(
            Column(
                "Attack Input",
                width=results_width,
                header_horiz_align=HorizontalAlignment.CENTER,
                data_horiz_align=HorizontalAlignment.LEFT,
            )
        )

    data_list: List[List[Any]] = list()

    elapsed_time_str = f"{summary['elapsed_time']:.1f}"
    query_rate_str = f"{summary['queries']:.0f} ({query_rate:.1f} {units})"

    for i, (si, li, conf_0, lf, conf_f, change, res, d) in enumerate(zip(
                summary["sample_index"],
                summary["initial_label"],
                summary["initial_confidence"],
                summary["final_label"],
                summary["final_confidence"],
                summary["input_change"],
                summary["result"],
                summary["degenerate"])):
        label_confidence = f"{li} ({conf_0:.4f})"
        final_confidence = f"{lf} ({conf_f:.4f})"

        if d:
            label_confidence = f"{bold_yellow('*')} " + label_confidence
            final_confidence = f"{bold_yellow('*')} " + final_confidence
            
        change_str = f"{change:.5%}"
        if results_width > 0:
            data_list.append(
                [
                    f"{i+1}.",
                    si,
                    label_confidence,
                    final_confidence,
                    change_str,
                    elapsed_time_str,
                    query_rate_str,
                    str(np.array(res)),
                ]
            )
        else:
            data_list.append(
                [
                    f"{i+1}.",
                    si,
                    label_confidence,
                    final_confidence,
                    change_str,
                    elapsed_time_str,
                    query_rate_str,
                ]
            )

    if sum(summary["degenerate"]) > 0:
        output += bold_yellow(" * target_class is the same as the original class") + "\n\n"

    if results_width <= 0:
        output = bold_yellow("""\nIncrease terminal width to show results.\n""") + output

    # return table as output
    st = SimpleTable(columns)
    return output + '\n' + st.generate_table(data_list, row_spacing=0) + '\n'


def get_scan_summary(list_of_runs):
    # summarize by attack -- what is the best
    #   - success rate
    #   - average time
    #   - best result (highest confidence confusion)
    #   - attack_id for best parameters
    #   - attack_name
    total_successes = sum([s["successes"] for s in list_of_runs])
    total_runs = sum([s["batch_size"] for s in list_of_runs])

    times = [s["elapsed_time"] for s in list_of_runs]
    queries = [s["queries"] for s in list_of_runs]

    best_attack = None
    best_id = None
    best_score = None
    best_params = None
    best_queries = None
    for s in list_of_runs:
        for conf, il, fl in zip(s['final_confidence'], s['initial_label'], s['final_label']):
            if (s['targeted'] and s['target_class'] == fl) or (s['targeted']==False and fl != il):
                if best_score is None or conf > best_score or (conf == best_score and s['queries'] < best_queries):
                    best_score = conf
                    best_id = s["attack_id"]
                    best_attack = s["attack_name"]
                    best_params = s["parameters"]
                    best_queries = s["queries"]

    return {
        "total_runs": total_runs,
        "total_successes": total_successes,
        "avg_time": np.mean(times),
        "min_time": np.min(times),
        "max_time": np.max(times),
        "avg_queries": int(np.mean(queries)),
        "min_queries": np.min(queries),
        "max_queries": np.max(queries),
        "best_attack_name": best_attack,
        "best_attack_id": best_id,
        "best_attack_score": best_score,
        "best_params": best_params,
    }


def get_printable_scan_summary(summaries_by_attack, summaries_by_label=None):
    output = "\n =============== \n SCAN SUMMARY \n ===============\n\n"

    terminal_cols = os.get_terminal_size().columns
    results_width = terminal_cols - 128  # default Windows is 120x30

    if results_width <= 0:
        output += bold_yellow("""\nIncrease terminal width to show parameters.\n\n""")

    columns: List[Column] = list()
    columns.append(
        Column(
            "Attack Name",
            width=15,
            header_horiz_align=HorizontalAlignment.LEFT,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Total Runs",
            width=10,
            header_horiz_align=HorizontalAlignment.LEFT,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Successes (%)",
            width=13,
            header_horiz_align=HorizontalAlignment.LEFT,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Time[sec] (min/avg/max)",
            width=15,
            header_horiz_align=HorizontalAlignment.LEFT,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Queries (min/avg/max)",
            width=18,
            header_horiz_align=HorizontalAlignment.LEFT,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    columns.append(
        Column(
            "Best Score (attack_id)",
            width=15,
            header_horiz_align=HorizontalAlignment.LEFT,
            data_horiz_align=HorizontalAlignment.RIGHT,
        )
    )
    if results_width > 0:
        columns.append(
            Column(
                "Best Parameters",
                width=25,
                header_horiz_align=HorizontalAlignment.RIGHT,
                data_horiz_align=HorizontalAlignment.RIGHT,
            )
        )

    data_list: List[List[Any]] = list()

    for name, summary in summaries_by_attack.items():
        frac = summary["total_successes"] / summary["total_runs"]
        successes = f"{summary['total_successes']} ({frac:>.1%})"
        times = f"{summary['min_time']:>4.1f}/{summary['avg_time']:>4.1f}/{summary['max_time']:>4.1f}"
        queries = f"{summary['min_queries']:>5d}/{summary['avg_queries']:>5d}/{summary['max_queries']:>5d}"
        best = (
            f"{summary['best_attack_score']:0.1f} ({summary['best_attack_id']})"
            if summary["best_attack_score"]
            else "N/A"
        )
        if results_width > 0:
            if summary["best_params"] is not None:
                trunc_params = shallow_dict_to_fixed_width((summary["best_params"]))
                param_str = json.dumps(trunc_params, indent=1, separators=("", "="))[2:-1].replace('"', "")
            else:
                param_str = "N/A"
            data_list.append([name, summary["total_runs"], successes, times, queries, best, param_str])
        else:
            data_list.append([name, summary["total_runs"], successes, times, queries, best])
    st = SimpleTable(columns)
    output += '\n' + st.generate_table(data_list, row_spacing=0) + '\n'

    if summaries_by_label is not None:
        output += "\n"

        # table by sample_index
        columns: List[Column] = list()
        columns.append(
            Column(
                "Class Label",
                width=15,
                header_horiz_align=HorizontalAlignment.LEFT,
                data_horiz_align=HorizontalAlignment.RIGHT,
            )
        )
        columns.append(
            Column(
                "Total Runs",
                width=10,
                header_horiz_align=HorizontalAlignment.LEFT,
                data_horiz_align=HorizontalAlignment.RIGHT,
            )
        )
        columns.append(
            Column(
                "Successes (%)",
                width=13,
                header_horiz_align=HorizontalAlignment.LEFT,
                data_horiz_align=HorizontalAlignment.RIGHT,
            )
        )
        columns.append(
            Column(
                "Time[sec] (min/avg/max)",
                width=15,
                header_horiz_align=HorizontalAlignment.LEFT,
                data_horiz_align=HorizontalAlignment.RIGHT,
            )
        )
        columns.append(
            Column(
                "Queries (min/avg/max)",
                width=18,
                header_horiz_align=HorizontalAlignment.LEFT,
                data_horiz_align=HorizontalAlignment.RIGHT,
            )
        )
        columns.append(
            Column(
                "Best Score (Attack)",
                width=15,
                header_horiz_align=HorizontalAlignment.LEFT,
                data_horiz_align=HorizontalAlignment.RIGHT,
            )
        )

        data_list: List[List[Any]] = list()

        for name, summary in sorted(summaries_by_label.items()):
            frac = summary["total_successes"] / summary["total_runs"]
            successes = f"{summary['total_successes']} ({frac:>.1%})"
            times = f"{summary['min_time']:>4.1f}/{summary['avg_time']:>4.1f}/{summary['max_time']:>4.1f}"
            queries = f"{summary['min_queries']:>5d}/{summary['avg_queries']:>5d}/{summary['max_queries']:>5d}"
            best = (
                f"{summary['best_attack_score']:0.1f} ({summary['best_attack_name']})"
                if summary["best_attack_score"]
                else "N/A"
            )
            data_list.append([name, summary["total_runs"], successes, times, queries, best])

        st = SimpleTable(columns)
        output += '\n' + st.generate_table(data_list, row_spacing=0) + '\n'

    return output
