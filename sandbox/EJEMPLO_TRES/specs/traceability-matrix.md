# Matriz de Trazabilidad de Requisitos (EventPass)

| Requisito | Tarea | Prueba Diseñada | Evidencia |
|---|---|---|---|
| REQ-001 (Autenticación) | T-002, T-003 | `test_register_success`, `test_login_success`, `test_login_wrong_password` | `test-report.md` |
| REQ-002 (Validación) | T-002 | `test_register_invalid_email`, `test_register_short_password` | `test-report.md` |
| REQ-003 (Persistencia) | T-001 | SQLite auto-creation & seeding | `test-report.md` |
| REQ-004 (Eventos y Reservas) | T-003 | `test_get_events_public`, `test_reserve_success`, `test_reserve_sold_out`, `test_reserve_duplicate` | `test-report.md` |
| REQ-005 (UI Premium) | T-005 | Interfaz reactiva e interactiva | `validation-report.md` |