from rest_framework.renderers import JSONRenderer
from rest_framework import status


class UnifiedJSONRenderer(JSONRenderer):
    """
    A custom renderer that wraps all successful API responses in a standard format.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders the data into the final JSON format.
        """
        response = renderer_context.get("response")

        # Check if the response is successful (2xx status code).
        # Error responses are already formatted by the exception handler.
        if response and status.is_success(response.status_code):
            # For successful responses, wrap the data in our standard format.
            # We also check to prevent double-wrapping.
            if not (isinstance(data, dict) and data.get("status") == "success"):
                formatted_data = {"status": "success", "data": data}
            else:
                formatted_data = data
        else:
            # For error responses, the data is already formatted by our
            # custom exception handler. We just pass it through.
            formatted_data = data

        # Call the parent class's render method to serialize the data to JSON.
        return super().render(formatted_data, accepted_media_type, renderer_context)
