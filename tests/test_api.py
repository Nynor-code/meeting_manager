import os
import pytest
from base64 import b64encode
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def auth_header():
    user = os.environ.get("APP_USER", "admin")
    pw = os.environ.get("APP_PASS", "admin")
    creds = b64encode(f"{user}:{pw}".encode()).decode("utf-8")
    return {"Authorization": f"Basic {creds}"}

def test_get_meetings(client):
    response = client.get("/meetings", headers=auth_header())
    assert response.status_code == 200

def test_create_meeting(client):
    data = {
        "title": "Test Meeting",
        "description": "Sample",
        "start_time": "2025-05-10T10:00:00",
        "end_time": "2025-05-10T11:00:00"
    }
    response = client.post("/meetings", json=data, headers=auth_header())
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_report_generation(client):
    response = client.get("/meetings/1/report", headers=auth_header())
    assert response.status_code in (200, 404)  # 404 if sample not seeded
