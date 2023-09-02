FROM python:3.11

RUN mkdir /lumen

WORKDIR /lumen

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
