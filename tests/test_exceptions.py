from django_unified_response.exceptions import (
    BaseAPIException,
    NotFoundException,
    ValidationException,
)


def test_base_exception_defaults():
    exc = BaseAPIException()
    assert exc.status_code == 400
    assert exc.code == "bad_request"


def test_not_found():
    exc = NotFoundException()
    assert exc.status_code == 404
    assert exc.code == "not_found"


def test_validation_exception_custom():
    exc = ValidationException(
        message="Custom message",
        code="custom_code",
        details={"field": "issue"},
    )
    assert exc.details == {"field": "issue"}
    assert exc.code == "custom_code"


def test_validation_exception_default_details():
    exc = ValidationException(message="Invalid")
    assert exc.details == {"error": "Input validation failed."}
