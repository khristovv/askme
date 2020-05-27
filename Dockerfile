FROM python:3.7-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache zlib-dev jpeg jpeg-dev gcc

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .