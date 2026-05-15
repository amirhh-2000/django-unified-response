import typing

from rest_framework import serializers

try:
    from drf_spectacular.openapi import AutoSchema
    from drf_spectacular.utils import inline_serializer

    HAS_SPECTACULAR = True
except ImportError:
    AutoSchema = object
    HAS_SPECTACULAR = False

if HAS_SPECTACULAR:

    class UnifiedResponseAutoSchema(AutoSchema):
        """
        Custom AutoSchema to wrap DRF Spectacular responses in our unified format.
        """

        def get_response_serializers(self) -> typing.Any:
            response_serializers = super().get_response_serializers()

            if getattr(self.view, "_bypass_unified_response", False):
                return response_serializers

            if not response_serializers or not isinstance(response_serializers, dict):
                return response_serializers

            wrapped_serializers = {}
            for status_code, serializer in response_serializers.items():
                status_str = str(status_code)

                if status_str.startswith("2"):
                    wrapped_serializers[status_code] = inline_serializer(
                        name=f"UnifiedSuccess{status_str}Response",
                        fields={
                            "success": serializers.BooleanField(default=True),
                            "data": serializer
                            if isinstance(serializer, serializers.Serializer)
                            else serializers.DictField(),
                            "meta": serializers.DictField(
                                default={}, help_text="Pagination and extra meta data"
                            ),
                        },
                    )
                else:
                    error_detail_serializer = inline_serializer(
                        name="ErrorDetail",
                        fields={
                            "field": serializers.CharField(
                                help_text="Name of the field with error"
                            ),
                            "issue": serializers.CharField(
                                help_text="Error description"
                            ),
                        },
                    )
                    wrapped_serializers[status_code] = inline_serializer(
                        name=f"UnifiedError{status_str}Response",
                        fields={
                            "success": serializers.BooleanField(default=False),
                            "error": inline_serializer(
                                name="ErrorPayload",
                                fields={
                                    "type": serializers.CharField(default="Fail"),
                                    "code": serializers.CharField(default="ERROR_CODE"),
                                    "message": serializers.CharField(
                                        default="Error message here"
                                    ),
                                    "details": error_detail_serializer(
                                        many=True, required=False
                                    ),
                                },
                            ),
                        },
                    )
            return wrapped_serializers
else:

    class UnifiedResponseAutoSchema:
        pass
