# Aclaraciones de Requisitos

## 1. Supuestos asumidos
- **PERSISTENCIA:** Los datos se guardarán en una base de datos SQLite local (`db.sqlite3`) alojada en el backend.
- **IMÁGENES:** Se confirma que NO se persistirán imágenes por cada registro, solo URLs de texto simples si aplica (según Q-001 de la especificación).
- **AUTENTICACIÓN:** Para esta app pequeña se utilizará una autenticación básica por tokens simulados en cabecera HTTP o bypass directo para facilitar el desarrollo local.

## 2. Decisiones de diseño
- Los datos de entrada del frontend se validarán primero en el navegador de forma reactiva y luego con Pydantic en FastAPI de manera estricta.