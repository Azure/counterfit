import pickle
import warnings
import numpy as np
from counterfit.core import config
from counterfit.core.state import ArtTarget


class CreditFraud(ArtTarget):
    """Target definition for a binary classifier built using scikit-learn from the Kaggle fraudulent credit card transaction dataset at https://www.kaggle.com/mlg-ulb/creditcardfraud
    """
    model_name = "creditfraud"
    model_data_type = "numpy"
    model_location = "local"
    model_endpoint = f"{config.targets_path}/{model_name}/creditfraud_sklearn_pipeline.pkl"
    model_output_classes = ["benign", "fraud"]
    model_input_shape = (30,)
    sample_input_path = f"{config.targets_path}/{model_name}/creditcard.npz"
    sample_input_shape = (30,)
    label_lookup = None
    clip_values = None
    X = []
    n_samples = None

    def __init__(self, **kwargs):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("ignore", category=UserWarning)
            with open(self.model_endpoint, "rb") as infile:
                self.model = pickle.load(infile)
            self.data = np.load(self.sample_input_path, allow_pickle=True)

        self.X = self.data["X"]  # set data

    def __call__(self, x):
        # x is of shape (batch, features)
        scores = self.model.predict_proba(x.reshape(x.shape[0], -1))
        return scores.tolist()  # return a list of class probabilities
