import yaml
import glob
import pathlib
import numpy as np

from textattack import Attacker
from textattack.datasets import Dataset

from counterfit.core.attacks import CFAttack
from counterfit.core.frameworks import CFFramework


class TextAttackFramework(CFFramework):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_attacks(cls, framework_path=f"{pathlib.Path(__file__).parent.resolve()}/attacks"):
        attacks = {}
        files = glob.glob(f"{framework_path}/*.yml")

        for attack in files:
            with open(attack, 'r') as f:
                data = yaml.safe_load(f)
        
            attacks[data['attack_name']] = data

        return attacks

    def create_dataset(self, cfattack):
        # return Dataset([("This is a test", 1)])
        return Dataset(list(zip(cfattack.samples, cfattack.initial_labels)))

    def build(self, target, attack):
        class TextAttackWrapperObject(object):
            def __init__(self, predict_wrapper):
                self.model = predict_wrapper

            def __call__(self, x):
                return self.model(x)

        text_attack_obj = TextAttackWrapperObject(target.predict_wrapper)
        new_attack = attack.build(text_attack_obj)
        return new_attack

    def run(self, cfattack):
        # get labels for samples and zip with samples
        dataset = self.create_dataset(cfattack)

        new_attack = Attacker(cfattack.attack, dataset)
        results = new_attack.attack_dataset()
        return [r.perturbed_text() for r in results]

    def set_parameters(self, cfattack: CFAttack):
        # Does nothing. Allow for future extensibility.
        pass

    def pre_attack_processing(self, cfattact: CFAttack):
        # Does nothing. Allow for future extensibility.
        pass

    def post_attack_processing(self, cfattack: CFAttack):
        pass
        # current_datatype = cfattack.target.target_data_type
        # current_dt_report_gen = get_target_data_type_obj(current_datatype)
        # summary = current_dt_report_gen.get_run_summary(cfattack)
        # current_dt_report_gen.print_run_summary(summary)

    def check_success(self, cfattack: CFAttack) -> bool:
        final_outputs, final_labels = cfattack.target.get_sample_labels(
            cfattack.results)
        new_labels = np.atleast_1d(final_labels)
        old_labels = np.atleast_1d(cfattack.initial_labels)

        cfattack.final_labels = final_labels
        cfattack.final_outputs = final_outputs

        success_arr = new_labels != np.array(old_labels)
        return success_arr
