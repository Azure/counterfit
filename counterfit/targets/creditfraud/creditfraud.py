import pickle

import numpy as np
import warnings

from counterfit.core.targets import Target


class CreditFraud(Target):
    """Target definition for a binary classifier built using scikit-learn from the Kaggle fraudulent credit card transaction dataset at https://www.kaggle.com/mlg-ulb/creditcardfraud
    """
    target_name = "creditfraud"
    target_data_type = "tabular"
    target_endpoint = "creditfraud_sklearn_pipeline.pkl"
    target_input_shape = (30,)
    target_output_classes = ["benign", "fraud"]
    target_classifier = "BlackBox"
    sample_input_path = "creditcard.npz"
    X = []

    def load(self, **kwargs):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("ignore", category=UserWarning)
            with open(self.fullpath(self.target_endpoint), "rb") as infile:
                self.model = pickle.load(infile)
                self.model._final_estimator.fitted_ = True  # tell new version of sklearn that the model is fitted
            self.data = np.load(self.fullpath(
                self.sample_input_path), allow_pickle=True)

        self.X = self.data["X"]  # set data

    def predict(self, x):
        # x is of shape (batch, features) with np.float32 dtype
        scores = self.model.predict_proba(x.reshape(x.shape[0], -1))
        return scores.tolist()  # return a list of class probabilities
