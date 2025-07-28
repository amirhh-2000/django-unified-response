from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_unified_response.exceptions import NotFoundException, IntegrityException


class SuccessView(APIView):
    """Tests a standard successful response."""

    def get(self, request):
        data = {"user_id": 1, "status": "active"}
        # We also test the 'meta' field
        return Response({"data": data, "meta": {"request_id": "xyz-123"}})


class ValidationErrorView(APIView):
    """Tests a DRF validation error."""

    def get(self, request):
        # This will be caught by our handler and formatted correctly.
        raise ValidationError({"field": ["This field has an error."]})


class NotFoundView(APIView):
    """Tests our custom NotFoundException."""

    def get(self, request):
        # We raise our custom exception.
        raise NotFoundException()


class IntegrityErrorView(APIView):
    """Tests our custom IntegrityException."""

    def get(self, request):
        # We raise our custom exception with a custom message.
        raise IntegrityException("This item already exists in the database.")
