FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=dev
ENV DOCKER_CONTAINER=1

RUN apt-get update && \
         apt-get install -y --no-install-recommends \
         gcc \
         curl \
         libpq-dev \
         && rm -rf /var/lib/apt/lists/*


RUN mkdir /app
WORKDIR /app


EXPOSE 8000


COPY requirements.txt .


RUN pip install -U pip && pip install -r requirements.txt


COPY . .