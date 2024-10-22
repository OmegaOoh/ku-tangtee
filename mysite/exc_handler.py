"""Custom exception handler."""
from rest_framework.views import exception_handler
from rest_framework import response
from typing import Any


def custom_exception_handler(exc: Exception, context: Any) -> response.Response:
    """Return custom exception response by convert error message's key to message."""
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:

        if len(response.data) > 1 or not isinstance(response.data, dict):
            return response

        for _, v in response.data.items():

            if isinstance(v, list) and len(v) == 1:
                v = v[0]

            response.data = {'message': v}

    return response
