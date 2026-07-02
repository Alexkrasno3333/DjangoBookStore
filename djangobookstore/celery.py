import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangobookstore.settings")

app = Celery("djangobookstore")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
