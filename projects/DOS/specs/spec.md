# Especificación SDD: TaskLiteJota - Gestor Personal de Tareas (TaskLiteJota)

## 1. Nombre del sistema
- **Nombre:** TaskLiteJota — Gestor Personal de Tareas
- **Dueño:** PO de Fábrica (Usuario)
- **Fecha:** 2026-05-26
- **ID de Proyecto:** DOS
- **Estado:** `spec_validated`

## 2. Objetivo
- **Qué problema resuelve:** Desarrollar un sistema web pequeño para administrar tareas personales de forma simple con persistencia en SQLite, backend FastAPI y frontend React + Bootstrap.
- **Para quién:** Usuarios que requieren organizar sus pendientes diarios localmente.
- **Resultado esperado:** Una app web CRUD fluida, con filtros de estado y prioridad, y diseño premium.

## 3. Usuarios y roles
| Rol | Qué puede hacer | Restricciones |
|---|---|---|
| Usuario Único | Administrar tareas (Crear, Listar, Editar, Completar, Eliminar, Filtrar). | Acceso local monousuario sin login en esta fase. |

## 4. Flujos transaccionales
| Flujo | Actor | Entrada | Acción | Salida | Error esperado |
|---|---|---|---|---|---|
| Crear Tarea | Usuario | Título, descripción (opc), fecha límite (opc), prioridad | Inserta en DB con estado 'pendiente' y timestamps | ID + datos de tarea | Título vacío o <3 o >100 caracteres |
| Listar Tareas | Usuario | Filtros de estado / prioridad | Consulta DB ordenada desc por fecha creación | Lista de tareas | Sin tareas registradas |
| Editar Tarea | Usuario | ID + nuevos datos (título, desc, fecha, prioridad, estado) | Actualiza en DB y setea `updated_at` | Tarea modificada | Tarea no encontrada |
| Completar/Reabrir | Usuario | ID de tarea | Modifica estado y setea `updated_at` | Estado alternado | Tarea no encontrada |
| Eliminar Tarea | Usuario | ID de tarea (con confirmación previa) | Borra registro físicamente | Mensaje de éxito | Tarea no encontrada |

## 5. Requisitos funcionales
- **REQ-001 (API CRUD):** Endpoints REST para crear, listar, editar, eliminar y cambiar estado de tareas.
- **REQ-002 (Validación):** Validar título obligatorio de 3 a 100 caracteres. Prioridades permitidas: baja, media, alta.
- **REQ-003 (Persistencia):** Persistencia íntegra en base de datos SQLite local (`db.sqlite3`).
- **REQ-004 (Ordenamiento y Filtros):** Ordenar por fecha creación descendente. Filtros por estado (Todas, Pendientes, Completadas) y prioridad (Baja, Media, Alta).
- **REQ-005 (Frontend Interactivo):** Interfaz premium y responsiva en React + Bootstrap.

## 6. Requisitos no funcionales
- **Simplicidad y Ejecución local:** Inicia localmente sin servicios externos.
- **Usabilidad:** Interfaz clara, moderna y limpia. Con confirmación antes de eliminar.
- **Robustez:** Control de errores e integridad de transacciones SQLite.

## 7. Datos (Modelo Task)
| Entidad | Campos principales | Sensible sí/no | Validaciones |
|---|---|---|---|
| Task | id (int, PK), titulo (string, 3-100), descripcion (string, opc), fecha_limite (string, opc), prioridad (string, baja/media/alta), estado (string, pendiente/completada), created_at (datetime), updated_at (datetime) | No | titulo obligatorio, prioridad en enum, estado en enum |

## 8. Base de datos candidata
- **Base:** SQLite (`db.sqlite3`)
- **Justificación:** Base integrada, liviana y transaccional para ejecución monousuario local.

## 9. API Endpoints
| Endpoint | Método | Request Body | Response | Permiso |
|---|---|---|---|---|
| `/api/tasks` | GET | Ninguno (filtros opcionales query) | `[ { "id": 1, "titulo": "Tarea A", ... } ]` | Todos |
| `/api/tasks` | POST | `{ "titulo": "A", "descripcion": "...", "fecha_limite": "...", "prioridad": "media" }` | `{ "id": 1, ... }` | Todos |
| `/api/tasks/{id}` | PUT | `{ "titulo": "B", "descripcion": "...", "fecha_limite": "...", "prioridad": "alta", "estado": "pendiente" }` | `{ "id": 1, ... }` | Todos |
| `/api/tasks/{id}/complete` | PUT | Ninguno | `{ "id": 1, "estado": "completada", ... }` | Todos |
| `/api/tasks/{id}/reopen` | PUT | Ninguno | `{ "id": 1, "estado": "pendiente", ... }` | Todos |
| `/api/tasks/{id}` | DELETE | Ninguno | `{ "status": "deleted", "id": 1 }` | Todos |

## 10. Frontend Pantallas y Componentes
- **Dashboard Principal:** Formulario para agregar/editar tareas, barra de filtros interactiva, lista de tareas en tarjetas modernas, alertas.
- **Componentes:** `TaskForm`, `TaskCard`, `FilterBar`, `Header`, `DeleteConfirmationModal`.

## 11. Criterios de aceptación (AC)
- **AC-001:** Se puede agregar una tarea con título válido y se lista al inicio de forma descendente.
- **AC-002:** El sistema no permite crear tareas con título menor a 3 caracteres o mayor a 100.
- **AC-003:** Se puede editar el título, descripción, prioridad y fecha límite de una tarea existente, actualizando `updated_at`.
- **AC-004:** Se puede marcar como completada y reabrir una tarea, alternando el estado y actualizando `updated_at`.
- **AC-005:** Se puede eliminar una tarea después de aceptar el aviso de confirmación.
- **AC-006:** Los filtros por estado (Todas/Pendientes/Completadas) y prioridad funcionan reactivamente.

## 12. Pruebas esperadas
- **Unitarias/API:** Tests FastAPI TestClient para validar CRUD, reglas de título, y filtros de consulta.

## 13. Fuera de alcance
- Autenticación multiusuario, carga de adjuntos y notificaciones push.