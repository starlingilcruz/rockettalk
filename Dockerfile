FROM python:3.11

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

ADD ./ /app/

RUN pip install -r requirements.txt
