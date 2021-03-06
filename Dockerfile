FROM python:3.9.0-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tzdata \
    && \
    rm -rf /var/lib/apt/lists/*

ARG POETRY_HTTP_BASIC_OLIST_USERNAME
ARG POETRY_HTTP_BASIC_OLIST_PASSWORD
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt