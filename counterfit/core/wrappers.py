import numpy as np

from art.estimators.estimator import BaseEstimator, NeuralNetworkMixin
from art.estimators.classification import ClassifierMixin
from secml.array import CArray
from secml_malware.attack.blackbox.c_wrapper_phi import CWrapperPhi


class BlackBoxClassifierWrapper(BaseEstimator, NeuralNetworkMixin, ClassifierMixin):
    """This counterfit class wraps the Adversarial Robustness blackbox classifier"""

    def __init__(self, submit_sample, model_input_shape, nb_output_classes, clip_values, channels_first):
        # do not call parent constructor.  We're inheriting only for the sake of ART type checking
        # ...and tending to the other variables manually
        # super(BlackBoxClassifierWrapper, self).__init__(model,clip_values=clip_values)
        self._predictions = submit_sample
        self._input_shape = model_input_shape
        self._nb_classes = nb_output_classes
        self._clip_values = clip_values  # Tuple of the form `(min, max)` of floats or `np.ndarray` representing the minimum and maximum values allowed for features. If arrays are provided, each value will be considered the bound for a feature, thus
        # the shape of clip values needs to match the total number of features.
        self._channels_first = channels_first  # Boolean to indicate index of the color channels in the sample `X`.

    def fit(self, X, y):
        pass

    def class_gradient(self, *args, **kwargs):
        """Compute per-class derivatives w.r.t. `X`."""
        raise Exception("I didn't expect to be called!")

    def loss_gradient(self, *args, **kwargs):
        raise Exception("I didn't expect to be called!")

    def get_activations(self, *args, **kwargs):
        raise Exception("I didn't expect to be called!")

    def set_learning_phase(self, *args, **kwargs):
        raise Exception("I didn't expect to be called!")

    # ART 1.61
    def compute_loss(self, x: np.ndarray, y: np.ndarray, **kwargs) -> np.ndarray:
        raise NotImplementedError

    # ART < 1.6
    def loss(self, x: np.ndarray, y: np.ndarray, **kwargs) -> np.ndarray:
        raise NotImplementedError

    @property
    def input_shape(self):
        return self._input_shape

    def predict(self, X, batch_size=1):
        """
        Abstract method performs prediction of the estimator for input `X`.

        :param X: Samples of shape (nb_samples, nb_features) or (nb_samples, nb_pixels_1, nb_pixels_2,
                  nb_channels) or (nb_samples, nb_channels, nb_pixels_1, nb_pixels_2).
        :param batch_size: Batch size.
        :return: predictions.
        :rtype: format as expected by the `model`
        """

        predictions = np.zeros((X.shape[0], self._nb_classes), dtype=np.float32)
        for batch_index in range(int(np.ceil(X.shape[0] / float(batch_size)))):
            begin, end = (
                batch_index * batch_size,
                min((batch_index + 1) * batch_size, X.shape[0]),
            )

            predictions[begin:end] = self._predictions(X[begin:end])

        return predictions


class SecMLBlackBoxClassifierWrapper:
    """This counterfit class wraps the BlackBox SecML malware class"""

    def __init__(self, model : CWrapperPhi, prediction_function):
        self._wrapper = model
        self._prediction_function = prediction_function

    def predict(self, x : CArray, return_decision_function : bool = True):
        padding_position = x.find(x == 256)
        if padding_position:
            x = x[0, :padding_position[0]]
        feature_vector = self.extract_features(x)
        labels, scores =  self._prediction_function(feature_vector)
        return CArray(labels), CArray(scores)

    @property
    def classifier(self):
        return self._wrapper.classifier

    def extract_features(self, x : CArray):
        return self._wrapper.extract_features(x)