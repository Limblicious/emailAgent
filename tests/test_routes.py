from unittest.mock import patch
import json

from app import app


def test_index():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert b'<form' in response.data


def test_flyer_form_route():
    tester = app.test_client()
    response = tester.get('/flyer-form')
    assert response.status_code == 200
    assert b'<form' in response.data


def test_generate_flyer_success():
    tester = app.test_client()

    payload = {
        "address": "123 Test St, Test City, TS",
        "price": "$123,456",
        "features": ["Pool", "Garage"],
        "agent_name": "Agent Smith",
        "agent_phone": "555-1234",
        "agent_email": "agent@example.com",
        "recipient_email": "recipient@test.com",
    }

    with patch("app_pkg.routes.smtplib.SMTP"):
        response = tester.post("/generate-flyer", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    expected_subject = f"Beautiful Home in {payload['address'].split(',')[0]} – Don\u2019t Miss Out!"
    assert data["status"] == "Email sent successfully"
    assert data["subject"] == expected_subject
    assert payload["features"][0] in data["html_body"]
    assert payload["agent_name"] in data["html_body"]


def test_generate_flyer_defaults():
    tester = app.test_client()
    payload = {
        "address": "1 Test Way",
        "price": "$1",
    }

    with patch("app_pkg.routes.smtplib.SMTP") as mock_smtp:
        response = tester.post("/generate-flyer", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "Email sent successfully"
    assert data["subject"] == "Beautiful Home in 1 Test Way – Don’t Miss Out!"
    assert "<ul>" in data["html_body"]


def test_generate_flyer_form_submission():
    tester = app.test_client()
    form_data = {
        "address": "1 Test Way",
        "price": "$1",
        "features": "feature1\nfeature2",
        "agent_name": "Agent",
        "agent_phone": "123",
        "agent_email": "agent@test.com",
        "subject": "Test Subject",
    }

    with patch("app_pkg.routes.smtplib.SMTP"):
        response = tester.post("/generate-flyer", data=form_data)

    assert response.status_code == 200
    assert b"Email sent successfully" in response.data

