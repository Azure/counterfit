from PIL import Image
import tqdm
import numpy as np
import yaml 
import pathlib
import glob
import pydoc

# Used for typing function arguments
from counterfit.core.frameworks import CFFramework
from counterfit.core.attacks import CFAttack
from counterfit.core.targets import CFTarget


def cross_entropy(predictions, targets):
    N = np.array(predictions).shape[0]
    ce = -np.sum(targets * np.log(predictions)) / N
    return ce


class AuglyAttack:
    def __init__(self, classifier, attack_class, query_budget=5):
        self.predict = classifier
        self.attack_class = attack_class
        self.results = []
        self.query_budget = query_budget

    def generate(self, x: np.ndarray, **kwargs):
        query_budget = self.query_budget
        results = []
        all_scores = []
        for sample in x:
            # sample = np.squeeze(sample)
            # get the original output
            orig_pred = self.predict(sample)
            best_score = 0
            best_sample = None
            for _ in tqdm.tqdm(range(query_budget)):
                if isinstance(sample, np.ndarray) and sample.dtype == np.float32:
                    # convert to uint [0,255], apply transform, and convert back to float [0,1]
                    im = Image.fromarray((sample*255).astype(np.uint8))
                    aug_im = self.attack_class(im)
                    aug = np.array(aug_im, dtype=np.float32) / 255.0
                elif isinstance(sample, np.ndarray) and sample.dtype == np.uint8:
                    im = Image.fromarray(sample)
                    aug_im = self.attack_class(im)
                    aug = np.array(aug_im, dtype=np.uint8)
                else:
                    raise Exception(
                        "Expecting X to be numpy array of np.uint8 [0,255] or np.float32 [0,1]")

                
                new_pred = self.predict(aug)
                self.results.append(new_pred)

                # score the sample using  log loss (maximize loss)
                score = cross_entropy(new_pred, orig_pred)
                if score > best_score:
                    best_score = score
                    best_sample = aug

                all_scores.append(score)
            # append best sample
            results.append(best_sample)

        # return the "best" augmentation as the adversarial example
        return np.array(results, dtype=x.dtype), np.array(all_scores).reshape((x.shape[0], query_budget)).mean(axis=-1)


class AuglyFramework(CFFramework):
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

    def build(self, target: CFTarget, attack: str):
        attack = pydoc.locate(attack)
        loaded_attack = attack()

        new_attack = AuglyAttack(
            target.predict_wrapper, loaded_attack)

        return new_attack

    def run(self, cfattack: CFAttack):
        results, avscores = cfattack.attack.generate(cfattack.samples)
        return results
    
    def post_attack_processing(self, cfattack: CFAttack):
        pass
        # current_datatype = cfattack.target.data_type
        # current_dt_report_gen = get_data_type_obj(current_datatype)
        # summary = current_dt_report_gen.get_run_summary(cfattack)
        # current_dt_report_gen.print_run_summary(summary)

    def fix_grayscale(x):
        return np.squeeze(x, axis=2)

    def check_success(self, cfattack: CFAttack) -> bool:
        attack_results = cfattack.results
        final_outputs, final_labels = cfattack.target.get_sample_labels(attack_results)
        cfattack.final_labels = final_labels
        cfattaccurrent_dt_report_gen.print_run_summary(summary)k.final_outputs = final_outputs
        cfattack.initial_labels = final_labels
        # successful
        success = cfattack.final_labels != np.array(cfattack.initial_labels)
        return success
    