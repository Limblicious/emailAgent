from app import app

def test_index():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Hello, World!'}


def test_generate_flyer_success(monkeypatch):
    tester = app.test_client()

    payload = {
        "address": "123 Main St",
        "price": "$100",
        "features": ["a", "b"],
        "agent_name": "Agent",
        "agent_phone": "123",
        "agent_email": "a@b.com",
    }

    expected = {"subject": "hi", "html_body": "<p>body</p>"}

    def fake_generate_flyer(data):
        assert data == payload
        return expected

    monkeypatch.setattr("app.routes.generate_flyer", fake_generate_flyer)

    response = tester.post("/generate-flyer", json=payload)
    assert response.status_code == 200
    assert response.get_json() == expected


def test_generate_flyer_missing_field():
    tester = app.test_client()
    payload = {
        "address": "123 Main St",
        "price": "$100",
        "features": ["a", "b"],
        "agent_name": "Agent",
        "agent_phone": "123",
        # missing agent_email
    }

    response = tester.post("/generate-flyer", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_generate_flyer_openai_error(monkeypatch):
    tester = app.test_client()
    payload = {
        "address": "123 Main St",
        "price": "$100",
        "features": ["a", "b"],
        "agent_name": "Agent",
        "agent_phone": "123",
        "agent_email": "a@b.com",
    }

    def fake_generate_flyer(data):
        raise RuntimeError("OpenAI API request failed: boom")

    monkeypatch.setattr("app.routes.generate_flyer", fake_generate_flyer)

    response = tester.post("/generate-flyer", json=payload)
    assert response.status_code == 502
    assert "error" in response.get_json()
