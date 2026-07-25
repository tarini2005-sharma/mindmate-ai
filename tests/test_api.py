from fastapi.testclient import TestClient

from backend.api import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "MindMate API is running"


def test_analyze():
    response = client.post(
        "/analyze",
        json={"text": "I feel really anxious about tomorrow."}
    )

    assert response.status_code == 200

    data = response.json()

    assert "emotion" in data
    assert "confidence" in data
    assert "message" in data
    assert "activities" in data