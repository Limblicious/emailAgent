from unittest.mock import patch

from app import app


def test_index():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Hello, World!'}


def test_generate_flyer_success():
    tester = app.test_client()

    payload = {
        "address": "123 Main St",
        "price": "$100",
        "features": ["a", "b"],
        "agent_name": "Agent",
        "agent_phone": "123",
        "agent_email": "a@b.com",
        "recipient_email": "recipient@test.com",
        "subject": "Beautiful Home in 123 Main St – Don’t Miss Out!",
    }

    with patch("app.routes.smtplib.SMTP") as mock_smtp:
        response = tester.post("/generate-flyer", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "Email sent successfully"
    assert data["subject"] == payload["subject"]
    assert "<li>a</li>" in data["html_body"]
    assert "<li>b</li>" in data["html_body"]
    assert "Agent" in data["html_body"]


def test_generate_flyer_defaults():
    tester = app.test_client()
    payload = {
        "address": "1 Test Way",
        "price": "$1",
    }

    with patch("app.routes.smtplib.SMTP") as mock_smtp:
        response = tester.post("/generate-flyer", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "Email sent successfully"
    assert data["subject"] == "Beautiful Home in 1 Test Way – Don’t Miss Out!"
    assert "<ul>" in data["html_body"]

