from celery import shared_task
from django.core.management import call_command

@shared_task
def archive_reservations_task():
    call_command("archive_reservations")
