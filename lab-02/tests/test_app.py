import pytest

import app as catshop


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(catshop, "COUNTER_FILE", tmp_path / "visits.txt")
    monkeypatch.setattr(catshop, "DATABASE_URL", None)
    return catshop.app.test_client()


def test_health_says_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "ok\n"


def test_ready_names_the_file_store(client, tmp_path):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json() == {"ready": True, "store": f"file:{tmp_path / 'visits.txt'}"}


def test_ready_is_503_when_the_store_is_broken(client, monkeypatch, tmp_path):
    blocker = tmp_path / "blocker"
    blocker.write_text("")
    monkeypatch.setattr(catshop, "COUNTER_FILE", blocker / "visits.txt")

    response = client.get("/ready")
    assert response.status_code == 503
    assert response.get_json()["ready"] is False


def test_visits_counts_up_and_saves_the_count(client, tmp_path):
    first = client.get("/visits")
    second = client.get("/visits")

    assert first.get_json() == {"visits": 1, "store": "file"}
    assert second.get_json() == {"visits": 2, "store": "file"}
    assert (tmp_path / "visits.txt").read_text() == "2"
