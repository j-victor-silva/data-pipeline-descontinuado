# syntax=docker/dockerfile:1
FROM python:latest
LABEL authors="jvict"

WORKDIR /app

COPY ../../.fake-data/requirements.txt requirements.txt
RUN ["pip3", "install", "-r", "requirements.txt"]

COPY ../../.fake-data .

RUN ["python3", "main.py"]