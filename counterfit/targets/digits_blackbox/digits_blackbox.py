import pickle

import numpy as np
from counterfit.core.targets import Target


class Digits(Target):
    target_data_type = "image"
    target_name = "digits_blackbox"
    target_classifier = "blackbox"
    target_endpoint = "mnist_sklearn_pipeline.pkl"
    target_input_shape = (1, 28, 28)
    target_output_classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    X = []

    def load(self):
        with open(self.fullpath(self.target_endpoint), "rb") as f:
            self.model = pickle.load(f)

        sample_data = np.load(self.fullpath(
            "mnist_784.npz"), allow_pickle=True)

        self.X = sample_data["X"]
        # .astype(np.uint8)

    def predict(self, x):
        x = np.array(x)
        scores = self.model.predict_proba(x.reshape(x.shape[0], -1))
        # return a list of class probabilities; each row must be the same length as target_output_classes
        return scores.tolist()
