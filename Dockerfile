FROM python:jessie

WORKDIR /harvey

ADD ./harvey/ /harvey/

RUN pip install -r requirements.txt

CMD python -u harvey.py
