# 02. Arquitectura, Stack y Flujos SDD

**Nombre:** FabricaWebTransaccionalSDD  
**Versión:** 1.0.0  
**Fecha:** 2026-05-25  
**Estado:** `complete`  
**Propósito:** definir la arquitectura objetivo, stack gobernado, repositorios, ambientes, CI/CD, seguridad, datos, APIs, flujo SDD completo, roadmap y anti-patrones para una fábrica básica de sistemas web transaccionales pequeños.

---

## 1. Principio arquitectónico

La fábrica debe ser **simple primero**:

```text
monolito web modular pequeño
+ API FastAPI
+ frontend React/Bootstrap
+ una base de datos principal
+ specs versionadas
+ orquestador por estados
+ agentes mínimos
+ pruebas obligatorias
+ trazabilidad completa
```

No se parte con microservicios, colas, Kubernetes, multi-cloud, event sourcing, CQRS ni herramientas enterprise salvo que la spec del proyecto lo exija y el usuario lo apruebe.

---

## 2. Vista de arquitectura objetivo

```text
Usuario / Product Owner
        |
        v
Work Order / Solicitud
        |
        v
Orquestador de Ciclo 12 Pasos
        |
        +--> Agente Especificador SDD  [siempre primero]
        +--> Agente Clarificador / Checklist
        +--> Context Manager + Index + Cache
        +--> Agente Arquitecto / Plan
        +--> Agente Task Planner / Analyze
        +--> Agente Implementador
        +--> Agente QA / Validador
        +--> Agente Seguridad / Operación
        |
        v
Repositorio del Proyecto
        |
        +-- specs/<feature>/
        +-- backend/ FastAPI Python3
        +-- frontend/ React Bootstrap
        +-- db/ migraciones o scripts
        +-- tests/
        +-- docs/
        |
        v
CI/CD con gates
        |
        +-- validar SDD
        +-- validar trazabilidad
        +-- validar dependencias
        +-- ejecutar pruebas
        +-- revisar seguridad
        +-- generar PR/deploy con aprobación
```

---

## 3. Componentes

| Componente | Responsabilidad | No debe hacer |
|---|---|---|
| Orquestador | Controlar estado, agentes, permisos, presupuesto, gates y cierre. | Implementar código directamente. |
| Agente Especificador SDD | Pedir y mejorar la spec simple al inicio de cada ciclo. | Elegir stack no aprobado o escribir código. |
| Context Manager | Preparar contexto mínimo desde index/cache/memoria. | Volcar historial completo. |
| Index | Buscar specs, código, contratos, tests y aprendizaje. | Sustituir decisiones humanas. |
| Cache | Reusar resultados por hash de spec, plan, commit, tool y modelo. | Cachear secretos o datos sensibles. |
| Tool Registry | Exponer skills permitidas con schema y permisos. | Permitir shell libre. |
| Policy Engine | Bloquear dependencias, acciones y estados inválidos. | Delegar reglas críticas al LLM. |
| CI/CD | Ejecutar validaciones y gates. | Aceptar cambios sin spec. |
| Observability | Logs, métricas, trazas y reportes. | Ocultar fallos. |
| Learning Loop | Registrar aprendizajes aprobados. | Aprender automáticamente sin validación. |

---

## 4. Stack aprobado y prohibido

### 4.1 Stack aprobado inicial

| Capa | Aprobado |
|---|---|
| Backend | Python 3, FastAPI |
| Frontend | React, Bootstrap |
| Datos | MySQL, LiteSQL, MongoDB |
| API | REST sobre HTTP, OpenAPI generado por FastAPI cuando aplique |
| Documentación | Markdown |
| Especificación | Spec SDD simple + artefactos `spec.md`, `plan.md`, `tasks.md`, `analyze-report.md` |
| Orquestación | Orquestador propio simple por estados o workflow local controlado |
| Logs | Archivos JSONL por ciclo en el repo o storage autorizado |
| Tests | Herramientas `TBD` por proyecto; deben ser aprobadas antes de implementación |

### 4.2 Política de selección de base de datos

| Caso | Base recomendada | Regla |
|---|---|---|
| CRUD transaccional, relaciones, reportes simples | MySQL | Default para producción transaccional. |
| Prototipo local o app pequeña sin concurrencia alta | LiteSQL | `TBD`: confirmar tecnología exacta antes de implementar. |
| Datos tipo documento, formularios flexibles, estructura variable | MongoDB | Requiere justificación en `plan.md`. |
| Más de una base en un proyecto | No default | Requiere ADR y aprobación. |

### 4.3 Stack prohibido por defecto

| Elemento | Estado |
|---|---|
| Framework backend distinto de FastAPI | Prohibido sin aprobación. |
| Frontend distinto de React/Bootstrap | Prohibido sin aprobación. |
| Librerías no listadas ni presentes en repo | Prohibidas sin aprobación. |
| Shell libre | Prohibido. |
| Acceso directo a producción por agentes | Prohibido. |
| Lectura de secretos por agentes | Prohibido por defecto. |
| Deploy productivo sin gate | Prohibido. |
| Código generado sin spec | Prohibido. |

---

## 5. Estructura recomendada de repositorio

```text
repo/
  .factory/
    constitution.md
    policies/
      dependency-policy.yml
      tool-policy.yml
      security-policy.yml
      budget-policy.yml
    workflows/
      cycle-12-steps.yml
    runs/
      <cycle_id>/
        state.json
        cycle_log.jsonl
        usage_ledger.jsonl
        user_updates.log
        validation-report.md
    memory/
      Aprendizaje.Fabrica.md

  .specify/
    memory/
      constitution.md
    templates/
      spec-template.md
      plan-template.md
      tasks-template.md
      checklist-template.md

  specs/
    001-feature-name/
      work_order.json
      spec.md
      clarifications.md
      checklist.md
      context-pack.md
      plan.md
      data-model.md
      contracts/
        openapi.yaml
      tasks.md
      analyze-report.md
      traceability-matrix.md
      test-plan.md
      validation-report.md
      security-review.md
      deployment-plan.md
      rollback-plan.md
      final-report.md

  backend/
    app/
    tests/
    pyproject.toml or requirements.txt

  frontend/
    src/
    tests/
    package.json

  db/
    migrations/
    seeds/
    fixtures/

  docs/
    adr/
    runbooks/
```

---

## 6. Ambientes

| Ambiente | Uso | Reglas |
|---|---|---|
| `local` | Desarrollo humano o agente en sandbox local. | Sin secretos reales por defecto. |
| `agent-sandbox` | Implementación y pruebas por agentes. | FS limitado, red bloqueada/allowlist, comandos allowlist, timeout. |
| `staging` | Validación previa a release. | Datos sintéticos o anonimizados. |
| `production` | Operación real. | Deploy solo con gate humano o política explícita. |

Ambientes adicionales (`ephemeral-pr`, `preprod`) quedan `TBD` por proyecto.

---

## 7. Integración CI/CD mínima

### 7.1 Pipeline recomendado

```text
push / pull_request
  -> validate_sdd_artifacts
  -> validate_traceability
  -> validate_dependency_policy
  -> backend_static_checks
  -> backend_tests
  -> frontend_static_checks
  -> frontend_tests
  -> api_contract_checks
  -> security_basic_scan
  -> build
  -> staging_deploy_dry_run
  -> human_gate_if_needed
  -> deploy
  -> smoke_tests
  -> observe
  -> close
```

### 7.2 Gates obligatorios

| Gate | Bloquea si |
|---|---|
| `sdd_artifacts` | falta spec, plan, tasks o analyze. |
| `sdd_spec_first` | el Agente Especificador SDD no fue llamado al inicio del ciclo. |
| `requirements_quality` | faltan criterios de aceptación o hay preguntas críticas abiertas. |
| `context_grounded` | no hay evidencia de repo/contexto para plan. |
| `dependency_policy` | hay dependencia no aprobada. |
| `cross_artifact_analysis` | requisito sin tarea, tarea sin requisito o requisito sin prueba. |
| `tests` | falla prueba crítica. |
| `security` | hay secreto, vulnerabilidad crítica o permiso inválido. |
| `budget` | se supera presupuesto de tokens/herramientas sin aprobación. |
| `user_informed` | faltan mensajes de plan, progreso o cierre. |

---

## 8. Seguridad

### 8.1 Controles mínimos

- Validación de entrada en API.
- Validación de salida en API.
- Autenticación y autorización `TBD` por proyecto.
- Roles y permisos definidos en spec.
- No registrar secretos.
- No registrar PII innecesaria.
- Protección básica contra inyección de prompts en documentos y tool results.
- Allowlist de comandos.
- Revisión de dependencias.
- Escaneo de secretos.
- Dry-run para migraciones, PR, deploy y cambios externos.

### 8.2 Política de secretos

```text
Agentes no leen secretos.
Herramientas no imprimen secretos.
Logs redaccionan valores sensibles.
Pruebas usan fixtures sintéticos.
Producción requiere gate humano.
```

### 8.3 Amenazas básicas por proyecto

Cada `security-review.md` debe cubrir:

| Riesgo | Pregunta |
|---|---|
| Acceso indebido | ¿Quién puede crear, leer, actualizar o borrar registros? |
| Validación de datos | ¿Qué inputs pueden romper la transacción? |
| Exposición de datos | ¿Qué campos son sensibles? |
| Integridad | ¿Qué reglas deben ser atómicas? |
| Auditoría | ¿Qué eventos deben registrarse? |
| Disponibilidad | ¿Qué ocurre si falla la base de datos? |

---

## 9. Datos

### 9.1 Reglas de modelo de datos

- Toda entidad transaccional debe tener owner funcional.
- Todo campo sensible debe marcarse.
- Todo cambio de esquema debe tener migración o estrategia de compatibilidad.
- Todo dato de prueba debe ser sintético o anonimizado.
- Toda retención de datos queda `TBD` si el usuario no la define.
- Todo endpoint que escribe datos debe tener prueba de validación.

### 9.2 Artefacto `data-model.md`

```markdown
# Data Model

## Entities

| Entity | Purpose | Storage | Sensitive | Owner |
|---|---|---|---|---|

## Fields

| Entity | Field | Type | Required | Validation | Sensitive |
|---|---|---|---|---|---|

## Transactions

| Transaction | Entities | Atomicity | Failure behavior |
|---|---|---|---|

## Migrations

| Migration | Reason | Backward compatible | Rollback |
|---|---|---|---|
```

---

## 10. APIs y eventos

### 10.1 API

- Default: REST JSON.
- Contrato: OpenAPI si hay FastAPI.
- Versionado: `TBD` por proyecto; default `/api/v1` si no hay restricción.
- Cada endpoint debe mapear a requisito y prueba.
- Cada error relevante debe estar especificado.

### 10.2 Eventos

No se usan eventos por defecto.  
Si la spec requiere eventos, debe generarse `events.md` con:

```markdown
# Events

| Event | Producer | Consumer | Payload | Retry | Idempotency |
|---|---|---|---|---|---|
```

---

## 11. Flujo SDD completo obligatorio

El flujo de software de la fábrica es:

```text
Constitution
-> Specify
-> Clarify
-> Checklist
-> Context Grounding
-> Plan
-> Plan Validation
-> Tasks
-> Analyze
-> Implement
-> Validate
-> PR/Deploy
-> Observe
-> Close
```

### 11.1 Regla especial del usuario

Antes de `Specify`, el orquestador debe llamar siempre al:

```text
Agente Especificador SDD
```

Este agente debe pedir o completar la estructura SDD simple, detectar vacíos y producir:

- `sdd_intake.md`
- `missing_fields.md`
- `spec_draft.md`
- `questions.md`

Si faltan datos críticos, el ciclo sigue hasta `Clarify` y queda en `needs_user_input`.

---

## 12. Mapa entre ciclo de 12 pasos y SDD

| Paso del ciclo obligatorio | Fase SDD relacionada | Artefacto |
|---|---|---|
| 1. Planificar ciclo | Work Order / Constitution | `state.json` |
| 2. Index/cache | Context Grounding | `context-cache.json` |
| 3. Aprendizaje | Context Grounding | `Aprendizaje.md` |
| 4. Logs por agente | Todas | `cycle_log.jsonl` |
| 5. Tokens/hora inicio | Todas | `usage_ledger.jsonl` |
| 6. Informar plan | Todas | `user_updates.log` |
| 7. Ejecutar SDD | Todas | artefactos `specs/` |
| 8. Pruebas | Validate | `validation-report.md` |
| 9. Aprender/reintentar | Close / Learning | `Aprendizaje.md` |
| 10. Actualizar index/cache | Close | `index-report.md` |
| 11. Informar resultado | Close | `final-report.md` |
| 12. Informar cierre/tokens | Close | `usage_ledger.jsonl` |

---

## 13. Roadmap de implementación

### Fase 1: Fábrica mínima operativa

- Crear constitución.
- Crear templates SDD simples.
- Crear orquestador por estados.
- Crear Agente Especificador SDD.
- Crear logs y usage ledger.
- Definir gates manuales.
- Ejecutar validación manual.

### Fase 2: Validación automática básica

- Validar existencia de artefactos.
- Validar trazabilidad requisito→tarea→prueba.
- Validar stack aprobado.
- Validar que el agente SDD fue llamado primero.
- Validar que hubo pruebas.

### Fase 3: Implementación controlada

- Implementador en sandbox.
- Skills allowlist.
- Aplicación de parches por tarea.
- Pruebas incrementales.
- Reporte de cambios.

### Fase 4: CI/CD simple

- Pull requests.
- Gates en CI.
- Staging deploy dry-run.
- Smoke tests.
- Cierre con reporte.

### Fase 5: Operabilidad

- Métricas.
- Dashboards.
- Alertas.
- Aprendizaje gobernado.
- Detección de drift.

---

## 14. Anti-patrones

Evitar siempre:

1. Implementar desde prompt libre.
2. Omitir el Agente Especificador SDD.
3. Saltarse el orquestador.
4. Saltarse cualquiera de los 12 pasos.
5. Aceptar “hacer frontend” como tarea.
6. Aceptar “hacer backend” como tarea.
7. Usar dependencias por preferencia del agente.
8. Usar más de una base de datos sin justificación.
9. Crear microservicios para sistemas pequeños sin necesidad.
10. Crear specs enormes que nadie revisa.
11. Tratar `spec.md` como decoración.
12. Ejecutar shell sin allowlist.
13. Dejar que el agente apruebe su propio trabajo.
14. Guardar secretos en logs o cache.
15. No medir tokens, costo y tiempo.
16. No informar al usuario antes o después del ciclo.
17. Cerrar sin pruebas.
18. Desplegar sin rollback.
19. Actualizar memoria sin aprobación.
20. Resolver ambigüedades críticas inventando.

---

## 15. Checklist de arquitectura

- [x] Arquitectura objetivo definida.
- [x] Stack aprobado/prohibido definido.
- [x] Repositorio recomendado definido.
- [x] Ambientes definidos.
- [x] CI/CD básico definido.
- [x] Seguridad mínima definida.
- [x] Datos definidos.
- [x] APIs/eventos definidos.
- [x] Flujo SDD completo definido.
- [x] Roadmap definido.
- [x] Anti-patrones definidos.
