"""URL configuration for activities app."""
from django.urls import path
from . import views

app_name = "activities"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:activity_id>/join", views.join, name="join"),
    path("<int:pk>", views.ActivityDetailView.as_view(), name="detail")
]
