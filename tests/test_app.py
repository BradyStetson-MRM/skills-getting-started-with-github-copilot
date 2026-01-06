import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"

    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": test_email})

    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

    # Duplicate sign up should fail
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 400

    # Unregister
    response = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response.status_code == 200
    assert f"Removed {test_email}" in response.json()["message"]

    # Unregister again should fail
    response = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response.status_code == 404


def test_signup_invalid_activity():
    response = client.post("/activities/NonexistentActivity/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404


def test_unregister_invalid_activity():
    response = client.delete("/activities/NonexistentActivity/unregister", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
