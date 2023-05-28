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
    author_email='devel@bitjungle.com',
    url='https://github.com/bitjungle/comp_models',
    version='0.2.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(include=['comp_models', 'comp_models.*']),
    install_requires=[],
    extras_require={
        'dev': [
            'matplotlib',
            'numpy',
            'pip-tools',
            'pylint',
            'pytest',
            'pytest-cov'
        ]
    }
)