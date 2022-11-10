import pickle

import numpy as np
from counterfit.core.targets import CFTarget


class Digits(CFTarget):
    data_type = "image"
    name = "digits_mlp"
    log_probs = True
    endpoint = "digits_mlp/mnist_sklearn_pipeline.pkl"
    input_shape = (1, 28, 28)
    output_classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    X = []

    def load(self):
        with open(self.fullpath(self.endpoint), "rb") as f:
            self.model = pickle.load(f)

        sample_data = np.load(self.fullpath(
            "digits_mlp/mnist_784.npz"), allow_pickle=True)

        self.X = sample_data["X"]  # float in [0,255]

    def predict(self, x):
        x = np.array(x).astype(np.uint8).astype(np.float)  # quantize to valid range
        scores = self.model.predict_proba(x.reshape(x.shape[0], -1))
        # return a list of class probabilities; each row must be the same length as output_classes
        return scores.tolist()
