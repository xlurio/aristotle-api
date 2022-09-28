#! /bin/bash

./venv/bin/pip install autoflake black isort
clear
./venv/bin/autoflake ./app --remove-all-unused-imports --recursive --remove-unused-variables --in-place --exclude=__init__.py
./venv/bin/black ./app
./venv/bin/isort .