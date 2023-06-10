# syntax=docker/dockerfile:1
FROM python:latest
LABEL authors="jvict"

RUN ["mkdir", "app-mongo"]

WORKDIR /app-mongo

RUN ["mkdir", "output"]

# Copy the requirements that we will install with pip
COPY ../../requirements.txt requirements.txt
RUN ["pip3", "install", "-r", "requirements.txt"]

# Copying the folder of our project
COPY ../../mongo_client-descontinuado ./mongo

# Copying .env file
COPY ../../.env .

CMD python3 mongo/client.py