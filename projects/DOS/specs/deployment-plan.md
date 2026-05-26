# Plan de Despliegue (Deployment Plan - TaskLiteJota)

- **Entorno Objetivo:** Local / Académico
- **Método:** Ejecución local con Uvicorn para el backend y navegación del frontend estático en el browser.

## Pasos Operativos
1. Iniciar backend FastAPI usando Uvicorn:
   `uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`
2. Abrir el archivo `frontend/index.html` en cualquier navegador web moderno (Chrome, Safari, Firefox).
3. Verificar persistencia agregando una tarea de prueba y reiniciando el backend.