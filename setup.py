import setuptools
import os
import sys

if sys.version_info[:2] < (3, 8):
    raise RuntimeError("Python version must be >=3.8.")

with open("./requirements.txt") as fd:
    required = fd.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()

extras = {}
extras["docs"] = [
    "recommonmark",
    "nbsphinx",
    "sphinx",
    "sphinx-autobuild",
    "sphinx-rtd-theme",
    "sphinx-markdown-tables",
    "sphinx-copybutton"
]

extras["augly"] = ["augly==0.1.10"]
extras["textattack"] = ["textattack[tensorflow]"]
extras["art"] = ["adversarial-robustness-toolbox==1.12.1"]
extras["dev"] = (
    extras["docs"] + extras["augly"] + extras["textattack"] + extras["art"]
)

setuptools.setup(
    name="counterfit",
    maintainer=[
        "Raja Sekhar Rao Dheekonda", 
        "Will Pearce", 
        "Hyrum Anderson",
        "Ram Shankar Siva Kumar",
        "Gary Lopez",
        "Shiven Chawla",
        "Amanda Minnich",
        "Sudipto Rakshit"
    ],
    version="1.1.0",
    author=[
        "Raja Sekhar Rao Dheekonda", 
        "Will Pearce", 
        "Hyrum Anderson",
        "Ram Shankar Siva Kumar",
        "Gary Lopez",
        "Shiven Chawla",
        "Amanda Minnich",
        "Sudipto Rakshit"
    ],
    description="Counterfit project to simulate attacks on ML systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Azure/counterfit",
    classifiers=[
        "Development Status :: development",
        "Intended Audience :: security/ML/research",
        "Programming Language :: Python :: 3.8+",
        "Operating System :: OS Independent",
    ],
    package_data={
        "": ["*.yml", "*"],
    },
    packages=setuptools.find_namespace_packages(
        exclude=[
            "build",
            "docs",
            "dist",
            "tests",
            "infrastructure",
            "examples"
        ]
    ),
    install_requires=required,
    python_requires=">=3.8",
    extras_require=extras,
    entry_points={
        "console_scripts": [
            "counterfit=examples.terminal.terminal:main"
        ],
    },
)