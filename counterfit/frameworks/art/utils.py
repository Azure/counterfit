import pydoc
import numpy as np

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
    'MalwareGDTensorFlow', # error
    'OverTheAirFlickeringPyTorch', # error
    'RobustDPatch', # error
    'ShadowAttack', # error
    # 'SquareAttack', # error
    'TargetedUniversalPerturbation', # error
    'ThresholdAttack', # error
    # 'ZooAttack', # error
    'AdversarialPatchTensorFlowV2',
    'AdversarialPatchPyTorch',
    'AutoProjectedGradientDescent',
    "AutoAttack",
    "FrameSaliencyAttack",
    "ImperceptibleASRPyTorch",
    "ShapeShifter",
    'PoisoningAttackAdversarialEmbedding',
    "PoisoningAttackBackdoor",
    "PoisoningAttackCleanLabelBackdoor",
    "PoisoningAttackSVM",
    "FeatureCollisionAttack",
    "BullseyePolytopeAttackPyTorch",
    "AttributeInferenceBlackBox",
    "AttributeInferenceBaseline",
    "AttributeInferenceBaselineTrueLabel",
    "AttributeInferenceWhiteBoxLifestyleDecisionTree",
    "AttributeInferenceMembership",
    # "MembershipInferenceBlackBox",
    "DatabaseReconstruction"

])

attack_types = {
    "AdversarialPatch": "open-box",
    "AdversarialPatchNumpy": "open-box",
    "BasicIterativeMethod": "open-box",
    "BrendelBethgeAttack": "open-box",
    "BoundaryAttack": "closed-box",
    "CarliniL0Method": "open-box",
    "CarliniLInfMethod": "open-box",
    "CarliniWagnerASR": "open-box",
    "CopycatCNN": "closed-box",
    "DPatch": "open-box",
    "DecisionTreeAttack": "open-box",
    "DeepFool": "open-box",
    "ElasticNet": "open-box",
    "FeatureAdversariesNumpy": "open-box",
    "FeatureAdversariesPyTorch": "open-box",
    "FeatureAdversariesTensorFlowV2": "open-box",
    "FunctionallyEquivalentExtraction": "closed-box",
    "GeoDA": "open-box",
    "HopSkipJump": "closed-box",
    "KnockoffNets": "closed-box",
    "LabelOnlyDecisionBoundary": "open-box",
    "LowProFool": "open-box",
    "MIFace": "open-box",
    "MalwareGDTensorFlow": "open-box",
    "NewtonFool": "open-box",
    "OverTheAirFlickeringPyTorch": "open-box",
    "ProjectedGradientDescentCommon": "open-box",
    "RobustDPatch": "open-box",
    "SaliencyMapMethod": "open-box",
    "ShadowAttack": "open-box",
    "ShapeShifter": "open-box",
    "ProjectedGradientDescentCommon": "open-box",
    "SimBA": "open-box",
    "SpatialTransformation": "open-box",
    "SquareAttack": "closed-box",
    "TargetedUniversalPerturbation": "open-box",
    "ThresholdAttack": "closed-box",
    "UniversalPerturbation": "open-box",
    "Wasserstein": "open-box",
    "VirtualAdversarialMethod": "open-box",
    "ZooAttack": "closed-box",
}

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


def attack_factory(attack_module: str) -> object:
    """Take an an attack loaded with pydoc.locate and instantiate it. Used in self.build()

    Args:
        attack (object): pydoc.locate("art.attacks.evasion.hop_skip_jump")

    Returns:
        object: Returns an instantiated attack class.
    """
    attack = pydoc.locate(attack_module)
    loaded_attack = attack(
        wrapper(
            attack._estimator_requirements,
            input_shape=(1, 28, 28),
            channels_first=True, _channels_first=True,
            clip_values=(0.0, 255.0), _clip_values=(0.0, 255.0),
            nb_classes=10, _nb_classes=10
        ))

    return loaded_attack

def get_default_params(loaded_attack: object) -> dict:
    """Gathers the default parameters for the attack.

    Args:
        loaded_attack (object): An attack object returned by self.attack_factory.

    Returns:
        dict: the default parameters for the attack. 
    """
    default_params = {}
    for i in loaded_attack.attack_params:
        default_params[i] = loaded_attack.__dict__.get(i)

    for estimator in loaded_attack._estimator_requirements:
        try:
            for prop in estimator.estimator_params:
                if prop == "clip_values":
                    default_params["clip_values"] = (0.0, 1.0)
                if prop == "channels_first":
                    default_params["channels_first"] = False
        except Exception as e:
            continue

    return default_params



