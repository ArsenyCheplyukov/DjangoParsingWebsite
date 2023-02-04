import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_crawl_teach.settings")
app = Celery("search_crawl_teach")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
