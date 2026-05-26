import pytest
from fastapi.testclient import TestClient
import os
import sys

# Append parent dir to PYTHONPATH to find app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app, engine, Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

def test_create_item():
    response = client.post(
        "/api/items",
        json={"nombre": "Tornillos", "descripcion": "Tornillos de acero", "cantidad": 100, "precio": 2.50}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Tornillos"
    assert data["precio"] == 2.50
    assert data["id"] is not None

def test_validate_negative_price():
    response = client.post(
        "/api/items",
        json={"nombre": "Martillo", "descripcion": "Martillo pesado", "cantidad": 10, "precio": -15.0}
    )
    assert response.status_code == 422 # Unprocessable Entity due to Field ge=0.0

def test_get_items():
    response = client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)