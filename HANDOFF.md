# Documentación de Traspaso (HANDOFF.md)

Este documento sirve como bitácora y estado de situación formal para la fábrica de software agentica **FabricaWebTransaccionalSDD**. Contiene información clave para los agentes y desarrolladores que inicien nuevos hilos de proyecto.

- **Última Actualización:** 2026-05-26 12:14:58 UTC
- **Estado de la Fábrica:** `OPERATIONAL` (Activa, Limpia y Validada para Nuevos Ciclos)

---

## 1. Métricas Acumuladas del Sistema
Estas métricas son calculadas dinámicamente de forma acumulada desde el historial en `.factory/runs/`:

| Métrica | Valor Registrado |
|---|---|
| Ciclos de Orquestación Ejecutados | 19 |
| Proyectos Gestionados | 5 |
| Consumo Acumulado de Tokens | 382115 |
| Costo Estimado Acumulado | $0.068731 |
| Llamadas a Herramientas | 0 |

---

## 2. Documentos Fundacionales de la Fábrica
Para entender los lineamientos, stack y políticas operativas antes de iniciar código:

1. [01. Constitución y Especificación de la Fábrica](file:///Users/jota/Desktop/GEMINI/Fabrica BÁSICA APP WEB/01_Constitucion_y_Especificacion_Fabrica.md) - Misión, stack técnico autorizado y reglas de no improvisación.
2. [02. Arquitectura, Stack y Flujos SDD](file:///Users/jota/Desktop/GEMINI/Fabrica BÁSICA APP WEB/02_Arquitectura_Stack_y_Flujos_SDD.md) - Monolito modular, FastAPI, React, SQLite/MySQL y ciclo de desarrollo.
3. [03. Agentes, Skills, Herramientas y Permisos](file:///Users/jota/Desktop/GEMINI/Fabrica BÁSICA APP WEB/03_Agentes_Skills_Herramientas_y_Permisos.md) - Responsabilidad y permisos específicos de cada rol agéntico.
4. [04. Orquestador, Ciclo de 12 Pasos y Operabilidad](file:///Users/jota/Desktop/GEMINI/Fabrica BÁSICA APP WEB/04_Orquestador_Ciclo_12_Pasos_Operabilidad.md) - La máquina de estados operativa y gates de calidad obligatorios.

---

## 3. Estado de los Directorios y Entornos

### 3.1 Proyectos Activos (Directorio `projects/`)
- **Proyecto ID:** `EJEMPLO_DOS` (Especificación: Sí) | [Abrir Directorio](file://C:\Users\Ainsi\Desktop\proyectos\espe3-S_8\projects\EJEMPLO_DOS)
- **Proyecto ID:** `EJEMPLO_UNO` (Especificación: Sí) | [Abrir Directorio](file://C:\Users\Ainsi\Desktop\proyectos\espe3-S_8\projects\EJEMPLO_UNO)
- **Proyecto ID:** `test_project` (Especificación: Sí) | [Abrir Directorio](file://C:\Users\Ainsi\Desktop\proyectos\espe3-S_8\projects\test_project)

*Nota: Los proyectos listados sirven de referencia histórica para implementaciones transaccionales y modularización.*

### 3.2 Sandbox Temporal (`sandbox/`)
- **Estado actual:** `CLEAN` (100% libre de residuos).
- La carpeta temporal `sandbox/` ha sido completamente vaciada de ejecuciones anteriores y está lista para que el orquestador cree y valide nuevos proyectos de forma aislada.

### 3.3 Log de Aprendizajes (`Aprendizaje.md`)
- El archivo global [Aprendizaje.md](file:///Users/jota/Desktop/GEMINI/Fabrica BÁSICA APP WEB/Aprendizaje.md) está plenamente integrado. Contiene lecciones aprendidas aprobadas (como evitar comentarios HTML clásicos en JSX compilado por Babel y mantener la estructura exacta del tuple retornado por los agentes) que previenen la regresión de errores en nuevos ciclos.

---

## 4. Instrucciones para Iniciar Nuevo Hilo de Proyecto

Para un nuevo agente o desarrollador que tome el control en un nuevo hilo:

1. **Leer la Constitución:** Comienza leyendo `01_Constitucion_y_Especificacion_Fabrica.md` y `04_Orquestador_Ciclo_12_Pasos_Operabilidad.md` para familiarizarte con las reglas obligatorias de desarrollo de la fábrica.
2. **Iniciar Menú Interactivo:** Ejecuta el panel interactivo en la terminal:
   ```bash
   python chat.py
   ```
3. **Crear un Nuevo Proyecto:**
   - Selecciona la **Opción 1** ("Iniciar nuevo Ciclo de Desarrollo SDD").
   - Ingresa un `ID de proyecto` único (ej. `gestion_inventario_app`).
   - Ingresa el `Nombre del proyecto`.
   - Proporciona la descripción detallada del requerimiento funcional.
4. **Validación Automática:** El orquestador guiará el desarrollo por las fases SDD, aislará el código en `sandbox/<project_id>`, ejecutará las suites de test automáticas y, tras pasar todos los gates, entregará los artefactos finales validados y consolidados en la carpeta `projects/<project_id>`.

---

## 5. Integridad Técnica y Caché
- **Index:** Regenerado con éxito en `.factory/index.json`.
- **Caché:** Activa y óptima en `.factory/cache.json`.
- **Pytest:** Configurado correctamente en `pytest.ini` para evitar búsquedas recursivas que contaminen los entornos temporales.