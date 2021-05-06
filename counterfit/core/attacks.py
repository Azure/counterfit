import datetime
import uuid

from hyperopt import pyll
import numpy
from counterfit.core import config, wrappers, enums
from counterfit.core.interfaces import AbstractAttack


class Attack(AbstractAttack):
    """Attack class inherits AbstractAttack and sets attack parameters. It also persists attack results and logs to json configuration file"""

    def __init__(self, status=enums.AttackStatus.pending.value):
        self.attack_id = uuid.uuid4().hex[:8]
        self.status = status

        # Set in the target
        self.samples = None
        self.sample_index = None
        self.target_class = None

        # Logs
        self._logs = []

        # Results of the attack
        self.results = []

        # set creation time
        self.created_time = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    def set_attack_parameters(self, parameters):
        if parameters == "default":
            self.parameters = self.default

        elif parameters == "random":
            self.parameters = self._param_floats_to_ints(pyll.stochastic.sample(self.random))

        elif type(parameters) == dict:
            self.parameters = self._param_floats_to_ints(parameters)

        else:
            print("\n[!] Parameters arguement not understood. Setting default.")
            self.parameters = self.default

    def _param_floats_to_ints(self, parameters):
        new_parameters = {}
        for k, v in parameters.items():
            if isinstance(v, float) and v < numpy.inf:
                if int(v) == v:
                    v = int(v)
            new_parameters[k] = v

        return new_parameters

    def dump(self):
        return {
            "attack_name": self.attack_name,
            "created": self.created_time,
            "attack_id": self.attack_id,
            "sample_index": self.sample_index,
            "target_class": self.target_class,
            "parameters": self.parameters,
            "results": self.results,
            "logs": self._logs,
        }

    def append_log(self, log):
        self._logs.append(log)
