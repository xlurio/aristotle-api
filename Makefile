migrate:
	cd app/ && \
	../venv/bin/python manage.py makemigrations core && \
	../venv/bin/python manage.py migrate

run:
	cd app/ && \
	../venv/bin/python manage.py migrate && \
	../venv/bin/python manage.py runserver

setup:
	./venv/bin/pip install -r requirements.txt