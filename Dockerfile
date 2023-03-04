FROM python:3

ENV PYTHONBUFFERED 1

ADD . /app

WORKDIR /app/search_crawl_teach

COPY ./requirements.txt /app/search_crawl_teach/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app