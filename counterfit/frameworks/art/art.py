import importlib
import inspect
import re
import os
from counterfit.core.output import CFPrint

import numpy as np
from pydoc import locate
import tensorflow as tf
from collections import defaultdict
from rich.table import Table

from art.utils import compute_success_array
from art.attacks.poisoning.perturbations import add_pattern_bd
from art.attacks.poisoning import PoisoningAttackBackdoor
from art.estimators.classification import KerasClassifier
from art.attacks.inference.membership_inference import (
    MembershipInferenceBlackBox)
from art.attacks.evasion.fast_gradient import FastGradientMethod

from counterfit.core.attacks import CFAttack
from counterfit.report.report_generator import get_target_data_type_obj
from counterfit.core.frameworks import Framework
from counterfit.core.targets import Target

# These are some random things that are used for loading and pulling default params.
# These should be hot-patched during self.build or self.run
tf.compat.v1.disable_eager_execution()

attacks_still_wip = set([
    'AdversarialPatch',   # error
    'AdversarialPatchNumpy',  # error
    'BasicIterativeMethod',   # error
    'BrendelBethgeAttack',  # error
    'CarliniWagnerASR', # no ASR models
    'DPatch', # error
    'DecisionTreeAttack', # error
    'FeatureAdversariesNumpy', # error
    'FeatureAdversariesPyTorch', # error
    'FeatureAdversariesTensorFlowV2', # error
    'GeoDA', # error
    'HighConfidenceLowUncertainty', # error: requires GPR models
    'LowProFool', # error
    # 'MIFace', # THIS ACTUALLY WORKS, but counerfit can't deal with it currently
    'MalwareGDTensorFlow', # error
    'OverTheAirFlickeringPyTorch', # error
    'RobustDPatch', # error
    'ShadowAttack', # error
    'SquareAttack', # error
    'TargetedUniversalPerturbation', # error
    'ThresholdAttack', # error
    'ZooAttack', # error
])

attack_tags = {
    "AdversarialPatch": ["image"],
    "AdversarialPatchNumpy": ["image"],
    "BasicIterativeMethod": ["image", "tabular"],
    "BrendelBethgeAttack": ["image", "tabular"],
    "BoundaryAttack": ["image", "tabular"],
    "CarliniL0Method": ["image", "tabular"],
    "CarliniLInfMethod": ["image", "tabular"],
    "CarliniWagnerASR": ["image", "tabular"],
    "CopycatCNN": ["image"],
    "DPatch": ["image"],
    "DecisionTreeAttack": ["image", "tabular"],
    "DeepFool": ["image", "tabular"],
    "ElasticNet": ["image", "tabular"],
    "FeatureAdversariesNumpy": ["image", "tabular"],
    "FeatureAdversariesPyTorch": ["image", "tabular"],
    "FeatureAdversariesTensorFlowV2": ["image", "tabular"],
    "FunctionallyEquivalentExtraction": ["image", "tabular"],
    "GeoDA": ["image", "tabular"],
    "HopSkipJump": ["image", "tabular"],
    "KnockoffNets": ["image", "tabular"],
    "LabelOnlyDecisionBoundary": ["image", "tabular"],
    "LowProFool": ["image", "tabular"],
    "MIFace": ["image", "tabular"],
    "MalwareGDTensorFlow": ["image", "tabular"],
    "NewtonFool": ["image", "tabular"],
    "OverTheAirFlickeringPyTorch": ["image", "tabular"],
    "ProjectedGradientDescentCommon": ["image", "tabular"],
    "RobustDPatch": ["image", "tabular"],
    "SaliencyMapMethod": ["image", "tabular"],
    "ShadowAttack": ["image", "tabular"],
    "ShapeShifter": ["image", "tabular"],
    "ProjectedGradientDescentCommon": ["image", "tabular"],
    "SimBA": ["image"],
    "SpatialTransformation": ["image", "tabular"],
    "SquareAttack": ["image"],
    "TargetedUniversalPerturbation": ["image", "tabular"],
    "ThresholdAttack": ["image"],
    "UniversalPerturbation": ["image"],
    "Wasserstein": ["image"],
    "VirtualAdversarialMethod": ["image"],
    "ZooAttack": ["image"],
}


attack_types = {
    "AdversarialPatch": "WhiteBox",
    "AdversarialPatchNumpy": "WhiteBox",
    "BasicIterativeMethod": "WhiteBox",
    "BrendelBethgeAttack": "WhiteBox",
    "BoundaryAttack": "BlackBox",
    "CarliniL0Method": "WhiteBox",
    "CarliniLInfMethod": "WhiteBox",
    "CarliniWagnerASR": "WhiteBox",
    "CopycatCNN": "BlackBox",
    "DPatch": "WhiteBox",
    "DecisionTreeAttack": "WhiteBox",
    "DeepFool": "WhiteBox",
    "ElasticNet": "WhiteBox",
    "FeatureAdversariesNumpy": "WhiteBox",
    "FeatureAdversariesPyTorch": "WhiteBox",
    "FeatureAdversariesTensorFlowV2": "WhiteBox",
    "FunctionallyEquivalentExtraction": "BlackBox",
    "GeoDA": "WhiteBox",
    "HopSkipJump": "BlackBox",
    "KnockoffNets": "BlackBox",
    "LabelOnlyDecisionBoundary": "WhiteBox",
    "LowProFool": "WhiteBox",
    "MIFace": "WhiteBox",
    "MalwareGDTensorFlow": "WhiteBox",
    "NewtonFool": "WhiteBox",
    "OverTheAirFlickeringPyTorch": "WhiteBox",
    "ProjectedGradientDescentCommon": "WhiteBox",
    "RobustDPatch": "WhiteBox",
    "SaliencyMapMethod": "WhiteBox",
    "ShadowAttack": "WhiteBox",
    "ShapeShifter": "WhiteBox",
    "ProjectedGradientDescentCommon": "WhiteBox",
    "SimBA": "WhiteBox",
    "SpatialTransformation": "WhiteBox",
    "SquareAttack": "BlackBox",
    "TargetedUniversalPerturbation": "WhiteBox",
    "ThresholdAttack": "BlackBox",
    "UniversalPerturbation": "WhiteBox",
    "Wasserstein": "WhiteBox",
    "VirtualAdversarialMethod": "WhiteBox",
    "ZooAttack": "BlackBox",
}


def wrapper(*args, **kwargs):
    """
    This function returns a wrapped estimator for art. It takes anything art asks for a instantiates a class.
    """
    estimators = args[0]

    class OneWrapperToRuleThemAll(*estimators):
        def __init__(self, *args, **kwargs):
            for k, v in kwargs.items():
                self.__dict__[k] = v

            self.postprocessing_defences = []
            self.preprocessing_operations = []

        def fit(self):
            pass

        def loss_gradient(self, **kwargs):
            pass

        def predict(self, x, **kwargs):
            return np.array(self.predict_wrapper(x, **kwargs))

        def compute_loss(self):
            pass

        def get_activations(self):
            pass

        def class_gradient(self):
            pass

        def input_shape(self):
            return self.w_input_shape

        def compute_loss_and_decoded_output(self):
            pass

        def sample_rate(self):
            pass

        def to_training_mode(self):
            pass

        def native_label_is_pytorch_format(self):
            pass

        def perturbation(self):
            pass

    return OneWrapperToRuleThemAll(estimators, **kwargs)


class ArtFramework(Framework):
    def __init__(self):
        super().__init__()

        self.classifiers = defaultdict()

    def load(self):
        temp_model = tf.keras.models.load_model("counterfit/targets/digits_keras/mnist_model.h5")
        temp_classifier = KerasClassifier(model=temp_model, channels_first=False)
        adv_crafter = FastGradientMethod(temp_classifier, eps=0.1)
        meminf_attack = MembershipInferenceBlackBox(temp_classifier, attack_model_type="nn")
        backdoor = PoisoningAttackBackdoor(add_pattern_bd)

        def some_func():
            return True

        self.load_classifiers()
        art_attacks = importlib.import_module("art.attacks")
        attacks = {}

        # Hunt for the different attack categories
        for attack_type in art_attacks.Attack.__subclasses__():
            if attack_type.__name__ not in attacks.keys():
                attacks[attack_type.__name__] = []

            for attack_class in attack_type.__subclasses__():
                if attack_class.__subclasses__():
                    for subclass in attack_class.__subclasses__():
                        attacks[attack_type.__name__].append(subclass)
                        new_attack = subclass
                else:
                    attacks[attack_type.__name__].append(attack_class)
                    new_attack = attack_class

                # filter out attacks that are still being worked on
                if new_attack.__name__ in attacks_still_wip:
                    continue

                try:
                    if new_attack.__name__ not in self.attacks.keys():

                        if new_attack.__name__ in attack_tags.keys():
                            attack_data_tags = attack_tags.get(
                                new_attack.__name__)
                        else:
                            attack_data_tags = ["unknown"]

                        attack_category = attack_types.get(new_attack.__name__, "unknown")

                        if "ImperceptibleASR" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(new_attack._estimator_requirements), masker=locate(
                                'art.attacks.evasion.imperceptible_asr.imperceptible_asr.PsychoacousticMasker')())
                        elif "PoisoningAttackAdversarialEmbedding" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                new_attack._estimator_requirements), backdoor=backdoor, feature_layer="test", target="")
                        elif "PoisoningAttackCleanLabelBackdoor" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                new_attack._estimator_requirements), backdoor=backdoor, proxy_classifier=temp_classifier, target="")
                        elif "FrameSaliencyAttack" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                (temp_classifier), attacker=adv_crafter))
                        elif "FeatureAdversariesPyTorch" == new_attack.__name__:
                            loaded_attack = new_attack(
                                wrapper(new_attack._estimator_requirements), delta=0.1, step_size=1)
                        elif "FeatureAdversariesTensorFlowV2" == new_attack.__name__:
                            loaded_attack = new_attack(
                                wrapper(new_attack._estimator_requirements), delta=0.1, step_size=1)
                        elif "FeatureAdversariesNumpy" == new_attack.__name__:
                            loaded_attack = new_attack(
                                wrapper(new_attack._estimator_requirements), delta=0.1, layer=1)
                        elif "MalwareGDTensorFlow" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                new_attack._estimator_requirements), embedding_weights=np.array([1, 2]), param_dic={})
                        elif "ShapeShifter" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                new_attack._estimator_requirements, random_transform=some_func))
                        elif "AttributeInferenceBaseline" == new_attack.__name__:
                            loaded_attack = new_attack(
                                wrapper(temp_classifier))
                        elif "AttributeInferenceMembership" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                temp_classifier), membership_attack=meminf_attack)
                        elif "AutoProjectedGradientDescent" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                new_attack._estimator_requirements, loss_type=None))
                        elif "SquareAttack" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                new_attack._estimator_requirements), adv_criterion=np.array([1.0]), loss=some_func())
                        elif "MembershipInferenceBlackBox" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                new_attack._estimator_requirements))
                        elif "LabelOnlyDecisionBoundary" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                new_attack._estimator_requirements), distance_threshold_tau=1.0)
                        elif "FunctionallyEquivalentExtraction" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                new_attack._estimator_requirements,
                                _nb_classes=10,
                                input_shape=(28, 28, 1)),
                                num_neurons=10)
                        elif "ZooAttack" == new_attack.__name__:
                            loaded_attack = new_attack(wrapper(
                                    new_attack._estimator_requirements,
                                    clip_values=(0.0, 255.0),
                                    input_shape=(1, 28, 28),
                                    nb_classes=10,
                                    channels_first=True))
                        else:
                            loaded_attack = new_attack(
                                wrapper(
                                    new_attack._estimator_requirements,
                                    input_shape=(1, 28, 28),
                                    channels_first=True, _channels_first=True,
                                    clip_values=(0.0, 255.0), _clip_values=(0.0, 255.0),
                                    nb_classes=10, _nb_classes=10
                                ))

                        default_params = {}
                        for i in loaded_attack.attack_params:
                            default_params[i] = loaded_attack.__dict__.get(i)

                        for estimator in new_attack._estimator_requirements:
                            try:
                                for prop in estimator.estimator_params:
                                    if prop == "clip_values":
                                        default_params["clip_values"] = (
                                            0.0, 1.0)
                                    if prop == "channels_first":
                                        default_params["channels_first"] = False
                            except Exception as e:
                                continue

                        # Add the attack to the framework
                        self.add_attack(
                            attack_name=new_attack.__name__,
                            attack_type=attack_type.__name__,
                            attack_category=attack_category,
                            attack_data_tags=attack_data_tags,
                            attack_class=loaded_attack,
                            attack_default_params=default_params)

                except Exception as e:
                    # print(new_attack.__name__, e)
                    continue
        self.loaded_status = True

    def load_classifiers(self):
        """
        Load ART classifiers
        """
        base_import = importlib.import_module(f"art.estimators.classification")
        for classifier in base_import.__dict__.values():
            if inspect.isclass(classifier):
                if len(classifier.__subclasses__()) > 0:
                    for subclass in classifier.__subclasses__():
                        if "classification" not in subclass.__module__:
                            continue

                        if "classifier" in subclass.__module__:
                            continue

                        else:
                            classifier_name = re.findall(
                                r"\w+", str(subclass).split(".")[-1])[0]
                            self.classifiers[classifier_name] = subclass

    def build(self, target: Target, attack: object) -> CFAttack:
        """
        Build the attack.

        Initialize parameters.
        Set samples.
        """
        # Return the correct estimator for the target selected.
        # Keep an empty classifier around for extraction attacks.
        classifier = self.get_classifier(target)

        # Build the classifier
        if "BlackBox" in classifier.__name__:
            target_classifier = classifier(
                target.predict_wrapper,
                target.target_input_shape,
                len(target.target_output_classes)
            )

        # Everything else takes a model file.
        else:
            target_classifier = classifier(
                model=target.model
            )

        # 100% build rate. Same % run rate.
        attack._estimator = target_classifier

        return attack

    def run(self, cfattack: CFAttack):
        # Find the appropriate "run" function
        attack_attributes = set(cfattack.attack.__dir__())

        # ART has its own set_params function. Use it.
        cfattack.attack.set_params(**cfattack.options.get_current_options())

        # Run the attack. Each attack type has it's own execution function signature.
        if "infer" in attack_attributes:
            results = cfattack.attack.infer(
                np.array(cfattack.samples, dtype=np.float32), y=np.array(cfattack.target.target_output_classes, dtype=np.float32))

        elif "reconstruct" in attack_attributes:
            results = cfattack.attack.reconstruct(
                np.array(cfattack.samples, dtype=np.float32))

        elif "generate" in attack_attributes:
            if "CarliniWagnerASR" == cfattack.attack_name:
                y = cfattack.target.target_output_classes
            elif "FeatureAdversariesNumpy" in attack_attributes:
                y = cfattack.samples
            elif "FeatureAdversariesPyTorch" in attack_attributes:
                y = cfattack.samples
            elif "FeatureAdversariesTensorFlowV2" in attack_attributes:
                y = cfattack.samples
            else:
                y = None

            if "ZooAttack" == cfattack.attack_name:
                # patch ZooAttack
                cfattack.attack.estimator.channels_first = True

            results = cfattack.attack.generate(
                np.array(cfattack.samples, dtype=np.float32), y=y)

        elif "poison" in attack_attributes:
            results = cfattack.attack.poison(
                np.array(cfattack.samples, dtype=np.float32))

        elif "poison_estimator" in attack_attributes:
            results = cfattack.attack.poison(
                np.array(cfattack.samples, dtype=np.float32))

        elif "extract" in attack_attributes:
            # Returns a thieved classifier
            training_shape = (
                len(cfattack.target.X), *cfattack.target.target_input_shape)

            samples_to_query = cfattack.target.X.reshape(
                training_shape).astype(np.float32)
            results = cfattack.attack.extract(
                x=samples_to_query, thieved_classifier=cfattack.attack.estimator)

            cfattack.thieved_classifier = results
        else:
            print("Not found!")
        return results

    def post_attack_processing(self, cfattack: CFAttack):
        attack_attributes = set(cfattack.attack.__dir__())

        if "generate" in attack_attributes:
            current_datatype = cfattack.target.target_data_type
            current_dt_report_gen = get_target_data_type_obj(current_datatype)
            summary = current_dt_report_gen.get_run_summary(cfattack)
            current_dt_report_gen.print_run_summary(summary)
            
        elif "extract" in attack_attributes:
            # Override default reporting for the attack type
            extract_table = Table(header_style="bold magenta")
            # Add columns to extraction table
            extract_table.add_column("Success")
            extract_table.add_column("Copy Cat Accuracy")
            extract_table.add_column("Elapsed time")
            extract_table.add_column("Total Queries")

            # Add data to extraction table
            success = cfattack.success[0]  # Starting value
            thieved_accuracy = cfattack.results
            elapsed_time = cfattack.elapsed_time
            num_queries = cfattack.logger.num_queries
            extract_table.add_row(str(success), str(
                thieved_accuracy), str(elapsed_time), str(num_queries))

            CFPrint.output(extract_table)

    def check_success(self, cfattack: CFAttack) -> bool:
        attack_attributes = set(cfattack.attack.__dir__())

        if "generate" in attack_attributes:
            return self.evasion_success(cfattack)

        elif "extract" in attack_attributes:
            return self.extraction_success(cfattack)

    def get_classifier(self, target: Target):
        # this code attempts to match the .target_classifier attribute of a target with an ART
        if not getattr(target, "target_classifier"):
            return self.classifiers.get("BlackBoxClassifierNeuralNetwork")
        elif target.target_classifier == None:
            return self.classifiers.get("BlackBoxClassifierNeuralNetwork")
        else:
            for classifier in self.classifiers.keys():
                if target.target_classifier.lower() in classifier.lower():
                    return self.classifiers.get(classifier)

    def evasion_success(self, cfattack: CFAttack):
        if cfattack.options.__dict__.get("targeted") == True:
            labels = cfattack.options.target_labels
            targeted = True
        else:
            labels = cfattack.initial_labels
            targeted = False

        success = compute_success_array(
            cfattack.attack._estimator,
            cfattack.samples,
            labels,
            cfattack.results,
            targeted
        )

        final_outputs, final_labels = cfattack.target.get_sample_labels(
            cfattack.results)
        cfattack.final_labels = final_labels
        cfattack.final_outputs = final_outputs
        return success

    def extraction_success(self, cfattack: CFAttack):
        training_shape = (
            len(cfattack.target.X), *cfattack.target.target_input_shape)
        training_data = cfattack.target.X.reshape(training_shape)

        victim_preds = np.atleast_1d(np.argmax(
            cfattack.target.predict_wrapper(x=training_data), axis=1))
        thieved_preds = np.atleast_1d(np.argmax(
            cfattack.thieved_classifier.predict(x=training_data), axis=1))

        acc = np.sum(victim_preds == thieved_preds) / len(victim_preds)

        cfattack.results = acc

        if acc > 0.1:  # TODO add to options struct
            return [True]
        else:
            return [False]
