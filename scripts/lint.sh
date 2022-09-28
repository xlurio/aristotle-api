#! /bin/bash

./venv/bin/pip install flake8 isort black
clear
./venv/bin/flake8 ./app
./venv/bin/isort . --check --diff
./venv/bin/black ./app --check