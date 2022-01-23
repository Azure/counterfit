# Counterfit
Counterfit is a generic automation layer for assessing the security of machine learning systems. Built on the Python cmd2 library, Counterfit provides a terminal interface to launch and manage attacks against ML models. Counterfit wraps excellent open source projects, including, [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox), [TextAttack](https://github.com/QData/TextAttack), and [Augly](https://github.com/facebookresearch/AugLy).

# Installation
## Docker -- JupyterLab
1. Install Docker
2. Pull and execute Counterfit-Jupyterlab as follows
    ```
   docker pull azuretrustworthyml/counterfit-jupyterlab:latest
   docker run -p8888:8888 azuretrustworthyml/counterfit-jupyterlab:latest
   ```
3. Navigate your browser to the URL specified that includes a token, e.g., `http://127.0.0.1:8888/lab?token=<token>`

## Docker -- Terminal Only
1. Install Docker Desktop
2. Pull and execute Counterfit as follows
   ```
   docker run -it azuretrustworthyml/counterfit:latest python counterfit.py
   ```
## Anaconda Python Environment
1. Install [Anaconda Python](https://www.anaconda.com/products/individual) and [git](https://git-scm.com/downloads).
2. Clone the repository.
   ```
   git clone https://github.com/Azure/counterfit.git
   ```
3. Open an Anaconda shell and create a virtual environment and install dependencies.
  ```
  cd counterfit
  conda create --yes -n counterfit python=3.7
  conda activate counterfit
  pip install -r requirements.txt
  ```
4. Launch Counterfit
    ```
    python counterfit.py
    ```

## Python Virtual Environment
1. Clone this repository.
  ```
  git clone https://github.com/Azure/counterfit.git
  ```
2. Create a virtual environment.
  ```
  python -m venv counterfit
  ```
3. Activate virtual environment
  - On Windows:
    ```
    counterfit-venv\scripts\activate.bat
    ```
  - On Linux:
    ```
    source counterfit-venv/bin/activate
    ```
4. Install requirements
  ```
  pip install -r requirements.txt
  ```
5. Launch Counterfit
  ```
  python counterfit.py
  ```

# What's New?
First and foremost, the ATML team would like the thank everyone for their support over the last few months. Counterfit recieved a very warm welcome from the community. What started as some simple red team tooling has become a place for collaboration, experiementatation, and of course security assessments. While verson 0.1 was useful, unless a user was familiar with the code, it was admitedly difficult to use beyond it's basic functionality. Users of Counterfit should know that their frustrations with the tool were also our frustrations. While our internal version may have different targets, custom algos, reporting, the public version of Counterfit is ultimately the base of our internal version. For those unfamiliar with infosec, this is a common practice that creates a shared experience. These shared experiences will allow us to communicate and come to a common understanding of risk in the ML space. 

Let's checkout the new digs. We will cover the changes at a high-level and get into details later,

- Frameworks are a first-class concept.
- New logging capabilities
- Options structure
- New attacks from art, textattack
- New attacks via Augly
- Various command functionality
- Running via run_pyscript
- New reporting structure
- Python Rich integration
- Test and Docs

## Frameworks are a first-class concept
Frameworks are the drivers behind Counterfit and they provide the functionality for Counterfit. Counterfit now takes a back seat and offloads the majority of work to the framework responsible for an attack. Frameworks are not loaded on start, rather by using the `load` command Like other objects in Counterfit, frameworks are built around their folder structure within the project. Each framework has its own folder under `counterfit/frameworks`.In order to be loaded by Counterfit, a framework should inherit from `counterfit.core.frameworks.Framework`. A framework should also define a number of core functions. These include `load()`, `build()`, `run()`, `check_success()`, `pre_attack_proccessing()`, `post_attack_processing()`. Everything begins and ends with a framework and so in order to add a new framework it is important to be familiar with some Counterfit internals.

### `load()`: 
During load, a framework should load the attacks classes it is responsible for. There are many ways to do this, and some frameworks can be extremely complicated and heavy to load (`art`), or be really lightweight and custom (`augly`). Counterfit also provides the option to load a framework from a json config file.

To load from an attack, use `add_attack` with the required parameters. This function creates a namedtuple that Counterfit references to populate the interface and build attacks. A namedtuple was chosen because of it immutable properties, this allows Counterfit to keep the interface nice and tidy without a user being able to overwrite or create various properties during run time.

```python
# The attack class to add
new_attack = module.AttackClass

# Add the attack to the framework
self.add_attack(
    attack_name=new_attack.__name__,
    attack_type=attack_type.__name__,
    attack_category=attack_category,
    attack_data_tags=attack_data_tags,
    attack_class=loaded_attack,
    attack_default_params=default_params)
```

### `build()`:
Build is called by `state.build_new_attack()` and should return an instantiated attack ready to be configured and run. Build takes the namedtuple object created during load. It pulls the attack out of attack_class and should return an instantiated attack. For any given framework, this build step is usually found in the examples section. After building the attack, Counterfit creates a `CFAttack` object that is used for the remainder of the attack life-cycle. Unlike the namedtuple, `CFAttack` is a standard class and can be altered as needed or required by the framework.

```python

attack_entry.attack_class.build()
```

### `run()`:
Run is called by `state.run_attack()` and takes a `CFAttack` object as a parameter. This is where the framework can execute the attack and return the results. `CFAttack` is an aggregation and carries a large amount of information with it, for example `cfattack.target` provoide ccess to the target instance, `cfattack.options` provides access attack options, `cfattack.logger`provided access to the logger instance. 

### `check_success()`
check_success is called by `state.run_attack()` and should return a bool value denoting the success of the attack. 

### `post_attack_processing()`
Counterfit comes with some basic reporting functionality. If there are custom reports or attacks or datatypes Counterfit does not support. This can be overridden to create these reports. 

## Python Rich integration
Thanks to Python Rich, Counterfit has a lot more colors and is generally better looking. Rich requires that everything is string or a "renderable". Be aware of this when using the `logging` module. 

## Options structure
During `framework.load()` a framework author has the opportunity to set options for an attack via `attack_default_params`. Counterfit uses these to populate the `set` command arguments. Every attack will reflect its own unique options that can be changed with the `set` command, it will also loosely enforce some typing on the arguments. It is advised to handle any options issues in the framework rather than in `set`.

## Logging structure
Counterfit injects its own options into the options structure. Options related to logging being `enable_logging` and `logger`. Technically logging is always enabled, and only collects the number of queries sent. To set a logger other than the default logger, use `set --logger json`. 

## New attacks from art, textattack
Because frameworks are first class concept, Counterfit no longer wraps attacks, rather it depends on the framework code to handle the majority of the attack life-cycle. This means that Counterfit can support the full menu of attacks that the orginial frameworks provided. For example, where Counterfit v0.1 only supported blackbox evasion attacks from the Adversarial Robustness Toolbox, Counterfit v1.0 supports MIFace (blackbox-inversion), KnockOffNets(blackbox-extraction), CariliniWagner(whitebox-evasion), and several others out of the box.

## New attacks via Augly
Augly is a powerful data augmentation framework built by Facebook. While not explicilty "adversarial", Counterfit uses Augly to include a new bug class for testing - CommonCorruption. In terms of implementation, Augly is a good example of how to both use a "config" only load and wrap a class to create a custom attack.

## Various command functionality
Most commands remain the same in functionality, however some arguments may have changed. 

- set: Arguments are part of argparse
- show attacks: Access historical attacks
- reload: frameworks, targets, and commands
- exit: target, attack, or counterfit. 

## New reporting structure
Counterfit comes with some basic reporting functionality, but if there are attacks or datatypes Counterfit does not support for reporting, a user can override them in the framework via `post_attack_processing()`.

## Running Counterfit via run_pyscript
The core code and the terminal commands have been decoupled. It is possible to use th

## Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks
This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

## Contact Us
For comments or questions about how to leverage Counterfit, please contact <counterfithelpline@microsoft.com>. 