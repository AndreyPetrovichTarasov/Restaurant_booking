from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Столик {self.number} ({self.seats} мест)"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tables = models.ManyToManyField(Table)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Бронь {self.user.email} {self.date} {self.start_time}-{self.end_time}"

    @staticmethod
    def get_reserved_tables(date, time):
        """Возвращает список уже забронированных столиков на указанное время"""
        reservations = Reservation.objects.filter(date=date, time=time)
        reserved_tables = set()
        for res in reservations:
            reserved_tables.update(res.tables.all())
        return reserved_tables


class ArchivedReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    tables = models.ManyToManyField(Table)
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Архивная бронь {self.id} - {self.user} ({self.date} {self.start_time}-{self.end_time})"
