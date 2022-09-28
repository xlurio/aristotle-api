#! /bin/bash

./venv/bin/pip install -r requirements.txt
cd ./app
clear
../venv/bin/python manage.py startapp $1