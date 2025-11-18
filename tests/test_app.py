import pytest
from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    # basic sanity check for a known activity
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "tester+pytest@example.com"

    # Ensure clean starting state (remove if present)
    if email in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].remove(email)

    # Sign up
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # Verify participant appears
    r = client.get("/activities")
    assert r.status_code == 200
    participants = r.json()[activity]["participants"]
    assert email in participants

    # Unregister
    r = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert r.status_code == 200
    assert "Unregistered" in r.json().get("message", "")

    # Verify removed
    r = client.get("/activities")
    participants = r.json()[activity]["participants"]
    assert email not in participants
