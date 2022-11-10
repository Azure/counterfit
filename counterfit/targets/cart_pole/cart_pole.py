import numpy as np
import os
import pickle as pkl
import torch
import tensorflow as tf
import gzip

from counterfit.targets.cart_pole.DCPW import DeepCPWrapper
from counterfit.core.targets import CFTarget

from counterfit.core.output import CFPrint

# for ART
tf.compat.v1.disable_eager_execution()
device = torch.device("cpu")


class CartPole(CFTarget):
    data_type = "tabular"
    target_name = "cart_pole"
    output_classes = ["fallen", "upright"]
    classifier = "closed-box"
    # how many episodes will the RL's policy model be trained on?
    num_episodes = 10_000
    num_frames = 100
    input_shape = (num_frames * 3 * 40 * 90,)
    endpoint = f"cartpole_dqn_{num_episodes}.pt.gz"
    data_path = f"cartpole_samples_{num_episodes}_{num_frames}.pkl.gz"
    # since the model is using difference of frames, 1 index is lost in the difference
    episode_len_to_success = num_frames - 1
    max_episode_len = num_frames
    # each row is a flattened sequence of screenshots (internally, the DCPW wrapper uses differences)
    X = []
    deep_cp_wrapper = None

    def load(self):
        """ Load the Counterfit Target model.

        If a model file is not available, the method will train one automatically.
        """
        cart_pole_endpoint_file = self.fullpath(self.endpoint)
        caty_pole_data_file = self.fullpath(self.data_path)
        if not os.path.isfile(cart_pole_endpoint_file):
            # Train a new model when the model not found.
            CFPrint.warn("Model not found. Training new model...")
            self.deep_cp_wrapper = DeepCPWrapper()
            self.deep_cp_wrapper.train(self.num_episodes)
            CFPrint.success("Model trained")
            self.model = self.deep_cp_wrapper.policy_net
            torch.save(self.model, gzip.open(self.fullpath(self.endpoint), 'w'))
            CFPrint.success("Model saved")
            # sets self.X
            self._generate_new_memory()
            pkl.dump(self.X, gzip.open(caty_pole_data_file, 'w'))
            pkl.dump(self.init_state, gzip.open(self.fullpath(self.data_path[:-7] + "_init_state.gz"), 'w'))
            CFPrint.success("Dataset saved")
        else:
            uncompressed_cart_pole_model = gzip.open(cart_pole_endpoint_file)
            self.model = torch.load(uncompressed_cart_pole_model, map_location=torch.device('cpu'))
            CFPrint.success("Model loaded")
            # let's run the model a few times until we find success
            self.deep_cp_wrapper = DeepCPWrapper(memory=None, policy_net=self.model)
            if os.path.isfile(caty_pole_data_file):
                self.X = pkl.load(gzip.open(caty_pole_data_file, 'rb'))
                self.init_state = pkl.load(gzip.open(self.fullpath(self.data_path[:-7] + "_init_state.gz"), 'rb'))
                CFPrint.success(f"Dataset loaded from {caty_pole_data_file}")
            else:
                self._generate_new_memory()  # sets self.X
                pkl.dump(self.X, gzip.open(caty_pole_data_file, 'wb'))
                pkl.dump(self.init_state, gzip.open(self.fullpath(self.data_path[:-7] + "_init_state.gz"), 'w'))
                CFPrint.success("Dataset created from loaded model memory")

    def _generate_new_memory(self):
        CFPrint.success("Generating a good memory")
        while True:
            screens, memory, self.init_state = self.deep_cp_wrapper.play(self.max_episode_len, init_state=None)
            if len(memory.memory) >= self.episode_len_to_success:
                # didn't fail in the first N steps..a good memory!
                break
        self.X = np.array(screens[:self.num_frames]).reshape((1,) + self.input_shape)

    def predict(self, x):
        # replay, but with noise
        x = x.reshape(len(x), self.num_frames, 3, 40, 90)
        results = []
        for x_i in x:
            done, n_steps, _, final_state = self.deep_cp_wrapper.replay(x_i, max_steps=self.episode_len_to_success, init_state=self.init_state)
            success = int(not done and n_steps >= self.episode_len_to_success)
            results.append([1 - success, success])
        return np.array(results, dtype=np.float32)
