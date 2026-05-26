import pytest
from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app, engine, Base

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

def test_create_task_success():
    response = client.post(
        "/api/tasks",
        json={"titulo": "Aprender FastAPI", "descripcion": "Leer la documentación", "prioridad": "alta"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Aprender FastAPI"
    assert data["prioridad"] == "alta"
    assert data["estado"] == "pendiente"
    assert data["id"] is not None

def test_create_task_invalid_title():
    # Title too short (< 3)
    response1 = client.post("/api/tasks", json={"titulo": "Hi", "prioridad": "baja"})
    assert response1.status_code == 422

    # Title empty
    response2 = client.post("/api/tasks", json={"titulo": "", "prioridad": "baja"})
    assert response2.status_code == 422

    # Title too long (> 100)
    response3 = client.post("/api/tasks", json={"titulo": "A" * 101, "prioridad": "alta"})
    assert response3.status_code == 422

def test_get_tasks_sorting():
    # Insert multiple tasks
    client.post("/api/tasks", json={"titulo": "Tarea 1"})
    client.post("/api/tasks", json={"titulo": "Tarea 2"})
    
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    # Check creation descending order (newest first)
    assert data[0]["titulo"] == "Tarea 2"
    assert data[1]["titulo"] == "Tarea 1"

def test_edit_task_success():
    resp_create = client.post("/api/tasks", json={"titulo": "Tarea Inicial", "prioridad": "baja"})
    task_id = resp_create.json()["id"]
    
    resp_edit = client.put(
        f"/api/tasks/{task_id}",
        json={"titulo": "Tarea Editada", "prioridad": "alta", "estado": "pendiente", "descripcion": "Nueva desc"}
    )
    assert resp_edit.status_code == 200
    data = resp_edit.json()
    assert data["titulo"] == "Tarea Editada"
    assert data["prioridad"] == "alta"
    assert data["descripcion"] == "Nueva desc"
    assert data["updated_at"] is not None

def test_toggle_status():
    resp_create = client.post("/api/tasks", json={"titulo": "Hacer Ejercicio"})
    task_id = resp_create.json()["id"]
    
    # Complete task
    resp_comp = client.put(f"/api/tasks/{task_id}/complete")
    assert resp_comp.status_code == 200
    assert resp_comp.json()["estado"] == "completada"
    
    # Reopen task
    resp_reop = client.put(f"/api/tasks/{task_id}/reopen")
    assert resp_reop.status_code == 200
    assert resp_reop.json()["estado"] == "pendiente"

def test_delete_task_success():
    resp_create = client.post("/api/tasks", json={"titulo": "Eliminar Tarea"})
    task_id = resp_create.json()["id"]
    
    resp_del = client.delete(f"/api/tasks/{task_id}")
    assert resp_del.status_code == 200
    
    # Verify 404 on get/edit/delete
    resp_get = client.delete(f"/api/tasks/{task_id}")
    assert resp_get.status_code == 404