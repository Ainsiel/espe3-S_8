# Modelo de Datos (TaskLiteJota)

## 1. Entidades
| Entidad | Propósito | Almacenamiento | Sensible | Owner |
|---|---|---|---|---|
| Task | Almacena las tareas personales del usuario | SQLite | No | PO de Fábrica |

## 2. Campos
| Entidad | Campo | Tipo | Requerido | Validación | Sensible |
|---|---|---|---|---|---|
| Task | id | INTEGER | Sí (PK, Auto) | Autoincrementado | No |
| Task | titulo | VARCHAR(100)| Sí | len(x) >= 3 and len(x) <= 100 | No |
| Task | descripcion | TEXT | No | Opcional | No |
| Task | fecha_limite | VARCHAR(50) | No | Opcional (ISO Date string) | No |
| Task | prioridad | VARCHAR(20) | Sí | En enum: baja, media, alta | No |
| Task | estado | VARCHAR(20) | Sí | En enum: pendiente, completada | No |
| Task | created_at | DATETIME | Sí | Seteado en inserción | No |
| Task | updated_at | DATETIME | Sí | Actualizado en edición/estado | No |

## 3. Comportamiento ante Fallo
- Toda escritura sobre `Task` debe ser atómica. Ante excepciones se ejecuta rollback de la sesión.