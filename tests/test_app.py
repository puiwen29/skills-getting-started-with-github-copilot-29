from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def setup_function():
    activities["Basketball Team"]["participants"] = ["alice@example.com", "bob@example.com"]


def test_unregister_participant_removes_email_from_activity():
    response = client.delete(
        "/activities/Basketball%20Team/unregister?email=alice@example.com"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered alice@example.com from Basketball Team"
    }
    assert "alice@example.com" not in activities["Basketball Team"]["participants"]


def test_unregister_participant_returns_404_for_missing_activity():
    response = client.delete("/activities/Unknown%20Club/unregister?email=alice@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
