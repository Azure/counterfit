# Hands-on Hacking of Reinforcement Learning Systems

The instructions below should enable you to start attacking reinforcement learning systems using Counterfit. These instructions work on Linux.

OpenAI gym, which we are using for our reinforcement learning target, normally has some kind of visual pop-up window. This is fine for running locally, but if you are running this code on a server, you will want to run it headless.<br><br>

### Install counterfit:
1. Install Anaconda
1. Clone this repository and install Counterfit
    ```bash
    git clone https://github.com/Azure/counterfit.git
    cd counterfit
    conda create --yes -n counterfit python=3.8.8
    conda activate counterfit
    pip install .[dev]
    ```
1. If you get warning messages about protocol buffer, run the following commands to silence the warnings:
   1. On Windows box: `set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`
   1. On Linux box: `export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`

### Start counterfit normally:
1. Activate your counterfit conda environment: `conda activate counterfit`
1. Start counterfit command line interface, running `counterfit`

### Start counterfit in headless mode:
1. Install xvfb (`sudo apt install xvfb`, or the appropriate installation method for your distro)
1. Install OpenGL`sudo apt install python-opengl` or appropriate installation method for your distro.
1. Activate your counterfit conda environment: `conda activate counterfit`
1. Start counterfit: `xvfb-run -a counterfit`

### To run the attacks:
1. Pick your target.
   1. To run the initial state perturbation attack, use the cart_pole_initstate target: `set_target cart_pole_initstate`.
   1. To run the Corrupted Replay Attack (CRA), use the cart_pole target `set_target cart_pole`.
1. Select the attack: `set_attack hop_skip_jump`
1. For a test run, you can adjust some settings to make it run more quickly: `set_params --max_eval 100 --init_eval 10 --init_size 10` 
1. Run the attack: `run`
1. Save the results: `save -r`.
1. Save the parameters: `save -p`.

### To generate gifs and pngs of your attack:

1. To run with the GUI for the cart pole showing:
   ```bash
   python -m counterfit.targets.cart_pole.generate_videos \
       # set the init_attack_id to the ID from the cart_pole_initstate 
       --init_attack_id <PREV_ATTACK_ID> \
       # else set the attack_id to the ID from the cart_pole
       --attack_id <PREV_ATTACK_ID>
   ```
2. To run in headless mode:
   ```bash
   xvfb-run -a python -m counterfit.targets.cart_pole.generate_videos \
       # set the init_attack_id to the ID from the cart_pole_initstate 
       --init_attack_id <PREV_ATTACK_ID> \
       # else set the attack_id to the ID from the cart_pole
       --attack_id <PREV_ATTACK_ID>
   ```
3.    Use the ID of the attack you just ran, with the flag `init_attack_id` if you used `cart_pole_initstate`. Otherwise, use `attack_id` if you used `cart_pole`.

[[Demo Home]](./README.MD)