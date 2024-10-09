"""URL configuration for mysite project."""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("activities/", include("activities.urls")),
    path("rest-auth/", include("dj_rest_auth.urls")),
    path("auth/", include('auth.urls')),
]
