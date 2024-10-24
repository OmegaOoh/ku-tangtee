"""Module for redirect user to authentication page."""

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics, mixins, response
from .serializer import UserSerializer, SocialAccount
from django.contrib.auth.models import User
from django.http import HttpRequest


class GoogleLogin(SocialLoginView):
    """Social Login View for Google OAuth."""

    adapter_class = GoogleOAuth2Adapter


class UserList(generics.GenericAPIView, mixins.ListModelMixin):
    """User data view."""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request: HttpRequest, *args, **kwargs) -> response.Response:
        """Response GET request by send list of serialized user."""
        return self.list(request, args, kwargs)
