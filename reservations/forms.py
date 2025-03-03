from django import forms
import datetime

from reservations.models import Reservation, Table


from django.utils.timezone import now


class CheckAvailabilityForm(forms.Form):
    date = forms.DateField(
        label="Дата",
        widget=forms.DateInput(
            attrs={"type": "date", "min": datetime.date.today().isoformat()}
        ),
    )
    start_time = forms.ChoiceField(label="Время от")
    end_time = forms.ChoiceField(label="Время до")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Генерируем временные слоты с шагом 30 минут
        time_slots = [
            (f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}")
            for h in range(10, 22)
            for m in (0, 30)
        ]
        self.fields["start_time"].choices = time_slots
        self.fields["end_time"].choices = time_slots

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if date:
            today = now().date()
            if date < today:
                self.add_error("date", "Вы не можете выбрать прошедшую дату.")

        if start_time and end_time:
            start_dt = datetime.datetime.strptime(start_time, "%H:%M").time()
            end_dt = datetime.datetime.strptime(end_time, "%H:%M").time()
            current_time = now().time()
            today = now().date()

            if date == today and start_dt < current_time:
                self.add_error("start_time", "Вы не можете выбрать прошедшее время.")

            if end_dt <= start_dt:
                self.add_error("end_time", "Время окончания должно быть позже времени начала.")


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["date", "start_time", "end_time", "tables"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "start_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "end_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "tables": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """Фильтруем список столиков, исключая занятые в это время"""
        super().__init__(*args, **kwargs)

        if "instance" in kwargs and kwargs["instance"]:
            reservation = kwargs["instance"]
            reserved_tables = (
                Reservation.objects.filter(
                    date=reservation.date,
                    start_time__lt=reservation.end_time,
                    end_time__gt=reservation.start_time,
                )
                .exclude(id=reservation.id)
                .values_list("tables", flat=True)
            )

            self.fields["tables"].queryset = Table.objects.exclude(
                id__in=reserved_tables
            )
