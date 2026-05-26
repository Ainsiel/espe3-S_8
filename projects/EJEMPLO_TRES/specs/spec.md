# Especificación del sistema web: Reserva de Entradas a Eventos

## 1. Nombre del sistema

**EventPass — Sistema de Reserva de Entradas a Eventos**

---

## 2. Objetivo general

Desarrollar un sistema web sencillo para que los usuarios puedan registrarse, iniciar sesión, explorar un catálogo de eventos disponibles y reservar entradas de forma controlada.

El sistema debe permitir:

- Registrar una cuenta de usuario con correo y contraseña.
- Iniciar sesión con autenticación JWT.
- Ver un listado de eventos disponibles con filtros.
- Ver el detalle de un evento específico.
- Reservar una entrada a un evento si hay disponibilidad.
- Ver el historial de reservas del usuario.
- Cancelar una reserva antes del evento.
- Guardar la información en una base de datos **SQLite**.

Este sistema está pensado como un ejercicio académico sencillo, fácil de ejecutar localmente y adecuado para ser desarrollado por una fábrica de agentes de IA.

---

## 3. Alcance del sistema

El sistema será una aplicación web básica con una interfaz moderna y funcional.

Debe incluir:

- Backend web con API REST.
- Base de datos SQLite.
- Frontend web con React + Bootstrap.
- Autenticación de usuarios con JWT.
- Catálogo de eventos con datos de prueba precargados.
- Sistema de reservas con control de disponibilidad.
- Validaciones básicas.
- Estructura clara de archivos.
- Documentación mínima para instalación y ejecución.

No se requiere en esta primera versión:

- Autenticación OAuth con proveedores externos.
- Pasarela de pago real.
- Gestión de roles o permisos avanzados.
- Generación de boletos con QR o PDF.
- Notificaciones por email.
- Panel de administración para gestionar eventos.

---

## 4. Tipo de aplicación

Aplicación web multiusuario sencilla.

El sistema puede ejecutarse localmente en el computador del usuario usando un servidor web de desarrollo.

Tecnologías:

- Backend: Python con FASTAPI.
- Base de datos: SQLite.
- ORM: SQLAlchemy.
- Autenticación: JWT (python-jose + passlib con bcrypt).
- Frontend: React + Bootstrap 5 (CDN con Babel standalone).
- Documentación API: Swagger/OpenAPI automático de FastAPI.

Arquitectura mínima:

```text
backend/
  app/
    main.py
  tests/
    test_main.py
frontend/
  index.html
```

---

# 5. Funcionalidades principales

## 5.1 Registro de usuario

El usuario debe poder crear una cuenta nueva desde un formulario.

Campos requeridos:

- Correo electrónico.
- Contraseña.
- Confirmación de contraseña (solo en frontend).

Reglas:

- El correo electrónico es obligatorio y debe tener formato válido.
- El correo electrónico debe ser único en el sistema.
- La contraseña es obligatoria y debe tener mínimo 6 caracteres.
- La contraseña debe almacenarse encriptada con bcrypt.
- Al registrarse exitosamente, el sistema devuelve un mensaje de confirmación.
- El usuario queda con estado activo por defecto.

---

## 5.2 Inicio de sesión

El usuario registrado debe poder iniciar sesión con su correo y contraseña.

Campos requeridos:

- Correo electrónico.
- Contraseña.

Reglas:

- Si las credenciales son correctas, el sistema genera un token JWT.
- El token JWT tiene una expiración de 60 minutos.
- Si las credenciales son incorrectas, el sistema devuelve error 401.
- Si el correo no existe, el sistema devuelve error 401 (sin revelar si el correo existe o no).
- El token JWT se almacena en el frontend (localStorage).
- Las rutas protegidas validan el token en cada petición mediante header `Authorization: Bearer <token>`.

---

## 5.3 Listar eventos

El sistema debe mostrar un catálogo de todos los eventos disponibles.

Cada evento debe mostrar en la lista:

- Nombre del evento.
- Categoría.
- Fecha y hora del evento.
- Ubicación.
- Precio de la entrada.
- Entradas disponibles / total de entradas.
- Estado de disponibilidad (disponible / agotado).
- Imagen representativa o icono de categoría.

Filtros disponibles:

- Por categoría (Todas, Concierto, Deporte, Teatro, Conferencia, Festival).
- Por disponibilidad (Todos, Disponibles, Agotados).
- Búsqueda por nombre del evento.

Reglas:

- Los eventos se muestran ordenados por fecha ascendente (próximos primero).
- Los eventos agotados se muestran con indicación visual pero siguen visibles.
- No se requiere autenticación para ver la lista de eventos.

---

## 5.4 Ver detalle de evento

El usuario debe poder hacer clic en un evento para ver su información completa.

Campos del detalle:

- Nombre del evento.
- Descripción completa.
- Categoría.
- Fecha y hora del evento.
- Ubicación / lugar.
- Precio de la entrada.
- Entradas totales.
- Entradas disponibles.
- Entradas reservadas.
- Estado (disponible / agotado).

Reglas:

- No se requiere autenticación para ver el detalle.
- Si hay entradas disponibles, se muestra el botón "Reservar Entrada".
- Si está agotado, el botón se muestra deshabilitado con texto "Agotado".
- Si el usuario no ha iniciado sesión, el botón redirige a la pantalla de login.

---

## 5.5 Reservar entrada

Un usuario autenticado debe poder reservar una entrada a un evento disponible.

Campos de la reserva:

- ID del evento (automático).
- ID del usuario (del token JWT).
- Cantidad de entradas (siempre 1 por reserva en esta versión).
- Fecha de la reserva (automática).
- Estado inicial: confirmada.

Reglas:

- Solo usuarios autenticados pueden reservar.
- No se puede reservar más de 1 entrada por usuario por evento.
- No se puede reservar si el evento no tiene entradas disponibles.
- Al confirmar la reserva, se descuenta 1 del stock de entradas disponibles.
- Cada reserva genera un código único de confirmación (formato: `EVP-XXXXXXXX` con 8 caracteres alfanuméricos).
- Si la reserva es exitosa, se muestra el código de confirmación al usuario.

---

## 5.6 Ver mis reservas

Un usuario autenticado debe poder ver el historial de sus reservas.

Cada reserva debe mostrar:

- Código de confirmación.
- Nombre del evento.
- Fecha del evento.
- Ubicación.
- Precio pagado.
- Fecha de la reserva.
- Estado (confirmada / cancelada).

Reglas:

- Solo se muestran las reservas del usuario autenticado.
- Las reservas se ordenan por fecha de reserva descendente (más recientes primero).
- Las reservas canceladas se muestran con indicación visual diferenciada.

---

## 5.7 Cancelar reserva

Un usuario autenticado debe poder cancelar una reserva activa.

Reglas:

- Solo se puede cancelar una reserva con estado "confirmada".
- Solo el dueño de la reserva puede cancelarla.
- Al cancelar, la reserva cambia a estado "cancelada".
- Al cancelar, se devuelve 1 entrada al stock disponible del evento.
- Antes de cancelar, la interfaz debe pedir confirmación.
- No se puede cancelar una reserva si la fecha del evento ya pasó.

---

# 6. Requisitos no funcionales

## RNF-01 Simplicidad

El sistema debe ser fácil de entender, instalar y ejecutar.

## RNF-02 Ejecución local

El sistema debe ejecutarse localmente sin depender de servicios externos.

## RNF-03 Código ordenado

El código debe estar separado por responsabilidades.

## RNF-04 Seguridad básica

El sistema debe validar los datos recibidos, encriptar contraseñas y proteger rutas con JWT.

## RNF-05 Usabilidad

La interfaz debe ser clara, moderna y usable.

## RNF-06 Compatibilidad

El sistema debe funcionar en un navegador moderno.

## RNF-07 Datos de prueba

El sistema debe incluir datos de prueba precargados al iniciar por primera vez.

---

# 7. Datos de prueba precargados

El sistema debe crear automáticamente los siguientes eventos de prueba al inicializar la base de datos si no existen registros:

```text
| # | Nombre                                 | Categoría    | Fecha           | Ubicación                     | Precio | Entradas Totales | Entradas Disponibles |
|---|----------------------------------------|--------------|-----------------|-------------------------------|--------|------------------|----------------------|
| 1 | Concierto Rock Nacional 2026           | Concierto    | 2026-07-15 20:00| Estadio Nacional              | 45.00  | 500              | 120                  |
| 2 | Final Campeonato de Fútbol             | Deporte      | 2026-06-28 18:30| Estadio Olímpico              | 35.00  | 1000             | 0                    |
| 3 | Obra de Teatro: El Quijote Moderno     | Teatro       | 2026-08-05 19:00| Teatro Municipal              | 25.00  | 150              | 45                   |
| 4 | Tech Summit Ecuador 2026               | Conferencia  | 2026-09-12 09:00| Centro de Convenciones        | 15.00  | 300              | 210                  |
| 5 | Festival de Jazz de Verano             | Festival     | 2026-07-22 16:00| Parque Central                | 30.00  | 800              | 0                    |
| 6 | Concierto Sinfónico: Beethoven         | Concierto    | 2026-10-01 20:00| Auditorio Nacional            | 55.00  | 200              | 180                  |
| 7 | Maratón Ciudad Capital 10K             | Deporte      | 2026-08-18 07:00| Avenida Principal             | 10.00  | 2000             | 1500                 |
| 8 | Stand-Up Comedy Night                  | Teatro       | 2026-06-30 21:00| Bar Cultural La Ronda         | 20.00  | 80               | 12                   |
```

Nota: Los eventos 2 y 5 tienen **0 entradas disponibles** (agotados) para probar ese escenario.

---

# 8. Flujo principal del usuario

1. El usuario abre la aplicación en el navegador.
2. El sistema muestra la lista de eventos disponibles (público, sin login).
3. El usuario puede filtrar eventos por categoría o disponibilidad.
4. El usuario hace clic en un evento para ver detalles.
5. Si quiere reservar, debe registrarse o iniciar sesión.
6. El usuario se registra con correo y contraseña.
7. El usuario inicia sesión y recibe un token JWT.
8. El usuario vuelve al evento deseado y presiona "Reservar Entrada".
9. El sistema valida disponibilidad y crea la reserva.
10. El sistema muestra el código de confirmación.
11. El usuario puede ver sus reservas en "Mis Reservas".
12. El usuario puede cancelar una reserva activa.

---

# 9. Casos de uso

## Caso de uso 1: Registrar cuenta

Actor: Visitante.

Flujo:

1. Visitante abre la aplicación.
2. Visitante hace clic en "Registrarse".
3. Visitante ingresa correo electrónico y contraseña.
4. Sistema valida formato de correo y longitud de contraseña.
5. Sistema verifica que el correo no esté registrado.
6. Sistema crea la cuenta con contraseña encriptada.
7. Sistema muestra mensaje de éxito.

Resultado: El visitante queda registrado y puede iniciar sesión.

---

## Caso de uso 2: Iniciar sesión

Actor: Usuario registrado.

Flujo:

1. Usuario accede a la pantalla de login.
2. Usuario ingresa correo y contraseña.
3. Sistema valida credenciales.
4. Sistema genera token JWT.
5. Sistema redirige al catálogo de eventos.

Resultado: El usuario accede al sistema autenticado.

---

## Caso de uso 3: Explorar eventos

Actor: Cualquier usuario (público).

Flujo:

1. Usuario visualiza la lista de eventos.
2. Usuario aplica filtros por categoría o disponibilidad.
3. Usuario busca por nombre.
4. Sistema filtra y muestra resultados.

Resultado: El usuario visualiza los eventos según sus filtros.

---

## Caso de uso 4: Ver detalle de evento

Actor: Cualquier usuario (público).

Flujo:

1. Usuario hace clic en un evento de la lista.
2. Sistema muestra todos los detalles del evento.
3. Si hay entradas disponibles, se muestra botón de reserva.
4. Si está agotado, se muestra indicación visual.

Resultado: El usuario ve toda la información del evento.

---

## Caso de uso 5: Reservar entrada

Actor: Usuario autenticado.

Flujo:

1. Usuario visualiza detalle de un evento con disponibilidad.
2. Usuario presiona "Reservar Entrada".
3. Sistema verifica autenticación (token JWT válido).
4. Sistema verifica que el usuario no tenga reserva previa en ese evento.
5. Sistema verifica disponibilidad de entradas.
6. Sistema crea la reserva y descuenta 1 entrada.
7. Sistema genera código de confirmación único.
8. Sistema muestra mensaje de éxito con código.

Resultado: La entrada queda reservada y el stock se actualiza.

---

## Caso de uso 6: Cancelar reserva

Actor: Usuario autenticado.

Flujo:

1. Usuario accede a "Mis Reservas".
2. Usuario presiona "Cancelar" en una reserva activa.
3. Sistema solicita confirmación.
4. Usuario confirma.
5. Sistema cambia estado a "cancelada".
6. Sistema devuelve 1 entrada al stock disponible.

Resultado: La reserva queda cancelada y la entrada vuelve a estar disponible.

---

# 10. Criterios de aceptación

El sistema se considera terminado cuando cumple lo siguiente:

- Se puede ejecutar localmente.
- Crea automáticamente la base de datos SQLite si no existe.
- Carga los datos de prueba de eventos al iniciar.
- Permite registrar una cuenta con correo y contraseña.
- No permite registrar un correo duplicado.
- Permite iniciar sesión con credenciales válidas.
- No permite iniciar sesión con credenciales inválidas.
- Genera y valida tokens JWT correctamente.
- Permite listar eventos sin autenticación.
- Permite filtrar eventos por categoría y disponibilidad.
- Permite buscar eventos por nombre.
- Permite ver el detalle de un evento.
- Permite reservar una entrada a un evento disponible (autenticado).
- No permite reservar si el evento está agotado.
- No permite reservar dos veces el mismo evento.
- Genera código de confirmación único por reserva.
- Permite ver el historial de reservas del usuario.
- Permite cancelar una reserva confirmada.
- Al cancelar, devuelve la entrada al stock disponible.
- Valida que el correo tenga formato válido.
- Valida que la contraseña tenga mínimo 6 caracteres.
- Guarda los datos correctamente en SQLite.
- Tiene una interfaz moderna y entendible.
- Incluye un README con instrucciones de instalación y ejecución.

---

# 11. Checklist de pruebas

```text
[ ] La aplicación inicia sin errores.
[ ] La base de datos SQLite se crea automáticamente.
[ ] Los eventos de prueba se cargan al iniciar.
[ ] Se puede registrar una cuenta con correo y contraseña válidos.
[ ] No se puede registrar con correo duplicado.
[ ] No se puede registrar con contraseña menor a 6 caracteres.
[ ] No se puede registrar con correo inválido.
[ ] Se puede iniciar sesión con credenciales correctas.
[ ] No se puede iniciar sesión con contraseña incorrecta.
[ ] No se puede iniciar sesión con correo inexistente.
[ ] El token JWT se genera correctamente al iniciar sesión.
[ ] Las rutas protegidas rechazan peticiones sin token.
[ ] Las rutas protegidas rechazan tokens expirados o inválidos.
[ ] Se muestran los eventos al abrir la aplicación.
[ ] Se pueden filtrar eventos por categoría.
[ ] Se pueden filtrar eventos por disponibilidad.
[ ] Se puede buscar un evento por nombre.
[ ] Se puede ver el detalle de un evento.
[ ] Los eventos agotados muestran indicación visual.
[ ] Se puede reservar entrada a evento disponible (autenticado).
[ ] No se puede reservar si el evento está agotado.
[ ] No se puede reservar el mismo evento dos veces.
[ ] Se genera código de confirmación único.
[ ] Se descuenta 1 entrada del stock al reservar.
[ ] Se puede ver el historial de mis reservas.
[ ] Se puede cancelar una reserva confirmada.
[ ] Se pide confirmación antes de cancelar.
[ ] Al cancelar se devuelve 1 entrada al stock.
[ ] Los datos persisten al reiniciar la aplicación.
```

---

# 12. Modelo de datos

## 12.1 Tabla `users`

```text
id              INTEGER   PRIMARY KEY AUTOINCREMENT
email           TEXT      NOT NULL UNIQUE
password_hash   TEXT      NOT NULL
is_active       INTEGER   DEFAULT 1
created_at      DATETIME  DEFAULT CURRENT_TIMESTAMP
```

## 12.2 Tabla `events`

```text
id              INTEGER   PRIMARY KEY AUTOINCREMENT
nombre          TEXT      NOT NULL
descripcion     TEXT
categoria       TEXT      NOT NULL  (concierto, deporte, teatro, conferencia, festival)
fecha_evento    DATETIME  NOT NULL
ubicacion       TEXT      NOT NULL
precio          REAL      NOT NULL  (>= 0)
entradas_total  INTEGER   NOT NULL  (> 0)
entradas_disp   INTEGER   NOT NULL  (>= 0)
imagen_url      TEXT      (opcional, para ícono o imagen)
created_at      DATETIME  DEFAULT CURRENT_TIMESTAMP
```

## 12.3 Tabla `reservations`

```text
id              INTEGER   PRIMARY KEY AUTOINCREMENT
user_id         INTEGER   NOT NULL REFERENCES users(id)
event_id        INTEGER   NOT NULL REFERENCES events(id)
codigo_conf     TEXT      NOT NULL UNIQUE  (formato EVP-XXXXXXXX)
estado          TEXT      NOT NULL DEFAULT 'confirmada'  (confirmada, cancelada)
created_at      DATETIME  DEFAULT CURRENT_TIMESTAMP
updated_at      DATETIME  DEFAULT CURRENT_TIMESTAMP
```

Restricción: UNIQUE(user_id, event_id) — un usuario solo puede tener una reserva por evento.

---

# 13. Endpoints API

## 13.1 Autenticación

```text
POST   /api/auth/register        Registrar cuenta (email, password)
POST   /api/auth/login            Iniciar sesión (email, password) → token JWT
GET    /api/auth/me               Obtener perfil del usuario autenticado
```

## 13.2 Eventos (público)

```text
GET    /api/events                Listar eventos (filtros: categoria, disponibilidad, search)
GET    /api/events/{id}           Detalle de un evento
```

## 13.3 Reservas (requiere autenticación JWT)

```text
POST   /api/reservations                  Reservar entrada (event_id)
GET    /api/reservations/me               Mis reservas
PUT    /api/reservations/{id}/cancel      Cancelar reserva
```

---

# 14. Esquemas de request/response

## 14.1 Registro

Request:
```json
{
  "email": "usuario@ejemplo.com",
  "password": "mipassword123"
}
```

Response (201):
```json
{
  "message": "Cuenta creada exitosamente",
  "user_id": 1
}
```

## 14.2 Login

Request:
```json
{
  "email": "usuario@ejemplo.com",
  "password": "mipassword123"
}
```

Response (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

## 14.3 Listar eventos

Response (200):
```json
[
  {
    "id": 1,
    "nombre": "Concierto Rock Nacional 2026",
    "categoria": "concierto",
    "fecha_evento": "2026-07-15T20:00:00",
    "ubicacion": "Estadio Nacional",
    "precio": 45.00,
    "entradas_total": 500,
    "entradas_disp": 120,
    "agotado": false
  }
]
```

## 14.4 Reservar entrada

Request:
```json
{
  "event_id": 1
}
```

Response (201):
```json
{
  "message": "Reserva confirmada",
  "reservation_id": 1,
  "codigo_confirmacion": "EVP-A3B8K9X2",
  "evento": "Concierto Rock Nacional 2026",
  "fecha_evento": "2026-07-15T20:00:00"
}
```

## 14.5 Mis reservas

Response (200):
```json
[
  {
    "id": 1,
    "codigo_conf": "EVP-A3B8K9X2",
    "evento_nombre": "Concierto Rock Nacional 2026",
    "fecha_evento": "2026-07-15T20:00:00",
    "ubicacion": "Estadio Nacional",
    "precio": 45.00,
    "estado": "confirmada",
    "created_at": "2026-05-26T08:00:00"
  }
]
```

---

# 15. Reglas de negocio

- Las contraseñas se almacenan con hash bcrypt, nunca en texto plano.
- El token JWT se genera con `python-jose` usando algoritmo HS256.
- El token JWT expira en 60 minutos.
- El SECRET_KEY de JWT se define como constante en la aplicación (ejercicio académico).
- No se permite stock negativo de entradas.
- Un usuario solo puede tener una reserva activa (confirmada) por evento.
- Si el usuario cancela su reserva, puede volver a reservar en el mismo evento.
- El código de confirmación se genera con `uuid4` truncado a 8 caracteres en mayúsculas, prefijado con `EVP-`.
- Los eventos de prueba se insertan automáticamente si la tabla `events` está vacía al iniciar.
- Las rutas de reservas requieren token JWT válido.
- Las rutas de eventos son públicas (no requieren autenticación).

---

# 16. Pantallas del frontend

Pantallas mínimas:

1. **Catálogo de Eventos** (página principal) — lista de eventos con filtros y búsqueda.
2. **Detalle de Evento** — información completa con botón de reserva.
3. **Login** — formulario de inicio de sesión.
4. **Registro** — formulario de registro de cuenta.
5. **Mis Reservas** — historial de reservas del usuario autenticado.

Componentes:

- `EventCard` — tarjeta de evento en la lista.
- `EventDetail` — vista de detalle expandida.
- `LoginForm` — formulario de autenticación.
- `RegisterForm` — formulario de registro.
- `ReservationList` — listado de reservas del usuario.
- `Navbar` — barra de navegación con opciones dinámicas según autenticación.
- `FilterBar` — barra de filtros (categoría, disponibilidad, búsqueda).
- `ConfirmationModal` — modal de confirmación para cancelar reserva.
- `Toast/Alert` — notificaciones de éxito y error.

---

# 17. Diseño de interfaz

El frontend debe usar tema oscuro premium con glassmorphism.

Paleta de colores:
- Fondo principal: `#020617` (slate-950).
- Cristal/glass: `rgba(15, 23, 42, 0.65)` con backdrop-filter blur.
- Bordes glass: `rgba(255, 255, 255, 0.08)`.
- Texto principal: `#f8fafc`.
- Texto secundario: `#94a3b8`.
- Acento primario: `#8b5cf6` (violeta).
- Acento secundario: `#06b6d4` (cian).
- Disponible: `#34d399` (verde).
- Agotado: `#f87171` (rojo).

Tipografía: Google Fonts `Outfit` (weights 300-800).

Los badges de categoría deben usar colores diferenciados:
- Concierto: violeta.
- Deporte: verde.
- Teatro: ámbar.
- Conferencia: azul.
- Festival: rosa.

---

# 18. Validaciones mínimas

Validaciones en backend y frontend:

- Email obligatorio y con formato válido.
- Contraseña obligatoria con mínimo 6 caracteres.
- Email único al registrar.
- Token JWT válido en rutas protegidas.
- Event ID existente al reservar.
- Evento con entradas disponibles > 0 al reservar.
- No duplicar reserva activa del mismo usuario al mismo evento.
- Solo el dueño puede cancelar su propia reserva.
- Solo reservas con estado "confirmada" pueden cancelarse.

---

# 19. Estructura sugerida del backend

```text
backend/
  app/
    main.py        # FastAPI app, modelos, rutas, lógica, datos de prueba
  tests/
    test_main.py   # Suite de pruebas con TestClient
```

Nota: Por ser un sistema sencillo, todo el backend puede estar en un solo archivo `main.py` con secciones claras:
1. Configuración y base de datos.
2. Modelos SQLAlchemy.
3. Esquemas Pydantic.
4. Utilidades JWT y autenticación.
5. Datos de prueba (seed).
6. Endpoints de autenticación.
7. Endpoints de eventos.
8. Endpoints de reservas.

---

# 20. Estructura sugerida del frontend

```text
frontend/
  index.html       # Aplicación React completa (CDN + Babel standalone)
```

Nota: Por ser un sistema sencillo con React CDN, toda la aplicación frontend se implementa en un solo archivo HTML con secciones claras:
1. Estilos CSS (glassmorphism dark mode).
2. Componente App (router de vistas).
3. Componente EventList (catálogo con filtros).
4. Componente EventDetail (detalle y reserva).
5. Componente LoginForm.
6. Componente RegisterForm.
7. Componente MyReservations.
8. Componente Navbar.

---

# 21. Pruebas esperadas (suite pytest)

```text
test_register_success              → Registro exitoso con email y password válidos (201)
test_register_duplicate_email      → Registro rechazado con email duplicado (400)
test_register_invalid_email        → Registro rechazado con email inválido (422)
test_register_short_password       → Registro rechazado con contraseña < 6 chars (422)
test_login_success                 → Login exitoso retorna access_token (200)
test_login_wrong_password          → Login con contraseña incorrecta (401)
test_login_nonexistent_email       → Login con correo no registrado (401)
test_get_events_public             → Listar eventos sin token (200)
test_get_events_filter_category    → Filtrar eventos por categoría (200)
test_get_event_detail              → Detalle de evento por ID (200)
test_get_event_not_found           → Evento inexistente (404)
test_reserve_success               → Reserva exitosa con token válido (201)
test_reserve_no_auth               → Reserva sin token (401)
test_reserve_sold_out              → Reserva en evento agotado (400)
test_reserve_duplicate             → Reserva duplicada mismo evento (400)
test_get_my_reservations           → Listar mis reservas (200)
test_cancel_reservation            → Cancelar reserva existente (200)
test_cancel_already_cancelled      → Cancelar reserva ya cancelada (400)
```

---

# 22. Casos de prueba funcionales

## CP-01 Registro exitoso

Datos:
- Email: test@ejemplo.com
- Password: secret123

Resultado esperado:
- Cuenta creada (201).
- Password almacenado como hash bcrypt.

## CP-02 Registro con email duplicado

Datos:
- Email: test@ejemplo.com (ya registrado)

Resultado esperado:
- Sistema rechaza con error 400.
- Mensaje claro: "El correo ya está registrado".

## CP-03 Login exitoso

Datos:
- Email: test@ejemplo.com
- Password: secret123

Resultado esperado:
- Token JWT válido retornado.

## CP-04 Login con credenciales incorrectas

Datos:
- Email: test@ejemplo.com
- Password: wrongpassword

Resultado esperado:
- Error 401 "Credenciales inválidas".

## CP-05 Reservar entrada disponible

Datos:
- Token JWT válido.
- Event ID: 1 (tiene entradas disponibles).

Resultado esperado:
- Reserva creada (201).
- Código de confirmación generado.
- Entradas disponibles descontadas en 1.

## CP-06 Reservar entrada agotada

Datos:
- Token JWT válido.
- Event ID: 2 (0 entradas disponibles).

Resultado esperado:
- Error 400 "No hay entradas disponibles".

## CP-07 Reserva duplicada

Datos:
- Token JWT válido.
- Event ID: 1 (ya reservado por el usuario).

Resultado esperado:
- Error 400 "Ya tienes una reserva para este evento".

## CP-08 Cancelar reserva

Datos:
- Token JWT válido.
- Reservation ID de una reserva confirmada.

Resultado esperado:
- Estado cambia a "cancelada".
- Entradas disponibles aumentan en 1.

---

# 23. Fuera de alcance

- **OOS-001:** Autenticación OAuth (Google, Facebook, etc.).
- **OOS-002:** Pasarela de pago real (Stripe, PayPal, etc.).
- **OOS-003:** Generación de boletos PDF o QR.
- **OOS-004:** Panel de administración para crear/editar eventos.
- **OOS-005:** Notificaciones por email.
- **OOS-006:** Roles y permisos avanzados.
- **OOS-007:** Múltiples entradas por reserva.
- **OOS-008:** Sistema de colas o waiting list para eventos agotados.

---

# 24. Entregables técnicos mínimos

El proyecto debe entregar:

- Código backend FastAPI (`backend/app/main.py`).
- Suite de pruebas Pytest (`backend/tests/test_main.py`).
- Código frontend React + Bootstrap (`frontend/index.html`).
- Base de datos SQLite auto-generada con datos de prueba.
- Documentación de endpoints en Swagger (`/docs`).
- README con instrucciones de instalación y ejecución.

---

# 25. Definición final del producto mínimo viable

El producto mínimo viable debe ser una aplicación web local llamada **EventPass**, desarrollada con **FastAPI, React + Bootstrap 5 y SQLite**, que permita a usuarios registrarse, iniciar sesión con JWT, explorar un catálogo de eventos con filtros, ver detalles de eventos y reservar entradas de forma controlada.

Debe incluir registro de usuario, autenticación JWT, catálogo de eventos con datos de prueba precargados (incluyendo eventos disponibles y agotados), reserva de entradas con control de disponibilidad, historial de reservas, cancelación de reservas y validaciones de negocio.

El sistema debe estar organizado, documentado y listo para ser ejecutado como ejercicio académico.