import pickle
import warnings

import numpy as np
from counterfit.core.targets import CFTarget


class CreditFraud(CFTarget):
    """Target definition for a binary classifier built using scikit-learn from 
    he Kaggle fraudulent credit card transaction dataset at
    https://www.kaggle.com/mlg-ulb/creditcardfraud
    """
    target_name = "creditfraud"
    data_type = "tabular"
    endpoint = "creditfraud/creditfraud_sklearn_pipeline.pkl"
    input_shape = (30,)
    output_classes = ["benign", "fraud"]
    classifier = "blackbox"
    sample_input_path = "creditfraud/creditcard.npz"
    X = []

    def load(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("ignore", category=UserWarning)
            with open(self.fullpath(self.endpoint), "rb") as infile:
                self.model = pickle.load(infile)

            self.model._final_estimator.fitted_ = True  # tell new version of sklearn that the model is fitted
            self.data = np.load(self.fullpath(self.sample_input_path), allow_pickle=True)

        self.X = self.data["X"]  # set data

    def predict(self, x):
        # x is of shape (batch, features) with np.float32 dtype
        scores = self.model.predict_proba(x.reshape(x.shape[0], -1))
        return scores.tolist()  # return a list of class probabilities:
