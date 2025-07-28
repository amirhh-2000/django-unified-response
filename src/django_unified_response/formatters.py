class ResponseFormatter:
    """
    Default formatter for API responses.
    This class can be swapped out in settings to provide a custom response structure.
    """

    @staticmethod
    def format_success(data, status_code=200, message="Success", meta=None):
        """
        Formats a successful response.
        """
        return {
            "status": "success",
            "message": message,
            "data": data,
            "meta": meta or {},
        }

    @staticmethod
    def format_error(message, error_code, errors=None, status_code=400, meta=None):
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
