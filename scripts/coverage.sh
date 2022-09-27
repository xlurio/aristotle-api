#! /bin/bash

./venv/bin/pip install -r requirements.txt
./venv/bin/pip install coverage
cd app
coverage run --source='.' manage.py test
clear
coverage report
mv .coverage ..