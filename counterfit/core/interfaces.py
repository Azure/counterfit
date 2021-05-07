# interfaces.py
# Contains the primary interfaces for counterfit core objects (Targets and Attacks).
# Ensures counterfit core object compliance with attack framework requirements.
#

import abc


# Target
class AbstractTarget(abc.ABC):
    """Abstract Target class for all the targets"""
    @property
    @abc.abstractmethod
    def model_name(self, model_name):
        """Counterfit requirement.
        :param name: Name of the target. Should be descriptive of the model or
                     endpoint.
        :return: None. Sets the name property for the target class.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def model_data_type(self, model_data_type):
        """Counterfit requirement.
        :param tag: Data type tag. Is used to match relevant attacks to a
                    target. Should be 'image' or 'generic'.
        :return: None. Sets the tag property on the target class.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def model_input_shape(self, model_input_shape):
        """Adversarial Robustness Toolbox requirement.
        :param input_shape: Is the shape of the input that will be perturbed by
                            the Adversarial Robustness Toolbox. In most cases
                            shape should be (batch, channels, height, width)
                            This is not necessarily the same shape as a target
                            models input shape. See `predict`
        :return: None. Sets the input_shape property for the target class that
                 is used by the BlackboxClassfierWrapper.
        """

        raise NotImplementedError

    @property
    @abc.abstractmethod
    def model_output_classes(self, model_output_classes):
        """Adversarial Robustness Toolbox requirement.
        :param nb_classes: Is the number of output classes from the target
                           model. If unknown nb_classes should equal '(2, )'
                           for true or false.
        :return: None. Set the nb_classes property on the target class.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def X(self, X):
        """Couterfit requirement.

        :param X: a list of input samples
        :return: None. Sets the attack results after an attack.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __call__(self, x):
        """Adversarial Robustness Toolbox requirement.

        :param batch: A batch of samples. Constrained to (1, ).
        :return: A score_array

        The Adversarial Robustness Toolbox uses this function to interact
        with a target model. It will make a prediction and use the output
        to inform the next perturbation.

        During runtime the Adversarial Robustness Toolbox will call this
        function interatively. Submitting inputs via 'batch'. However,
        'batch' is a numpy array which is not always suitable for a target
        model, i.e an image classifer that requires a PNG file. Input
        processing required before submitting a sample to the target model
        and should happen in this function.

        Additionally, because this function is called iteratively, any
        post-processing steps should happen in this function.

        This function should return a 'score_array'
        """

        raise NotImplementedError

    @abc.abstractmethod
    def outputs_to_labels(self, output):
        """
        Counterfit requirement.

        :param output: a single output from the model (could be a hard/soft label or a vector of scores)
        :return: a label, i.e., any type that can be compared
        """
        raise NotImplementedError


# Attack
class AbstractAttack(abc.ABC):
    """Abstract Attack class for the attacks"""
    @property
    @abc.abstractmethod
    def attack_cls(self, attack_cls):
        """Counterfit requirement."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def attack_name(self, attack_name):
        """Counterfit requirement"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def attack_type(self, attack_type):
        """Counterfit requirment"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def category(self, category):
        """Counterfit requirement"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def framework(self, framework):
        """Counterfit requirement"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def random(self, framework):
        """Counterfit requirement"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def default(self, framework):
        """Counterfit requirement"""
        raise NotImplementedError
