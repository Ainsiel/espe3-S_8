# 04. Orquestador, Ciclo de 12 Pasos y Operabilidad

**Nombre:** FabricaWebTransaccionalSDD  
**Versión:** 1.0.0  
**Fecha:** 2026-05-25  
**Estado:** `complete`  
**Propósito:** definir la misión del orquestador, máquina de estados, ciclo obligatorio de 12 pasos, estado canónico, routing, context manager, index/cache, logs, tokens, costos, circuit breakers, validaciones, retries, aprendizaje, observabilidad y checklist de producción.

---

## 1. Misión del orquestador

El orquestador es el controlador operativo de la fábrica. No es un chat libre ni un agente autónomo sin límites.

Debe:

1. recibir la solicitud;
2. normalizarla como Work Order;
3. llamar siempre primero al Agente Especificador SDD;
4. ejecutar siempre el ciclo de 12 pasos;
5. informar al usuario antes, durante y al cerrar;
6. controlar agentes, skills, permisos, herramientas y presupuesto;
7. aplicar flujo SDD completo;
8. ejecutar pruebas y validación;
9. registrar logs, tokens, costo y tiempos;
10. actualizar aprendizaje, index y cache cuando corresponda;
11. cerrar con estado controlado.

---

## 2. Estados cerrados

```text
complete
needs_user_input
not_answerable
error
```

### 2.1 Significado

| Estado | Uso |
|---|---|
| `complete` | Meta cumplida, validaciones pasan, evidencias registradas. |
| `needs_user_input` | Falta decisión o dato crítico del usuario. |
| `not_answerable` | La decisión exige evidencia y no existe evidencia suficiente. |
| `error` | Falló una herramienta, validación, política o ejecución no recuperable. |

---

## 3. Máquina de estados del ciclo

```text
INIT
  -> NORMALIZE_WORK_ORDER
  -> PLAN_CYCLE
  -> LOAD_INDEX_CACHE
  -> READ_LEARNING
  -> START_LOGS
  -> START_USAGE_LEDGER
  -> INFORM_USER_PLAN
  -> CALL_SDD_SPEC_AGENT
  -> SPECIFY
  -> CLARIFY
  -> CHECKLIST
  -> CONTEXT_GROUNDING
  -> PLAN
  -> PLAN_VALIDATION
  -> TASKS
  -> ANALYZE
  -> IMPLEMENT
  -> VALIDATE
  -> PR_DEPLOY
  -> OBSERVE
  -> LEARNING_AND_RETRY_DECISION
  -> UPDATE_INDEX_CACHE
  -> INFORM_RESULT
  -> CLOSE
```

### 3.1 Transiciones críticas

| Transición | Condición |
|---|---|
| `PLAN_CYCLE -> LOAD_INDEX_CACHE` | `cycle_id` creado y objetivo definido. |
| `INFORM_USER_PLAN -> CALL_SDD_SPEC_AGENT` | usuario informado del plan, agentes, skills, herramientas, permisos, presupuesto y gates. |
| `CALL_SDD_SPEC_AGENT -> SPECIFY` | agente SDD iniciado y logueado. |
| `CLARIFY -> CHECKLIST` | preguntas críticas respondidas o estado `needs_user_input`. |
| `CHECKLIST -> CONTEXT_GROUNDING` | requisitos claros, testables y con aceptación. |
| `PLAN -> PLAN_VALIDATION` | plan usa stack aprobado y evidencia de contexto. |
| `TASKS -> ANALYZE` | tasks atómicas y trazables. |
| `ANALYZE -> IMPLEMENT` | sin contradicciones críticas. |
| `IMPLEMENT -> VALIDATE` | implementación por tasks, sin scope creep. |
| `VALIDATE -> PR_DEPLOY` | pruebas críticas pasan. |
| `OBSERVE -> CLOSE` | métricas y cierre registrados. |

---

## 4. Ciclo obligatorio de 12 pasos

Este ciclo debe ejecutarse en todo diseño y en cada ciclo agéntico de la fábrica.

### Paso 1. Planifica nuevo ciclo

**Meta:** definir objetivo, producto esperado y regla de no inventar.

```yaml
step_id: 1_plan_cycle
required: true
owner: orchestrator
outputs:
  - state.json
  - work_order.json
gate:
  goal_defined: true
  no_invention_rule_set: true
```

El orquestador debe declarar:

- `cycle_id`
- `trace_id`
- `work_order_id`
- objetivo
- producto esperado
- alcance
- fuera de alcance
- stack aplicable
- presupuesto inicial
- condición de cierre
- regla: no inventar.

### Paso 2. Usa siempre Index y Cache de Contexto

**Meta:** evitar contexto gigante y reutilizar evidencia.

```yaml
step_id: 2_load_index_cache
owner: orchestrator
skills:
  - load_index_cache
outputs:
  - context-cache.json
  - retrieval-plan.json
```

Debe cargar:

- índice de specs;
- índice de código;
- índice de docs;
- índice de tests;
- índice de aprendizaje;
- cache de contexto;
- cache de tool results;
- cache de validaciones.

### Paso 3. Analiza `Aprendizaje.md` de fábrica, proyecto y agentes

**Meta:** usar aprendizajes validados sin contaminar el ciclo.

```yaml
step_id: 3_read_learning
owner: orchestrator
inputs:
  - .factory/memory/Aprendizaje.Fabrica.md
  - .factory/memory/Aprendizaje.Proyecto.<project_id>.md
  - .factory/memory/agents/Aprendizaje.<agent_id>.md
```

Reglas:

- ignorar aprendizaje no aprobado;
- no cargar secretos;
- usar máximo contexto definido por presupuesto;
- registrar qué aprendizajes influyeron en el ciclo.

### Paso 4. Inicia registro de logs para trazabilidad por cada agente

**Meta:** abrir trazas antes de ejecutar agentes.

```yaml
step_id: 4_start_logs
owner: orchestrator
outputs:
  - cycle_log.jsonl
  - agent_logs/<agent_id>.jsonl
```

Cada log debe incluir:

```json
{
  "timestamp": "datetime",
  "cycle_id": "string",
  "trace_id": "string",
  "agent_id": "string",
  "phase": "string",
  "event": "string",
  "status": "running|success|blocked|error",
  "evidence_path": "string|null"
}
```

### Paso 5. Registra consumo de tokens y hora de inicio

**Meta:** medir costo y presupuesto desde el inicio.

```yaml
step_id: 5_start_usage
owner: orchestrator
outputs:
  - usage_ledger.jsonl
```

Campos mínimos:

```json
{
  "cycle_id": "string",
  "started_at": "datetime",
  "model": "string",
  "input_tokens": 0,
  "cached_input_tokens": 0,
  "output_tokens": 0,
  "tool_calls": 0,
  "estimated_cost": 0,
  "budget": {
    "max_tokens": 0,
    "max_tool_calls": 0,
    "max_duration_minutes": 0
  }
}
```

Si el proveedor no entrega tokens reales, registrar `not_available` y usar estimación marcada como `estimated`.

### Paso 6. Informa al usuario el plan en detalle

**Meta:** transparencia obligatoria antes de ejecutar.

El mensaje al usuario debe incluir:

```markdown
## Plan de ciclo

- cycle_id:
- objetivo:
- producto esperado:
- agente inicial obligatorio: sdd_spec_agent
- agentes:
- skills:
- herramientas:
- permisos:
- presupuesto:
- gates:
- riesgos:
- condición de bloqueo:
```

No avanzar a ejecución si este mensaje no fue emitido y registrado.

### Paso 7. Ejecuta el plan dentro del ciclo usando flujo SDD

**Meta:** ejecutar SDD completo informando avance.

Flujo obligatorio:

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

Sub-reglas:

- `sdd_spec_agent` siempre antes de `Specify`;
- no pasar a `Plan` con preguntas críticas abiertas;
- no pasar a `Implement` sin `Analyze`;
- no pasar a `Close` sin `Validate`.

### Paso 8. Ejecuta pruebas de validación

**Meta:** probar siempre.

Pruebas mínimas:

| Tipo | Obligatorio si |
|---|---|
| requisitos/checklist | siempre |
| trazabilidad | siempre |
| backend | hay backend |
| frontend | hay frontend |
| integración | hay DB/API |
| contrato API | hay endpoints |
| seguridad básica | hay auth/datos/deploy |
| smoke | hay deploy |

Salida:

```text
validation-report.md
test-report.md
quality-gate.json
```

### Paso 9. Si no cumple, registra `Aprendizaje.md` y repite o bloquea

**Meta:** no repetir errores sin aprendizaje.

Si falla:

```text
1. registrar finding;
2. clasificar causa;
3. actualizar Aprendizaje.md si aplica;
4. decidir retry, rollback o bloqueo;
5. informar al usuario;
6. volver a la fase SDD correcta.
```

Reintentos:

```yaml
max_retries_per_phase: 1
max_total_cycle_retries: 2
on_exceeded: "needs_user_input|error"
```

### Paso 10. Si hay nuevos archivos de sistema, actualiza index y cache

**Meta:** mantener contexto reproducible.

Actualizar si cambian:

- constitución;
- spec;
- clarifications;
- checklist;
- context-pack;
- plan;
- tasks;
- analyze;
- contracts;
- data-model;
- tests;
- code;
- aprendizaje;
- policies.

Salida:

```text
index-update-report.md
cache-update-report.md
```

### Paso 11. Informa al usuario y registra resultado del plan y ciclo

**Meta:** cierre operacional claro.

Debe informar:

- qué se hizo;
- qué artefactos se crearon o modificaron;
- qué gates pasaron/fallaron;
- qué pruebas se ejecutaron;
- qué riesgos quedan;
- estado final;
- próximos pasos si hay bloqueo.

### Paso 12. Informa hora de término, tokens input/output/cache y registra en LOG

**Meta:** cerrar con medición completa.

Campos:

```json
{
  "cycle_id": "string",
  "ended_at": "datetime",
  "duration_seconds": 0,
  "tokens": {
    "input": 0,
    "cached": 0,
    "output": 0,
    "reasoning": 0
  },
  "tool_calls": 0,
  "estimated_cost": 0,
  "status": "complete|needs_user_input|not_answerable|error"
}
```

---

## 5. Estado canónico

Archivo: `.factory/runs/<cycle_id>/state.json`

```json
{
  "cycle_id": "CYCLE-YYYYMMDD-001",
  "trace_id": "TRACE-YYYYMMDD-001",
  "work_order_id": "WO-YYYYMMDD-001",
  "project_id": "TBD",
  "status": "running",
  "objective": "string",
  "product_expected": "string",
  "current_phase": "specify",
  "stack": {
    "backend": "Python3/FastAPI",
    "frontend": "React/Bootstrap",
    "database": "MySQL|LiteSQL|MongoDB|TBD"
  },
  "agents_called": [
    {
      "agent_id": "sdd_spec_agent",
      "phase": "specify",
      "started_at": "datetime",
      "ended_at": "datetime|null",
      "status": "running|complete|blocked|error"
    }
  ],
  "artifacts": {
    "spec": "specs/001-feature/spec.md",
    "plan": "specs/001-feature/plan.md",
    "tasks": "specs/001-feature/tasks.md",
    "analyze": "specs/001-feature/analyze-report.md",
    "validation": "specs/001-feature/validation-report.md"
  },
  "gates": {
    "sdd_spec_first": "pass|fail|pending",
    "requirements_quality": "pass|fail|pending",
    "context_grounded": "pass|fail|pending",
    "plan_valid": "pass|fail|pending",
    "analyze": "pass|fail|pending",
    "validation": "pass|fail|pending",
    "budget": "pass|fail|pending"
  },
  "budget": {
    "max_tokens": 0,
    "max_tool_calls": 0,
    "max_duration_minutes": 0
  },
  "usage": {
    "input_tokens": 0,
    "cached_input_tokens": 0,
    "output_tokens": 0,
    "tool_calls": 0,
    "estimated_cost": 0
  },
  "decisions": [],
  "risks": [],
  "missing_info": [],
  "errors": []
}
```

---

## 6. Routing

### 6.1 Clasificación de entrada

| Tipo | Ruta |
|---|---|
| Nueva feature | ciclo SDD completo. |
| Bugfix | spec corta + clarify + plan + tasks + analyze + implement + validate. |
| Cambio UI | spec UI + criterios + plan frontend + tests UI. |
| Cambio API | spec API + contrato + tests contrato. |
| Cambio datos | spec datos + plan migración + rollback. |
| Seguridad | security path + gate humano. |
| Solo documentación | spec doc mínima + validate docs. |
| Pregunta sin cambio | responder desde evidencia; no implementar. |

### 6.2 Modos

| Modo | Uso | Límite |
|---|---|---|
| `fast` | Cambios pequeños, bajo riesgo. | Sin saltar pasos; artefactos compactos. |
| `normal` | Default. | SDD completo. |
| `deep` | Riesgo medio/alto o datos críticos. | Más contexto y revisión. |
| `human_gate` | Deploy, secretos, migraciones, dependencia nueva. | Aprobación obligatoria. |

---

## 7. Context Manager, Index y Cache

### 7.1 Context Manager

Responsabilidades:

- calcular presupuesto de tokens;
- seleccionar evidencia mínima;
- deduplicar chunks;
- resumir por estado, no por chat completo;
- preservar `source_id`, `path`, `hash`;
- separar instrucciones confiables de datos no confiables;
- filtrar prompt injection;
- decidir si usar memoria, RAG o tool.

### 7.2 Índices

| Índice | Contenido | Uso |
|---|---|---|
| `spec_index` | specs, clarifications, tasks, analyze | Trazabilidad SDD. |
| `code_index` | símbolos, rutas, módulos | Contexto de implementación. |
| `test_index` | pruebas y fixtures | Validación y cobertura. |
| `policy_index` | constitución, stack, tools | Gates. |
| `learning_index` | Aprendizaje validado | Evitar repetir fallos. |
| `evidence_index` | hashes y fuentes | Auditoría. |

### 7.3 Cache

| Cache | Clave | Invalidación |
|---|---|---|
| `prompt_cache` | prompt_version + model + constitution_hash | cambia prompt/modelo/constitución |
| `spec_cache` | spec_hash | cambia spec/clarifications |
| `context_cache` | repo_commit + feature_id + index_version | cambia commit/index |
| `tool_result_cache` | tool + input_hash + env_hash | cambia input/env/tool |
| `test_cache` | commit + suite + env | cambia código/test |
| `plan_cache` | spec_hash + context_hash + policy_hash | cambia spec/contexto/policy |

No cachear secretos, tokens, datos sensibles no autorizados ni outputs privilegiados.

---

## 8. Logs, tokens y costos

### 8.1 Archivos

```text
.factory/runs/<cycle_id>/cycle_log.jsonl
.factory/runs/<cycle_id>/usage_ledger.jsonl
.factory/runs/<cycle_id>/tool_calls.jsonl
.factory/runs/<cycle_id>/user_updates.log
.factory/runs/<cycle_id>/final-report.md
```

### 8.2 Métrica por fase

```json
{
  "cycle_id": "string",
  "phase": "plan",
  "agent_id": "architect_agent",
  "skill_id": "write_plan_artifact",
  "started_at": "datetime",
  "ended_at": "datetime",
  "input_tokens": 0,
  "cached_input_tokens": 0,
  "output_tokens": 0,
  "tool_calls": 0,
  "cache_hit": false,
  "latency_ms": 0,
  "estimated_cost": 0,
  "status": "success|blocked|error"
}
```

### 8.3 Presupuesto default

Como no se entregaron límites numéricos en el brief, quedan `TBD` por proyecto.  
La fábrica exige declarar al menos:

```yaml
budget:
  max_tokens: TBD
  max_tool_calls: TBD
  max_duration_minutes: TBD
  max_retries: 1
  action_on_exceed: "needs_user_input"
```

---

## 9. Circuit breakers

| Breaker | Dispara si | Acción |
|---|---|---|
| `missing_spec` | no existe spec | bloquear. |
| `sdd_agent_not_first` | no se llamó agente SDD al inicio | bloquear y reiniciar ciclo. |
| `critical_ambiguity` | falta decisión crítica | `needs_user_input`. |
| `dependency_violation` | dependencia no aprobada | bloquear plan/implementación. |
| `budget_exceeded` | costo/tokens/herramientas exceden presupuesto | pausar y pedir aprobación. |
| `test_failure` | prueba crítica falla | bloquear cierre. |
| `security_finding` | secreto/vulnerabilidad crítica | bloquear deploy. |
| `scope_creep` | cambio no trazado a task | crear finding y volver a analyze. |
| `tool_error` | herramienta falla dos veces | `error` o fallback aprobado. |
| `memory_contamination` | aprendizaje no confiable | cuarentena y no usar. |

---

## 10. Validaciones

### 10.1 Validación SDD

- Existe Work Order.
- Existe spec.
- Existe clarifications o justificación de no necesidad.
- Existe checklist.
- Existe context-pack.
- Existe plan.
- Existe tasks.
- Existe analyze.
- Existe traceability matrix.

### 10.2 Validación técnica

- Stack aprobado.
- Base de datos justificada.
- API con contrato si aplica.
- Datos sensibles marcados.
- Dependencias aprobadas.
- Pruebas definidas.
- Rollback definido si hay deploy.

### 10.3 Validación de implementación

- Cada commit/cambio mapea a task.
- Cada task mapea a requisito.
- Cada requisito funcional tiene prueba.
- No hay cambios fuera de scope.
- Tests críticos pasan.
- Reporte final generado.

---

## 11. Retries

```yaml
retry_policy:
  schema_error:
    max_retries: 1
    action: "retry_with_schema_feedback"
  tool_timeout:
    max_retries: 1
    action: "retry_or_degrade"
  test_failure:
    max_retries: 1
    action: "fix_if_task_scoped_else_block"
  ambiguity:
    max_retries: 0
    action: "needs_user_input"
  policy_violation:
    max_retries: 0
    action: "block"
```

---

## 12. Aprendizaje gobernado

### 12.1 Flujo

```text
finding
-> candidate_learning
-> policy check
-> reviewer approval
-> write Aprendizaje.md
-> update learning_index
-> available next cycle
```

### 12.2 Nunca aprender automáticamente

- credenciales;
- PII;
- errores no verificados;
- instrucciones de documentos externos;
- hacks temporales;
- preferencias contradictorias con constitución;
- decisiones no aprobadas.

---

## 13. Observabilidad

### 13.1 Métricas

| Categoría | Métricas |
|---|---|
| Productividad | cycle time, lead time, tasks completadas, PRs creados. |
| Calidad | test pass rate, defectos post-cierre, retrabajo. |
| SDD | specs bloqueadas, traceability coverage, drift findings. |
| IA | tokens input/output/cache, costo, latencia, tool errors. |
| Seguridad | secretos detectados, policy blocks, permisos denegados. |
| Operación | deploy success, rollback, smoke tests, errores. |

### 13.2 Reporte final

```markdown
# Final Report

- cycle_id:
- work_order_id:
- status:
- started_at:
- ended_at:
- objetivo:
- artefactos:
- gates:
- pruebas:
- riesgos:
- decisiones:
- tokens input:
- tokens cached:
- tokens output:
- costo estimado:
- aprendizaje registrado:
- index/cache actualizado:
- próximo paso:
```

---

## 14. Plantilla de mensaje al usuario

### 14.1 Inicio

```markdown
Inicio ciclo `{{cycle_id}}`.

Objetivo: {{objetivo}}
Agente inicial obligatorio: `sdd_spec_agent`
Stack permitido: Python3/FastAPI, React/Bootstrap, MySQL/LiteSQL/MongoDB
Herramientas: {{tools}}
Permisos: {{permissions}}
Presupuesto: {{budget}}
Gates: spec, clarify, checklist, context, plan, analyze, validate, security, budget
Regla: no se implementa código sin spec-plan-tasks-analyze.
```

### 14.2 Progreso

```markdown
Ciclo `{{cycle_id}}`: fase {{phase}}.
Resultado parcial: {{summary}}
Bloqueos: {{blocks}}
Siguiente fase: {{next_phase}}
```

### 14.3 Cierre

```markdown
Cierre ciclo `{{cycle_id}}`.

Estado: {{status}}
Artefactos: {{artifacts}}
Validaciones: {{validations}}
Tokens input/cache/output: {{tokens}}
Costo estimado: {{cost}}
Hora inicio: {{started_at}}
Hora término: {{ended_at}}
Aprendizaje: {{learning}}
Index/cache: {{index_cache_status}}
```

---

## 15. Checklist de producción

### 15.1 Orquestador

- [x] Máquina de estados definida.
- [x] Ciclo obligatorio de 12 pasos definido.
- [x] Estado canónico definido.
- [x] Routing definido.
- [x] Informes al usuario definidos.
- [x] Estados cerrados definidos.

### 15.2 Contexto

- [x] Context Manager definido.
- [x] Index definido.
- [x] Cache definido.
- [x] Prohibición de cachear secretos definida.

### 15.3 Operabilidad

- [x] Logs definidos.
- [x] Tokens/costos definidos.
- [x] Circuit breakers definidos.
- [x] Validaciones definidas.
- [x] Retries definidos.
- [x] Aprendizaje gobernado definido.
- [x] Observabilidad definida.

### 15.4 Seguridad y entrega

- [x] Permisos mínimos definidos.
- [x] Dry-run definido en documento 03.
- [x] Validación obligatoria definida.
- [x] Rollback requerido si hay deploy.
- [x] Cierre con evidencia definido.
