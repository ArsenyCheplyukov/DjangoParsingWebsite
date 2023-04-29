FROM python:3.11-alpine

ENV PYTHONBUFFERED 1

ADD . /search_crawl_tech

WORKDIR /usr/src/search_crawl_teach

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .