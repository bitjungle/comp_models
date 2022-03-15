# Installation

```shell
pip install git+https://github.com/bitjungle/comp_models.git
```

# Development installation

```shell
git clone https://github.com/bitjungle/comp_models.git
cd comp_models
python3 -m venv venv
source ./venv/bin/activate
pip install -e .
pip install -r requirements-dev.txt
```

Try running one of the examples, e.g:

```shell
python examples/covid-19_diamond_princess_SEIR.py
```

Run tests after code updates:

```shell
python -m pytest 
```
