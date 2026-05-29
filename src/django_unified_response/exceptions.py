from rest_framework import status
from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "bad_request"
    default_message = "A server error occurred."

    def __init__(self, message=None, code=None, details=None):
        super().__init__(detail=message or self.default_message)

        self.message = message or self.default_message
        self.code = code or self.error_code
        self.details = details


class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"
    default_message = "The requested resource was not found."


class IntegrityException(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "integrity_error"
    default_message = "A data conflict occurred. The resource may already exist."


class ValidationException(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "validation_error"
    default_message = "Input validation failed."

    def __init__(self, message=None, code=None, details=None):
        super().__init__(message, code, details)

        if details is None:
            self.details = []


class AuthenticationFailedException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "authentication_failed"
    default_message = "Authentication credentials were not provided or are invalid."
