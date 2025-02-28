from django.urls import path
from .views import (
    TableAvailabilityView,
    TableBookingView,
    ReservationSuccessView, UserReservationsView, ReservationDeleteView, ReservationUpdateView, ArchivedReservationsView
)

app_name = "reservations"

urlpatterns = [
    path("check-availability/", TableAvailabilityView.as_view(), name="check_availability"),  # Страница выбора даты и времени
    path("book/", TableBookingView.as_view(), name="table_booking"),  # Бронирование столиков
    path("success/", ReservationSuccessView.as_view(), name="reservation_success"),  # Успешное бронирование
    path("my-reservations/", UserReservationsView.as_view(), name="user_reservations"),
    path("reservation/<int:pk>/delete/", ReservationDeleteView.as_view(), name="delete_reservation"),
    path("reservation/<int:pk>/edit/", ReservationUpdateView.as_view(), name="edit_reservation"),
    path("archived/", ArchivedReservationsView.as_view(), name="archived_reservations"),
]
