import re
import importlib

from textattack import Attacker
import numpy as np
from textattack.datasets import Dataset

from counterfit.core.attacks import CFAttack
from counterfit.core.frameworks import Framework
from counterfit.core.utils import get_subclasses
from counterfit.report.report_generator import get_target_data_type_obj

class TextAttackFramework(Framework):
    def __init__(self):
        super().__init__()

    def load(self, config_path=None):
        if config_path:
            self.load_from_config(config_path)
        else:
            self.load_attacks()
        self.loaded_status = True

    def load_attacks(self):
        base_import = importlib.import_module(
            "textattack.attack_recipes")
        attacks = get_subclasses(base_import.AttackRecipe)

        for attack_class in attacks:
            attack_name = re.findall(
                r"\w+", str(attack_class).split(".")[-1].strip())[0]
            attack_category = "BlackBox"
            attack_type = "IntegrityAttack" if "Seq" in attack_name else "EvasionAttack"
            attack_data_tags = ["text"]
            attack_params = {}

            # Create the Attack Object
            if attack_name not in self.attacks.keys():
                self.add_attack(
                    attack_name=attack_name,
                    attack_class=attack_class,
                    attack_type=attack_type,
                    attack_category=attack_category,
                    attack_data_tags=attack_data_tags,
                    attack_default_params=attack_params
                )

    def create_dataset(self, cfattack):
        # return Dataset([("This is a test", 1)])
        return Dataset(list(zip(cfattack.samples, cfattack.initial_labels)))

    def build(self, target, attack):

        class TextAttackWrapperObject(object):
            def __init__(self, predict_wrapper):
                self.model = predict_wrapper

            def __call__(self, x):
                return self.model(x)

        new_attack = attack.build(
            TextAttackWrapperObject(target.predict_wrapper))
        return new_attack

    def run(self, cfattack):

        # get labels for samples and zip with samples
        dataset = self.create_dataset(cfattack)

        new_attack = Attacker(cfattack.attack, dataset)
        results = new_attack.attack_dataset()
        return [r.perturbed_text() for r in results]

    def post_attack_processing(self, cfattack: CFAttack):

        current_datatype = cfattack.target.target_data_type
        current_dt_report_gen = get_target_data_type_obj(current_datatype)
        summary = current_dt_report_gen.get_run_summary(cfattack)
        current_dt_report_gen.print_run_summary(summary)

    def check_success(self, cfattack: CFAttack) -> bool:
        final_outputs, final_labels = cfattack.target.get_sample_labels(
            cfattack.results)
        new_labels = np.atleast_1d(final_labels)
        old_labels = np.atleast_1d(cfattack.initial_labels)

        cfattack.final_labels = final_labels
        cfattack.final_outputs = final_outputs

        success_arr = new_labels != np.array(old_labels)
        return success_arr
