from rest_framework.renderers import JSONRenderer

from django_unified_response.conf import dur_settings


class UnifiedJSONRenderer(JSONRenderer):
    """
    Custom JSON Renderer that intercepts the response and wraps it
    in the unified structure using the configured formatter.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not dur_settings.ENABLE:
            return super().render(data, accepted_media_type, renderer_context)

        response = renderer_context.get("response") if renderer_context else None

        if response is None:
            return super().render(data, accepted_media_type, renderer_context)

        if isinstance(data, dict) and "success" in data:
            return super().render(data, accepted_media_type, renderer_context)

        if 200 <= response.status_code < 300:
            formatter = dur_settings.FORMATTER_CLASS()

            # TODO: In the future, extract pagination data from 'data' into 'meta'
            meta = {}

            unified_data = formatter.format_success(data=data, meta=meta)
            return super().render(unified_data, accepted_media_type, renderer_context)

        return super().render(data, accepted_media_type, renderer_context)
