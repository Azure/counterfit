import os
import orjson
import datetime

from counterfit.core.output import CFPrint
from counterfit.logging.logging import get_attack_logger_obj
from counterfit.report.report_generator import get_target_data_type_obj

class CFAttackOptions:
    """A container class for all settable options for a `CFAttack.attack`. Default parameters should 
    be loaded during `framework.load()` and added to `attack_default_params`. Additionally, a
    number of global Counterfit options are injected.
    """
    def __init__(self, **kwargs):
        self.previous_options = []
        for key, value in kwargs.items():
            if key == "targeted":
                value = False
                setattr(self, "target_labels", 0)
            if key == "verbose":
                value = False
            setattr(self, key, value)

        # Save the default options as the first value in previous_options
        self.save_previous_options()

    def get_default_options(self) -> dict:
        """Get the default options.

        Returns:
            dict: A dictionary of default options for `CFAttack.attack`
        """
        default_options = {}
        for option in self.default_options_list:
            default_options[option] = getattr(self, option)

        return default_options

    def get_current_options(self) -> dict:
        """Get the current options.

        Returns:
            dict: A dictionary of current options for `CFAttack`
        """
        parameters = {}
        for param in self.default_options_list:
            parameters[param] = getattr(self, param)
        return parameters

    def get_all_options(self) -> dict:
        """Get all options.

        Returns:
            dict: A dictionary of all available options for `CFAttack`
        """
        available_options = {}
        all_options_list = self.default_options_list + self.cfattack_options_list
        for option in all_options_list:
            available_options[option] = getattr(self, option)
        return available_options

    def save_previous_options(self):
        """Save the previous options.
        """
        current_options = self.get_all_options()
        self.previous_options.append(current_options)        

    def set_options(self, options_to_update: dict) -> None:
        """Sets an option. Take in a dictionary of options and applies attack specific checks before saving them as attributes.

        Args:
            params_to_update (dict): A dictionary of `{option:value}`
        """

        # Save the previous options
        self.save_previous_options()

        for k, v in options_to_update.items():
            setattr(self, k, v)

    def save_options(self, filename: str = None):
        """Saves the current options to a json file.

        Args:
            filename (str, optional): the output path. Defaults to None.
        """
        options = self.get_all_options()
        data = orjson.dumps(
            options,
            option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_APPEND_NEWLINE
        )

        if not filename:
            filename = f"{self.attack_id}_params.json"

        with open(filename, "w") as paramfile:
            paramfile.write(data.decode())

class CFAttack(object):
    """
    The base class for all attacks in all frameworks.
    """

    def __init__(self, attack_id, attack_name, attack, default_params, framework_name, target, scan_id=None):
        # Parent framework
        self.framework_name = framework_name

        # Target information
        self.target = target
        self.target_data_type = self.set_datatype()

        # Attack information
        self.attack_id = attack_id
        self.attack_name = attack_name
        self.attack = attack
        self.created_on = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.attack_status = "pending"

        # Scan group information
        self.scan_id = scan_id

        # Algo parameters
        self.default_params = default_params
        self.samples = None
        self.initial_labels = None
        self.initial_outputs = None

        # Attack results
        self.final_outputs = None
        self.final_labels = None
        self.results = None
        self.success = None
        self.elapsed_time = None

        # reporting
        self.run_summary = None

        # CFAttack options
        self.cfattack_options = {
            "sample_index": 0,
            "logger": "default",
        }

        self.options = self.init_options()

    def init_options(self):
        all_options = {**self.default_params, **self.cfattack_options}
        return CFAttackOptions(
            **all_options,
            default_options_list=list(self.default_params.keys()),
            cfattack_options_list=list(self.cfattack_options.keys()))

    def set_datatype(self):
        datatype = get_target_data_type_obj(self.target.target_data_type)
        self.target_data_type = datatype

    def prepare_attack(self):
        # Set the datatype.
        # TODO I don't think this is needed.
        self.set_datatype()

        # Set the samples
        self.samples = self.target.get_samples(self.options.sample_index)

        # Send a request to the target for the selected sample
        self.initial_outputs, self.initial_labels = self.target.get_sample_labels(
            self.samples)

        # Set the logger
        self.set_logger(self.options.logger)

    def get_default_params(self):
        return self.default_params

    def set_results(self, results: object) -> None:
        self.results = results

    def set_status(self, status: str) -> None:
        self.attack_status = status

    def set_success(self, success: bool = False) -> None:
        self.success = success

    def set_logger(self, logger="default"):
        new_logger = get_attack_logger_obj(logger)
        results_folder = self.get_results_folder()
        self.logger = new_logger(filepath=results_folder)
        self.target.logger = self.logger

    def set_elapsed_time(self, start_time, end_time):
        self.elapsed_time = end_time - start_time

    def get_results_folder(self):
        module_path = "/".join(self.target.__module__.split(".")[:-1])

        if "results" not in os.listdir(module_path):
            os.mkdir(f"{module_path}/results")
        if self.attack_id not in os.listdir(f"{module_path}/results"):
            os.mkdir(f"{module_path}/results/{self.attack_id}")

        results_folder = f"{module_path}/results/{self.attack_id}"
        return results_folder

    def save_run_summary(self, filename=None, verbose=False):
        run_summary = {
            "sample_index": self.options.sample_index,
            "initial_labels": self.initial_labels,
            "final_labels": self.final_labels,
            "elapsed_time": self.elapsed_time,
            "num_queries": self.logger.num_queries,
            "success": self.success,
            "results": self.results
        }

        if verbose:
            run_summary["input_samples"] = self.samples

        data = orjson.dumps(
            run_summary,
            option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_APPEND_NEWLINE
        )

        if not filename:
            results_folder = self.get_results_folder()
            filename = f"{results_folder}/run_summary.json"

        with open(filename, "w") as summary_file:
            summary_file.write(data.decode())
