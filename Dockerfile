FROM python:alpine

WORKDIR /scripts

ADD ./scripts/ /scripts/

RUN pip install -r requirements.txt

CMD python -u scheduler.py
