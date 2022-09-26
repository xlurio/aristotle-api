#! /bin/bash

./venv/bin/pip install -r requirements.txt
cd ./app && \
../venv/bin/python manage.py migrate && \
clear && \
../venv/bin/python manage.py test