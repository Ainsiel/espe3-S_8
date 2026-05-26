# Plan de Pruebas del Proyecto (EventPass)

## 1. Pruebas Unitarias y API (Backend)
- `test_register_success`: Registro exitoso con email y password válidos (201).
- `test_register_duplicate_email`: Registro rechazado con email duplicado (400).
- `test_register_invalid_email`: Registro rechazado con email inválido (422).
- `test_register_short_password`: Registro rechazado con contraseña < 6 chars (422).
- `test_login_success`: Login exitoso retorna access_token (200).
- `test_login_wrong_password`: Login con contraseña incorrecta (401).
- `test_login_nonexistent_email`: Login con correo no registrado (401).
- `test_get_events_public`: Listar eventos sin token (200).
- `test_get_events_filter_category`: Filtrar eventos por categoría (200).
- `test_get_event_detail`: Detalle de evento por ID (200).
- `test_get_event_not_found`: Evento inexistente (404).
- `test_reserve_success`: Reserva exitosa con token válido (201).
- `test_reserve_no_auth`: Reserva sin token (401).
- `test_reserve_sold_out`: Reserva en evento agotado (400).
- `test_reserve_duplicate`: Reserva duplicada mismo evento (400).
- `test_get_my_reservations`: Listar mis reservas (200).
- `test_cancel_reservation`: Cancelar reserva existente (200).
- `test_cancel_already_cancelled`: Cancelar reserva ya cancelada (400).