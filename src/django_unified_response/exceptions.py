from rest_framework.exceptions import APIException
from rest_framework import status


class BaseAPIException(APIException):
    """
    Base class for custom API exceptions in the project.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "bad_request"
    default_detail = "A server error occurred."

    def __init__(self, detail=None, error_code=None):
        super().__init__(detail, None)
        self.detail = detail or self.default_detail
        self.error_code = error_code or self.error_code


class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"
    default_detail = "The requested resource was not found."


class IntegrityException(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "integrity_error"
    default_detail = "A data conflict occurred. The resource may already exist."


class ValidationException(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "validation_error"
    default_detail = "Input validation failed."

    def __init__(self, detail=None, error_code=None):
        """
        For validation, the detail is often a dictionary of errors.
        """
        super().__init__(detail, error_code)
        if detail is None:
            self.detail = {"error": self.default_detail}


class AuthenticationFailedException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "authentication_failed"
    default_detail = "Authentication credentials were not provided or are invalid."
