"""Module for redirect user to authentication page."""

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics, mixins, response
from .serializer import UserSerializer, SocialAccount
from django.contrib.auth.models import User
from django.http import HttpRequest
from typing import Any


class GoogleLogin(SocialLoginView):
    """Social Login View for Google OAuth."""

    adapter_class = GoogleOAuth2Adapter


class UserDetail(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin
):
    """User information detail view."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Response GET request by return detail of user with specific username.

        :return: HttpResponse object
        """
        return self.retrieve(request, *args, **kwargs)
