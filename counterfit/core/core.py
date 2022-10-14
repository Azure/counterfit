import glob
import importlib
import inspect
import os
import time
import traceback

import yaml
from counterfit.core.attacks import CFAttack
from counterfit.core.frameworks import CFFramework
from counterfit.core.options import CFOptions
from counterfit.core.output import CFPrint
from counterfit.core.targets import CFTarget


class Counterfit:

    # Frameworks
    @classmethod
    def get_frameworks(cls) -> dict:
        """Imports the available frameworks from the frameworks folder. Adds
        the loaded frameworks into self.frameworks. Frameworks contain the
        methods required for managing the attacks that are found within the
        framework.

        Args:
            frameworks_path (str): A folder path where frameworks are kept. 
        """
        frameworks = {}
        cf_frameworks = importlib.import_module("counterfit.frameworks")
        for framework in cf_frameworks.CFFramework.__subclasses__():
            framework_name = framework.__module__.split(".")[-1]

            frameworks[framework_name] = {}
            frameworks[framework_name]["attacks"] = {}
            frameworks[framework_name]["module"] = framework

            framework_path = os.path.dirname(inspect.getfile(framework)) 

            for attack in glob.glob(f"{framework_path}/attacks/*.yml"):
                with open(attack, 'r') as f:
                    data = yaml.safe_load(f)

                if data["attack_name"] not in frameworks[framework_name]["attacks"].keys():
                    frameworks[framework_name]["attacks"][data['attack_name']] = data

        return frameworks

    @classmethod
    def build_target(
        cls, 
        data_type: str, 
        endpoint: str, 
        output_classes: list,
        classifier: str,
        input_shape: tuple,
        load_func: object,
        predict_func: object,
        X: list) -> CFTarget:
        try:
            target = CFTarget(
                data_type=data_type, 
                endpoint=endpoint,
                output_classes=output_classes, 
                classifier=classifier,
                input_shape=input_shape,
                load=load_func,
                predict=predict_func,
                X=X)
        except Exception as error:
            CFPrint.failed(f"Failed to build target: {error}")
        try:
            target.load()
        except Exception as error:
            CFPrint.failed(f"Failed to load target: {error}")
        CFPrint.success(f"Successfully created target")
        return target

    @classmethod
    def build_attack(
        cls,
        target: CFTarget,
        attack: str,
        scan_id: str = None) -> CFAttack:
        """Build a new CFAttack. 
        
        Search through the loaded frameworks for the attack and create a new
        CFAttack object for use.

        Args:
            target_name (CFTarget, required): The target object.
            attack_name (str, required): The attack name.
            scan_id (str, Optional): A unique value
 
        Returns:
            CFAttack: A new CFAttack object.
        """
        # Resolve the attack
        framework: CFFramework
        try:
            # Look for framework based on name.
            for k, v in cls.get_frameworks().items():
                if attack in list(v["attacks"].keys()):
                    framework = v["module"]()
                    attack = v["attacks"][attack]
        except Exception as error:
            msg = f"Failed to load framework or resolve {attack}: {error}"
            CFPrint.failed(msg)
            traceback.print_exc()
        # Ensure the attack is compatible with the target
        if target.data_type not in attack["attack_data_tags"]:
            msg = f"Target data type ({target.data_type}) is not compatible"
            msg += f" with the attack chosen ({attack['attack_data_tags']})"
            CFPrint.failed(msg)
            return False


        # Have the framework build the attack.
        try:
            new_attack = framework.build(
                target=target,
                attack=attack["attack_class"]) # The dotted path of the attack. 
        except Exception as error:
            CFPrint.failed(f"Framework failed to build attack: {error}")
            traceback.print_exc()
            return

        # Create a CFAttack object
        try:
            cfattack = CFAttack(
                name=attack["attack_class"],
                target=target,
                framework=framework,
                attack=new_attack,
                options=CFOptions(attack["attack_parameters"])
            )

        except Exception as error:
            CFPrint.failed(f"Failed to build CFAttack: {error}")
            traceback.print_exc()

        return cfattack

    @classmethod
    def run_attack(cls, attack: CFAttack) -> bool:
        """Run a prepared attack. Get the appropriate framework and execute
        the attack.

        Args:
            attack_id (str, required): The attack id to run.

        Returns:
            Attack: A new Attack object with an updated cfattack_class. 
            Additional properties set in this function include, attack_id (str)
            and the parent framework (str). The framework string is added to 
            prevent the duplication of code in run_attack.
        """
        # Set the initial values for the attack. Samples, logger, etc.
        attack.prepare_attack()

        # Run the attack
        attack.set_status("running")

        # Start timing the attack for the elapsed_time metric
        start_time = time.time()

        # Run the attack
        try:
            results = attack.framework.run(attack)
        except Exception as error:
            # postprocessing steps for failed attacks
            success = [False] * len(attack.initial_labels)

            msg = f"Failed to run {attack.attack_id} ({attack.name}): {error}"
            CFPrint.failed(msg)

            results = None
            return

        # postprocessing steps for successful attacks
        finally:

            # Stop the timer
            end_time = time.time()

            # Set the elapsed time metric
            attack.set_elapsed_time(start_time, end_time)

            # Set the results the attack returns
            # Results are attack and framework specific. 
            attack.set_results(results)

            # Determine the success of the attack
            success = attack.framework.check_success(attack)

            # Set the success value
            attack.set_success(success)

            # Give the framework an opportunity to process the results, generate reports, etc
            attack.framework.post_attack_processing(attack)

            # Mark the attack as complete
            attack.set_status("complete")

            # Let the user know the attack has completed successfully.
            CFPrint.success(f"Attack completed {attack.attack_id}")
