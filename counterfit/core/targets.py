import datetime
import inspect
import os
import pathlib
from typing import Union

from abc import ABC, abstractmethod
from collections import defaultdict

import numpy as np
from counterfit.core.output import CFPrint
from counterfit.core.attacks import CFAttack
from counterfit.core.utils import set_id

class Target(ABC):
    """Base class for all targets.
    """

    def __init__(self):
        self.target_id = set_id()
        self.loaded_status = False
        self.active_attack = None
        self.logger = None
        self.attacks = defaultdict()

    @abstractmethod
    def load(self):
        """Loads data, models, etc in preparation. Is called by `interact`.

        Raises:
            NotImplementedError: Is required to be implemented by a framework.
        """
        raise NotImplementedError
    
    @abstractmethod
    def predict(self, x):
        """The predict interface to the target model.

        Raises:
            NotImplementedError: Is required to be implemented by a framework.
        """
        raise NotImplementedError

    def set_loaded_status(self, status: bool = False) -> None:
        """Set the loaded status of a framework

        Args:
            status (bool, optional): [description]. Defaults to False.
        """
        self.loaded_status = status

    def add_attack(self, attack: CFAttack) -> None:
        """Add a CFAttack to the target.

        Args:
            attack (CFAttack): The CFAttack object
        """
        self.attacks[attack.attack_id] = attack

    def set_active_attack(self, attack_id: str) -> None:
        """Sets the active attack

        Args:
            attack_id (str): The attack_id of the attack to use. 
        """
        active_attack = self.attacks.get(attack_id, None)
        if not active_attack:
            CFPrint.failed(f"{attack_id} not found")
        else:
            CFPrint.success(f"Using {attack_id}")
            self.active_attack = active_attack

    def get_active_attack(self) -> None:
        """Get the active attack
        """
        if self.active_attack is None:
            return None
        return self.active_attack.attack_id

    def get_attacks(self, scan_id: str = None) -> dict:
        """Get all of the attacks

        Args:
            scan_id (str, optional): The scan_id to filter on. Defaults to None.

        Returns:
            dict: [description]
        """
        if scan_id:
            scans_by_scan_id = {}
            for attack_id, attack in self.attacks.items():
                if attack.scan_id == scan_id:
                    scans_by_scan_id[attack_id] = attack
            return scans_by_scan_id
        else:
            return self.attacks


    def get_samples(self, sample_index: Union[int, list, range] = 0) -> np.ndarray:
        """This function helps to directly set sample_index and samples for a target not depending on attack.

        Args:
            sample_index (int, list or range, optional): [single or multiple indices]. Defaults to 0.

        Returns:
            np.ndarray: [description]
        """
        if hasattr(sample_index, "__iter__"):
            sample_index = list(sample_index)  # in case "range" was used
            # multiple index
            if type(self.X[sample_index[0]]) is str:
                # multiple index (str)
                out = np.array([self.X[i] for i in sample_index])
                batch_shape = (-1,)
            else:
                # multiple index (numpy)
                out = np.array([self.X[i] for i in sample_index])
                batch_shape = (-1,) + self.target_input_shape
        elif type(self.X[sample_index]) is str:
            # single index (string)
            # array of strings (textattack)
            out = np.array(self.X[sample_index])
            batch_shape = (-1,)
        else:
            # single index (array)
            # array of arrays (art)
            out = np.atleast_2d(self.X[sample_index])
            batch_shape = (-1,) + self.target_input_shape

        return out.reshape(batch_shape)

    def predict_wrapper(self, x, **kwargs):
        output = self.predict(x)
        if self.logger:
            labels = self.outputs_to_labels(output)
            for sample, tmp_output in zip(x, output):
                try:
                    log_entry = {
                        "timestamp": datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        "input": np.array(sample).flatten().reshape(-1).tolist(),
                        "output": tmp_output,
                        "labels": labels
                    }

                    self.logger.log(log_entry)

                except Exception as e:
                    print(e)
                    continue

        return output

    def fullpath(self, file: str) -> str:
        """A conveiance function

        Args:
            file (str): The file tp get the full path for.

        Returns:
            str: The full path of the file
        """
        basedir = pathlib.Path(os.path.abspath(
            inspect.getfile(self.__class__))).parent.resolve()
        return os.path.join(basedir, file)

    def get_sample_labels(self, samples):
        """A covienance function to get outputs and labels for a target query.

        Args:
            samples ([type]): [description]

        Returns:
            [type]: [description]
        """
        output = self.predict_wrapper(samples)
        labels = self.outputs_to_labels(output)
        return output, labels

    def outputs_to_labels(self, output):
        """Default multiclass label selector via argmax. User can override this function if, for example, one wants to choose a specific threshold
        Args:
            output ([type]): [description]

        Returns:
            [type]: [description]
        """
        output = np.atleast_2d(output)
        return [self.target_output_classes[i] for i in np.argmax(output, axis=1)]
