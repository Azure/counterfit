# Hands-on Hacking of Reinforcement Learning Systems

## The instructions below should enable you to start attacking reinforcement learning systems using Counterfit. You will first need to install Counterfit using the [installation instructions](https://github.com/Azure/counterfit/blob/attackingRL/README.md). 

### OpenAI gym, which we are using for our reinforcement learning target, normally has some kind of visual pop-up window. This is fine for running locally, but if you are running this code on a server, you will want to run it headless.<br><br>

### To start counterfit normally:
1. `cd counterfit`
2. Activate your counterfit conda environment: `conda activate counterfit`
3. `export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` for Linux or `set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` for Windows (if not already added to your .bashrc) 
4. `sudo apt install python-opengl`
5. Start counterfit: `python counterfit.py`
<br><br>
### To start counterfit in headless mode:
1. Install xvfb (`sudo apt install xvfb`, or the appropriate installation method for your distro)
2. `sudo apt install python-opengl` or appropriate installation method for your distro.
3. `cd counterfit`
4. Activate your counterfit conda environment: `conda activate counterfit`
5. `export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` for Linux or `set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` for Windows (if not already added to your .bashrc) 
6. Start counterfit: `xvfb-run -a python counterfit.py`
<br><br>
### To run the attacks:
1. Load the ART attack framework `load art`
2. Pick your target. To run the initial state perturbation attack, use the cart_pole_initstate target: `interact cart_pole_initstate`. To run the Corrupted Replay Attack (CRA), use the cart_pole target `interact cart_pole`.
3. Select the attack: `use HopSkipJump`
4. For a test run, you can adjust some settings to make it run more quickly: `set --max_eval 100 --init_eval 10 --init_size 10` 
5. `run`
6. `save -r` to save results
7. `save -p` to save parameters

### To generate gifs and pngs of your attack:
1. Run `python -m counterfit.targets.cart_pole.generate_videos --init_attack_id <> --attack_id <>`.  To run this headless: `xvfb-run -a python -m counterfit.targets.cart_pole.generate_videos --init_attack_id <> attack_id <>`. Use the ID of the attack you just ran, with the flag `init_attack_id` if you used `cart_pole_initstate`. Otherwise, use `attack_id` if you used `cart_pole`.
<br><br>
