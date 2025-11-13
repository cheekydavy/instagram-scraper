"""API tests."""

from fastapi.testclient import TestClient
from src.instagram_scraper.main import app

client = TestClient(app)

def test_profile_endpoint():
    response = client.get("/api/v1/profile/nasa")
    assert response.status_code == 200
    assert "username" in response.json()

def test_posts_endpoint():
    response = client.get("/api/v1/posts/nasa?max_posts=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)