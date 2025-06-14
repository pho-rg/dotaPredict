from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

app = Celery('matchapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks([])

app.conf.beat_schedule = {
    'matchAppScheduledTask-every-5-seconds': {
        'task': 'matchapp.tasks.matchAppScheduledTask',
        'schedule': timedelta(minutes=1),
    },
}

app.conf.timezone = 'UTC'