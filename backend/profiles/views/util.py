"""Utility module for profile model."""
from django.http import HttpRequest
from profiles import models
from rest_framework import decorators
from rest_framework.response import Response


@decorators.api_view(['get'])
def check_missing_attendance(request: HttpRequest) -> Response:
    """Deduct reputation in case attendee does not attend and activity ended or cancelled.

    :param request: Http request object
    :return: Message response
    """
    models.Profile.check_missed_check_ins()
    return Response({"message": "Attendance check and deductions completed."})
