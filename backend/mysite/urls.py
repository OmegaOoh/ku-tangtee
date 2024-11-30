"""URL configuration for mysite project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("activities/", include("activities.urls")),
    path("chat/", include("chat.urls")),
    path("rest-auth/", include("dj_rest_auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("auth/", include('auth.urls')),
    path("profile/", include("profiles.urls")),
    path("profile-pic/", views.profile_picture_view),
    path("get-user/<int:user_id>/", views.get_user_data),
    path('', RedirectView.as_view(url='activities/'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # pragma: no cover
