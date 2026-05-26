# Aclaraciones de Requisitos (EventPass)

## 1. Supuestos asumidos
- **PERSISTENCIA:** Los datos se guardarán en una base de datos SQLite local (`db.sqlite3`) alojada en el backend.
- **AUTENTICACIÓN:** Autenticación por token JWT en header `Authorization: Bearer <token>`, con expiración de 60 minutos.
- **COMPORTAMIENTO DE RESERVAS:** Restringido estrictamente a 1 entrada por usuario por evento. Las reservas en eventos agotados no se permiten.
- **CANCELACIÓN:** Devuelve la entrada al stock disponible y cambia el estado a 'cancelada'.

## 2. Decisiones de diseño
- Las validaciones críticas se ejecutarán en frontend con React y de forma estricta en el backend con modelos Pydantic.