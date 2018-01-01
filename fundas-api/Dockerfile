FROM python:3.6.3-slim
MAINTAINER Udit Sharma <sharma.uditt@gmail.com>

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /fundas-api
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
#RUN pip install --editable .

CMD python run.py
