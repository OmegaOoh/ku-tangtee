from django.urls import path

from . import views

urlpatterns = [
    path('google-oauth2/', views.GoogleLogin.as_view(), name='google_login'),
]