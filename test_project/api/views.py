from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from django_unified_response.decorators import bypass_unified_response
from django_unified_response.exceptions import IntegrityException, NotFoundException


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


class PaginatedMockView(APIView):
    """Tests the automatic extraction of DRF paginated responses."""

    def get(self, request):
        paginated_data = {
            "count": 42,
            "next": "http://localhost:8000/api/paginated/?page=3",
            "previous": "http://localhost:8000/api/paginated/?page=1",
            "results": [
                {"id": 1, "name": "Amir"},
                {"id": 2, "name": "Deniz"},
                {"id": 3, "name": "David"},
            ],
        }
        return Response(paginated_data)


@bypass_unified_response
class RawBypassView(APIView):
    """Tests the bypass decorator (Opt-out)."""

    def get(self, request):
        return Response({"message": "I am a rebel! No unified response for me!"})
