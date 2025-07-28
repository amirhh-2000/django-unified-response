from django.urls import path
from . import views

urlpatterns = [
    path("success/", views.SuccessView.as_view(), name="success"),
    path(
        "validation-error/",
        views.ValidationErrorView.as_view(),
        name="validation_error",
    ),
    path("not-found/", views.NotFoundView.as_view(), name="not_found"),
    path(
        "integrity-error/", views.IntegrityErrorView.as_view(), name="integrity_error"
    ),
]
