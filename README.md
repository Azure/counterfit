# Counterfit
[About](#About) | [Getting Started](#Getting-Started) |  [Acknowledgments](#Acknowledgments) | [Contributing](#Contributing) | [Trademarks](#Trademarks) | [Contact Us](#Contact-Us)

```
                          __            _____ __
  _________  __  ______  / /____  _____/ __(_) /_
 / ___/ __ \/ / / / __ \/ __/ _ \/ ___/ /_/ / __/
/ /__/ /_/ / /_/ / / / / /_/  __/ /  / __/ / /
\___/\____/\__,_/_/ /_/\__/\___/_/  /_/ /_/\__/

                                        #ATML

---------------------------------------------------
```

## About
Counterfit is a command-line tool and generic automation layer for assessing the security of machine learning systems.

### Requirements
- Python 3.7 or 3.8
- On Windows the [Visual C++ 2019 redistributable](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) is required

## Getting Started
Choose one of these methods to get started quickly:
* [Option 1: Deploy via Azure Shell](#Option-1-Deploy-now-on-Azure-via-Azure-Shell)
* [Option 2: Setup an Anaconda Python environment and install locally](#Option-2-Setup-an-Anaconda-Python-environment-and-install-locally)

For more information including alternative installation instructions, please visit our [wiki](https://github.com/Azure/counterfit/wiki).

### Option 1: Deploy via Azure Shell
To run Counterfit from your browser
1. Click the button below to initiate small resource deployment to your Azure account.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fcounterfit%2Fmaster%2Finfrastructure%2Fazuredeploy.json) 

2. In the configuration blade, specify your subscription and resource group.
3. In your [Azure Shell](https://shell.azure.com), type the following, replacing `RESOURCE_GROUP` with the name of the resource group selected in the previous step.
```
az container exec --resource-group RESOURCE_GROUP --name counterfit --exec-command '/bin/bash'
```
4. Within the container, launch Counterfit.
```
python counterfit.py
```

### Option 2: Setup an Anaconda Python environment and install locally

1. Install [Anaconda Python](https://www.anaconda.com/products/individual) and [git](https://git-scm.com/downloads).
2. Clone this repository.
```
git clone https://github.com/Azure/counterfit.git
```
3. Open an Anaconda shell and create a virtual environment and dependencies.
```
cd counterfit
conda create --yes -n counterfit python=3.8.8
conda activate counterfit
pip install -r requirements.txt
```
4. Launch Counterfit.
```
python counterfit.py
```

## Acknowledgments

Counterfit leverages excellent open source projects, including, [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox), [TextAttack](https://github.com/QData/TextAttack), and [Augly](https://github.com/facebookresearch/AugLy)

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
# Version 1.0
First and foremose, the ATML team would like the thank everyone for their support over the last few months. Counterfit recieved a very warm welcome from the community. What started as some simple red team tooling has become a place for collaboration, experiementatation, and of course security assessments. While verson 0.1 was useful, unless a user was familiar with the code, it was admitedly difficult to use beyond it's basic functionality. Users of Counterfit should know that their frustrations with the tool were also our frustrations. While our internal version may have different targets, custom algos, reporting, the public version of Counterfit is ultimately the base of our internal version. For those unfamiliar with infosec, this is a common practice that creates a shared experience. These shared experiences will allow us to communicate and come to a common understanding of risk in the ML space. 

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
- docs and tests

# Frameworks are a first-class concept
Frameworks are the drivers behind Counterfit and they provide the functionality for Counterfit. Counterfit now takes a back seat and offloads the majority of work to the framework responsible for an attack. Frameworks are not loaded on start, rather by using the `load` command Like other objects in Counterfit, frameworks are built around their folder structure within the project. Each framework has its own folder under `counterfit/frameworks`.In order to be loaded by Counterfit, a framework should inherit from `counterfit.core.frameworks.Framework`. A framework should also define a number of core functions. These include `load()`, `build()`, `run()`, `check_success()`, `pre_attack_proccessing()`, `post_attack_processing()`. Everything begins and ends with a framework and so in order to add a new framework it is important to be familiar with some Counterfit internals.

# Python Rich integration
Thanks to Python Rich, Counterfit has a lot more colors and is generally better looking. Rich requires that everything is string or a "renderable". Be aware of this when using the `logging` module. 

## Options structure
During `framework.load()` a framework author has the opportunity to set options for an attack via `attack_default_params`. Counterfit uses these to populate the `set` command arguments. Every attack will reflect its own unique options that can be changed with the `set` command, it will also loosely enforce some typing on the arguments. It is advised to handle any options issues in the framework rather than in `set`.

## Logging structure
Counterfit injects its own options into the options structure. Options related to logging being `enable_logging` and `logger`. Technically logging is always enabled, and only collects the number of queries sent. To set a logger other than the default logger, use `set --logger json`. 

## New attacks from art, textattack
Because frameworks are first class concept, Counterfit no longer wraps attacks, rather it depends on the framework code to handle the majority of the attack life-cycle. This means that Counterfit can support the full menu of attacks that the orginial frameworks provided. For example, where Counterfit v0.1 only supported blackbox evasion attacks from the Adversarial Robustness Toolbox, Counterfit v1.0 supports MIFace (blackbox-inversion), KnockOffNets(blackbox-extraction), CariliniWagner(whitebox-evasion), and several others out of the box.

## New attacks via Augly
Augly is a powerful data augmentation framework built by Facebook. While not explicilty "adversarial", Counterfit uses Augly to include a new bug class for testing - common corruptions. In terms of implementation, Augly is a good example of how to both use a "config" only load and wrap a class to create a custom attack.

## Various command functionality
Most commands remain the same in functionality, however some arguments may have changed. 

- set: Arguments are part of argparse
- show attacks: Access historical attacks
- reload: frameworks, targets, and commands
- exit: target, attack, or counterfit. 

## New reporting structure
Counterfit comes with some basic reporting functionality, but if there are attacks or datatypes Counterfit does not support for reporting, a user can override them in the framework via `post_attack_processing()`.

## Running Counterfit via run_pyscript
The core code and the terminal commands have been decoupled. It is possible to use the cmd2 `run_pyscript` to automate scans. 

## Docs and Tests
Tests are implement via Pyest and make docs with `counterfit\docs\make html`. Use the `docs` command to start a local server for browsing.
