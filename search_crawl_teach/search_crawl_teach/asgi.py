"""
ASGI config for search_crawl_teach project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""


# AS FOR ME THE ONLY COMPATIBLE VERSIONS ARE DJANGO==4.0 AND CHANNELS==3.0.4


import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_crawl_teach.settings")

application = ProtocolTypeRouter({"http": get_asgi_application()})
