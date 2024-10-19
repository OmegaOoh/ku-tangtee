"""Utility module."""

from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
import pytz
from datetime import datetime
from django.conf import settings


def csrf_token_view(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return csrf token."""
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def get_timezone(request: HttpRequest) -> JsonResponse:  # pragma: no cover
    """Return time zone offset to vue."""
    tzo = get_time_zone_offset()
    return JsonResponse({'offset': tzo})


def get_time_zone_offset() -> int:  # type: ignore[no-untyped-def] ## pragma: no cover
    """Get the UTC offset for a given time zone."""
    try:
        # Get the timezone object
        time_zone = settings.TIME_ZONE
        tz = pytz.timezone(time_zone)
        # Get the current time in UTC
        now_utc = datetime.now(pytz.utc)
        # Get the local time in the specified timezone
        local_time = now_utc.astimezone(tz)
        # Calculate the offset in hours
        offset = local_time.utcoffset()

        if offset is not None:
            return int(offset.total_seconds() / 3600)
        else:
            return 0  # If utcoffset is None, return 0
    except Exception as e:
        print(f"Error getting offset for time zone {time_zone}: {e}")
        return 0  # Return 0 if there's an error