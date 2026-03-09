"""
Tests for Project 01 — FastAPI Basics.
Run with: pytest tests/ -v
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_item_exists():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Sensor A"


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404


def test_create_item():
    new_item = {"name": "Pressure Gauge", "price": 49.99, "in_stock": True}
    response = client.post("/items/", json=new_item)
    assert response.status_code == 201
    assert response.json()["name"] == "Pressure Gauge"


def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 204
