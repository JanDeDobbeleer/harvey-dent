FROM python:alpine

WORKDIR /scheduler

ADD ./scheduler/ /scheduler/

RUN pip install -r requirements.txt

CMD python -u scheduler.py
