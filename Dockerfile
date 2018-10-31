FROM python:3.6-alpine

# Add missing packages for Postgres bindings
# Disable caching to keep container small
# https://stackoverflow.com/a/42224405/148781
RUN apk --no-cache add gcc postgresql-dev python3-dev musl-dev

# Copy version specs first so they can be cached by Docker
COPY ./requirements* /install/
RUN pip install -r /install/requirements-develop.txt

# Declare application root for easier copying of files
WORKDIR /app

# Copy source code last so it can be mounted in Compose
COPY . .

# Using "-u" with python did not work, so set an environment variable
ENV PYTHONUNBUFFERED=0

RUN pip install -e .
