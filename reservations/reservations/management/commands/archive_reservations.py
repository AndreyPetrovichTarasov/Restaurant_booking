from django.core.management.base import BaseCommand
from django.utils.timezone import now
from reservations.models import Reservation, ArchivedReservation


class Command(BaseCommand):
    help = "Перемещает завершенные брони в архив"

    def handle(self, *args, **kwargs):
        current_datetime = now()
        expired_reservations = Reservation.objects.filter(
            date__lt=current_datetime.date()
        ) | Reservation.objects.filter(
            date=current_datetime.date(), end_time__lt=current_datetime.time()
        )

        for reservation in expired_reservations:
            archived_reservation = ArchivedReservation.objects.create(
                user=reservation.user,
                date=reservation.date,
                start_time=reservation.start_time,
                end_time=reservation.end_time
            )
            archived_reservation.tables.set(reservation.tables.all())

            reservation.delete()

        self.stdout.write(self.style.SUCCESS("Завершенные брони перемещены в архив."))
