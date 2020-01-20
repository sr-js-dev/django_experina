FROM python:3.6.5

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN mkdir /app
ADD . /app/

WORKDIR /app

RUN apt-get update && apt-get upgrade -y -qq && \
  apt-get install -y -qq postgresql-client

RUN pip install --upgrade pip && \
  pip install -U pipenv && \
  pipenv install --system --deploy

EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080/health-check/ || exit 1
