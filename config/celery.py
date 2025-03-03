from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Если используешь django-celery-beat, укажи DatabaseScheduler
app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"

# Если используешь PersistentScheduler, можешь оставить этот вариант
# app.conf.beat_scheduler = "celery.beat.schedulers.PersistentScheduler"

"""
Загрузить настройки из Django settings
"""
app.config_from_object("django.conf:settings", namespace="CELERY")

"""
Автоматически загружать задачи из приложений
"""
app.autodiscover_tasks()

# Периодическая задача
app.conf.beat_schedule = {
    "archive-reservations-every-hour": {
        "task": "reservations.tasks.archive_reservations_task",
        "schedule": crontab(minute=0, hour="*"),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
