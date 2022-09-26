#! /bin/bash

./venv/bin/pip install -r requirements.txt
clear
cd ./app
../venv/bin/python manage.py check --deploy