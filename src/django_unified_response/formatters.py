class BaseFormatter:
    """
    Abstract base class for all response formatters.
    Any custom formatter must inherit from this class and override its methods.
    """

    def format_success(self, data, meta=None):
        raise NotImplementedError("format_success() must be implemented.")

    def format_fail(self, error_code, message, details=None):
        raise NotImplementedError("format_fail() must be implemented.")

    def format_error(self, error_code, message, details=None):
        raise NotImplementedError("format_error() must be implemented.")


class DefaultFormatter(BaseFormatter):
    def format_success(self, data, meta=None):
        return {
            "success": True,
            "data": data,
            "meta": meta or {},
        }

    def format_fail(self, error_code, message, details=None):
        return {
            "success": False,
            "error": {
                "type": "Fail",
                "code": error_code,
                "message": message,
                "details": details or [],
            },
        }

    def format_error(self, error_code, message, details=None):
        return {
            "success": False,
            "error": {
                "type": "Error",
                "code": error_code,
                "message": message,
                "details": None,
            },
        }
