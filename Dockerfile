FROM python:latest
LABEL maintainer="Lucas Calegario"

COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app
COPY ./scripts/runserver.sh /scripts/runserver.sh
WORKDIR /app

EXPOSE 8000

ENTRYPOINT [ "bash", "/scripts/runserver.sh" ]