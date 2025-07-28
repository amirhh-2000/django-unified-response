class DefaultResponseFormatter:
    """
    The default formatter for API responses.
    Developers can inherit from this class and override only the methods
    they need to change.
    """

    def format_success(self, data, status_code=200, message="Success", meta=None):
        """
        Formats a successful response.
        """
        return {
            "status": "success",
            "message": message,
            "data": data,
            "meta": meta or {},
        }

    def format_error(
        self, message, error_code, errors=None, status_code=400, meta=None
    ):
        """
        Formats an error response.
        """
        return {
            "status": "error",
            "message": message,
            "error_code": error_code,
            "errors": errors or None,
            "meta": meta or {},
        }
