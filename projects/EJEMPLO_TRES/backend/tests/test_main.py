import pytest
from fastapi.testclient import TestClient
from app.main import app, Base, engine, SessionLocal, EventDB
from datetime import datetime

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    events = [
        EventDB(nombre="Concierto Rock Nacional 2026", categoria="concierto", fecha_evento=datetime.strptime("2026-07-15 20:00", "%Y-%m-%d %H:%M"), ubicacion="Estadio Nacional", precio=45.00, entradas_total=500, entradas_disp=120),
        EventDB(nombre="Final Campeonato de Fútbol", categoria="deporte", fecha_evento=datetime.strptime("2026-06-28 18:30", "%Y-%m-%d %H:%M"), ubicacion="Estadio Olímpico", precio=35.00, entradas_total=1000, entradas_disp=0),
        EventDB(nombre="Obra de Teatro: El Quijote Moderno", categoria="teatro", fecha_evento=datetime.strptime("2026-08-05 19:00", "%Y-%m-%d %H:%M"), ubicacion="Teatro Municipal", precio=25.00, entradas_total=150, entradas_disp=45)
    ]
    db.add_all(events)
    db.commit()
    db.close()
    yield

def test_register_success():
    response = client.post("/api/auth/register", json={"email": "newuser@test.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json()["message"] == "Cuenta creada exitosamente"
    assert "user_id" in response.json()

def test_register_duplicate_email():
    client.post("/api/auth/register", json={"email": "newuser@test.com", "password": "password123"})
    response = client.post("/api/auth/register", json={"email": "newuser@test.com", "password": "password456"})
    assert response.status_code == 400
    assert response.json()["detail"] == "El correo ya está registrado."

def test_register_invalid_email():
    response = client.post("/api/auth/register", json={"email": "invalidemail", "password": "password123"})
    assert response.status_code == 422

def test_register_short_password():
    response = client.post("/api/auth/register", json={"email": "newuser@test.com", "password": "123"})
    assert response.status_code == 422

def test_login_success():
    client.post("/api/auth/register", json={"email": "newuser@test.com", "password": "password123"})
    response = client.post("/api/auth/login", json={"email": "newuser@test.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password():
    client.post("/api/auth/register", json={"email": "newuser@test.com", "password": "password123"})
    response = client.post("/api/auth/login", json={"email": "newuser@test.com", "password": "wrongpassword"})
    assert response.status_code == 401

def test_login_nonexistent_email():
    response = client.post("/api/auth/login", json={"email": "notfound@test.com", "password": "password123"})
    assert response.status_code == 401

def test_get_events_public():
    response = client.get("/api/events")
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 3
    assert events[0]["nombre"] == "Final Campeonato de Fútbol"

def test_get_events_filter_category():
    response = client.get("/api/events?categoria=concierto")
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 1
    assert events[0]["nombre"] == "Concierto Rock Nacional 2026"

def test_get_event_detail():
    response = client.get("/api/events/1")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Concierto Rock Nacional 2026"

def test_get_event_not_found():
    response = client.get("/api/events/999")
    assert response.status_code == 404

def get_auth_headers(email="test@user.com", password="password123"):
    client.post("/api/auth/register", json={"email": email, "password": password})
    login_resp = client.post("/api/auth/login", json={"email": email, "password": password})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_reserve_success():
    headers = get_auth_headers()
    response = client.post("/api/reservations", json={"event_id": 1}, headers=headers)
    assert response.status_code == 201
    assert response.json()["message"] == "Reserva confirmada"
    assert response.json()["codigo_confirmacion"].startswith("EVP-")
    
    event_response = client.get("/api/events/1")
    assert event_response.json()["entradas_disp"] == 119

def test_reserve_no_auth():
    response = client.post("/api/reservations", json={"event_id": 1})
    assert response.status_code == 401

def test_reserve_sold_out():
    headers = get_auth_headers()
    response = client.post("/api/reservations", json={"event_id": 2}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "No hay entradas disponibles"

def test_reserve_duplicate():
    headers = get_auth_headers()
    client.post("/api/reservations", json={"event_id": 1}, headers=headers)
    response = client.post("/api/reservations", json={"event_id": 1}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Ya tienes una reserva para este evento"

def test_get_my_reservations():
    headers = get_auth_headers()
    client.post("/api/reservations", json={"event_id": 1}, headers=headers)
    response = client.get("/api/reservations/me", headers=headers)
    assert response.status_code == 200
    reservations = response.json()
    assert len(reservations) == 1
    assert reservations[0]["evento_nombre"] == "Concierto Rock Nacional 2026"

def test_cancel_reservation():
    headers = get_auth_headers()
    res = client.post("/api/reservations", json={"event_id": 1}, headers=headers)
    res_id = res.json()["reservation_id"]
    
    cancel_resp = client.put(f"/api/reservations/{res_id}/cancel", headers=headers)
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["message"] == "Reserva cancelada exitosamente"
    
    event_response = client.get("/api/events/1")
    assert event_response.json()["entradas_disp"] == 120

def test_cancel_already_cancelled():
    headers = get_auth_headers()
    res = client.post("/api/reservations", json={"event_id": 1}, headers=headers)
    res_id = res.json()["reservation_id"]
    
    client.put(f"/api/reservations/{res_id}/cancel", headers=headers)
    cancel_resp = client.put(f"/api/reservations/{res_id}/cancel", headers=headers)
    assert cancel_resp.status_code == 400
    assert cancel_resp.json()["detail"] == "La reserva ya se encuentra cancelada"