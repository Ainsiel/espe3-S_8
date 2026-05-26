# Plan Técnico y de Diseño Arquitectónico (TaskLiteJota)

## 1. Resumen de Arquitectura
Se propone un monolito estructurado modular pequeño:
- **Backend:** FastAPI (Python 3.9+) estructurado en modelos y controladores de tareas.
- **Frontend:** React + Bootstrap servido estáticamente en página única interactiva.
- **Base de Datos:** SQLite local (`db.sqlite3`) en modo archivo persistente.

## 2. Estructura de Módulos (Backend)
- `main.py`: Entrada del servidor, base de datos SQLite con SQLAlchemy, esquemas Pydantic y endpoints de API integrados.
- `tests/test_main.py`: Suite de pruebas Pytest utilizando `TestClient` de FastAPI.

## 3. Política de Dependencias Aprobada
- FastAPI (v0.95.0+)
- Uvicorn (v0.22.0+)
- SQLAlchemy (v2.0.0+)
- Pydantic (v1.10.0+)