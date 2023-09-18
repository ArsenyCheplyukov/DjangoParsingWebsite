FROM python:3.11-alpine

# prevent from bytecode files (pyc)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# lint
RUN pip install --upgrade pip
RUN pip install flake8==6.0.0
# RUN flake8 --ignore=E501,F401 # don't run with it

WORKDIR /usr/src/search_crawl_teach/

# data
COPY . /usr/src/

# requisits installation
COPY requirements.txt ./
RUN pip install -r requirements.txt                   # --no-deps
# RUN pip wheel --no-cache-dir --wheel-dir /usr/src/wheels -r /usr/src/requirements.txt
