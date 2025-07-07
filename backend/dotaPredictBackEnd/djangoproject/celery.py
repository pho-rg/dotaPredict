from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

app = Celery('matchapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks([])

app.conf.beat_schedule = {
    'updateMatchesScheduledTask-every-5-seconds': {
        'task': 'matchapp.tasks.updateMatchesScheduledTask',
        'schedule': timedelta(seconds=5),
    },
    'updateWinnerScheduledTask-every-30-minutes': {
        'task': 'matchapp.tasks.updateWinnerScheduledTask',
        'schedule': timedelta(minutes=5),
    },
}

app.conf.timezone = 'UTC'