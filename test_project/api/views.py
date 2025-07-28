# test_project/api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_unified_response.exceptions import NotFoundException, IntegrityException


class SuccessView(APIView):
    """Tests a standard successful response."""

    def get(self, request):
        data = {"user_id": 1, "status": "active"}
        response_data = {"user": data, "meta": {"request_id": "xyz-123"}}
        return Response(response_data)


class ValidationErrorView(APIView):
    """Tests a DRF validation error."""

    def get(self, request):
        raise ValidationError({"field": ["This field has an error."]})


class NotFoundView(APIView):
    """Tests our custom NotFoundException."""

    def get(self, request):
        raise NotFoundException()


class IntegrityErrorView(APIView):
    """Tests our custom IntegrityException."""

    def get(self, request):
        raise IntegrityException("This item already exists in the database.")
