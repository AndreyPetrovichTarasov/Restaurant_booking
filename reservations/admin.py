from django.contrib import admin
from .models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "seats")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "get_tables",
        "date",
        "start_time",
        "end_time",
        "created_at",
    )
    list_filter = ("date", "start_time", "end_time", "tables")
    search_fields = ("user__email", "tables__number")

    def get_tables(self, obj):
        return ", ".join([str(table) for table in obj.tables.all()])

    get_tables.short_description = "Столики"
