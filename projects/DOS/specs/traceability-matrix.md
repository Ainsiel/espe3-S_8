# Matriz de Trazabilidad de Requisitos (TaskLiteJota)

| Requisito | Tarea | Prueba Diseñada | Evidencia |
|---|---|---|---|
| REQ-001 (API CRUD) | T-001, T-003 | CRUD endpoints: `test_create_task_success`, `test_edit_task_success`, `test_delete_task_success` | `test-report.md` |
| REQ-002 (Validación) | T-002 | Validación de Pydantic: `test_create_task_invalid_title` | `test-report.md` |
| REQ-003 (Persistencia) | T-001 | SQLite auto-creation & saving | `test-report.md` |
| REQ-004 (Orden y Filtro) | T-003 | GET queries: `test_get_tasks_sorting` | `test-report.md` |
| REQ-005 (UI Premium) | T-005 | Interfaz reactiva e interactiva | `validation-report.md` |