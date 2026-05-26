# 03. Agentes, Skills, Herramientas y Permisos

**Nombre:** FabricaWebTransaccionalSDD  
**Versión:** 1.0.0  
**Fecha:** 2026-05-25  
**Estado:** `complete`  
**Propósito:** definir agentes mínimos, skills, herramientas, permisos, aprendizaje, guardrails, dry-run y pruebas para la fábrica básica de sistemas web transaccionales pequeños.

---

## 1. Principio de diseño

La fábrica usa **pocos agentes**, con responsabilidades claras y permisos mínimos.

```text
un agente = una responsabilidad clara
una skill = una acción tipada, validable y con permisos
una herramienta = ejecución gobernada por policy
un ciclo = orquestador + 12 pasos + evidencia
```

No se crean agentes por comodidad. Se crean solo si separan responsabilidad, permisos, memoria o evaluación.

---

## 2. Agentes mínimos

| agent_id | Nombre | Obligatorio | Responsabilidad principal |
|---|---|---:|---|
| `orchestrator` | Orquestador | Sí | Controlar ciclo, estado, permisos, presupuesto, gates y comunicación al usuario. |
| `sdd_spec_agent` | Agente Especificador SDD | Sí, siempre primero | Pedir, estructurar y mejorar la especificación SDD simple del sistema. |
| `clarifier_qa_agent` | Agente Clarificador y QA de Requisitos | Sí | Detectar ambigüedades, validar checklist y bloquear specs incompletas. |
| `architect_agent` | Agente Arquitecto | Sí | Crear plan técnico con stack aprobado, datos, APIs, seguridad y pruebas. |
| `task_analyzer_agent` | Agente de Tareas y Análisis | Sí | Generar tareas atómicas y verificar consistencia antes de implementar. |
| `implementer_agent` | Agente Implementador | Condicional | Implementar solo tasks aprobadas en sandbox/branch controlada. |
| `validation_agent` | Agente QA / Validador | Sí | Ejecutar pruebas, validar aceptación, seguridad básica y trazabilidad. |
| `ops_security_agent` | Agente Seguridad / Operación | Condicional | Revisar permisos, secretos, rollback, deploy, observabilidad. |

Para mantener simplicidad, costos y velocidad, el `orchestrator` también asume inicialmente registro de tokens/costos, routing y cierre. Si crece el volumen, se podrá separar un `cost_agent`.

---

## 3. Agentes preexistentes reutilizados

No se declararon agentes existentes en el brief.

```yaml
preexisting_agents:
  status: "TBD"
  policy:
    - "No reutilizar agente externo sin ficha, permisos, owner, versión y pruebas."
    - "Todo agente preexistente debe pasar evaluación de compatibilidad."
    - "Si un agente no puede cumplir el ciclo SDD, no se reutiliza."
```

---

## 4. Fichas de agentes

### 4.1 `orchestrator`

```yaml
agent_id: "orchestrator"
owner: "factory"
status: "production_candidate"
single_responsibility: "Controlar el ciclo completo y asegurar que se cumplan los 12 pasos."
use_when:
  - "Siempre, en todo ciclo."
do_not_use_when:
  - "Nunca se omite."
can_write_code: false
can_deploy: false
can_call_tools: true
requires_user_update: true
success_definition:
  - "12 pasos ejecutados o bloqueo justificado."
  - "usuario informado de plan, progreso, resultado y cierre."
  - "logs, tokens, costo y gates registrados."
failure_definition:
  - "ciclo sin cycle_id."
  - "agente SDD no llamado primero."
  - "validación omitida."
```

### 4.2 `sdd_spec_agent`

```yaml
agent_id: "sdd_spec_agent"
owner: "product/factory"
status: "production_candidate"
single_responsibility: "Pedir, normalizar y mejorar la especificación SDD simple al comienzo del ciclo."
use_when:
  - "Siempre al inicio de cada ciclo, antes de planificar implementación."
do_not_use_when:
  - "Nunca después de implementar para justificar código ya escrito."
can_write_specs: true
can_write_code: false
can_deploy: false
can_read_repo: true
can_call_tools:
  - "read_constitution"
  - "read_project_memory"
  - "write_spec_draft"
  - "write_questions"
success_definition:
  - "spec draft creado con requisitos, datos, flujos, criterios y preguntas abiertas."
  - "campos críticos faltantes marcados como needs_user_input."
failure_definition:
  - "rellenar reglas de negocio inventadas."
  - "elegir dependencias sin aprobación."
```

### 4.3 `clarifier_qa_agent`

```yaml
agent_id: "clarifier_qa_agent"
single_responsibility: "Cerrar ambigüedades críticas y validar calidad de requisitos."
use_when:
  - "Después de spec draft."
can_write_specs: true
can_write_code: false
outputs:
  - "clarifications.md"
  - "checklist.md"
blocks_when:
  - "preguntas críticas abiertas"
  - "criterios de aceptación ausentes"
  - "datos sensibles sin política"
```

### 4.4 `architect_agent`

```yaml
agent_id: "architect_agent"
single_responsibility: "Crear plan técnico simple usando stack aprobado."
use_when:
  - "Después de checklist aprobado y context pack."
can_read_repo: true
can_write_plan: true
can_write_code: false
outputs:
  - "plan.md"
  - "data-model.md"
  - "contracts/openapi.yaml"
  - "test-plan.md"
blocks_when:
  - "dependencia no aprobada"
  - "base de datos no justificada"
  - "seguridad omitida"
```

### 4.5 `task_analyzer_agent`

```yaml
agent_id: "task_analyzer_agent"
single_responsibility: "Crear tasks atómicas y ejecutar análisis cruzado."
outputs:
  - "tasks.md"
  - "analyze-report.md"
  - "traceability-matrix.md"
blocks_when:
  - "requisito sin tarea"
  - "tarea sin requisito"
  - "requisito funcional sin prueba"
  - "plan contradice spec"
```

### 4.6 `implementer_agent`

```yaml
agent_id: "implementer_agent"
single_responsibility: "Implementar tareas aprobadas en orden."
use_when:
  - "Solo si analyze-report permite implementar."
can_write_code: true
can_install_dependencies: false
can_deploy: false
environment: "agent-sandbox"
blocks_when:
  - "test crítico falla"
  - "scope creep detectado"
  - "dependency request sin aprobación"
```

### 4.7 `validation_agent`

```yaml
agent_id: "validation_agent"
single_responsibility: "Ejecutar pruebas y validar aceptación."
outputs:
  - "validation-report.md"
  - "test-report.md"
  - "quality-gate.json"
can_write_code: false
can_deploy: false
blocks_when:
  - "falla prueba obligatoria"
  - "falta evidencia"
  - "matriz de trazabilidad incompleta"
```

### 4.8 `ops_security_agent`

```yaml
agent_id: "ops_security_agent"
single_responsibility: "Revisar seguridad, rollback, deploy y observabilidad."
use_when:
  - "Si hay deploy, datos sensibles, permisos, migraciones o riesgo medio/alto."
outputs:
  - "security-review.md"
  - "deployment-plan.md"
  - "rollback-plan.md"
can_deploy: false
can_approve_deploy: false
requires_human_gate_for:
  - "deploy_to_production"
  - "merge"
  - "migration"
  - "secret_access"
```

---

## 5. Herramientas permitidas

| Herramienta | Uso | Entrada mínima | Salida | Error |
|---|---|---|---|---|
| `files/RAG` | Leer specs, repo, docs, memoria y evidencia | consulta + filtros | chunks con IDs, paths, hashes | `not_answerable` |
| `code/shell` | Ejecutar comandos del sistema sin restricciones (excepto SUDO) | comando + cwd | stdout, stderr, exit code, logs | `error` |
| `git` | Branch, diff, PR dry-run | repo + branch + task_id | diff, PR payload | `error` |
| `test_runner` | Pruebas unitarias/integración/UI/API | suite + env | reportes | `error` |
| `policy_engine` | Validar permisos, stack, dependencias | artefactos + policy | pass/fail/findings | `error` |
| `indexer` | Actualizar índice y cache | paths + hashes | index report | `error` |

### 5.1 Web

Web no se usa por defecto.  
Solo se permite si el usuario autoriza datos públicos actuales o si una decisión técnica exige verificación de versión actual. En ese caso debe registrarse fuente y fecha.

### 5.2 Acciones externas y SUDO

La ejecución de comandos ordinarios de shell, instalación de dependencias, ejecución de pruebas y manipulación de archivos locales está completamente liberada para los agentes de la fábrica sin confirmación intermedia. Sin embargo:
- Todo comando que incluya **SUDO** para elevar privilegios requiere confirmación interactiva expresa del usuario antes de ser ejecutado.
- Acciones externas mayores (como PR reales, deploy productivo y merge final) siguen los canales informativos de la fábrica.

---

## 6. Skills mínimas

| skill_id | Fase | Agente | Side effects | Aprobación | Descripción |
|---|---|---|---:|---:|---|
| `read_constitution` | todas | todos | no | no | Lee constitución aplicable. |
| `load_index_cache` | paso 2 | orchestrator | no | no | Carga index/cache de contexto. |
| `read_aprendizaje` | paso 3 | orchestrator | no | no | Lee aprendizaje de fábrica, proyecto y agentes. |
| `start_cycle_log` | paso 4 | orchestrator | sí | no | Abre logs por ciclo. |
| `start_usage_ledger` | paso 5 | orchestrator | sí | no | Registra hora, presupuesto y tokens iniciales. |
| `inform_user_plan` | paso 6 | orchestrator | sí | no | Informa plan, agentes, skills, tools, permisos y gates. |
| `ask_sdd_spec` | specify | sdd_spec_agent | sí | no | Solicita y estructura la spec SDD simple. |
| `write_spec_artifact` | specify | sdd_spec_agent | sí | no | Escribe `spec.md` o `spec_draft.md`. |
| `write_clarifications` | clarify | clarifier_qa_agent | sí | no | Escribe `clarifications.md`. |
| `run_requirements_checklist` | checklist | clarifier_qa_agent | no | no | Valida requisitos. |
| `build_context_pack` | context | architect_agent | sí | no | Genera `context-pack.md`. |
| `validate_stack_policy` | plan | architect_agent | no | no | Verifica stack aprobado. |
| `write_plan_artifact` | plan | architect_agent | sí | no | Escribe `plan.md`. |
| `write_tasks_artifact` | tasks | task_analyzer_agent | sí | no | Escribe `tasks.md`. |
| `run_cross_artifact_analysis` | analyze | task_analyzer_agent | no | no | Verifica spec-plan-tasks-tests. |
| `apply_patch` | implement | implementer_agent | sí | no en sandbox | Aplica cambio por task. |
| `run_backend_tests` | validate | validation_agent | no | no | Ejecuta pruebas backend aprobadas. |
| `run_frontend_tests` | validate | validation_agent | no | no | Ejecuta pruebas frontend aprobadas. |
| `run_api_contract_tests` | validate | validation_agent | no | no | Valida contrato API si existe. |
| `run_security_basic_scan` | validate | ops_security_agent | no | no | Escaneo básico de secretos/deps. |
| `create_pr_dry_run` | PR | orchestrator | no | no | Prepara payload PR sin enviarlo. |
| `create_pr` | PR | orchestrator | sí | según política | Crea PR si repositorio autorizado. |
| `deploy_dry_run` | deploy | ops_security_agent | no | no | Simula deploy. |
| `deploy_to_staging` | deploy | ops_security_agent | sí | gate | Despliega staging. |
| `deploy_to_production` | deploy | ops_security_agent | sí | sí | Despliega producción. |
| `update_index_cache` | paso 10 | orchestrator | sí | no | Actualiza índice/cache si hay nuevos archivos. |
| `write_aprendizaje` | paso 9/close | orchestrator | sí | gate | Registra aprendizaje validado. |
| `close_cycle` | paso 11/12 | orchestrator | sí | no | Cierra ciclo e informa resultado. |

---

## 7. Contratos de entrada y salida

### 7.1 Entrada de agente

```json
{
  "cycle_id": "string",
  "trace_id": "string",
  "work_order_id": "string",
  "agent_id": "string",
  "phase": "constitution|specify|clarify|checklist|context|plan|tasks|analyze|implement|validate|deploy|observe|close",
  "goal": "string",
  "authorized_context": [
    {
      "source_id": "string",
      "source_type": "user_input|spec|repo|memory|tool_result",
      "path": "string|null",
      "hash": "string|null",
      "content_summary": "string",
      "trust_level": "low|medium|high"
    }
  ],
  "constraints": {
    "stack_allowed": ["Python3", "FastAPI", "React", "Bootstrap", "MySQL", "LiteSQL", "MongoDB"],
    "no_new_dependencies_without_approval": true,
    "no_code_without_analyze": true,
    "must_validate": true
  },
  "budget": {
    "max_input_tokens": 12000,
    "max_output_tokens": 2000,
    "max_tool_calls": 5,
    "max_retries": 1
  }
}
```

### 7.2 Salida de agente

```json
{
  "status": "complete|needs_user_input|not_answerable|error",
  "agent_id": "string",
  "phase": "string",
  "summary": "string",
  "artifacts_created": ["string"],
  "decisions": [
    {
      "decision_id": "string",
      "decision": "string",
      "source_id": "string",
      "confidence": "low|medium|high"
    }
  ],
  "missing_fields": ["string"],
  "risks": ["string"],
  "tool_calls": [
    {
      "skill_id": "string",
      "status": "success|failed|blocked",
      "evidence_path": "string"
    }
  ],
  "validation": {
    "schema_valid": true,
    "policy_valid": true,
    "traceability_valid": true
  }
}
```

---

## 8. Permisos por agente

| Permiso | orchestrator | sdd_spec | clarifier | architect | task_analyzer | implementer | validation | ops_security |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Leer constitución | sí | sí | sí | sí | sí | sí | sí | sí |
| Leer repo | sí | sí | sí | sí | sí | sí | sí | sí |
| Leer memoria | sí | sí | sí | sí | sí | limitado | sí | sí |
| Escribir specs | sí | sí | sí | no | no | no | no | no |
| Escribir plan | no | no | no | sí | no | no | no | no |
| Escribir tasks | no | no | no | no | sí | no | no | no |
| Escribir código | no | no | no | no | no | sí | no | no |
| Ejecutar tests | sí | no | no | no | no | sí limitado | sí | sí limitado |
| Cambiar dependencias | no | no | no | no | no | no | no | no |
| Crear PR | dry-run/sí | no | no | no | no | no | no | no |
| Merge | no | no | no | no | no | no | no | no |
| Deploy staging | gate | no | no | no | no | no | no | gate |
| Deploy producción | aprobación | no | no | no | no | no | no | aprobación |
| Leer secretos | no | no | no | no | no | no | no | no por defecto |

---

## 9. Aprendizaje por agente, proyecto y fábrica

### 9.1 Archivos

```text
.factory/memory/Aprendizaje.Fabrica.md
.factory/memory/Aprendizaje.Proyecto.<project_id>.md
.factory/memory/agents/Aprendizaje.<agent_id>.md
```

### 9.2 Cuándo registrar aprendizaje

Registrar solo si:

- hubo fallo, bloqueo, drift, regresión o mejora validada;
- el aprendizaje tiene `cycle_id`, `source_id` y evidencia;
- no contiene secretos ni PII innecesaria;
- no contradice constitución;
- un gate de aprendizaje lo aprueba.

### 9.3 Template

```markdown
# Aprendizaje

## LEARN-YYYYMMDD-###

- Fecha:
- cycle_id:
- agent_id:
- project_id:
- Tipo: error|mejora|policy|test|seguridad|costo|contexto
- Observación:
- Evidencia:
- Causa raíz:
- Acción correctiva:
- Prevención:
- Aplica a: fábrica|proyecto|agente
- Estado: proposed|approved|rejected|deprecated
- Aprobador:
```

---

## 10. Guardrails

### 10.1 Entrada

- Validar schema de Work Order.
- Sanitizar contenido externo.
- Separar instrucciones confiables de datos no confiables.
- Detectar prompt injection.
- Bloquear instrucciones de documentos que intenten cambiar reglas.
- Verificar permisos de usuario y proyecto.

### 10.2 Herramientas

- Tool allowlist por agente.
- Validación de argumentos.
- Timeout.
- Retry limitado.
- Idempotency key.
- No secretos.
- Dry-run para side effects.
- Logs obligatorios.

### 10.3 Salida

- JSON válido si alimenta otro sistema.
- Markdown estructurado si es artefacto humano.
- Decisiones críticas con fuente.
- No afirmar datos sin evidencia.
- No ocultar `TBD`.
- No cerrar si falta validación.

---

## 11. Dry-run

Acciones con side effects deben seguir:

```text
1. Preparar payload.
2. Ejecutar dry-run.
3. Mostrar resultado al usuario.
4. Validar policy.
5. Pedir aprobación si corresponde.
6. Ejecutar.
7. Registrar evidencia.
8. Permitir rollback si aplica.
```

Acciones que requieren este flujo:

- crear PR real;
- merge;
- deploy;
- migración de base de datos;
- escritura externa;
- generación de issue externo;
- cambio de configuración;
- acceso a secretos;
- borrado;
- rollback productivo.

---

## 12. Diseño y ejecución de pruebas

### 12.1 Pruebas mínimas por feature

| Tipo | Cuándo aplica | Evidencia |
|---|---|---|
| Requisitos | Siempre | `checklist.md` |
| Trazabilidad | Siempre | `traceability-matrix.md` |
| Unitarias backend | Si hay backend | `test-report.md` |
| Unitarias frontend | Si hay frontend | `test-report.md` |
| Integración | Si hay DB/API | `integration-report.md` |
| Contrato API | Si hay endpoints | `contract-report.md` |
| UI/E2E | Si hay flujo crítico | `e2e-report.md` |
| Seguridad básica | Si hay datos, auth o deploy | `security-review.md` |
| Smoke | Si hay deploy | `smoke-report.md` |
| Regresión de agentes | Si cambia agente/prompt/skill | `evals-report.md` |

### 12.2 Gate de validación

```yaml
gate: validation_required
pass_condition:
  sdd_artifacts_valid: true
  traceability_complete: true
  required_tests_executed: true
  critical_tests_passed: true
  security_critical_findings: 0
  user_informed: true
on_fail:
  action: "block_close_and_register_learning"
```

---

## 13. Checklist del documento

- [x] Agentes mínimos definidos.
- [x] Agente SDD inicial obligatorio definido.
- [x] Agentes preexistentes tratados como `TBD`.
- [x] Responsabilidades y prohibiciones definidas.
- [x] Skills definidas.
- [x] Schemas definidos.
- [x] Herramientas y permisos definidos.
- [x] Aprendizaje por agente/proyecto/fábrica definido.
- [x] Guardrails definidos.
- [x] Dry-run definido.
- [x] Diseño y ejecución de pruebas definidos.
