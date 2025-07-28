from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    NotAuthenticated,
    PermissionDenied,
)
from django.http import Http404
from .exceptions import BaseAPIException


def custom_exception_handler(exc, context):
    """
    Custom exception handler that catches our custom exceptions first,
    and then provides specific codes for standard DRF exceptions.
    """
    # First, check if the exception is one of our custom exceptions
    if isinstance(exc, BaseAPIException):
        error_payload = {
            "status": "error",
            "message": exc.default_detail,
            "error_code": exc.error_code,
            "errors": exc.detail if isinstance(exc.detail, (dict, list)) else None,
        }
        return Response(error_payload, status=exc.status_code)

    # If it's not a custom exception, fall back to DRF's default handler
    response = exception_handler(exc, context)

    # If DRF handled the exception, we'll format it with a specific error code
    if response is not None:
        error_payload = {
            "status": "error",
            "message": "An error occurred.",
            "error_code": "server_error",  # Default code
            "errors": response.data,
        }

        # Determine the error code based on the original exception type
        if isinstance(exc, ValidationError):
            error_payload["message"] = "Input validation failed."
            error_payload["error_code"] = "validation_error"
        elif isinstance(exc, (NotAuthenticated)):
            error_payload["message"] = (
                "Authentication credentials were not provided or are invalid."
            )
            error_payload["error_code"] = "authentication_failed"
        elif isinstance(exc, PermissionDenied):
            error_payload["message"] = (
                "You do not have permission to perform this action."
            )
            error_payload["error_code"] = "permission_denied"
        elif isinstance(exc, Http404):
            error_payload["message"] = "The requested resource was not found."
            error_payload["error_code"] = "not_found"
            # For 404, we can clean up the errors field
            if "detail" in error_payload["errors"]:
                error_payload["errors"] = None

        response.data = error_payload
        return response

    # For any completely unhandled exception, return a generic 500 error
    error_payload = {
        "status": "error",
        "message": "A server error occurred, please try again later.",
        "error_code": "server_error",
        "errors": None,
    }
    return Response(error_payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
