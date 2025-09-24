# tests/test_api.py
import pytest


@pytest.mark.parametrize("url", ["/clients", "/clients/1"])
def test_get_endpoints(client, db_session, url):
    response = client.get(url)
    assert response.status_code in (200, 404)


def test_create_client(client):
    resp = client.post(
        "/clients",
        json={
            "name": "John",
            "surname": "Doe",
            "credit_card": "1234",
            "car_number": "A123BC",
        },
    )
    assert resp.status_code == 201
    assert resp.get_json()["name"] == "John"


def test_create_parking(client):
    resp = client.post(
        "/parkings", json={"address": "Center", "count_places": 10}
    )
    assert resp.status_code == 201
    assert resp.get_json()["count_available_places"] == 10
