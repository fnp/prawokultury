from __future__ import absolute_import

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prawokultury.settings')

from celery import Celery
from django.conf import settings

app = Celery('prawokultury')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
