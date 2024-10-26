"""URL configuration for mysite project."""
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("activities/", include("activities.urls")),
    path("chat/", include("chat.urls")),
    path("rest-auth/", include("dj_rest_auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("auth/", include('auth.urls')),
    path("profile-pic/", views.profile_picture_view),
    path("get-user/<int:user_id>/", views.get_user_data)
]
