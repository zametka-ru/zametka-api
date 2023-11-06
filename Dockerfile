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
RUN pip install --upgrade pip
COPY . .

#########
# FINAL #
#########

# pull official base image
FROM python:3.10.8-slim

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/backend
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN pip install --upgrade pip

# copy project
COPY . $APP_HOME
RUN pip install -e .

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app