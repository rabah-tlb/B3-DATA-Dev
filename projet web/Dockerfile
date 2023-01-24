FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y default-mysql-client

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .
