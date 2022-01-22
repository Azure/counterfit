import json
from abc import abstractmethod
from pydoc import locate

from collections import namedtuple, defaultdict
from counterfit.core.attacks import CFAttack


class Framework:
    """Base class for all frameworks. This class enforces standard functions used by Counterfit.
    """
    def __init__(self, loaded_status=False):
        self.loaded_status = loaded_status
        self.attacks = defaultdict()

    @abstractmethod
    def load(self, config_path: str = None) -> None:
        """Should load the attack classes for a framework.

        Args:
            config_path (str, optional): path to a frameworks `config.json`. Defaults to None.
        """
        if config_path:
            self.load_from_config(config_path)
        else:
            self.load()
        self.loaded_status = True

    @abstractmethod
    def build(self, target, attack):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @abstractmethod
    def pre_attack_processing(self, cfattack: CFAttack):
        pass

    @abstractmethod
    def post_attack_processing(self, cfattack: CFAttack):
        pass

    @abstractmethod
    def set_parameters(self, attack, parameters: dict) -> None:
        raise NotImplementedError

    def get_attack(self, attack_name: str) -> object:
        """Get an attack stored in `framework.attacks`

        Args:
            attack_name (str): The name (key value) of the attack.

        Returns:
            object: The attack.
        """
        attack = self.attacks.get(attack_name)
        return attack

    def load_from_config(self, config_path: str) -> None:
        """Loads a framework from a config file. Uses `pydoc.locate` to find the attack class.

        Args:
            config_path (str): The path to a config.json file.
        """
        with open(config_path, 'r') as config:
            attacks_to_load = json.load(config)

        for attack_name, properties in attacks_to_load.items():
            if attack_name not in self.attacks.keys():
                attack_class_to_load = properties.get("attack_class")
                attack_class = locate(f"{attack_class_to_load}.{attack_name}")
                attack_type = properties.get("attack_type")
                attack_category = properties.get("attack_category")
                attack_data_tags = properties.get("attack_data_tags")
                attack_params = properties.get("attack_parameters")

                self.add_attack(
                    attack_name=attack_name,
                    attack_class=attack_class,
                    attack_type=attack_type,
                    attack_category=attack_category,
                    attack_data_tags=attack_data_tags,
                    attack_default_params=attack_params,
                )
        self.loaded_status = True

    def add_attack(self, attack_name: str, attack_type: str, attack_category: str,
                   attack_data_tags: list, attack_class: object, attack_default_params: dict) -> None:
        """Adds an attacks the the framework, is called during load.

        Args:
            attack_name (str): The name of the attack.
            attack_type (str): The type of the attack (Extraction, Evasion, Inference, Inversion, Poisoning, Custom...)
            attack_category (str): Whitebox or blackbox attacks. Some attacks only work with local models (i.e access to gradients)
            attack_data_tags (list): A list of the data modalities an attack works with (image, tabular, video, etc)
            attack_class (object): The attack that will get built and run.
            attack_default_params (dict): Any settable parameters for the attack (max_iters, norm, query_budget, etc).
        """

        AttackEntry = namedtuple(
            "attack_entry", "attack_name, attack_type, attack_category, attack_data_tags, attack_class, attack_default_params, framework_name")

        framework_name = self.__module__.split(".")[-1]

        new_attack = AttackEntry(
            attack_name,
            attack_type,
            attack_category,
            attack_data_tags,
            attack_class,
            attack_default_params,
            framework_name=framework_name)
        self.attacks[attack_name] = new_attack
