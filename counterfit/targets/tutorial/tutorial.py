import pickle

import numpy as np
from counterfit.core.state import ArtTarget


class Tutorial(ArtTarget):
    model_name = "tutorial"
    model_data_type = "image"
    model_endpoint = "counterfit/targets/tutorial/mnist_sklearn_pipeline.pkl"
    model_input_shape = (1, 28, 28)
    model_output_classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    clip_values = (0.0, 255.0)

    X = []

    model_location = ""

    def __init__(self):
        with open(self.model_endpoint, "rb") as f:
            self.model = pickle.load(f)

        self.data_file = "counterfit/targets/tutorial/mnist_784.npz"
        self.sample_data = np.load(self.data_file, allow_pickle=True)

        self.X = self.sample_data["X"]

    def __call__(self, x):
        scores = self.model.predict_proba(x.reshape(x.shape[0], -1))
        return scores.tolist()  # return a list of class probabilities
        # each row must be the same length as model_output_classes
