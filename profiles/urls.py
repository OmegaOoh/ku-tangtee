"""URL configuration for profiles app."""
from django.urls import path
from . import views

app_name = "profiles"
urlpatterns = [
    path("", views.ProfileDetail.as_view(), name="detail"),
]
