import datetime
import functools
import os
import time
from abc import ABC
from collections import namedtuple

import magic
import numpy as np
from PIL import Image
from secml.array import CArray
from secml_malware.attack.blackbox.c_wrapper_phi import CWrapperPhi
from secml_malware.attack.blackbox.ga.c_base_genetic_engine import CGeneticAlgorithm
from tqdm import tqdm

from counterfit.core import wrappers, enums, config
from counterfit.core.interfaces import AbstractTarget

Query = namedtuple('Query', ['input', 'output', 'label'])

class Target(AbstractTarget):
    """Parent class for all targets"""
    # member variables expected
    active_attack = None
    model = None
    clip_values = None
    channels_first = True
    attacks = {}

    # for metrics
    num_evaluations = 0
    actual_evaluations = 0

    # optional cache
    cache = {}

    # Attack management
    def get_attacks(self, status=None):
        if not status:
            return self.attacks

        if status not in enums.AttackStatus:
            print(f"[!] {status} not understood")
            return False

        else:
            return {k: v for (k, v) in self.attacks.items() if v.status == status}

    def set_attack_samples(self, index=0):
        if hasattr(index, "__iter__"):
            # (unused) multiple index
            out = np.array([self.X[i] for i in index])
            batch_shape = (-1,) + self.model_input_shape
        elif type(self.X[index]) is str:
            # array of strings (textattack)
            out = np.array(self.X[index])
            batch_shape = (-1,)
        else:
            # array of arrays (art)
            out = np.atleast_2d(self.X[index])
            batch_shape = (-1,) + self.model_input_shape

        self.active_attack.sample_index = index
        self.active_attack.samples = out.reshape(batch_shape)

    def check_attack_success(self):
        new_labels = np.atleast_1d(self.active_attack.results['final']['label'])
        old_labels = np.atleast_1d(self.active_attack.results['initial']['label'])

        # successful
        if self.active_attack.parameters.get("targeted", False):
            # compare all new labels to all target classes (both as np arrays)
            return new_labels == np.array(self.model_output_classes)[self.active_attack.target_class]
        else:
            return new_labels != np.array(old_labels)

    def outputs_to_labels(self, output):
        # default multiclass label selector via argmax
        # user can override this function if, for example, one wants to choose a specific threshold
        output = np.atleast_2d(output)
        return [self.model_output_classes[i] for i in np.argmax(output, axis=1)]

    @staticmethod
    def _key(array):
        return np.array(array).data.tobytes()

    def _submit_with_cache(self, batch_input):
        # submit to model, with caching
        self.num_evaluations += len(batch_input)
        submit_batch, index, output = [], [], []
        for i, array in enumerate(batch_input):
            key = self._key(array)
            if key in self.cache:
                output.append(self.cache[key])
            else:
                output.append(None)
                submit_batch.append(array)
                index.append(i)

        # submit an entire batch at once for potential API efficiency
        if len(submit_batch) > 0:
            self.actual_evaluations += len(submit_batch)
            results = self.__call__(np.array(submit_batch))

            # merge new results with cached results
            for i, inp, outp in zip(index, submit_batch, results):
                key = self._key(inp)
                self.cache[key] = outp
                output[i] = outp

        return output

    def _submit(self, batch_input):
        # submit to model, without caching
        self.num_evaluations += len(batch_input)
        self.actual_evaluations += len(batch_input)
        return self.__call__(np.array(batch_input))

    def _submit_with_logging(self, batch_input, attack_name="", attack_id=""):
        timestamp = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        output = self._submit(batch_input)  # call the model predict function
        label = self.outputs_to_labels(output)  # get labels based on output(probabilities)

        for _inp, _outp, _lab in zip(batch_input, output, label):
            log_entry = {
                "timestamp": timestamp,
                "model_id": self.model_name,
                "attack_name": attack_name,
                "attack_id": attack_id,
                "input": np.array(_inp).flatten().reshape(-1).tolist(),
                "output": _outp,
                "label": _lab,
            }

            self.active_attack.append_log(log_entry)

        return output

    def _get_query(self, batch):
        inp = batch
        outp = self._submit(inp)
        labels = np.atleast_1d(self.outputs_to_labels(outp))  # call the model predict function and send perturbed text
        # convert to named-tuple in raw list format (JSON compatibility)
        return Query(np.array(inp).tolist(),
                     np.array(outp).tolist(),
                     np.array(labels).tolist())

    def _save_image(self, array, suffix='', extension='png', filename=None):
        assert self.model_data_type == "image", "Saving non-'image' types as an image is not supported"
        module_path = "/".join(self.__module__.split(".")[:-1])
        if filename is None:
            filename = f"{module_path}/results/{self.model_name}-{self.active_attack.attack_id}"
            if "results" not in os.listdir(module_path):
                os.mkdir(f"{module_path}/results")
        if suffix:
            filename += f'-{suffix}'
        filename += f'.{extension}'

        array = np.array(array)
        array[np.isnan(array)] = 0  # change NaNs to 0s

        if self.clip_values[1] == 255:
            array = np.uint8(array)
        elif self.clip_values[1] == 1:
            array = np.uint8(array * 255.)
        else:
            raise ValueError("Cannot determine image type from clip_values.  Expecting: (0,1) or (0,255)")

        if len(self.model_input_shape) == 3:  # color channel?
            if self.channels_first:
                array = array.transpose(1, 2, 0)  # convert (C, H, W) to (H, W, C)
                C = self.model_input_shape[0]
            else:
                C = self.model_input_shape[-1]

            im = Image.fromarray(array.squeeze(), mode='L' if C==1 else 'RGB')

        elif len(self.model_input_shape) == 2:  # grayscale
            im = Image.fromarray(array, 'L')

        else:
            raise ValueError("Expecting at least 2-dimensional image in model_input_shape")

        im.save(filename)
        return filename

    def init_run_attack(self):
        # get initial query input/output/label
        initial = self._get_query(self.active_attack.samples)
        self.active_attack.results = {'initial': initial._asdict()}

    def run_attack(self, logging=False):
        t0 = time.time()
        queries0 = self.num_evaluations
        actual_queries0 = self.actual_evaluations

        # run the attack
        resulting_samples = self._run_attack(logging)  # call the specific method

        # get result input/output/label
        final = self._get_query(resulting_samples)

        self.active_attack.results['final'] = final._asdict()

        # add timing statistics
        elapsed = time.time() - t0
        queries = self.num_evaluations - queries0
        actual_queries = self.actual_evaluations - actual_queries0
        self.active_attack.results['elapsed_time'] = elapsed
        self.active_attack.results['queries'] = queries
        self.active_attack.results['cache_hits'] = queries - actual_queries
        if self.model_data_type == 'image':
            filenames = []
            for i, array in enumerate(self.active_attack.results['initial']['input']):  # loop over initial images
                initial_label = self.active_attack.results["initial"]["label"][i]
                filenames.append(self._save_image(array, suffix=f'initial-{i}-label-{initial_label}'))
                self.active_attack.results['initial']['images'] = filenames

            filenames = []
            for i, array in enumerate(final[0]):  # loop over final images
                final_label = self.active_attack.results["final"]["label"][i]
                filenames.append(self._save_image(array, suffix=f'final-{i}-label-{final_label}'))
                self.active_attack.results['final']['images'] = filenames

    def _run_attack(self, logging):
        raise NotImplementedError()

    def dump(self):
        return {"model_name": self.model_name, "attacks": [v.dump() for k, v in self.attacks.items()]}



class ArtTarget(Target):
    """Art attacks specific implementation inherits Target class"""

    def _as_blackbox_art_target(self, logging, attack_name="", attack_id=""):
        func = functools.partial(self._submit_with_logging, attack_name=attack_name, attack_id=attack_id)
        return wrappers.BlackBoxClassifierWrapper(
            submit_sample=func if logging else self._submit,
            model_input_shape=self.model_input_shape,
            nb_output_classes=len(self.model_output_classes),
            clip_values=self.clip_values,
            channels_first=self.channels_first,
        )

    def _run_art_attack(self, logging):
        # Adversarial Robustness Toolkit

        # initialize attack
        attack_cls = self.active_attack.attack_cls(
            self._as_blackbox_art_target(
                logging,
                attack_name=self.active_attack.attack_name,
                attack_id=self.active_attack.attack_id,
            ),
            **self.active_attack.parameters,
        )
        if self.active_attack.parameters.get("targeted", False):
            adv_examples = attack_cls.generate(
                self.active_attack.samples, [self.active_attack.target_class] * len(self.active_attack.samples)
            ).tolist()

        else:
            adv_examples = attack_cls.generate(self.active_attack.samples).tolist()

        self.active_attack.status = enums.AttackStatus.completed
        return adv_examples

    def _run_attack(self, logging):
        return self._run_art_attack(logging)


class TextTarget(Target):
    def _as_blackbox_textattack_target(self, logging, attack_name="", attack_id=""):
        if logging:
            # return wrapper object with __call__ doing the logging
            func = functools.partial(self._submit_with_logging, attack_name=attack_name, attack_id=attack_id)
        else:
            func = self._submit
        class TextAttackWrapperObject(object):
            def __init__(self, model, logging_func):
                self.logging_func = logging_func
                self.model = model

            def __call__(self, x):
                return self.logging_func(x)

        return TextAttackWrapperObject(self.model, func)  # use wrapped __call__

    def _run_textattack_attack(self, logging):
        # TextAttack

        # initialize attack
        attack_cls = self.active_attack.attack_cls.build(
            self._as_blackbox_textattack_target(
                logging, attack_name=self.active_attack.attack_name, attack_id=self.active_attack.attack_id
            )
        )
        # use the appropriate batch of samples
        results_iter = attack_cls.attack_dataset(
            list(zip(self.active_attack.samples.tolist(), self.active_attack.results['initial']['label']))
        )

        results = [r.perturbed_text() for r in tqdm(results_iter)]

        self.active_attack.status = enums.AttackStatus.completed
        return results

    def _run_attack(self, logging):
        return self._run_textattack_attack(logging)


class SecMLMalwareTarget(Target, ABC):
    model: CWrapperPhi = None
    model_data_type = 'exe'
    model_output_classes = ["goodware", "malware"]
    model_location = "local"

    model_input_shape = (1,)
    sample_input_path = os.path.join(config.targets_path, 'malware', 'samples', 'malware')
    X = []

    def __init__(self):
        malware_files = os.listdir(self.sample_input_path)
        max_length = 0
        xx = []
        for f in malware_files:
            complete_path = os.path.join(self.sample_input_path, f)
            if 'PE' not in magic.from_file(complete_path):
                continue
            with open(complete_path, 'rb') as h:
                code = h.read()
            x_i = np.frombuffer(code, dtype=np.uint8)
            max_length = max(max_length, len(x_i))
            xx.append(x_i)
        self.X = [np.append(x_i, [256] * (max_length - len(x_i))) for x_i in xx]

    @staticmethod
    def _save_exe(exe, path):
        with open(path, 'wb') as h:
            x_real = exe.astype(np.uint8).tolist()
            x_real_adv = b''.join([bytes([i]) for i in x_real])
            h.write(x_real_adv)

    def outputs_to_labels(self, output: np.ndarray):
        # default multiclass label selector via argmax
        # user can override this function if, for example, one wants to choose a specific threshold
        output = np.atleast_2d(output)
        return [self.model_output_classes[i] for i in output.argmax(axis=1)]

    def _submit(self, batch_input: CArray, return_decision_function=True):
        # submit to model, without caching
        self.num_evaluations += batch_input.shape[0]
        self.actual_evaluations += batch_input.shape[0]
        return self.__call__(batch_input)

    def set_attack_samples(self, index=0):
        out = self.X[index]
        self.active_attack.sample_index = index
        self.active_attack.samples = out

    def __call__(self, x):
        if type(x) != CArray:
            x = CArray(x)
        _, scores = self.model.predict(x, return_decision_function=True)
        return scores.tondarray()

    def _create_blackbox_wrapper(self, logging):
        func = functools.partial(self._submit_with_logging, return_decision_function=True,
                                 attack_name=self.active_attack.attack_name, attack_id=self.active_attack.attack_id)
        prediction_function = func if logging else self._submit

        model = wrappers.SecMLBlackBoxClassifierWrapper(self.model, prediction_function)
        return model

    def _run_attack(self, logging):
        model = self.model
        problem = self.active_attack.attack_cls(model, **self.active_attack.parameters)
        engine = CGeneticAlgorithm(problem)
        X = np.atleast_2d(self.active_attack.samples)
        adv_examples = []
        max_length = 0
        for i in range(X.shape[0]):
            x_i = X[i, :]
            y_pred, scores, adv_ds, f_opt = engine.run(CArray(x_i), CArray([1]))
            adv_x = adv_ds.X[0, :]
            adv_examples.append(adv_x)
            max_length = max(max_length, adv_x.shape[1])
        carray_adv_examples = np.zeros((X.shape[0], max_length)) + 256
        for i, x_i in enumerate(adv_examples):
            carray_adv_examples[i, :x_i.shape[1]] = x_i.tondarray()
        self.active_attack.status = enums.AttackStatus.completed
        return carray_adv_examples

