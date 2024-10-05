import logging
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contentapi.settings")


app = Celery("contentapi")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()