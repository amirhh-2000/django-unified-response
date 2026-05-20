import pytest
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def reset_dur_settings():
    from django_unified_response.conf import dur_settings

    dur_settings.reload()
    if hasattr(settings, "DUR_SETTINGS"):
        delattr(settings, "DUR_SETTINGS")
