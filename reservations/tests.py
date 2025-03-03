from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now, timedelta
from reservations.models import Table, Reservation
from django.contrib.auth import get_user_model

User = get_user_model()


class ReservationsTestCase(TestCase):
    def setUp(self):
        """Создаём тестового пользователя и несколько столиков."""
        self.client = Client()
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.table1 = Table.objects.create(number=1, seats=4)
        self.table2 = Table.objects.create(number=2, seats=2)

        self.date = now().date() + timedelta(days=1)  # Завтрашний день
        self.start_time = (now() + timedelta(hours=1)).time()  # Через час
        self.end_time = (now() + timedelta(hours=3)).time()  # Через три часа

        # Бронирование
        self.reservation = Reservation.objects.create(
            user=self.user,
            date=self.date,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        self.reservation.tables.set([self.table1])

    def test_check_availability_view(self):
        """Проверка доступности страницы проверки столиков."""
        self.client.login(email="user@example.com", password="password")
        response = self.client.get(reverse("reservations:check_availability"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservations/check_availability.html")

    def test_table_availability_filter(self):
        """Проверка, что забронированные столики не показываются в списке доступных."""
        self.client.login(email="user@example.com", password="password")
        response = self.client.post(
            reverse("reservations:check_availability"),
            {
                "date": self.date,
                "start_time": self.start_time,
                "end_time": self.end_time,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Столик 1")  # Уже забронирован
        # self.assertContains(response, "Столик 2")  # Должен быть свободен

    def test_table_booking(self):
        """Проверка успешного бронирования столика."""
        self.client.login(email="user@example.com", password="password")
        response = self.client.post(
            reverse("reservations:table_booking"),
            {
                "date": self.date,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "tables": [self.table2.id],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservations/reservation_success.html")
        self.assertTrue(
            Reservation.objects.filter(user=self.user, tables=self.table2).exists()
        )

    def test_reservation_delete(self):
        """Удаление бронирования пользователем."""
        self.client.login(email="user@example.com", password="password")
        response = self.client.post(
            reverse("reservations:delete_reservation", args=[self.reservation.id])
        )

        self.assertRedirects(response, reverse("reservations:user_reservations"))
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

    def test_reservation_update(self):
        """Проверка обновления брони пользователем."""
        self.client.login(email="user@example.com", password="password")
        new_start_time = (now() + timedelta(hours=2)).time()

        response = self.client.post(
            reverse("reservations:edit_reservation", args=[self.reservation.id]),
            {
                "date": self.date,
                "start_time": new_start_time,
                "end_time": self.end_time,
                "tables": [self.table2.id],
            },
        )

        self.assertRedirects(response, reverse("reservations:user_reservations"))
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.start_time, new_start_time)
