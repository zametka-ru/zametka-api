###########
# BUILDER #
###########

# pull official base image
FROM python:3.10.8-slim-buster as builder

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
COPY . .

#########
# FINAL #
#########

# pull official base image
FROM python:3.10.8-slim

RUN mkdir -p /home/app/

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/backend
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -e .

