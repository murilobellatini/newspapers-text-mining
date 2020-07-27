FROM python:3.7

RUN mkdir /usr/src/backend

WORKDIR /usr/src/backend

COPY ./. /usr/src/backend

RUN pip install -r requirements.txt

EXPOSE 8000