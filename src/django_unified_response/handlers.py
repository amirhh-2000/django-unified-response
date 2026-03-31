from rest_framework.views import exception_handler

from django_unified_response.conf import dur_settings
from django_unified_response.utils import camelize_keys


def unified_exception_handler(exc, context):
    """
    Custom exception handler that intercepts DRF errors and wraps them
    in the unified standard structure.
    """
    response = exception_handler(exc, context)

    view = context.get("view")
    if view and getattr(view, "_bypass_unified_response", False):
        return response

    if response is None or not dur_settings.ENABLE:
        return response

    formatter = dur_settings.FORMATTER_CLASS()
    status_code = response.status_code
    data = response.data

    message = "An error occurred."
    error_code = f"HTTP_{status_code}"
    details = []

    # Parse DRF's weird error structures!
    if isinstance(data, dict):
        if "detail" in data:
            message = str(data["detail"])
            if hasattr(data["detail"], "code"):
                error_code = data["detail"].code
        else:
            message = "Validation Error"
            error_code = "VALIDATION_ERROR"
            for field, errors in data.items():
                if isinstance(errors, list):
                    for error in errors:
                        details.append({"field": field, "issue": str(error)})
                else:
                    details.append({"field": field, "issue": str(errors)})
    elif isinstance(data, list):
        message = "Validation Error"
        error_code = "VALIDATION_ERROR"
        details = [{"field": "non_field_errors", "issue": str(e)} for e in data]
    else:
        message = str(data)

    # Categorize into 'Fail' (Client Error) or 'Error' (Server Error)
    if 400 <= status_code < 500:
        unified_data = formatter.format_fail(
            error_code=error_code,
            message=message,
            details=details if details else None,
        )
    else:
        unified_data = formatter.format_error(
            error_code=error_code,
            message=message,
            details=None,
        )

    if dur_settings.CAMELCASE_KEYS:
        unified_data = camelize_keys(unified_data)

    response.data = unified_data
    return response
