"""
URL configuration for mysite project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("activity/", include("activities.urls"))
]
