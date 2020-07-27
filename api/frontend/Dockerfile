FROM python:3.7

RUN mkdir /usr/src/frontend

WORKDIR /usr/src/frontend

COPY ./. /usr/src/frontend

RUN pip install -r requirements.txt

EXPOSE 80