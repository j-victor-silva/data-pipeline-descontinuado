# syntax=docker/dockerfile:1
FROM python:latest
LABEL authors="jvict"

WORKDIR /app

COPY ../../requirements.txt requirements.txt
RUN ["pip3", "install", "-r", "requirements.txt"]

COPY ../.. .

CMD ["python3", "mongo_client/client.py", "&&", "python3", "mysql/mysql_client.py"]