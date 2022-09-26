#! /bin/bash

./venv/bin/pip install flake8 isort black
./venv/bin/flake8 ./app
./venv/bin/isort ./app --check --diff
./venv/bin/black ./app --check