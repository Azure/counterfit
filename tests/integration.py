from rich.table import Table
import argparse
import json
import sys
from counterfit.core.state import CFState
from counterfit.core.output import CFPrint
from counterfit.core.utils import set_id
from counterfit.core.attacks import CFAttack
from counterfit.CFPrint.logger import AttackLogger


def run_test(framework, targets, attacks=None):
    run_id = set_id()
    CFState.state().frameworks.get(framework).load()

    results = {}
    for target in targets:
        new_target = CFState.state().load_target(target)
        if target not in results:
            results[target] = {}
            results[target]["build"] = {}
            results[target]["run"] = {}

            if not attacks:
                attacks = CFState.state().frameworks.get(framework).attacks

            for attack in attacks:
                try:
                    attack_id = CFState.state().build_new_attack(
                        target_name=target,
                        attack_name=attack,
                        scan_id="test"
                    )

                    results[target]["build"][attack] = "success"
                except Exception as e:
                    print(f"failed: {e}")
                    results[target]["build"][attack] = f"failed: {e}"
                    continue

                try:
                    CFState.state().run_attack(target, attack_id)
                    results[target]["run"][attack] = "success"
                except Exception as e:
                    results[target]["run"][attack] = "failed"
                    continue
    return results


def print_results(results):
    table = Table(header_style="bold magenta",
                  title="Test Results (pass/fail)")
    table.add_column("Target", no_wrap=True)
    table.add_column("Build", no_wrap=True)
    table.add_column("Run", no_wrap=True)
    i = {}
    for target, tests in results.items():
        i[target] = []
        for test_type, attacks in tests.items():
            success = 0
            failed = 0
            for attack, result in attacks.items():
                if "success" in result:
                    success += 1
                if "failed" in result:
                    failed += 1
            i[target].append((test_type, success, failed))

    for k, v in i.items():
        target = k
        build = f"{v[0][1]}/{v[0][2]}"
        run = f"{v[1][1]}/{v[1][2]}"
        table.add_row(target, build, run)

    CFPrint.output(table)


def main(args):
    with open(args.config_file, "r") as f:
        test_set = json.load(f)

    results = run_test(
        framework=args.framework,
        targets=test_set[args.framework]["targets"]
    )

    print_results(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--config_file", help="the config file to use", default="tests/tests.json")
    parser.add_argument("-f", "--framework",
                        help="the framework to test", required=True)

    args = parser.parse_args()
    main(args)
