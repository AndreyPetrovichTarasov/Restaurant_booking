from django.contrib import admin
from django.urls import path, include

from config.views import HomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("users/", include("users.urls", namespace="users")),
]
