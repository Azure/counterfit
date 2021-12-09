import setuptools
import os
import sys

if sys.version_info[:2] < (3, 7):
    raise RuntimeError("Python version must be >=3.7.")

with open("./requirements.txt") as f:
    required = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="counterfit",
    maintainer="Counterfit Developers",
    version="1.0.0",
    author="ATML",
    description="Counterfit project to simulate attacks on ML systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Azure/counterfit",
    classifiers=[
        "Development Status :: development",
        "Intended Audience :: Security/ML/Research",
        "Programming Language :: Python :: 3.7+",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=required,
    python_requires=">=3.7",
)
