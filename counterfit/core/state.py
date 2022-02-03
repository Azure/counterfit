# state.py
# This file keeps track of all load targets.

import importlib
import sys
import time
from counterfit.core.config import Config
from counterfit.core import utils
from counterfit.core.output import CFPrint
from counterfit.core.attacks import CFAttack
from counterfit.core.frameworks import Framework
from counterfit.core.targets import Target

class CFState:
    """Singleton class responsible for managing targets and attacks. Instantiation of a class is restricted to one object.
    """
    __instance__ = None

    def __init__(self):
        if CFState.__instance__ is None:
            CFState.__instance__ = self
        else:
            raise Exception("You cannot create another CFState class")

        self.frameworks = {}
        self.targets = {}
        self.scans = {}
        self.active_target = None

    @staticmethod
    def state():
        """Static method to fetch the current instance.
        """
        if not CFState.__instance__:
            CFState.__instance__ = CFState()
        return CFState.__instance__

    def _init_state(self) -> None:
        """Initializes Counterfit
        """
        self.import_frameworks(frameworks_path="counterfit/frameworks")
        self.import_targets(targets_path="counterfit/targets")

    # Frameworks
    def import_frameworks(self, frameworks_path: str) -> None:
        """Imports the available frameworks from the frameworks folder. Adds the loaded frameworks into self.frameworks. Frameworks contain the methods required for managing the attacks that are found within the framework.

        Args:
            frameworks_path (str): A folder path where frameworks are kept. 
        """
        available_frameworks = utils.import_subclass(
            frameworks_path, Framework)

        for k, v in available_frameworks.items():
            self.add_framework(k, v())

    def add_framework(self, framework_name: str, framework: Framework = None) -> None:
        """Adds a framework to Counterfit.

        Args:
            framework_name (str): Name of the framework
            framework (Framework, optional): The Framework object to add. Defaults to None.
        """
        if not framework:
            framework = Framework()
        self.frameworks[framework_name] = framework

    def load_framework(self, framework: str, force_no_config: bool = False) -> None:
        """Load a framework by name. By loading a framework, the attacks under the framework are loaded and ready for use. Attacks are not loaded during import_frameworks as loading could be slow, or a particular framework could cause errors and prevent all frameworks from loading.

        Args:
            framework (str): The framework name
            force_no_config (bool, optional): [description]. Defaults to False.
        """

        framework_to_load = self.frameworks.get(framework)

        try:
            if force_no_config:
                framework_to_load.load()
            else:
                try:
                    config_path = f"{Config.frameworks_path}/{framework}/config.json"
                    framework_to_load.load(config_path=config_path)
                    CFPrint.success(f"{framework} successfully loaded!")
                except Exception:
                    CFPrint.info(f"unable to load from {config_path}. Initialize framework from default config.")
                    # load without config
                    framework_to_load.load()
                    CFPrint.success(
                        f"{framework} successfully loaded with defaults (no config file provided)")

        except Exception as e:
            CFPrint.failed(f"Could not load {framework}: {e}\n")

    def get_frameworks(self) -> dict:
        """Get all available frameworks

        Args:
            None

        Returns:
            dict: all frameworks.
        """
        return self.frameworks

    def reload_framework(self, framework_name):
        """Reimports the framework.

        Args:
            framework_name (str): framework to reload
        """

        if framework_name not in self.get_frameworks().keys():
            CFPrint.failed(f"{framework_name} not found")
        else:
            # Get the framework to reload
            framework_to_reload = self.get_frameworks().get(framework_name)

            # Get the class we want to instantiate after module reload
            framework_class = framework_to_reload.__class__.__name__

            # Reload the module
            reloaded_module = importlib.reload(
                sys.modules[framework_to_reload.__module__])

            # Reload the framework
            reloaded_framework = reloaded_module.__dict__.get(
                framework_class)()

            # Delete the old class
            del self.frameworks[framework_name]

            # Replace the old module with the new one
            self.frameworks[framework_name] = reloaded_framework

            # Load the attacks.
            self.load_framework(framework_name)

    # Targets
    def import_targets(self, targets_path: str) -> None:
        """Imports available targets from the targets folder. Adds the loaded frameworks to CFState.targets.
        Targets contain the data and methods to interact with a target machine learning system.

        Args:
            targets_path (str): Folder path to where targets are kept
        """
        available_targets = utils.import_subclass(
            targets_path, Target)

        for k, v in available_targets.items():
            self.add_target(k, v())

    def add_target(self, target_name: str, target: Target = None):
        """Add a target to Counterfit

        Args:
            target_name (str): The name of the target
            target (Target, optional): The Target object to add. Defaults to None.
        """
        if not target:
            target = Target()
        self.targets[target_name] = target

    def load_target(self, target: str) -> Target:
        """Load a target by name. Targets are not loaded during import to prevent loading unnecessary targets
        during a session. This function calls `target.load()`.

        Args:
            The target name

        Returns:
            None
        """
        target_to_load = self.targets.get(target, None)

        if not target_to_load.loaded_status:
            try:
                target_to_load.load()
                CFPrint.success(
                    f"{target_to_load.target_name} ({target_to_load.target_id}) successfully loaded!")
                target_to_load.set_loaded_status(True)

            except Exception as e:
                CFPrint.failed(
                    f"Could not load {target_to_load.target_name}: {e}\n")
        else:
            CFPrint.warn(
                f"{target} is already loaded, use 'reload' to reload a target")

        return target_to_load

    def reload_target(self):
        """Reloads the active target.
        """
        if not self.active_target:
            CFPrint.failed("No active target")
            return

        else:
            # Get the framework to reload
            target_name = self.active_target.target_name
            target_to_reload = self.targets[target_name]

            # Get the attacks
            attacks = target_to_reload.attacks
            active_attack = target_to_reload.active_attack

            # Get the class we want to instantiate after module reload
            target_class = target_to_reload.__class__.__name__

            # Reload the module
            reloaded_module = importlib.reload(
                sys.modules[target_to_reload.__module__])

            # Reload the target
            reloaded_target = reloaded_module.__dict__.get(
                target_class)()

            # Delete the old class
            del self.targets[target_name]

            # Replace the old module with the new one
            self.targets[target_name] = reloaded_target

            # Load the attacks.
            target_to_load = self.load_target(target_name)

            # Set it as the active target
            self.set_active_target(target_to_load)

            # Replace the history
            self.active_target.attacks = attacks
            self.active_target.active_attack = active_attack

    def list_targets(self) -> list:
        """Get a list of targets

        Returns:
            list: A list of imported targets
        """

        return list(self.targets.keys())

    def get_attacks(self) -> dict:
        """Get all available attacks

        Returns:
            dict: all available attacks from all frameworks.
        """
        all_attacks = {}
        frameworks = self.get_frameworks()
        for framework_name, framework in frameworks.items():
            for k, v in sorted(framework.attacks.items()):
                all_attacks[k] = v

        return all_attacks

    def get_active_target(self) -> Target:
        """Get the active target

        Returns:
            Target: The active target.
        """
        return self.active_target

    def add_attack_to_target(self, target_name: str, cfattack: CFAttack) -> None:
        """After a CFAttack object has been built, add it to the target for tracking.

        Args:
            target_name (str): The target name
            cfattack (CFAttack): The CFAttack object to add.
        """
        target = self.targets.get(target_name)
        target.add_attack(cfattack)

    def build_new_attack(self, target_name: str, attack_name: str, scan_id: str = None) -> CFAttack:
        """Build a new CFAttack. Search through the loaded frameworks for the attack and create a new CFAttack object for use.

        Args:
            target_name (str, required): The target name.
            attack_name (str, required): The attack name.
            scan_id (str, Optional): A unique value

        Returns:
            CFAttack: A new CFAttack object.
        """

        # Get the target to run the attack against.
        target = self.targets.get(target_name)

        # Hunt through frameworks for the attack.
        for framework_name, framework in self.frameworks.items():
            for attack in framework.attacks:
                if attack_name != attack:
                    continue
                else:
                    attack = framework.attacks.get(attack)

                    # Have the framework build the attack.
                    new_attack = framework.build(
                        target=target,
                        attack=attack.attack_class
                    )

                    cfattack = CFAttack(
                        attack_id=utils.set_id(),
                        attack_name=attack_name,
                        attack=new_attack,
                        default_params=attack.attack_default_params,
                        framework_name=framework_name,
                        target=target,
                        scan_id=scan_id
                    )  # This is a mutable runtime friendly structure.

                    self.add_attack_to_target(target_name, cfattack)

                    CFPrint.success(
                        f"New {attack_name} ({cfattack.attack_id}) created")
                    return cfattack.attack_id

    def run_attack(self, target_name: str, attack_id: str) -> bool:
        """Run a prepared attack. Get the appropriate framework and execute the attack.

        Args:
            attack_id (str, required): The attack id to run.

        Returns:
            Attack: A new Attack object with an updated cfattack_class. Additional properties set in this function include, attack_id (str)
            and the parent framework (str). The framework string is added to prevent the duplication of code in run_attack.
        """

        # Get the cfattack object to run
        cfattack = self.targets.get(target_name).attacks.get(attack_id)

        # Get the framework responsible for the attack
        framework = self.frameworks.get(cfattack.framework_name)

        # Make sure there is a cfattack object
        if not cfattack:
            CFPrint.failed("Attack id not found")
            return False

        # Set the initial values for the attack. Samples, logger, etc.
        CFPrint.info("Preparing attack...")
        cfattack.prepare_attack()

        # Run the attack
        CFPrint.info("Running attack...")
        cfattack.set_status("running")

        # Give the framework an opportunity to preprocess any thing in the attack.
        framework.pre_attack_processing(cfattack)

        # Start timing the attack for the elapsed_time metric
        start_time = time.time()

        try:
            # Get the results of the attack
            results = framework.run(cfattack)
        except Exception as e:
            # postprocessing steps for failed attacks
            success = [False] * len(cfattack.initial_labels)

            # Let the user know the attack failed
            CFPrint.failed(
                f"Failed to run {cfattack.attack_id} ({cfattack.attack_name}): {e}")

        finally:            
            # postprocessing steps for successful attacks
            # Set the results that the attack returns
            cfattack.set_results(results)

            # Determine the success of the attack
            success = framework.check_success(cfattack)

            # Stop the timer
            end_time = time.time()

            # Set the elapsed time metric
            cfattack.set_elapsed_time(start_time, end_time)

            # Set the success value
            cfattack.set_success(success)

            # Give the framework an opportunity to process the results, generate reports, etc
            framework.post_attack_processing(cfattack)

            # Mark the attack as complete
            cfattack.set_status("complete")

        # Let the user know the attack has completed successfully.
        CFPrint.success(
            f"Attack completed {cfattack.attack_id} ({cfattack.attack_name})")
        return True


    def set_active_target(self, target: Target) -> None:
        """Set the active target with the target name provided.

        Args:
            target (Target): The target object to set as the active target
        """
        self.active_target = target
