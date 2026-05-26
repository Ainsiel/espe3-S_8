# Modelo de Datos (EventPass)

## 1. Entidades
| Entidad | Propósito | Almacenamiento | Sensible | Owner |
|---|---|---|---|---|
| User | Almacena información de los usuarios registrados | SQLite | Sí (Password hash) | PO de Fábrica |
| Event | Almacena la información de los eventos y su disponibilidad | SQLite | No | PO de Fábrica |
| Reservation | Almacena las reservas de los usuarios para cada evento | SQLite | No | PO de Fábrica |

## 2. Campos
### User
- `id` (INTEGER, PK, Auto)
- `email` (TEXT, unique, required)
- `password_hash` (TEXT, required)
- `is_active` (INTEGER, default 1)
- `created_at` (DATETIME)

### Event
- `id` (INTEGER, PK, Auto)
- `nombre` (TEXT, required)
- `descripcion` (TEXT, optional)
- `categoria` (TEXT, required)
- `fecha_evento` (DATETIME, required)
- `ubicacion` (TEXT, required)
- `precio` (REAL, required)
- `entradas_total` (INTEGER, required)
- `entradas_disp` (INTEGER, required)
- `imagen_url` (TEXT, optional)
- `created_at` (DATETIME)

### Reservation
- `id` (INTEGER, PK, Auto)
- `user_id` (INTEGER, FK to User)
- `event_id` (INTEGER, FK to Event)
- `codigo_conf` (TEXT, unique, required)
- `estado` (TEXT, default 'confirmada')
- `created_at` (DATETIME)
- `updated_at` (DATETIME)

## 3. Comportamiento ante Fallo
- Toda escritura debe ser atómica. Ante excepciones se ejecuta rollback de la sesión.