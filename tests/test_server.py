from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_docs_endpoint():
    resp = client.get("/docs")
    assert resp.status_code == 200

def test_list_apps():
    # ADK exposes /list-apps – tiny integration test
    resp = client.get("/list-apps")
    assert resp.status_code == 200
    assert "agents" in resp.json()  # depends on ADK discovery
