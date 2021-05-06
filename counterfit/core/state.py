# state.py: holds global state of attacks and targets
import importlib
import inspect
import os
import sys
import uuid
from collections import defaultdict
from counterfit.core import config
from counterfit.core.attacks import Attack
from counterfit.core.targets import Target


class CFState:
    """
    Singleton class responsible for managing targets and attacks. Instantiation of a class is restricted to one object.
    """

    __instance__ = None

    def __init__(self):
        if CFState.__instance__ is None:
            CFState.__instance__ = self
        else:
            raise Exception("You cannot create another CFState class")
        self.loaded_targets = defaultdict()  # key as target_name and value as target_object
        self.loaded_attacks = defaultdict()  # key as attack_name and value as attack_object
        self.loaded_frameworks = defaultdict()  # key as framework_name and value as framework_object

        self.session_targets = defaultdict()
        self.session_frameworks = defaultdict()
        self.active_target = None

    @staticmethod
    def get_instance():
        """Static method to fetch the current instance."""
        if not CFState.__instance__:
            CFState.__instance__ = CFState()
        return CFState.__instance__

    def set_active_target(self, target_name):
        """Set the active_target with the target_name provided."""
        if target_name not in self.session_targets:  # target hasn't been used in this session. Instantiate it.
            target = self.load_target(target_name)
            self.session_targets[target_name] = target
            self.active_target = target

        else:
            self.active_target = self.session_targets.get(target_name, None)

    def set_active_attack(self, attack_id):
        """Sets active attack for the active_target"""
        active_attack = self.active_target.attacks.get(attack_id, None)
        if not active_attack:
            raise ValueError("Attack not in Target attacks")
        else:
            self.active_target.active_attack = active_attack
            print("\n[+] Using {0} {1}\n".format(self.active_target.active_attack.attack_name, attack_id))

    def _set_attack_params(self, attack_obj, parameters):
        # set defaults to the attack
        attack_obj.set_attack_parameters(parameters)
        attack_obj.sample_index = 0
        attack_obj.target_class = 0

    def add_attack_to_active_target(self, attack_name, parameters):
        """Add attack to the current target with respective parameters"""
        attack_obj = self.loaded_attacks.get(attack_name, None)
        if not attack_obj:
            raise ValueError(f"\n[!] Attack name {attack_name} not found.\n")
        elif self.active_target.model_data_type not in attack_obj.tags:
            raise ValueError(f"\n[!] Data type mismatch - {attack_name} and {self.active_target.model_name}.\n")
        else:
            attack_obj = attack_obj()
            # set attack id
            attack_obj.attack_id = uuid.uuid4().hex[:8]
            # set attack parameters
            self._set_attack_params(attack_obj, parameters)
            # add to target
            self.active_target.attacks[attack_obj.attack_id] = attack_obj
            # set as active attack
            self.set_active_attack(attack_obj.attack_id)

    def load_target(self, target_name):
        target_to_load = self.loaded_targets.get(target_name, None)
        target = target_to_load()

        target.target_id = uuid.uuid4().hex[:8]
        target.active_attack = None
        target.attacks = defaultdict()

        return target

    def reload_target(self):
        target_name = self.active_target.model_name
        target_id = self.active_target.target_id
        target_active_attack = self.active_target.active_attack
        target_attacks = self.active_target.attacks

        module = self.active_target.__module__
        targetcls = importlib.reload(sys.modules[module])
        target_subclasses = Target.__subclasses__()

        for _, obj in inspect.getmembers(targetcls):
            if inspect.isclass(obj):
                if inspect.getmro(obj)[1] in target_subclasses and obj is not Target:
                    self.add_target(obj)

        reloaded_target = self.load_target(target_name)

        reloaded_target.target_id = target_id
        reloaded_target.active_attack = target_active_attack
        reloaded_target.attacks = target_attacks

        self.session_targets[target_name] = reloaded_target
        self.active_target = reloaded_target

    def load_attack(self, attack_obj):
        """Update loaded_attacks with key as attack_name and value as attack object"""
        self.loaded_attacks[attack_obj.attack_name] = attack_obj

    def get_subclasses(self, class_name):
        """Find all the subclasses of a class given its name"""
        return class_name.__subclasses__()

    def add_target(self, target_obj):
        """Update loaded_targets with key as target_name and value as target object"""
        self.loaded_targets[target_obj.model_name] = target_obj

    def import_targets(self):
        """Import all targets in the provided path"""
        count = 0
        target_subclasses = self.get_subclasses(Target)
        for module in os.listdir(config.targets_path):
            if not os.path.isdir(f"{config.targets_path}/{module}"):
                continue

            for target in os.listdir(f"{config.targets_path}/{module}"):
                if target == "__init__.py" or target[-3:] != ".py":
                    continue
                else:
                    targets_path_split = config.targets_path.split("/")
                    module_directory = targets_path_split[0]
                    target_path = targets_path_split[1]
                    targetcls = importlib.import_module(f"{module_directory}.{target_path}.{module}.{target[:-3]}")
                    for _, obj in inspect.getmembers(targetcls):
                        if inspect.isclass(obj):
                            if inspect.getmro(obj)[1] in target_subclasses and obj is not Target:
                                self.add_target(obj)
                                count += 1

        return count

    def import_frameworks(self):
        """Gathers the attack modules in each available framework listed under "counterfit/frameworks".
        is used by the command load to find the available frameworks for loading.
        """
        num_attacks = 0
        for framework in os.listdir(config.attacks_path):
            if framework[-3:] == ".py":
                continue

            if "__" in framework:
                continue

            else:
                self.loaded_frameworks[framework] = []
                for module in os.listdir(f"{config.attacks_path}/{framework}"):
                    if module == "__init__.py" or module[-3:] != ".py":
                        continue
                    else:
                        attacks_path_split = config.attacks_path.split("/")
                        module_directory = attacks_path_split[0]
                        attack_path = attacks_path_split[1]
                        self.loaded_frameworks[framework].append(
                            f"{module_directory}/{attack_path}/{framework}/{module}"
                        )
                        num_attacks += 1
        return num_attacks

    def load_framework(self, framework_name="art"):
        modules_to_load = self.loaded_frameworks.get(framework_name, None)
        if modules_to_load is None:
            raise KeyError(f"[!] {modules_to_load} not found!")

        for module in modules_to_load:
            try:
                module_split = module.split("/")
                attacks_module_path = ".".join(module_split)
                attack_cls = importlib.import_module(f"{attacks_module_path[:-3]}")

                for obj in attack_cls.__dict__.values():
                    if inspect.isclass(obj):
                        if issubclass(obj, Attack) and obj is not Attack:
                            CFState.get_instance().loaded_attacks[obj.attack_name] = obj

            except Exception as e:
                print(f"\n[!] Failed to load {module}: {e}\n")
                continue

        print("\n[+] Framework loaded successfully!\n")
