# Checklist de Requisitos y QA (TaskLiteJota)

## Requisitos de la Constitución
- [x] Objetivo e ID de proyecto especificado (`UNO`).
- [x] Reglas de negocio claras de la especificación (sin invenciones).
- [x] Criterios de aceptación funcionales definidos.
- [x] Stack tecnológico gobernado (FastAPI + React + SQLite).

## Requisitos del Proyecto
- [x] **REQ-001 (API CRUD):** Endpoints definidos para crear, listar, editar, eliminar y cambiar estado.
- [x] **REQ-002 (Validación):** Validadores de Pydantic y JS para título (3-100 chars), prioridad y estado.
- [x] **REQ-003 (Persistencia):** Base de datos SQLite se crea automáticamente.
- [x] **REQ-004 (Ordenamiento y Filtro):** Orden descendente por creación, filtros reactivos de estado y prioridad.
- [x] **REQ-005 (Frontend premium):** Interfaz fluida, moderna con Bootstrap + React, con ventana de confirmación al eliminar.