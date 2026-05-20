from django.test import override_settings


@override_settings(DUR_SETTINGS={"ENABLE": True})
def test_handler_formats_validation_error(api_client):
    response = api_client.get("/error/")
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["type"] == "Fail"
    assert "details" in data["error"]


@override_settings(DUR_SETTINGS={"ENABLE": False})
def test_handler_disabled_returns_raw(api_client):
    response = api_client.get("/error/")
    data = response.json()
    assert "success" not in data


@override_settings(DUR_SETTINGS={"ENABLE": True})
def test_handler_formats_404_not_found(api_client):
    response = api_client.get("/not-found/")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["error"]["type"] == "Fail"


@override_settings(DUR_SETTINGS={"ENABLE": True})
def test_handler_server_error(api_client):
    response = api_client.get("/server-error/")
    assert response.status_code == 500
    data = response.json()
    assert data["success"] is False
    assert data["error"]["type"] == "Error"


@override_settings(DUR_SETTINGS={"ENABLE": True})
def test_handler_non_dict_data(api_client):
    pass
