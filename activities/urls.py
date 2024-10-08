"""URL configuration for activities app."""
from django.urls import path
from . import views

app_name = "activities"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:activity_id>/join", views.join, name="join"),
    path("<int:pk>", views.ActivityDetailView.as_view(), name="detail"),
    path("create", views.create, name="create"),
    path("<int:activity_id>/edit", views.edit_activity, name = "edit_activity"),
    path('get-csrf-token/', views.csrf_token_view, name='get_csrf_token'),
]
