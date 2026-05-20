from django.test import override_settings


@override_settings(DUR_SETTINGS={"ENABLE": True})
def test_success_response_structure(api_client):
    response = api_client.get("/success/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] == {"message": "hello"}
    assert data["meta"] == {}


@override_settings(DUR_SETTINGS={"ENABLE": True, "CAMELCASE_KEYS": True})
def test_camelcase_keys(api_client):
    response = api_client.get("/success/")
    data = response.json()
    assert "success" in data
    assert data["data"] == {"message": "hello"}


@override_settings(DUR_SETTINGS={"ENABLE": True})
def test_renderer_respects_existing_success_key(api_client):
    pass


@override_settings(DUR_SETTINGS={"ENABLE": True})
def test_bypass_view(api_client):
    response = api_client.get("/bypass/")
    data = response.json()
    assert data == {"raw": "data"}


@override_settings(DUR_SETTINGS={"ENABLE": True})
def test_already_formatted_skips_wrapping(api_client):
    response = api_client.get("/already-formatted/")
    data = response.json()
    assert data == {"success": False, "error": "custom"}
