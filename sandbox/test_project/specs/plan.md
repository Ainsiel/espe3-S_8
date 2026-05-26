# Plan Técnico y de Diseño Arquitectónico

## 1. Resumen de Arquitectura
Se propone un monolito estructurado modular pequeño:
- **Backend:** FastAPI (Python 3.9+) estructurado en controladores, modelos y esquemas de validación.
- **Frontend:** React + Bootstrap servido estáticamente o a través de servidor local de desarrollo.
- **Base de Datos:** SQLite local en modo archivo para asegurar persistencia transaccional simple.

## 2. Estructura de Módulos (Backend)
- `main.py`: Entrada del servidor y configuración de CORS.
- `db.py`: Inicialización de base de datos y sesión de SQLite.
- `models.py`: Modelo SQLAlchemy para la persistencia.
- `schemas.py`: Esquemas Pydantic para validación y serialización.
- `routes.py`: Rutas de la API FastAPI.

## 3. Estructura de Componentes (Frontend)
- `index.html`: Estructura HTML base que enlaza Bootstrap.
- `app.js`: Lógica interactiva en Vanilla JS/React para manejar la tabla, creación y borrado.

## 4. Política de Dependencias Aprobada
- FastAPI (v0.95.0+)
- Uvicorn (v0.22.0+)
- SQLAlchemy (v2.0.0+)
- Pydantic (v1.10.0+)