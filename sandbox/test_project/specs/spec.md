# Especificación SDD: Test Project

## 1. Nombre del sistema
- **Nombre:** Test Project
- **Dueño:** PO de Fábrica (Usuario)
- **Fecha:** 2026-05-26
- **ID de Proyecto:** test_project
- **Estado:** `spec_draft`

## 2. Objetivo
- **Qué problema resuelve:** Quiero una base de datos simple de items
- **Para quién:** Usuarios finales y administradores del sistema.
- **Resultado esperado:** Un sistema web transaccional pequeño, rápido y robusto.

## 3. Usuarios y roles
| Rol | Qué puede hacer | Restricciones |
|---|---|---|
| Administrador | Gestión total del sistema (CRUD de entidades). | Requiere credenciales de administrador. |
| Usuario Final | Consulta de información y operaciones transaccionales básicas. | No puede editar registros creados por otros. |

## 4. Flujos transaccionales
| Flujo | Actor | Entrada | Acción | Salida | Error esperado |
|---|---|---|---|---|---|
| Crear Registro | Administrador | Datos de la entidad | Guarda datos en DB | ID de nuevo registro | Validación de campos falla |
| Listar Registros | Todos | Filtros de búsqueda | Consulta DB | Lista de registros | Sin registros |
| Editar Registro | Administrador | ID + nuevos datos | Modifica registro | Mensaje de éxito | Registro no encontrado |
| Eliminar Registro | Administrador | ID de registro | Borra físicamente o lógico | Confirmación | Registro referenciado |

## 5. Requisitos funcionales
- **REQ-001:** El sistema debe proveer una API REST para la gestión (CRUD) de la entidad principal.
- **REQ-002:** El sistema debe validar que todos los campos requeridos estén presentes y limpios.
- **REQ-003:** El sistema debe persistir datos de manera íntegra.
- **REQ-004:** El frontend debe listar los registros actuales y permitir crear/editar a través de formularios limpios.

## 6. Requisitos no funcionales
- **Seguridad:** Validación rigurosa de entradas para prevenir inyecciones.
- **Rendimiento:** Tiempos de respuesta API por debajo de 200ms.
- **Disponibilidad:** Base de datos persistente.
- **Observabilidad:** Logs estructurados de transacciones.
- **Accesibilidad:** Uso de Bootstrap para responsividad total en móvil y escritorio.
- **Mantenibilidad:** Separación clara entre backend (FastAPI) y frontend.

## 7. Datos
| Entidad | Campos principales | Sensible sí/no | Retención | Validaciones |
|---|---|---|---|---|
| Item | id (int), nombre (string), descripcion (string), cantidad (int), precio (float) | No | Permanente | precio >= 0, cantidad >= 0 |

## 8. Base de datos candidata
- **Base:** LiteSQL (SQLite)
- **Justificación:** Ideal para app pequeña transaccional sin concurrencia gigante.
- **Migraciones requeridas:** Tabla única inicial.

## 9. API
| Endpoint | Método | Request | Response | Permiso |
|---|---|---|---|---|
| `/api/items` | GET | Ninguno | `[ { "id": 1, ... } ]` | Todos |
| `/api/items` | POST | `{ "nombre": "A", "precio": 10.0 }` | `{ "id": 1, ... }` | Administrador |
| `/api/items/{id}` | PUT | `{ "nombre": "B", ... }` | `{ "id": 1, ... }` | Administrador |
| `/api/items/{id}` | DELETE | Ninguno | `{ "status": "deleted" }` | Administrador |

## 10. Frontend
- **Pantallas:** Vista de Dashboard Principal, Formulario de Creación/Edición, Modal de Confirmación de Borrado.
- **Componentes:** `ItemTable`, `ItemForm`, `Header`, `NotificationBanner`.
- **Estados loading/error/empty:** Indicador spinner durante GET, alertas Bootstrap rojas ante errores de API, mensaje instructivo cuando la lista está vacía.
- **Validaciones:** Campos no vacíos en JS antes de enviar.

## 11. Criterios de aceptación
- **AC-001:** Se puede agregar un nuevo item con nombre y precio, apareciendo inmediatamente en la tabla.
- **AC-002:** El sistema no permite precios negativos.
- **AC-003:** La API devuelve códigos HTTP estándar (200, 201, 400, 404).

## 12. Pruebas esperadas
- **Unitarias:** Pruebas de validación de campos del modelo.
- **API/contrato:** Test suite de FastAPI (TestClient) para endpoints CRUD.
- **UI:** Render básico de tabla y inputs.

## 13. Fuera de alcance
- **OOS-001:** Pasarela de pagos integrada.
- **OOS-002:** Autenticación OAuth de terceros.

## 14. Preguntas abiertas
- **Q-001:** ¿Se requiere persistir imágenes por cada Item? (needs_user_input - Default: No).