import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_landing_page(client):
    """
    Test the landing page returns 200 OK, HTML content, and contains the expected API documentation.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.content_type
    assert b"Welcome to the AI Hiring Backend API" in response.data
    assert b"/generate-jd" in response.data
    assert b"/screen-resume" in response.data
    assert b"/generate-questions" in response.data
    assert b"/evaluate" in response.data
    assert b"/generate-feedback" in response.data


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
