# Counterfit
[About](#About) | [Getting Started](#Getting-Started) | [Learn More](#Learn-More) |  [Acknowledgments](#Acknowledgments) | [Contributing](#Contributing) | [Trademarks](#Trademarks) | [Contact Us](#Contact-Us)

```
---------------------------------------------------
Microsoft
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

## Getting Started
Choose one of these methods to get started quickly:
* [Option 1: Deploy via Azure Shell](#Option-1-Deploy-now-on-Azure-via-Azure-Shell) -- requires an Azure account (try it [free](https://azure.microsoft.com/en-us/free/))
* [Option 2: Setup an Anaconda Python environment and install locally](#Option-2-Setup-an-Anaconda-Python-environment-and-install-locally)

For more information including alternative installation instructions, please visit our [wiki](https://github.com/Azure/counterfit/wiki).

### Option 1: Deploy now on Azure via Azure Shell
To run Counterfit from your browser
1. Click the button below to initiate small resource deployment to your Azure account.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fcounterfit%2Fmaster%2Finfrastructure%2Fazuredeploy.json) 

2. In the configuration blade, specify your subscription and resource group.
3. In your [Azure Shell](https://shell.azure.com), type the following, replacing `RESOURCE_GROUP` with the name of the resource group selected in the previous step.
```
az container exec --resource-group RESOURCE_GROUP –name counterfit –exec-command '/bin/bash'
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
conda create --yes -n counterfit python=3.7
conda activate counterfit
pip install -r requirements.txt
```
4. Launch Counterfit.
```
python counterfit.py
```

## Learn More

Visit our [wiki](https://github.com/Azure/counterfit/wiki) for more detailed instructions on
* Basic Use
* Tutorials
* Key Concepts
* Assessment Guidance
* Extending Counterfit
* Advanced Use

## Acknowledgments

Counterfit leverages excellent open source projects, including, [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox) and [TextAttack](https://github.com/QData/TextAttack).

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
