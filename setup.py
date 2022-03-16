"""Package configuration."""
from setuptools import setup, find_packages

setup(
    name='comp_models',
    description='Implementation of some models for compartmental models in epidemiology',
    version='0.1.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(include=['comp_models', 'comp_models.*'])
)