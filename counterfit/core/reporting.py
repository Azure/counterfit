from abc import ABC
from abc import abstractmethod
import json

import numpy as np
from rich.table import Table
from counterfit.core.output import CFPrint

class CFReportGenerator(ABC):
    @abstractmethod
    def printable(target, batch):
        raise NotImplementedError()

    @abstractmethod
    def get_run_summary(target, cfattack):
        raise NotImplementedError()

    def printable_numpy(batch):
        o = np.get_printoptions()
        np.set_printoptions(
            threshold=30, precision=2, floatmode="maxprec_equal", formatter=dict(float=lambda x: f"{x:4.2f}")
        )
        result = [str(np.array(row)).replace("\n", " ") for row in batch]
        np.set_printoptions(
            threshold=o["threshold"], precision=o["precision"], floatmode=o["floatmode"], formatter=o["formatter"]
        )
        return result

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
                if (s['targeted'] and s['target_label'] == fl) or (s['targeted'] == False and fl != il):
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

    def printable_scan_summary(summaries_by_attack, summaries_by_label=None):
        """Print scan summaries in the command line console

        Args:
            summaries_by_attack ([dict]): Dictionary contains summary details per attack
            summaries_by_label ([dict], optional): Dictionary contains summary details per label. Defaults to None.
        """
        CFPrint.output(
            "\n =============== \n <SCAN SUMMARY> \n ===============\n\n")
        table = Table(header_style="bold magenta")
        table.add_column("Attack Name")
        table.add_column("Total Runs")
        table.add_column("Successes (%)")
        table.add_column("Best Score (attack_id)")
        table.add_column("Best Parameters", width=110)

        for name, summary in summaries_by_attack.items():
            frac = summary["total_successes"] / summary["total_runs"]
            successes = f"{summary['total_successes']} ({frac:>.1%})"
            best = (
                f"{summary['best_attack_score']:0.1f} ({summary['best_attack_id']})"
                if summary["best_attack_score"]
                else "N/A"
            )
            best_params = json.dumps(summary["best_params"])
            table.add_row(str(name), str(summary["total_runs"]), str(
                successes), str(best), str(best_params))
        st = Table(header_style="bold magenta")
        CFPrint.output(table)

        if summaries_by_label is not None:
            st.add_column("Class Label")
            st.add_column("Total Runs")
            st.add_column("Successes (%)")
            st.add_column("Best Score (Attack)")
            for name, summary in sorted(summaries_by_label.items()):
                frac = summary["total_successes"] / summary["total_runs"]
                successes = f"{summary['total_successes']} ({frac:>.1%})"
                best = (
                    f"{summary['best_attack_score']:0.1f} ({summary['best_attack_name']})"
                    if summary["best_attack_score"]
                    else "N/A"
                )
                st.add_row(str(name), str(
                    summary["total_runs"]), str(successes), str(best))

            CFPrint.output(st)
        output = ""
        times_str = f"{summary['min_time']:>4.1f}/{summary['avg_time']:>4.1f}/{summary['max_time']:>4.1f}"
        queries_str = f"{summary['min_queries']:>5d}/{summary['avg_queries']:>5d}/{summary['max_queries']:>5d}"
        output += f"[+] Time[sec] (min/avg/max) {times_str} \n"
        output += f"\n[+] Queries (min/avg/max) {queries_str} \n"
        CFPrint.output(output)
