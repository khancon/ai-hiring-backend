import pytest
from app import create_app  # or however you create your Flask app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client
