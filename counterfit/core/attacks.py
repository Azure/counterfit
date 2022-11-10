from __future__ import annotations

import datetime
import os
import uuid

import orjson
from counterfit.core.logger import CFLogger, get_attack_logger_obj
from counterfit.core.options import CFOptions
from counterfit.core.targets import CFTarget


class CFAttack:
    """
    The base class for all attacks in all frameworks.
    """

    name: str
    target: CFTarget
    framework: None
    attack: CFAttack
    attack_id: str
    options: CFOptions
    scan_id: str

    def __init__(
        self,
        name,
        target,
        framework,
        attack,
        options,
        scan_id=None):

        
        # Parent framework
        self.name = name
        self.attack_id = uuid.uuid4().hex[:8]
        self.scan_id = scan_id
        self.target = target
        self.framework = framework
        self.attack = attack
        self.options = options

        # Attack information
        self.created_on = datetime.datetime.utcnow().strftime("%m%d%y_%H:%M:%S_UTC")
        self.attack_status = "pending"

        # Algo parameters
        self.samples = None
        self.initial_labels = None
        self.initial_outputs = None

        # Attack results
        self.final_outputs = None
        self.final_labels = None
        self.results: list = None
        self.success = None
        self.elapsed_time = None

        # reporting
        self.run_summary = None
        self.logger: CFLogger = None


    def prepare_attack(self):
        curr_log = self.options.cf_options["logger"]["current"]
        self.logger = self.set_logger(logger=curr_log)
        self.target.logger = self.logger

        # Get the samples.
        curr_idx = self.options.cf_options["sample_index"]["current"]
        self.samples = self.target.get_samples(curr_idx)

        # Send a request to the target for the selected sample
        outputs, labels = self.target.get_sample_labels(self.samples)
        self.initial_outputs = outputs
        self.initial_labels = labels
  
    def set_results(self, results: object) -> None:
        self.results = results

    def set_status(self, status: str) -> None:
        self.attack_status = status

    def set_success(self, success: bool = False) -> None:
        self.success = success

    def set_logger(self, logger: str) -> CFLogger:
        new_logger = get_attack_logger_obj(logger)
        logger = new_logger(attack_id=self.attack_id, ts=self.created_on)
        return logger

    def set_elapsed_time(self, start_time, end_time) -> float:
        self.elapsed_time = end_time - start_time

    def get_results_folder(self) -> str:
        results_folder = self.target.get_results_folder()

        if not os.path.exists(results_folder):
            os.mkdir(results_folder)

        scan_folder = os.path.join(results_folder, self.attack_id)
        if not os.path.exists(scan_folder):
            os.mkdir(scan_folder)

        return scan_folder

    def save_run_summary(self, filename: str=None, verbose: bool =False) -> None:
        run_summary = {
            "sample_index": self.options.cf_options['sample_index'],
            "initial_labels": self.initial_labels,
            "final_labels": self.final_labels,
            "elapsed_time": self.elapsed_time,
            "num_queries": self.logger.num_queries,
            "success": self.success,
            "results": self.results
        }

        if verbose:
            run_summary["input_samples"] = self.samples

        options = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_APPEND_NEWLINE
        data = orjson.dumps(run_summary, option=options)

        if not filename:
            results_folder = self.get_results_folder()
            filename = f"{results_folder}/run_summary.json"

        with open(filename, "wb") as summary_file:
            summary_file.write(data)
