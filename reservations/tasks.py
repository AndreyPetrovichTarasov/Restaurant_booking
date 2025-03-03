from celery import shared_task
from django.core.management import call_command
import os


@shared_task
def archive_reservations_task():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # Убедимся, что Django загружен
    call_command("archive_reservations")
