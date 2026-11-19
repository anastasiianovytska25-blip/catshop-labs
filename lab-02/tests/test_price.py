import pytest
import requests

import app as catshop


class FakePartnerResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"sku": "MK-II", "price": "1234.56", "currency": "UAH"}


@pytest.fixture
def client():
    return catshop.app.test_client()


def test_price_comes_from_the_partner(client, monkeypatch):
    asked = []

    def fake_get(url, timeout):
        asked.append(url)
        return FakePartnerResponse()

    monkeypatch.setattr(catshop.requests, "get", fake_get)

    response = client.get("/price/MK-II")
    assert response.status_code == 200
    assert response.get_json()["price"] == "1234.56"
    assert asked == [f"{catshop.PARTNER_URL}/v1/catalog/MK-II"]


def test_price_is_502_when_the_partner_is_down(client, monkeypatch):
    def partner_down(url, timeout):
        raise requests.ConnectionError("partner is down")

    monkeypatch.setattr(catshop.requests, "get", partner_down)

    response = client.get("/price/MK-II")
    assert response.status_code == 502
    assert response.get_json()["error"] == "ConnectionError"
