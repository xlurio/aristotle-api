FROM python:bullseye
LABEL maintainer="Lucas Calegario"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get -y install iputils-ping

COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /app