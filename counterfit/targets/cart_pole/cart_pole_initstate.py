import numpy as np
import os
import pickle as pkl
import math

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
import tensorflow as tf
import gym
import gzip
import tqdm

from .DCPW import DeepCPWrapper
from .DCPW import ReplayMemory
from .DCPW import DQN

from counterfit.core.output import CFPrint
from counterfit.core.targets import Target

# for ART
tf.compat.v1.disable_eager_execution()
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu") 
class CartPoleInitState(Target):
    target_data_type = "tabular"
    target_name = "cart_pole_initstate"
    
    num_episodes = 10000   # how many episodes will the RL's policy model be trained on?
    target_endpoint = f"cartpole_dqn_{num_episodes}.pt.gz"
    data_path = f"cartpole_states_{num_episodes}.pkl.gz"

    target_input_shape = (4,)
    num_examples = 10
    episode_len_to_success = 100
    max_episode_len = 101
    
    target_output_classes = ["fallen", "upright"]
    target_classifier = "blackbox"
    X = []
    dcpw = None
    
    def load(self):
        if not os.path.isfile(self.fullpath(self.target_endpoint)):
            
            CFPrint.warn("[!] Model not found. Training new model...")
            
            self.dcpw = DeepCPWrapper()
            self.dcpw.train(self.num_episodes)
            CFPrint.success("Model trained")

            self.model = self.dcpw.policy_net
            torch.save(self.model, gzip.open(self.fullpath(self.target_endpoint), 'w'))
            CFPrint.success("[+] Model saved")

            self._generate_initial_states()  # sets self.X
            pkl.dump(self.X, gzip.open(self.fullpath(self.data_path), 'w'))
            CFPrint.success("[+] Dataset saved")
            
        else:
            self.model = torch.load(gzip.open(self.fullpath(self.target_endpoint)), map_location=torch.device('cpu'))
            CFPrint.success("[+] Model loaded")

            # let's run the model a few times until we find success
            self.dcpw = DeepCPWrapper(memory=None, policy_net=self.model)
        
            if os.path.isfile(self.fullpath(self.data_path)):
                self.X = pkl.load(gzip.open(self.fullpath(self.data_path)))
                CFPrint.success(f"[+] Dataset loaded from {self.fullpath(self.data_path)}")
            else:
                self._generate_initial_states()  # sets self.X
                pkl.dump(self.X, gzip.open(self.fullpath(self.data_path), 'w'))
                CFPrint.success("[+] Dataset created from loaded model memory")

    def _generate_initial_states(self):
        CFPrint.success("[+] Generating initial states that are successful")
        self.X = []
        for i in tqdm.tqdm(range(self.num_examples)):
            while True:
                _, memory, init_state = self.dcpw.play(self.max_episode_len)
                if len(memory.memory) > self.episode_len_to_success:
                    # didn't fail in the first N steps: success!
                    break
            self.X.append(np.array(init_state))
        self.X = np.asarray(self.X)
        
    
    def predict(self, x):
        # x is a batch of initial states
        results = []
        for x_i in x:
            _, memory, _ = self.dcpw.play(self.max_episode_len, init_state=x_i)
            succeeded = int(len(memory.memory) > self.episode_len_to_success)
            results.append([1-succeeded, succeeded])
        return np.array(results, dtype=np.float32)
