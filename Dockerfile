FROM python:3.9-slim

RUN apt-get update -y && \
    apt-get install --no-install-recommends -y -q \
    git libpq-dev python3-dev build-essential && \
    apt-get install -y vim nano lsof curl &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN pip install --upgrade pip && \
    pip install great_expectations && \
    pip install sqlalchemy==1.4.25 && \
    pip install sqlalchemy_bigquery && \
    pip install pybigquery && \
    pip install dbt-bigquery && \
    pip install apache-airflow[gcp] && \
    pip install airflow-dbt

RUN curl -sSL https://sdk.cloud.google.com | bash

ENV PATH $PATH:/root/google-cloud-sdk/bin

ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8
