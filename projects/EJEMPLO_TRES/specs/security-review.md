# Revisión de Seguridad (Security Review - EventPass)

- **ID de Proyecto:** EJEMPLO_TRES
- **Fecha de Análisis:** Análisis realizado sobre el código de EventPass.

## Análisis de Amenazas

| Riesgo | Pregunta | Evaluación de Seguridad | Estado |
|---|---|---|---|
| Inyección SQL | ¿Es vulnerable SQLite a inyecciones? | SQLAlchemy utiliza consultas parametrizadas a nivel de ORM, lo que bloquea por completo la inyección de SQL. | PROTEGIDO |
| Fuga de Contraseñas | ¿Cómo se guardan las contraseñas? | Las contraseñas se guardan encriptadas usando passlib con el algoritmo bcrypt. | PROTEGIDO |
| Reservas Agotadas | ¿Se puede reservar sin stock disponible? | El backend valida atómicamente la disponibilidad de stock antes de crear la reserva. | PROTEGIDO |
| Reservas Duplicadas | ¿Se puede reservar dos veces el mismo evento? | Se utiliza un índice único UNIQUE(user_id, event_id) a nivel de base de datos y validaciones en la API. | PROTEGIDO |
| Modificación No Autorizada | ¿Puede un usuario cancelar la reserva de otro? | El endpoint de cancelación verifica estrictamente que `user_id` de la reserva coincida con el del token JWT. | PROTEGIDO |

## Hallazgos de Secretos
- Cero llaves de API o tokens expuestos en el código de EventPass.