import pickle

import numpy as np
from counterfit.core.targets import CFTarget


class Digits(CFTarget):
    """ Target for the MNIST dataset. """
    data_type = "image"
    target_name = "digits_mlp"
    log_probs = True
    endpoint = "digits_mlp/mnist_sklearn_pipeline.pkl"
    data_path = "digits_mlp/mnist_784.npz"
    input_shape = (1, 28, 28)
    output_classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    classifier = "blackbox"
    X = []

    def load(self):
        with open(self.fullpath(self.endpoint), "rb") as f:
            self.model = pickle.load(f)

        sample_data = np.load(self.fullpath(self.data_path), allow_pickle=True)

        self.X = sample_data["X"].astype(np.float32)  # float in [0,255]

    def predict(self, x):
        # from IPython import embed; embed()
        x = np.array(x).astype(np.uint8).astype(np.float)  # quantize to valid range
        scores = self.model.predict_proba(x.reshape(x.shape[0], -1))
        # return a list of class probabilities; each row must be the same length as output_classes
        return scores.tolist()
