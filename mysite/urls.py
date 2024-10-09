"""URL configuration for mysite project."""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("activities/", include("activities.urls")),
    path("accounts/", include("allauth.urls")),
    path('is_authen', views.is_authen, name='is_authen'),
    path('get-time-zone-offset/', views.get_time_zone_offset_view, name='get_time_zone_offset'),
]
