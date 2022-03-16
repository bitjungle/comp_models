"""Package configuration."""
from setuptools import setup, find_packages

with open('README.md', mode='r') as fh:
    long_description = fh.read()

setup(
    name='comp_models',
    description='Implementation of some models for compartmental models in epidemiology',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='bitjungle',
    version='0.1.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(include=['comp_models', 'comp_models.*']),
    install_requires=[
            'typing_extensions==4.1.1'
        ],
    extras_require={
        'dev': [
            'typing_extensions==4.1.1',
            'matplotlib==3.5.1',
            'numpy==1.22.3',
            'pylint==2.12.2',
            'pytest==7.1.0'
        ]
    }
)