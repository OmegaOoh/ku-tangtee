"""Module for redirect user to authentication page."""

from typing import Any

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth.models import User
from django.http import HttpRequest
from mysite.settings import REST_AUTH
from rest_framework import generics, mixins, response, status
from rest_framework_simplejwt.views import TokenRefreshView

from .serializer import UserSerializer


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


class CustomTokenRefreshView(TokenRefreshView):
    """Views to refresh authentication using cookies token."""

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle Post request for Token Refresh."""
        # Get the refresh token from cookies
        refresh_token = request.COOKIES.get(REST_AUTH['JWT_AUTH_REFRESH_COOKIE'])
        if refresh_token:
            data = {'refresh': refresh_token}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            # Set new access token in cookies
            res = response.Response(serializer.validated_data, status=status.HTTP_200_OK)
            new_access_token = serializer.validated_data['access']
            res.set_cookie(
                REST_AUTH['JWT_AUTH_COOKIE'],
                new_access_token,
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            return res
        else:
            return response.Response({'error': 'Refresh token not found'}, status=status.HTTP_401_UNAUTHORIZED)
