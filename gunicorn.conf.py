import os
import sys

django_directory = os.path.abspath("./app")
sys.path.append(django_directory)

wsgi_app = "app.wsgi:application"
reload = True
