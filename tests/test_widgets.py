import os
import tempfile

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.environ["WIDGETS_DB"] = path
    # Import after env is set so module-level DB_PATH picks it up.
    from app import db, main
    db.DB_PATH = path
    db.init_db(path)
    with TestClient(main.app) as c:
        yield c
    os.unlink(path)


def test_add_and_get(client):
    r = client.post("/widgets", json={"name": "sprocket", "description": "spins"})
    assert r.status_code == 201
    wid = r.json()["id"]
    assert client.get(f"/widgets/{wid}").json()["name"] == "sprocket"


def test_rename(client):
    wid = client.post("/widgets", json={"name": "a"}).json()["id"]
    r = client.patch(f"/widgets/{wid}", json={"name": "b"})
    assert r.status_code == 200 and r.json()["name"] == "b"


def test_remove(client):
    wid = client.post("/widgets", json={"name": "gone"}).json()["id"]
    assert client.delete(f"/widgets/{wid}").status_code == 204
    assert client.get(f"/widgets/{wid}").status_code == 404


def test_remix_links_parent(client):
    parent = client.post("/widgets", json={"name": "orig", "description": "d"}).json()
    r = client.post(f"/widgets/{parent['id']}/remix", json={})
    assert r.status_code == 201
    child = r.json()
    assert child["parent_id"] == parent["id"]
    assert child["description"] == "d"
    assert child["name"] == "orig (remix)"


def test_remix_custom_name(client):
    parent = client.post("/widgets", json={"name": "orig"}).json()
    child = client.post(
        f"/widgets/{parent['id']}/remix", json={"name": "fresh"}
    ).json()
    assert child["name"] == "fresh"


def test_list(client):
    client.post("/widgets", json={"name": "one"})
    client.post("/widgets", json={"name": "two"})
    names = [w["name"] for w in client.get("/widgets").json()]
    assert names == ["one", "two"]


def test_missing_returns_404(client):
    assert client.get("/widgets/999").status_code == 404
    assert client.patch("/widgets/999", json={"name": "x"}).status_code == 404
    assert client.delete("/widgets/999").status_code == 404
