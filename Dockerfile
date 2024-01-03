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

# create the appropriate directories
ENV APP_HOME=/home/app/backend
WORKDIR $APP_HOME

RUN mkdir ./src
COPY ./pyproject.toml $APP_HOME

# install dependencies
RUN pip install --upgrade pip
RUN pip install -e .

#########
# FINAL #
#########

# pull official base image
FROM builder as production

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/backend
WORKDIR $APP_HOME

COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

