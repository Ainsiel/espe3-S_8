# Aclaraciones de Requisitos (TaskLiteJota)

## 1. Supuestos asumidos
- **PERSISTENCIA:** Los datos se guardarán en una base de datos SQLite local (`db.sqlite3`) alojada en el backend.
- **AUTENTICACIÓN:** Sin autenticación para simplificar la ejecución académica local.
- **FORMATO FECHA LÍMITE:** Se almacena como texto simple o formato ISO date (YYYY-MM-DD) y se valida en frontend.
- **ESTADO INICIAL:** Siempre se inicializa en 'pendiente'.

## 2. Decisiones de diseño
- Los datos de entrada se validan en frontend con JS/React y en backend con Pydantic.
- Si la tarea no se encuentra al editar o eliminar, se responde con HTTP 404.