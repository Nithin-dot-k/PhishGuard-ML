import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_analyze_endpoint_safe():
    response = client.post("/api/analyze", json={"url": "https://google.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] == 0
    assert data["is_whitelisted"] is True

def test_analyze_endpoint_phishing():
    response = client.post("/api/analyze", json={"url": "http://paypal-login-verify-account.badsite.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] >= 65
    assert data["is_brand_spoof"] is True
    assert "verdict" in data
