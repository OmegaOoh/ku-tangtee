"""Custom decorator for activities app."""

from typing import Callable, Any, Optional
from django.http import HttpRequest, JsonResponse
from rest_framework.generics import get_object_or_404
from . import models


def login_required(func: Callable[..., None]) -> Callable[..., None]:
    """Return a wrapper function that make function return error Json when user doesn't login."""

    def wrapper(request: HttpRequest, *args: tuple[Any], **kwargs: Optional[str]) -> JsonResponse:
        """If user already login just invoke request handler func."""
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return JsonResponse(
            {
                'error': 'User must authenticated before perform this action'
            },
            status=401
        )

    return wrapper


def host_restricted(func: Callable[..., None]) -> Callable[..., None]:
    """Return a wrapper function that make function return error Json when user isn't host."""

    def wrapper(request: HttpRequest, activity_id: int, *args: tuple[Any], **kwargs: Optional[str]) -> JsonResponse | None:
        """If user is host, just invoke request handler func."""
        activity = get_object_or_404(models.Activity, pk=activity_id)
        if request.user.is_authenticated and request.user == activity.host():
            return func(request, activity_id, *args, **kwargs)
        return JsonResponse(
            {
                'error': 'User must be the host to perform this action'
            },
            status=401
        )

    return wrapper
