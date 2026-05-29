from .utils import camelize_keys


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
    def format_success(self, data, meta=None, camelcase=False):
        meta = meta or {}
        return {
            "success": True,
            "data": camelize_keys(data) if camelcase else data,
            "meta": camelize_keys(meta) if camelcase else meta,
        }

    def format_fail(self, error_code, message, details=None, camelcase=False):
        return {
            "success": False,
            "error": {
                "type": "Fail",
                "code": error_code,
                "message": message,
                "details": [
                    {
                        "field": camelize_keys(d["field"]) if camelcase else d["field"],
                        "issue": d["issue"],
                    }
                    for d in (details or [])
                ],
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
