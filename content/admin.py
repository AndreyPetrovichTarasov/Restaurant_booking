from django.contrib import admin
from .models import HomePageContent, AboutContent, ServicesContent


@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ["about_text"]


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ["history_title"]


@admin.register(ServicesContent)
class ServicesContentAdmin(admin.ModelAdmin):
    list_display = ["menu_title"]
