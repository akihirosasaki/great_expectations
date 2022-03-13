FROM python:3.9-slim

# Update and install system packages
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y -q \
    git libpq-dev python3-dev build-essential && \
    apt-get install -y vim &&\
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install GE & PostgreSQL required package
RUN pip install --upgrade pip && \
    pip install great_expectations==0.13.38 && \
    pip install sqlalchemy psycopg2

RUN curl -sSL https://sdk.cloud.google.com | bash

ENV PATH $PATH:/root/google-cloud-sdk/bin

# Set environment variables
ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8

# Set WORKDIR and VOLUME
WORKDIR /usr/app
VOLUME /usr/app