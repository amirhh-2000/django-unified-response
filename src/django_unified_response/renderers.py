from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.renderers import JSONRenderer
from rest_framework import status


# --- Helper function to load the formatter ---
def get_formatter():
    """
    Gets the formatter class from Django settings, with a fallback to the default.
    """
    formatter_path = getattr(
        settings,
        "UNIFIED_RESPONSE_FORMATTER_CLASS",
        "django_unified_response.formatters.DefaultResponseFormatter",
    )
    return import_string(formatter_path)()


class UnifiedJSONRenderer(JSONRenderer):
    """
    A custom renderer that uses a pluggable formatter to wrap all successful API responses.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders the data into the final JSON format.
        """
        formatter = get_formatter()
        response = renderer_context.get("response")

        if response and status.is_success(response.status_code):
            # For successful responses, we need to extract any potential 'meta' data
            # passed along with the DRF Response object.
            meta_data = None
            if isinstance(data, dict):
                # We pop 'meta' so it's not included in the main 'data' field
                meta_data = data.pop("meta", None)

            # We check to prevent double-wrapping.
            if not (
                isinstance(data, dict) and data.get("status") in ["success", "error"]
            ):
                formatted_data = formatter.format_success(
                    data=data, status_code=response.status_code, meta=meta_data
                )
            else:
                formatted_data = data
        else:
            # Error responses are already formatted by the handler.
            formatted_data = data

        return super().render(formatted_data, accepted_media_type, renderer_context)
