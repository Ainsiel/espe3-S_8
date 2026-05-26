# Aprendizaje de Fábrica

Este archivo registra las lecciones aprendidas para mejorar la calidad, seguridad, y eficiencia operativa del orquestador y sus agentes.

## LEARN-20260525-001
- **Fecha:** 2026-05-25
- **cycle_id:** SETUP
- **agent_id:** factory
- **project_id:** global
- **Tipo:** policy
- **Observación:** Inicialización exitosa de la fábrica de software.
- **Causa raíz:** Creación del sistema de 12 pasos.
- **Acción correctiva:** Mantener el orquestador como único controlador de ciclos.
- **Estado:** APPROVED
- **Aprobador:** PO de Fábrica
## LEARN-20260525-002
- **Fecha:** 2026-05-25
- **cycle_id:** CYCLE-20260525-152517
- **agent_id:** implementer_agent
- **project_id:** global / frontend
- **Tipo:** coding_convention
- **Observación:** La inclusión de comentarios clásicos de HTML (`<!-- -->`) dentro de bloques JSX procesados por Babel Standalone rompe la compilación y genera pantallas en blanco.
- **Causa raíz:** JSX no permite comentarios HTML estándar, ya que son interpretados como elementos inválidos o tokens inesperados en el parser de React/JSX.
- **Acción correctiva:** Utilizar únicamente el formato `{/* comentario */}` para todos los comentarios dentro del bloque JSX en los agentes de generación de interfaces.
- **Estado:** APPROVED
- **Aprobador:** PO de Fábrica

## LEARN-20260525-003
- **Fecha:** 2026-05-25
- **cycle_id:** CYCLE-20260525-152517
- **agent_id:** implementer_agent
- **project_id:** global / core
- **Tipo:** unpack_error
- **Observación:** Modificaciones en agentes de software que bifurcan comportamientos según `project_id` deben mantener el retorno original en todas las ramas para evitar excepciones de descompresión.
- **Causa raíz:** El orquestador espera desempaquetar siempre un tuple de dos elementos (`backend_dir, frontend_dir`) del agente implementador. Al retornar implícitamente `None` en la rama fallback (`else: pass`), se genera un error catastrófico.
- **Acción correctiva:** Asegurar que todas las ramas lógicas de ejecución de los agentes retornen el tipo de dato y estructura exacta esperada por la interfaz del orquestador.
- **Estado:** APPROVED
- **Aprobador:** PO de Fábrica

## LEARN-20260525-004
- **Fecha:** 2026-05-25
- **cycle_id:** SETUP
- **agent_id:** factory
- **project_id:** global / core
- **Tipo:** warning_isolation
- **Observación:** Deprecaciones en bibliotecas estándar (como `datetime.utcnow()` y `datetime.utcfromtimestamp()`) y conflictos en la recolección de pytest en entornos de sandbox dinámicos ensucian la salida de diagnóstico y confunden a nuevos hilos.
- **Causa raíz:** Pytest busca recursivamente archivos `test_*.py` en carpetas como `sandbox/` y `projects/` sin aislamiento explícito. Además, Python 3.12+ depreca métodos UTC antiguos en favor de datetime consciente de zona horaria.
- **Acción correctiva:** Reemplazar el uso de `datetime.utcnow()` con `datetime.now(timezone.utc)` y `datetime.utcfromtimestamp()` con `datetime.fromtimestamp(..., timezone.utc)`. Crear un archivo `pytest.ini` en la raíz que restrinja el campo de acción de pytest a `core/tests` y excluya expresamente directorios dinámicos de sandbox.
- **Estado:** APPROVED
- **Aprobador:** PO de Fábrica
