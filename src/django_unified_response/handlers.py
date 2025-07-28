from django.conf import settings
from django.utils.module_loading import import_string
from django.http import Http404
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    NotAuthenticated,
    PermissionDenied,
)
from .exceptions import BaseAPIException


# --- Helper function to load the formatter ---
def get_formatter():
    """
    Gets the formatter class from Django settings, with a fallback to the default.
    """
    formatter_path = getattr(
        settings,
        "UNIFIED_RESPONSE_FORMATTER_CLASS",
        "django_unified_response.formatters.ResponseFormatter",
    )
    return import_string(formatter_path)()


def custom_exception_handler(exc, context):
    """
    Custom exception handler that uses a pluggable formatter class.
    """
    formatter = get_formatter()

    # Handle our custom exceptions first
    if isinstance(exc, BaseAPIException):
        payload = formatter.format_error(
            message=exc.default_detail,
            error_code=exc.error_code,
            errors=exc.detail if isinstance(exc.detail, (dict, list)) else None,
        )
        return Response(payload, status=exc.status_code)

    # Fall back to DRF's default handler
    response = exception_handler(exc, context)

    # If DRF handled it, format it with our formatter
    if response is not None:
        if isinstance(exc, ValidationError):
            payload = formatter.format_error(
                "Input validation failed.", "validation_error", response.data
            )
        elif isinstance(exc, (NotAuthenticated)):
            payload = formatter.format_error(
                "Authentication credentials were not provided or are invalid.",
                "authentication_failed",
                response.data,
            )
        elif isinstance(exc, PermissionDenied):
            payload = formatter.format_error(
                "You do not have permission to perform this action.",
                "permission_denied",
                response.data,
            )
        elif isinstance(exc, Http404):
            payload = formatter.format_error(
                "The requested resource was not found.", "not_found"
            )
        else:
            payload = formatter.format_error(
                "An error occurred.", "server_error", response.data
            )

        return Response(payload, status=response.status_code)

    # For any unhandled exception, return a generic 500 error
    payload = formatter.format_error(
        "A server error occurred, please try again later.", "server_error"
    )
    return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
