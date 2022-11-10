import orjson
from counterfit.core.output import CFPrint


class CFOptions:
    """A container class for all settable options for a `CFAttack.attack`. Default parameters should 
    be loaded during `framework.load()` and added to `attack_default_params`. Additionally, a
    number of global Counterfit options are injected.
    """
    attack_parameters: dict
    cf_options: dict

    def __init__(self, attack_parameters):
        self.attack_parameters = attack_parameters
        self.cf_options = {
            "sample_index": {
                "default": 0,
                "current": 0,
                "previous": [],
                "docs": "Sample index to attack"
            },
            "optimize": {
                "default": False,
                "current": False,
                "previous": [],
                "docs": "Use Optuna to optimize attack parameters"
            },
            "logger": {
                "default": "basic",
                "current": "basic",
                "previous": [],
                "docs": "Logger to log queries with"
            }
        }

        if 'targeted' in self.attack_parameters.keys():
            self.attack_parameters['target_labels'] = {"docs": "target labels for a targeted attack", "default": 0}
        for k, v in self.attack_parameters.items():
            v.update({"current": v["default"], "previous": []})


    def update(self, parameters_to_update: dict) -> None:
        """Sets an option. Take in a dictionary of options and applies attack specific checks before saving them as attributes.

        Args:
            params_to_update (dict): A dictionary of `{option:value}`
        """

        for k, v in parameters_to_update.items():
            if k in self.attack_parameters.keys():
                self.attack_parameters[k]["previous"].append(self.attack_parameters[k]["current"])
                self.attack_parameters[k]["current"] = v
            elif k in self.cf_options.keys():
                self.cf_options[k]["previous"].append(self.cf_options[k]["current"])
                self.cf_options[k]["current"] = v
            else:
                CFPrint.warn("Option not found")

    def get_all(self):
        return {**self.attack_parameters, **self.cf_options}

    def save_options(self, filename: str = None):
        """Saves the current options to a json file.

        Args:
            filename (str, optional): the output path. Defaults to None.
        """
        options = {**self.attack_parameters, **self.cf_options}
        dump_options = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_APPEND_NEWLINE
        data = orjson.dumps(options, option=dump_options)

        if not filename:
            filename = f"{self.attack_id}_params.json"

        with open(filename, "w") as paramfile:
            paramfile.write(data.decode())
