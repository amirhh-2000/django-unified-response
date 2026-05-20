from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView

from django_unified_response.decorators import bypass_unified_response


class SuccessView(APIView):
    def get(self, request):
        return Response({"message": "hello"})


class ErrorView(APIView):
    def get(self, request):
        from rest_framework.exceptions import ValidationError

        raise ValidationError({"email": ["Enter a valid email."]})


class NotFoundView(APIView):
    def get(self, request):
        from django.http import Http404

        raise Http404("Not found")


class ServerErrorView(APIView):
    def get(self, request):
        raise Exception("Boom")


@bypass_unified_response
class BypassView(APIView):
    def get(self, request):
        return Response({"raw": "data"})


class AlreadyFormattedView(APIView):
    def get(self, request):
        return Response({"success": False, "error": "custom"})


urlpatterns = [
    path("success/", SuccessView.as_view(), name="success"),
    path("error/", ErrorView.as_view(), name="error"),
    path("not-found/", NotFoundView.as_view(), name="not-found"),
    path("server-error/", ServerErrorView.as_view(), name="server-error"),
    path("bypass/", BypassView.as_view(), name="bypass"),
    path(
        "already-formatted/", AlreadyFormattedView.as_view(), name="already-formatted"
    ),
]
