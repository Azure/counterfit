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
import gzip

from .DCPW import DeepCPWrapper
from .DCPW import ReplayMemory
from .DCPW import DQN

from counterfit.core.output import CFPrint
from counterfit.core.targets import Target

# for ART
tf.compat.v1.disable_eager_execution()
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu") 
class CartPole(Target):
    target_data_type = "tabular"
    target_name = "cart_pole"
    
    num_episodes = 10000   # how many episodes will the RL's policy model be trained on?
    num_frames = 100
    target_input_shape = (num_frames*3*40*90,)
    
    target_endpoint = f"cartpole_dqn_{num_episodes}.pt.gz"
    data_path = f"cartpole_samples_{num_episodes}_{num_frames}.pkl.gz"

    episode_len_to_success = num_frames-1  # since the model is using difference of frames, 1 index is lost in the difference
    max_episode_len = num_frames
    
    target_output_classes = ["fallen", "upright"]
    target_classifier = "blackbox"
    X = []  # each row is a flattened sequence of screenshots (internally, the DCPW wrapper uses differences)
    dcpw = None
    
    def load(self):
        if not os.path.isfile(self.fullpath(self.target_endpoint)):
            
            CFPrint.warn("Model not found. Training new model...")
            
            self.dcpw = DeepCPWrapper()
            self.dcpw.train(self.num_episodes)
            CFPrint.success("Model trained")

            self.model = self.dcpw.policy_net
            torch.save(self.model, gzip.open(self.fullpath(self.target_endpoint), 'w'))
            CFPrint.success("Model saved")

            self._generate_new_memory()  # sets self.X
            pkl.dump(self.X, gzip.open(self.fullpath(self.data_path), 'w'))
            pkl.dump(self.init_state, gzip.open(self.fullpath(self.data_path[:-7]+"_init_state.gz"), 'w'))
            CFPrint.success("Dataset saved")
            
        else:
            self.model = torch.load(gzip.open(self.fullpath(self.target_endpoint)), map_location=torch.device('cpu'))
            CFPrint.success("Model loaded")
            # let's run the model a few times until we find success
            self.dcpw = DeepCPWrapper(memory=None, policy_net=self.model)
            
            if os.path.isfile(self.fullpath(self.data_path)):
                self.X = pkl.load(gzip.open(self.fullpath(self.data_path), 'rb'))
                self.init_state = pkl.load(gzip.open(self.fullpath(self.data_path[:-7]+"_init_state.gz"), 'rb'))
                CFPrint.success(f"Dataset loaded from {self.fullpath(self.data_path)}")
            else:
                self._generate_new_memory()  # sets self.X
                pkl.dump(self.X, gzip.open(self.fullpath(self.data_path), 'wb'))
                pkl.dump(self.init_state, gzip.open(self.fullpath(self.data_path[:-7]+"_init_state.gz"), 'w'))                
                CFPrint.success("Dataset created from loaded model memory")


    def _generate_new_memory(self):
        CFPrint.success("Generating a good memory")
        while True:
            screens, memory, self.init_state = self.dcpw.play(self.max_episode_len, init_state=None)
            if len(memory.memory) >= self.episode_len_to_success:
                # didn't fail in the first N steps..a good memory!
                break
      
        self.X = np.array(screens[:self.num_frames]).reshape((1,)+self.target_input_shape)        

    
    def predict(self, x):
        # replay, but with noise
        x = x.reshape(len(x), self.num_frames, 3, 40, 90)
        results = []
        for x_i in x:
            done, n_steps, _, final_state = self.dcpw.replay(x_i, max_steps=self.episode_len_to_success, init_state=self.init_state)
            success = int(not done and n_steps >= self.episode_len_to_success)
            results.append([1-success, success])
        return np.array(results, dtype=np.float32)
