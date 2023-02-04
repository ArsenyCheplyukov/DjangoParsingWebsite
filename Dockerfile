FROM python:3.10.8

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./search_crawl_teach ./search_crawl_teach

CMD [ "python", "./search_crawl_teach/manage.py", "runserver", "0.0.0.0:8000"]