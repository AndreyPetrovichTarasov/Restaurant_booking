from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView
from dateutil.parser import parse

from .forms import CheckAvailabilityForm, ReservationForm
from .models import Table, Reservation, ArchivedReservation


class TableAvailabilityView(LoginRequiredMixin, View):
    """Представление просмотра доступных столиков."""
    template_name = "reservations/check_availability.html"

    def get(self, request):
        form = CheckAvailabilityForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CheckAvailabilityForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]

            # Находим занятые столики
            reserved_tables = Reservation.objects.filter(
                Q(start_time__lt=end_time) & Q(end_time__gt=start_time),
                date=date,  # Фильтр по дате должен быть отдельным аргументом
            ).values_list("tables", flat=True)

            print(f"Занятые столики: {list(reserved_tables)}")

            # Если броней вообще нет — возвращаем все столики
            if not reserved_tables:
                available_tables = Table.objects.all()
            else:
                available_tables = Table.objects.exclude(id__in=reserved_tables)

            print(f"Свободные столики: {list(available_tables)}")

            return render(
                request,
                "reservations/table_list.html",
                {
                    "tables": available_tables,
                    "date": date,
                    "start_time": start_time,
                    "end_time": end_time,
                },
            )

        return render(request, self.template_name, {"form": form})


class TableBookingView(LoginRequiredMixin, View):
    """Представление подтверждения брони."""
    def post(self, request):
        date_str = request.POST.get("date")
        print(f"Полученная дата: {date_str}")  # Лог для отладки

        # Пробуем распарсить дату
        try:
            date = parse(date_str).date()  # Универсальное преобразование даты
        except ValueError:
            print(f"Ошибка формата даты: {date_str}")
            return render(
                request,
                "reservations/table_list.html",
                {
                    "error": "Ошибка в формате даты.",
                },
            )

        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        table_ids = request.POST.getlist("tables[]") or request.POST.getlist("tables")

        print(f"Выбранные столики: {table_ids}")  # Логирование для проверки

        if not table_ids:
            return render(
                request,
                "reservations/table_list.html",
                {
                    "error": "Выберите хотя бы один столик.",
                    "date": date,
                    "start_time": start_time,
                    "end_time": end_time,
                },
            )

        if not request.user.is_authenticated:
            print("Ошибка: Пользователь не авторизован!")
            return render(
                request,
                "reservations/table_list.html",
                {
                    "error": "Вы должны войти в систему, чтобы забронировать столик.",
                    "date": date,
                    "start_time": start_time,
                    "end_time": end_time,
                },
            )

        tables = Table.objects.filter(id__in=table_ids)

        reservation = Reservation.objects.create(
            user=request.user,
            date=date,  # Теперь в правильном формате
            start_time=start_time,
            end_time=end_time,
        )
        reservation.tables.set(tables)

        return render(
            request,
            "reservations/reservation_success.html",
            {"reservation": reservation},
        )


class ReservationSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "reservations/reservation_success.html"


class UserReservationsView(LoginRequiredMixin, ListView):
    """Список бронирований."""
    model = Reservation
    template_name = "reservations/user_reservations.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by(
            "date", "-start_time"
        )


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление брони."""
    model = Reservation
    template_name = "reservations/delete_reservation.html"
    success_url = reverse_lazy("reservations:user_reservations")

    def get_queryset(self):
        """Ограничиваем доступ к удалению только для владельца брони."""
        return Reservation.objects.filter(user=self.request.user)


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение брони."""
    model = Reservation
    form_class = ReservationForm
    template_name = "reservations/edit_reservation.html"
    success_url = reverse_lazy("reservations:user_reservations")

    def get_queryset(self):
        """Ограничиваем доступ к редактированию только для владельца брони."""
        return Reservation.objects.filter(user=self.request.user)


class ArchivedReservationsView(LoginRequiredMixin, ListView):
    """История бронирований."""
    model = ArchivedReservation
    template_name = "reservations/archived_reservations.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return ArchivedReservation.objects.filter(user=self.request.user).order_by('-id')
