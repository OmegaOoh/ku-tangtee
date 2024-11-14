"""Module for mapping authentication URL."""

from django.urls import path

from . import views

app_name = "auth"
urlpatterns = [
    path('google-oauth2/', views.GoogleLogin.as_view(), name='google_login'),
    path('user/<str:username>/', views.UserDetail.as_view(), name='user'),
]
