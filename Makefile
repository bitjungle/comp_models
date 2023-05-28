MOD_NAME := comp_models

help:  ## 💬 This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

requirements:  ## 💿  Compile a requirements.txt file from template dependencies
	pip-compile -o requirements.txt setup.py

venv:   ## 🐍 Create a virtual environment
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -e .[dev]

test:  ## 🎯 Unit tests
	pytest -vv -s --cov=$(MOD_NAME) tests/

clean:  ## 🧹 Clean up project
	rm -rf .pytest_cache
	rm -rf tests/__pycache__
	rm -rf $(MOD_NAME)/__pycache__
	rm -rf .venv
