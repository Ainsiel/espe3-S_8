# Checklist de Tareas del Proyecto (TaskLiteJota)

- [ ] **T-001 (Base de Datos):** Configuración de la base de datos SQLite y el modelo de datos SQLAlchemy `Task` en `backend/app/main.py`. (Mapea a REQ-003)
- [ ] **T-002 (Esquemas y Validaciones):** Implementar modelos Pydantic `TaskCreate` y `TaskResponse` con reglas de título (3-100 caracteres) y prioridades. (Mapea a REQ-002)
- [ ] **T-003 (Endpoints API):** Construir rutas de FastAPI para CRUD de tareas (GET /api/tasks con filtros, POST, PUT para edición, PUT para completar/reabrir, DELETE con control 404). (Mapea a REQ-001, REQ-004)
- [ ] **T-004 (Suite de Pruebas):** Escribir tests Pytest en `backend/tests/test_main.py` para todos los casos de uso. (Mapea a AC-001 al AC-006)
- [ ] **T-005 (Frontend Premium):** Crear la interfaz reactiva interactiva en `frontend/index.html` con React + Bootstrap y estilos dark/premium avanzados. (Mapea a REQ-005)