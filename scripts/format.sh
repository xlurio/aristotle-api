#! /bin/bash

./venv/bin/pip install isort black
./venv/bin/isort ./app
./venv/bin/black ./app