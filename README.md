# Counterfit

[![Tests](https://github.com/Azure/counterfit/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/Azure/counterfit/actions/workflows/tests.yaml)
[![License](http://img.shields.io/:license-mit-blue.svg)](https://github.com/Azure/counterfit/blob/main/LICENSE)

[About](#About) | [Getting Started](#Getting-Started) | [Acknowledgments](#Acknowledgments) | [Contributing](#Contributing) | [Trademarks](#Trademarks) | [Contact Us](#Contact-Us)

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
Counterfit is a generic automation layer for assessing the security of machine learning systems. It brings several existing adversarial frameworks under one tool, or allows users to create their own. 

### Requirements
- Ubuntu 18.04+
- Python 3.8
- Windows is supported by Counterfit, but not necessarily officially supported by each individual framework. 
- On Windows the [Visual C++ 2019 redistributable](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) is required

## Quick Start

### Installation with Python virtual environment
```bash
sudo apt install python3.8 python3.8-venv
python3 -m venv counterfit
git clone --depth 1 -b develop/1.1 https://github.com/Azure/counterfit.git
cd counterfit
pip install .[dev]
```

### Installation with Conda

```bash
conda create --yes -n counterfir python=3.8.0
conda activate counterfir
git clone --depth 1 -b develop/1.1 https://github.com/Azure/counterfit.git
cd counterfit
conda install --file requirements.txt
```


Notes: 
- Windows requires C++ build tools
- If textattack has been installed, it will initialize by downloading nltk data
## Acknowledgments
Counterfit leverages excellent open source projects, including,

- [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox)
- [TextAttack](https://github.com/QData/TextAttack)
- [Augly](https://github.com/facebookresearch/AugLy)

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
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

