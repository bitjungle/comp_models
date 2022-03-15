"""Package configuration."""
from setuptools import setup, find_packages

setup(
    name="comp_models",
    version="0.1.0",
    packages=find_packages(include=['comp_models', 'comp_models.*'])
)