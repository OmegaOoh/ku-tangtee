"""URL configuration for profiles app."""
from django.urls import path
from . import views

app_name = "profiles"
urlpatterns = [
    path("", views.ProfileList.as_view(), name="index"),
    path("<str:username>/", views.ProfileDetail.as_view(), name="detail"),
]
