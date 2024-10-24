"""Utility module."""

from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
import pytz
from datetime import datetime
from django.conf import settings
from rest_framework import decorators, response


@decorators.api_view(['get'])
def csrf_token_view(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return csrf token."""
    csrf_token = get_token(request)
    return response.Response({'csrfToken': csrf_token})
