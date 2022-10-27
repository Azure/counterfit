import numpy as np
import os
import pickle as pkl
import math

import torch
import tensorflow as tf
import gzip
import tqdm

from counterfit.targets.cart_pole.DCPW import DeepCPWrapper

from counterfit.core.output import CFPrint
from counterfit.core.targets import CFTarget

# for ART
tf.compat.v1.disable_eager_execution()
device = torch.device("cpu")


class CartPoleInitState(CFTarget):
    data_type = "tabular"
    target_name = "cart_pole_initstate"
    output_classes = ["fallen", "upright"]
    classifier = "blackbox"
    # how many episodes will the RL's policy model be trained on?
    num_episodes = 10_000
    endpoint = f"cartpole_dqn_{num_episodes}.pt.gz"
    data_path = f"cartpole_states_{num_episodes}.pkl.gz"
    input_shape = (4, )
    num_examples = 10
    episode_len_to_success = 100
    max_episode_len = 101
    X = []
    deep_cp_wrapper = None
    
    def load(self):
        cart_pole_model_file = self.fullpath(self.endpoint)
        cart_pole_data_file = self.fullpath(self.data_path)
        if not os.path.isfile(cart_pole_model_file):
            CFPrint.warn("[!] Model not found. Training new model...")
            self.deep_cp_wrapper = DeepCPWrapper()
            self.deep_cp_wrapper.train(self.num_episodes)
            CFPrint.success("Model trained")
            self.model = self.deep_cp_wrapper.policy_net
            torch.save(self.model, gzip.open(cart_pole_model_file, 'w'))
            CFPrint.success("[+] Model saved")
            self._generate_initial_states()
            pkl.dump(self.X, gzip.open(cart_pole_data_file, 'w'))
            CFPrint.success("[+] Dataset saved")
        else:
            self.model = torch.load(gzip.open(cart_pole_model_file), map_location=torch.device('cpu'))
            CFPrint.success("[+] Model loaded")
            # let's run the model a few times until we find success
            self.deep_cp_wrapper = DeepCPWrapper(memory=None, policy_net=self.model)
            if os.path.isfile(cart_pole_data_file):
                self.X = pkl.load(gzip.open(cart_pole_data_file))
                CFPrint.success(f"[+] Dataset loaded from {cart_pole_data_file}")
            else:
                self._generate_initial_states()  # sets self.X
                pkl.dump(self.X, gzip.open(cart_pole_data_file, 'w'))
                CFPrint.success("[+] Dataset created from loaded model memory")

    def _generate_initial_states(self):
        CFPrint.success("[+] Generating initial states that are successful")
        self.X = []
        for _ in tqdm.tqdm(range(self.num_examples)):
            while True:
                _, memory, init_state = self.deep_cp_wrapper.play(self.max_episode_len)
                if len(memory.memory) > self.episode_len_to_success:
                    # didn't fail in the first N steps: success!
                    break
            self.X.append(np.array(init_state))
        self.X = np.asarray(self.X)

    def predict(self, x):
        # x is a batch of initial states
        results = []
        for x_i in x:
            _, memory, _ = self.deep_cp_wrapper.play(self.max_episode_len, init_state=x_i)
            succeeded = int(len(memory.memory) > self.episode_len_to_success)
            results.append([1-succeeded, succeeded])
        return np.array(results, dtype=np.float32)
