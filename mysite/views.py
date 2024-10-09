"""Views for activities app, handle html request."""
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from . import utils


def get_time_zone_offset_view(request: HttpRequest) -> JsonResponse:
    """Return timezone offset as Json."""
    time_zone = settings.TIME_ZONE  # Fetch from settings.py
    offset = utils.get_time_zone_offset(time_zone)
    print(offset)
    return JsonResponse({'offset': offset})


@login_required
def is_authen(request: HttpRequest) -> JsonResponse:
    """Return Json which inform that user is login right now."""
    print(request.user.is_authenticated)
    return JsonResponse({"is_authen": request.user.is_authenticated})
