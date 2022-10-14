import numpy as np
from counterfit.core.reporting import CFReportGenerator
from counterfit.core.output import CFPrint
from rich.table import Table

class TabularReportGenerator(CFReportGenerator):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def printable(cls, target, batch, prefix=''):
        o = np.get_printoptions()
        np.set_printoptions(
            threshold=30, precision=2, floatmode="maxprec_equal", formatter=dict(float=lambda x: f"{x:4.2f}")
        )
        result = [str(np.array(row)).replace("\n", " ") for row in batch]
        np.set_printoptions(
            threshold=o["threshold"], precision=o["precision"], floatmode=o["floatmode"], formatter=o["formatter"]
        )
        return result

    @classmethod
    def get_run_summary(cls, cfattack):
        # count successes
        success_indicator = np.array(cfattack.success)  # numpy bool array
        batch_size = len(success_indicator)
        successes = sum(success_indicator)

        # initial scores/labels
        i_0 = cfattack.samples
        o_0 = cfattack.initial_outputs
        l_0 = cfattack.initial_labels

        # final scores/labels
        if cfattack.results is None:
            # failed attack? adopt originals
            i_f, o_f, l_f = i_0, o_0, l_0
        else:
            i_f = cfattack.results
            o_f = cfattack.final_outputs
            l_f = cfattack.final_labels

        # l2 norm
        i_0 = i_0.reshape(batch_size, -1).astype(float)
        i_f = i_f.reshape(batch_size, -1).astype(float)
        metric = "% Eucl. dist."
        eps = np.finfo("float32").eps
        rel_distance = np.sqrt(
            np.nansum(np.square(i_f - i_0), axis=1)) / (np.linalg.norm(i_0, axis=1) + eps)

        result = TabularReportGenerator.printable(
            cfattack.target, i_f, prefix=None)

        conf_0 = np.array([o_0[i][cfattack.target.output_classes.index(lab)]
                           for i, lab in enumerate(l_0)])
        conf_f = np.array([o_f[i][cfattack.target.output_classes.index(lab)]
                           for i, lab in enumerate(l_f)])

        degenerate = np.logical_and(l_0 != l_f, success_indicator == True)

        run_summary = {
            'batch_size': batch_size,
            'successes': successes,
            'input_change': rel_distance,
            'input_change_metric': metric,
            'initial_confidence': conf_0,
            'final_confidence': conf_f,
            'initial_label': l_0,
            'final_label': l_f,
            'sample_index': np.atleast_1d(cfattack.options.cf_options["sample_index"]["current"]),
            'type': cfattack.target.data_type,
            'result': result,
            'elapsed_time': cfattack.elapsed_time,
            'queries': cfattack.logger.num_queries,
            'attack_name': cfattack.name,
            'attack_id': cfattack.attack_id,
            'parameters': cfattack.options.attack_parameters,
            'targeted': cfattack.options.attack_parameters['targeted'] if 'targeted' in cfattack.options.attack_parameters.keys() else False,
            'target_label': cfattack.options.attack_parameters['target_labels'] if 'targeted' in cfattack.options.attack_parameters.keys() else "",
            'degenerate': degenerate
        }
        return run_summary

    @classmethod
    def print_run_summary(cls, summary):
        stats_table = Table(header_style="bold magenta")
        stats_table.add_column("Success", no_wrap=True)
        stats_table.add_column("Elapsed time", no_wrap=True)
        stats_table.add_column("Total Queries", no_wrap=True)

        if summary['elapsed_time'] > summary['queries']:
            query_rate = summary['elapsed_time'] / summary['queries']
            units = 'sec/query'
        else:
            query_rate = summary["queries"] / summary["elapsed_time"]
            units = "query/sec"

        stats_table.add_row(f"{summary['successes']}/{summary['batch_size']}",
                            f"{summary['elapsed_time']:.1f}", f"{summary['queries']:.0f} ({query_rate:.1f} {units})")

        CFPrint.output(stats_table)

        table = Table(header_style="bold magenta")
        metric = summary["input_change_metric"]
        table.add_column("Sample Index")
        table.add_column("Input Label (conf)")
        table.add_column("Adversarial Label (conf)")
        table.add_column(f"{metric}")
        table.add_column("Adversarial Input", width=110)
        table.add_column("success")
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
            table.add_row(
                str(si),
                str(label_confidence),
                str(final_confidence),
                str(round(change, 4)),
                str(res),
                str(d)
            )

        CFPrint.output(table)