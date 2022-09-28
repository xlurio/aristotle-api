FROM python:latest
LABEL maintainer="Lucas Calegario"

COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /app