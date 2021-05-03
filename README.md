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

* [Setup an Anaconda Python environment and install locally](#Option-2-Setup-an-Anaconda-Python-environment-and-install-locally)

For more information including alternative installation instructions, please visit our [wiki](https://github.com/Azure/counterfit/wiki).


### Setup an Anaconda Python environment and install locally

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
