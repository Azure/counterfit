# adapted from https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
import tensorflow as tf

import gym

import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
from PIL import Image
import pickle
import inspect
import os
import pathlib

BATCH_SIZE = 128
GAMMA = 0.999
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200
TARGET_UPDATE = 10
device = torch.device('cpu') # torch.device("cuda" if torch.cuda.is_available() else "cpu")
global Transition 
Transition = namedtuple('Transition', 
                             ('state', 'action', 'next_state', 'reward'))
resize = T.Compose([T.ToPILImage(),
            T.Resize(40, interpolation=Image.CUBIC),
            T.ToTensor()])


class ReplayMemory(object):
    
    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)
        
    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
        
    def __init__(self, h, w, outputs):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=5, stride=2)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, stride=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
        self.bn3 = nn.BatchNorm2d(32)

        # Number of Linear input connections depends on output of conv2d layers
        # and therefore the input image size, so compute it.
        def conv2d_size_out(size, kernel_size = 5, stride = 2):
            return (size - (kernel_size - 1) - 1) // stride  + 1
        convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(w)))
        convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(h)))
        linear_input_size = convw * convh * 32
        self.head = nn.Linear(linear_input_size, outputs)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = x.to(device)
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        return self.head(x.view(x.size(0), -1))
            
class DeepCPWrapper:
    def __init__(self, memory=None, policy_net=None):
        self.env = gym.make('CartPole-v0').unwrapped
        self.episode_durations = []
        # Get number of actions from gym action space
        self.n_actions = self.env.action_space.n 
        if memory:
            self.memory = memory
        else:
            self.memory = ReplayMemory(10000)
        self.steps_done = 0
        self.initialize_models(policy_net)
    
    def initialize_models(self, policy_net):
        self.env.reset()
        # Get screen size so that we can initialize layers correctly based on shape
        # returned from AI gym. Typical dimensions at this point are close to 3x40x90
        # which is the result of a clamped and down-scaled render buffer in get_screen()
        init_screen = self.get_screen()
        _, _, screen_height, screen_width = init_screen.shape
        if policy_net:
            self.policy_net = policy_net
        else:
            self.policy_net = DQN(screen_height, screen_width, self.n_actions).to(device)
        self.target_net = DQN(screen_height, screen_width, self.n_actions).to(device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.RMSprop(self.policy_net.parameters())

    def get_cart_location(self, screen_width):
        world_width = self.env.x_threshold * 2
        scale = screen_width / world_width
        return int(self.env.state[0] * scale + screen_width / 2.0)  # MIDDLE OF CART

    def get_screen(self):
        # Returned screen requested by gym is 400x600x3, but is sometimes larger
        # such as 800x1200x3. Transpose it into torch order (CHW).
        screen = self.env.render(mode='rgb_array').transpose((2, 0, 1))
        # Cart is in the lower half, so strip off the top and bottom of the screen
        _, screen_height, screen_width = screen.shape
        screen = screen[:, int(screen_height*0.4):int(screen_height * 0.8)]
        view_width = int(screen_width * 0.6)
        cart_location = self.get_cart_location(screen_width)
        if cart_location < view_width // 2:
            slice_range = slice(view_width)
        elif cart_location > (screen_width - view_width // 2):
            slice_range = slice(-view_width, None)
        else:
            slice_range = slice(cart_location - view_width // 2,
                                cart_location + view_width // 2)
        # Strip off the edges, so that we have a square image centered on a cart
        screen = screen[:, :, slice_range]
        # Convert to float, rescale, convert to torch tensor
        # (this doesn't require a copy)
        screen = np.ascontiguousarray(screen, dtype=np.float32) / 255
        screen = torch.from_numpy(screen)
        # Resize, and add a batch dimension (BCHW)
        return resize(screen).unsqueeze(0)

    def select_action(self, state):
        sample = random.random()
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * self.steps_done / EPS_DECAY)
        self.steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                # t.max(1) will return largest column value of each row.
                # second column on max result is index of where max element was
                # found, so we pick action with the larger expected reward.
                return self.policy_net(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(self.n_actions)]], device=device, dtype=torch.long)

    def select_action_inference(self, state):
        self.steps_done += 1
        return self.policy_net(state).max(1)[1].view(1, 1)

    def plot_durations(self):
        plt.figure(2)
        plt.clf()
        durations_t = torch.tensor(self.episode_durations, dtype=torch.float)
        plt.title('Training...')
        plt.xlabel('Episode')
        plt.ylabel('Duration')
        plt.plot(durations_t.numpy())
        # Take 100 episode averages and plot them too
        if len(durations_t) >= 100:
            means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
            means = torch.cat((torch.zeros(99), means))
            plt.plot(means.numpy())

    def optimize_model(self):
        if len(self.memory) < BATCH_SIZE:
            return
        transitions = self.memory.sample(BATCH_SIZE)
        # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
        # detailed explanation). This converts batch-array of Transitions
        # to Transition of batch-arrays.
        batch = Transition(*zip(*transitions))

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                            batch.next_state)), device=device, dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state
                                                    if s is not None])
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1)[0].
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(BATCH_SIZE, device=device)
        next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * GAMMA) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def replay(self, frames, max_steps=100, init_state=None, return_actual_frames=False):
        # Initialize the environment and state
        if init_state is None:
            init_state = self.env.reset()
        else:
            self.env.state = np.array(init_state, dtype=np.float32)
            self.env.steps_beyond_done = None

        if return_actual_frames:
            last_screen = self.get_screen()
            current_screen = self.get_screen()           
            actual_frames = [last_screen.detach().numpy(), current_screen.detach().numpy()]

        # from IPython.core.debugger import set_trace; set_trace()
        # from IPython import embed; embed()

        final_done = False

        for t in range(len(frames)-1):
            # convert from numpy array to tensor
            frame_diff = (frames[t+1]-frames[t]).reshape((1, 3, 40, 90))
            frame_diff = torch.tensor(frame_diff, dtype=torch.float32)

            # Select and perform an action
            action = self.select_action_inference(frame_diff)
            _, reward, done, _ = self.env.step(action.item())
            reward = torch.tensor([reward], device=device)

            if return_actual_frames:
                current_screen = self.get_screen()
                actual_frames.append(current_screen.detach().numpy())

            if done or t> max_steps:
                final_done = True
                final_steps = t+1
                # if "done" before memory reaches max_steps, it's a failure
                # if we every reach max_steps, it's a success
                print(f"final state after {t+1} steps is {self.env.state}") 
                if not return_actual_frames:
                    break

        if return_actual_frames:
            return final_done, t+1, init_state, self.env.state, actual_frames
        else:
            return final_done, t+1, init_state, self.env.state

    
    def play(self, max_steps=100, init_state=None, play_to_end=False):
        memory = ReplayMemory(max_steps+1)
        # Initialize the environment and state
        if init_state is None:
            init_state = self.env.reset()
        else:
            self.env.state = np.array(init_state, dtype=np.float32)
            self.env.steps_beyond_done = None
        last_screen = self.get_screen()
        current_screen = self.get_screen()
        frame_diff = current_screen - last_screen
        
        frames = [last_screen.detach().numpy(), current_screen.detach().numpy()]

        for t in count():
            # get frame difference
            frame_diff = torch.tensor((frames[t+1]-frames[t]).reshape((1, 3, 40, 90)), dtype=torch.float32)

            # Select and perform an action
            action = self.select_action_inference(frame_diff)
            _, reward, done, _ = self.env.step(action.item())
            reward = torch.tensor([reward], device=device)

            if not done or play_to_end:
                # New observation (difference of frames)
                current_screen = self.get_screen()

                # Store memory
                frames.append(current_screen.detach().numpy())
                next_frame_diff = torch.tensor((frames[t+2]-frames[t+1]).reshape((1, 3, 40, 90)))
                # Store the transition in memory
                memory.push(frame_diff.detach().numpy(), action, next_frame_diff.detach().numpy(), reward)
                

            if (play_to_end and len(memory) >= max_steps) or (not play_to_end and done):
                # if "done" before memory reaches max_steps, it's a failure
                # if we every reach max_steps, it's a success
                print(f"final state after {t+1} steps is {self.env.state}") 
                break

        self.env.render()
        self.env.close()
        plt.ioff()
        plt.show()

        return frames, memory, init_state

    def train(self, num_episodes):
        for i_episode in range(num_episodes):
            if i_episode % 10 == 0:
                print("Episode {}".format(i_episode))
            # Initialize the environment and state
            self.env.reset()
            last_screen = self.get_screen()
            current_screen = self.get_screen()
            state = current_screen - last_screen
            for t in count():
                # Select and perform an action
                action = self.select_action(state)
                _, reward, done, _ = self.env.step(action.item())
                reward = torch.tensor([reward], device=device)

                # Observe new state
                last_screen = current_screen
                current_screen = self.get_screen()
                if not done:
                    next_state = current_screen - last_screen
                else:
                    next_state = None

                # Store the transition in memory
                self.memory.push(state.detach().numpy(), action, next_state.detach().numpy(), reward)

                # Move to the next state
                state = next_state

                # Perform one step of the optimization (on the policy network)
                self.optimize_model()
                if done:
                    self.episode_durations.append(t + 1)
                    #plot_durations()
                    break
            # Update the target network, copying all weights and biases in DQN
            if i_episode % TARGET_UPDATE == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())
        print('Training complete')
        self.env.render()
        self.env.close()
        plt.ioff()
        plt.show()
        # detach tensors and convert to CPU
        basedir = pathlib.Path(os.path.abspath(
            inspect.getfile(self.__class__))).parent.resolve()
        torch.save(self.policy_net, 
                   os.path.join(basedir, 
                                f"cartpole_dqn_{num_episodes}.pt"))

def main():
    dcpw = DeepCPWrapper()
    dcpw.train()

if __name__ == "__main__":
    main()
