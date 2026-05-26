# 01. Constitución y Especificación de la Fábrica

**Nombre:** FabricaWebTransaccionalSDD  
**Versión:** 1.0.0  
**Fecha:** 2026-05-25  
**Estado:** `complete`  
**Idioma:** español neutro  
**Modo operativo:** básico, simple, eficaz, Spec-Driven, trazable y validado.

---

## 1. Fuentes y regla de evidencia

### 1.1 Fuentes usadas

| source_id | Tipo | Uso |
|---|---|---|
| `brief_usuario_2026-05-25` | Brief del usuario | Fuente principal para objetivo, tipo de software, stack, obligación de orquestador, agente SDD inicial, pruebas y validación. |
| `base_sdd_v2` | Documento base GPT | Reglas Spec-Driven, artefactos, gates, no improvisación, validaciones y trazabilidad. |
| `base_fabrica_agentica` | Documento base GPT | Orquestador por estados, contexto mínimo, cache, memoria, observabilidad y control de herramientas. |
| `base_plantillas_seguras` | Documento base GPT | Contratos estrictos, permisos, guardrails, token/cost ledger y evaluación continua. |
| `base_diseno_agentico` | Documento base GPT | Componentes mínimos: orquestador, estado compartido, memoria, RAG, cache, logs y facturación. |

### 1.2 Política de no invención

La fábrica no inventa requisitos, métricas, dependencias, SLA, SLO, ambientes, credenciales, endpoints externos ni reglas de negocio.  
Cuando una decisión no esté cubierta por el brief o por evidencia del proyecto:

- usar `TBD` si no bloquea el diseño;
- usar `needs_user_input` si bloquea una decisión crítica;
- usar `not_answerable` si se exige evidencia y no existe;
- bloquear implementación si falta spec, plan, tasks, analyze o validación.

---

## 2. Objetivo

Crear una fábrica básica, simple y eficaz para desarrollar y mantener **sistemas de software web pequeños**, de tipo **transaccional WEB**, usando un flujo Spec-Driven Development controlado por orquestador.

La fábrica transforma:

```text
idea / solicitud / cambio / bug
-> especificación SDD simple
-> aclaraciones
-> checklist
-> contexto
-> plan
-> tareas
-> análisis
-> implementación
-> pruebas
-> validación
-> entrega trazable
```

---

## 3. Alcance

### 3.1 Incluido

- Sistemas web transaccionales pequeños.
- Backends API con **Python 3 + FastAPI**.
- Frontend con **React + Bootstrap**.
- Persistencia con **MySQL**, **LiteSQL** o **MongoDB**, según la spec.
- Especificación SDD simple y ágil.
- Orquestador obligatorio en cada ciclo.
- Ciclo obligatorio de 12 pasos.
- Pruebas y validación obligatorias.
- Logs, trazas, estado compartido, costo/tokens y aprendizaje.
- CI/CD básico con gates de spec, pruebas y seguridad.
- Control de dependencias.
- Permisos mínimos por agente.
- Dry-run para acciones con side effects.

### 3.2 Excluido

- Sistemas grandes empresariales multi-equipo, salvo extensión futura.
- Microservicios distribuidos complejos por defecto.
- Deploy productivo automático sin gate humano.
- Dependencias no aprobadas.
- Implementación directa desde prompt libre.
- Uso de herramientas externas con side effects sin confirmación.
- Escritura de código antes de spec, plan, tasks y analyze.

### 3.3 Supuestos explícitos

| Supuesto | Estado | Acción |
|---|---|---|
| `LiteSQL` fue indicado por el usuario como tecnología permitida. | `TBD` | Confirmar si corresponde a una tecnología concreta o a `SQLite` antes de implementación. |
| “React o mejor” y “Bootstrap o mejor” no aprueban automáticamente alternativas. | Activo | Cualquier alternativa requiere aprobación en política de stack. |
| SLA/SLO no fueron definidos. | `TBD` | Cada proyecto debe declararlos en su spec si son críticos. |
| Ambientes no fueron detallados. | `TBD` | Usar mínimo `local`, `agent-sandbox`, `staging`, `production` si el proyecto despliega. |
| Herramientas de test específicas no fueron aprobadas. | `TBD` | El plan debe seleccionar herramientas existentes o pedir aprobación. |

---

## 4. Stakeholders

| Stakeholder | Responsabilidad |
|---|---|
| Usuario / Product Owner | Define objetivo, reglas de negocio, prioridades y aceptación. |
| Orquestador | Controla ciclo, gates, agentes, herramientas, presupuesto, logs y cierre. |
| Agente Especificador SDD | Solicita, ordena y mejora la especificación al inicio de cada ciclo. |
| Agente Arquitecto | Traduce spec a plan técnico usando stack aprobado. |
| Agente Implementador | Implementa solo tareas aprobadas y trazables. |
| Agente QA / Validador | Ejecuta pruebas, valida criterios de aceptación y bloquea fallos. |
| Agente Seguridad / Operación | Revisa permisos, secretos, vulnerabilidades básicas, rollback y observabilidad. |
| Usuario aprobador técnico | Autoriza excepciones, nuevas dependencias, merges y deploy productivo. |

---

## 5. Principios no negociables

1. **La especificación manda.** El código es expresión de la spec.
2. **Orquestador obligatorio.** Ningún ciclo se ejecuta fuera del orquestador.
3. **Agente Especificador SDD siempre primero.** Debe llamarse al comienzo de cada ciclo.
4. **Siempre informar al usuario.** El plan, agentes, skills, herramientas, permisos, presupuesto y gates se informan antes de ejecutar.
5. **Siempre probar y validar.** Ningún cambio se considera completo sin evidencia de pruebas.
6. **No código sin spec.** No se escribe código sin spec, aclaraciones necesarias, checklist, plan, tasks y analyze.
7. **Tareas atómicas.** Cada tarea debe mapear a requisito y validación.
8. **Stack gobernado.** Solo se usa stack aprobado o dependencia aprobada explícitamente.
9. **Permisos mínimos.** Cada agente y skill opera con menor privilegio.
10. **Dry-run primero.** PR, deploy, migraciones y acciones externas requieren dry-run y aprobación cuando aplique.
11. **Trazabilidad total.** Cada ciclo produce `cycle_id`, `trace_id`, logs, tokens, costo, herramientas, decisiones y resultado.
12. **Aprendizaje gobernado.** Solo se registra aprendizaje si está validado, tiene fuente y no contiene datos sensibles.
13. **Contexto mínimo.** El agente recibe solo lo necesario: objetivo, estado, evidencia, restricciones y schema.
14. **Cache-first.** Usar cache de contexto, retrieval, validaciones y planes cuando el hash coincida.
15. **Bloqueo ante ambigüedad crítica.** Si falta una regla de negocio crítica, el estado es `needs_user_input`.

---

## 6. Source of truth

Orden de autoridad:

```text
1. Constitución de la fábrica
2. Constitución del proyecto
3. Work Order
4. Spec SDD
5. Aclaraciones
6. Checklist
7. Context Pack
8. Plan técnico
9. Contratos API/datos
10. Tasks
11. Analyze report
12. Código
13. Pruebas y reportes
14. Release/deploy/observabilidad
15. Aprendizaje validado
```

Regla: si el código contradice la spec, se considera **drift**. Se debe actualizar la spec o corregir el código antes de cerrar.

---

## 7. Stack aprobado por constitución inicial

### 7.1 Backend

| Elemento | Estado | Regla |
|---|---|---|
| Python 3 | Aprobado | Lenguaje principal backend. |
| FastAPI | Aprobado | Framework API backend. |
| OpenAPI generado por FastAPI | Permitido | Debe usarse como contrato API si hay endpoints. |

### 7.2 Frontend

| Elemento | Estado | Regla |
|---|---|---|
| React | Aprobado | Framework frontend base. |
| Bootstrap | Aprobado | UI base simple. |
| Alternativa “mejor” | `TBD` | No aprobada automáticamente. Requiere decisión explícita en plan. |

### 7.3 Datos

| Base | Estado | Uso recomendado |
|---|---|---|
| MySQL | Aprobado | Base transaccional principal si hay integridad relacional, reportes y consistencia. |
| LiteSQL | Aprobado por nombre en brief | Usar solo tras confirmar definición concreta en proyecto. |
| MongoDB | Aprobado | Usar cuando la spec justifique documentos, flexibilidad de esquema o datos semiestructurados. |

### 7.4 Dependencias no listadas

Cualquier dependencia adicional requiere:

```yaml
dependency_request:
  package: "TBD"
  version: "TBD"
  reason: "TBD"
  license: "TBD"
  alternatives: []
  approved_by: "TBD"
  approval_status: "pending|approved|rejected"
```

---

## 8. Definición de éxito de la fábrica

La fábrica está lista cuando:

- todo ciclo arranca con orquestador;
- todo ciclo llama primero al Agente Especificador SDD;
- todo cambio tiene Work Order;
- toda feature tiene spec versionada;
- toda ambigüedad crítica se aclara o bloquea;
- todo plan usa solo stack aprobado;
- toda tarea se traza a requisito;
- todo requisito funcional tiene prueba o validación;
- todo código se implementa desde tareas aprobadas;
- toda validación queda registrada;
- todo cierre informa al usuario resultado, evidencias, tokens, costo y estado;
- todo aprendizaje queda en `Aprendizaje.md` solo si fue validado.

---

## 9. Requerimientos funcionales de la fábrica

| ID | Requerimiento | Fuente | Validación |
|---|---|---|---|
| FR-001 | La fábrica debe crear software web transaccional pequeño. | `brief_usuario_2026-05-25` | Spec del proyecto declara tipo `web_transaccional_pequeno`. |
| FR-002 | La fábrica debe usar Python 3 + FastAPI para backend. | `brief_usuario_2026-05-25` | Plan técnico no usa backend fuera del stack aprobado. |
| FR-003 | La fábrica debe usar React + Bootstrap para frontend base. | `brief_usuario_2026-05-25` | Plan técnico no usa frontend alternativo sin aprobación. |
| FR-004 | La fábrica debe soportar MySQL, LiteSQL y MongoDB. | `brief_usuario_2026-05-25` | Plan selecciona una base y justifica uso según spec. |
| FR-005 | La fábrica debe ser rápida, eficiente y eficaz. | `brief_usuario_2026-05-25` | Presupuestos, agentes mínimos, contexto mínimo y cache activados. |
| FR-006 | La fábrica debe tener un Agente Especificador SDD llamado al inicio de cada ciclo. | `brief_usuario_2026-05-25` | Log del ciclo contiene paso `call_sdd_spec_agent`. |
| FR-007 | El orquestador debe ejecutarse siempre. | `brief_usuario_2026-05-25` | No se acepta artefacto sin `cycle_id` emitido por orquestador. |
| FR-008 | El ciclo de 12 pasos debe ejecutarse siempre. | `brief_usuario_2026-05-25` | Checklist del ciclo contiene los 12 pasos completos. |
| FR-009 | El usuario debe ser informado durante cada ciclo. | `brief_usuario_2026-05-25` | Logs incluyen mensajes de plan, progreso, resultado y cierre. |
| FR-010 | Se debe probar y validar siempre. | `brief_usuario_2026-05-25` | Gate `validation` debe estar en `pass` o bloquear cierre. |
| FR-011 | La fábrica debe registrar logs, tokens, costo y tiempo. | `base_diseno_agentico`, `base_plantillas_seguras` | `usage_ledger.jsonl` y `cycle_log.jsonl` presentes. |
| FR-012 | La fábrica debe actualizar index/cache si hay nuevos archivos de sistema. | `base_fabrica_agentica` | `index_update_report.md` o `cache_update_report.md`. |
| FR-013 | Si falla una validación, debe registrar aprendizaje y repetir o bloquear. | `brief_usuario_2026-05-25` | `Aprendizaje.md` actualizado con causa y acción. |
| FR-014 | Debe existir matriz de trazabilidad requisito→tarea→prueba→evidencia. | `base_sdd_v2` | `traceability-matrix.md` completo. |
| FR-015 | Debe existir política de no improvisación. | `base_sdd_v2` | Gate bloquea supuestos críticos no aclarados. |

---

## 10. Requerimientos no funcionales

| ID | Requerimiento | Criterio |
|---|---|---|
| NFR-001 | Simplicidad | Mínimos agentes y skills; evitar herramientas complejas si no agregan valor. |
| NFR-002 | Rapidez | Usar cache, contexto mínimo, scopes pequeños y validaciones incrementales. |
| NFR-003 | Eficiencia | No pasar historial completo a agentes; usar context pack compacto. |
| NFR-004 | Eficacia | Cerrar solo si criterios de aceptación y pruebas pasan. |
| NFR-005 | Seguridad | Sin secretos por defecto, permisos mínimos, escaneo básico y revisión de inputs. |
| NFR-006 | Observabilidad | Logs, métricas, trazas, costos y estado por ciclo. |
| NFR-007 | Reproducibilidad | Versionar spec, plan, tasks, modelo, prompts, tools, commit, index y cache. |
| NFR-008 | Mantenibilidad | Artefactos Markdown simples y consistentes. |
| NFR-009 | Auditabilidad | Cada decisión crítica tiene fuente, responsable y evidencia. |
| NFR-010 | Baja variabilidad | Orquestador por estados, schemas y gates determinísticos. |

---

## 11. Restricciones

### 11.1 Restricciones técnicas

- No usar stack fuera de la lista aprobada sin aprobación.
- No mezclar MySQL, LiteSQL y MongoDB en un mismo proyecto salvo justificación explícita.
- No crear arquitectura de microservicios por defecto.
- No introducir colas, Kubernetes, IaC ni herramientas enterprise salvo necesidad aprobada.
- No ejecutar shell libre; solo comandos allowlist definidos por proyecto.
- No acceder a secretos desde agentes por defecto.

### 11.2 Restricciones operativas

- Todo ciclo debe tener `cycle_id`.
- Todo ciclo debe pasar por los 12 pasos.
- El usuario debe recibir plan antes de ejecución.
- El usuario debe recibir resultado y cierre.
- Todo fallo crítico bloquea avance.
- Todo aprendizaje permanente requiere validación.

### 11.3 Restricciones de datos

- Minimizar PII.
- Usar datos sintéticos para pruebas por defecto.
- No guardar datos sensibles en logs.
- No cachear secretos ni outputs privilegiados.
- Cada modelo de datos debe tener reglas de retención `TBD` o definidas.

---

## 12. Criterios de aceptación

| ID | Criterio | Evidencia requerida |
|---|---|---|
| AC-001 | Se genera Work Order normalizado. | `work_order.json` |
| AC-002 | Se ejecuta Agente Especificador SDD al inicio. | `cycle_log.jsonl` con evento `sdd_spec_agent_started`. |
| AC-003 | La spec tiene objetivo, actores, reglas, requisitos y criterios de aceptación. | `spec.md` validado. |
| AC-004 | Las preguntas críticas se resuelven o bloquean. | `clarifications.md` y estado `clarified` o `needs_user_input`. |
| AC-005 | El checklist de requisitos pasa antes del plan. | `checklist.md`. |
| AC-006 | El plan usa stack aprobado. | `plan.md` + gate `dependency_policy`. |
| AC-007 | Tasks atómicas y trazables. | `tasks.md` con IDs `T-###` y referencias `REQ-###`. |
| AC-008 | Analyze pasa antes de implementar. | `analyze-report.md` con `Proceed: yes`. |
| AC-009 | Validaciones ejecutadas. | `test-report.md`, `security-review.md`, `validation-report.md`. |
| AC-010 | Matriz de trazabilidad completa. | `traceability-matrix.md`. |
| AC-011 | Ciclo cerrado con logs de tokens/costo. | `usage_ledger.jsonl`. |
| AC-012 | Usuario informado de inicio, plan, progreso, resultado y cierre. | `cycle_log.jsonl` + `final-report.md`. |

---

## 13. Matriz de trazabilidad inicial

| Requisito | Artefacto SDD | Gate | Prueba/Validación |
|---|---|---|---|
| FR-001 | `work_order.json`, `spec.md` | `spec_exists` | Revisión de tipo de sistema. |
| FR-002 | `plan.md` | `stack_policy` | Validar backend FastAPI/Python3. |
| FR-003 | `plan.md` | `stack_policy` | Validar frontend React/Bootstrap. |
| FR-004 | `data-model.md` | `data_policy` | Validar selección de DB. |
| FR-005 | `state.json`, `usage_ledger.jsonl` | `budget` | Tokens, duración y tool calls bajo presupuesto. |
| FR-006 | `cycle_log.jsonl` | `sdd_spec_first` | Primer agente funcional del ciclo es `sdd_spec_agent`. |
| FR-007 | `state.json` | `orchestrator_required` | `orchestrator_run_id` presente. |
| FR-008 | `cycle_checklist.md` | `cycle_12_steps` | 12 pasos en estado `done`. |
| FR-009 | `user_updates.log` | `user_informed` | Mensajes requeridos emitidos. |
| FR-010 | `validation-report.md` | `validation_required` | Pruebas obligatorias ejecutadas. |
| FR-011 | `usage_ledger.jsonl` | `usage_recorded` | Tokens/costo/tiempo presentes. |
| FR-012 | `index-report.md` | `index_cache_updated` | Nuevos archivos indexados o justificación. |
| FR-013 | `Aprendizaje.md` | `learning_gate` | Aprendizaje registrado tras fallo validado. |
| FR-014 | `traceability-matrix.md` | `traceability_complete` | Cobertura 100% de requisitos funcionales. |
| FR-015 | `clarifications.md` | `no_improvisation` | Supuestos críticos resueltos o bloqueados. |

---

## 14. Especificación SDD simple que debe pedir el agente inicial

El Agente Especificador SDD debe solicitar o construir esta estructura mínima:

```markdown
# Especificación SDD Simple

## 1. Nombre del sistema
- Nombre:
- Dueño:
- Fecha:

## 2. Objetivo
- Qué problema resuelve:
- Para quién:
- Resultado esperado:

## 3. Usuarios y roles
| Rol | Qué puede hacer | Restricciones |
|---|---|---|

## 4. Flujos transaccionales
| Flujo | Actor | Entrada | Acción | Salida | Error esperado |
|---|---|---|---|---|---|

## 5. Requisitos funcionales
- REQ-001:
- REQ-002:

## 6. Requisitos no funcionales
- Seguridad:
- Rendimiento:
- Disponibilidad:
- Observabilidad:
- Accesibilidad:
- Mantenibilidad:

## 7. Datos
| Entidad | Campos principales | Sensible sí/no | Retención | Validaciones |
|---|---|---|---|---|

## 8. Base de datos candidata
- MySQL / LiteSQL / MongoDB:
- Justificación:
- Migraciones requeridas:

## 9. API
| Endpoint | Método | Request | Response | Permiso |
|---|---|---|---|---|

## 10. Frontend
- Pantallas:
- Componentes:
- Estados loading/error/empty:
- Validaciones:

## 11. Criterios de aceptación
- AC-001:
- AC-002:

## 12. Pruebas esperadas
- Unitarias:
- Integración:
- API/contrato:
- UI:
- Seguridad básica:

## 13. Fuera de alcance
- OOS-001:

## 14. Preguntas abiertas
- Q-001:
```

---

## 15. Política de no improvisación

| Situación | Acción obligatoria |
|---|---|
| Falta regla de negocio crítica | `needs_user_input` |
| Falta stack o dependencia aprobada | bloquear plan o pedir aprobación |
| Falta estructura de datos | volver a `clarify` |
| Falta criterio de aceptación | bloquear checklist |
| Falta prueba para requisito funcional | bloquear analyze |
| Error de test crítico | bloquear implementación/cierre |
| Cambio fuera de scope | crear finding y volver a spec/plan/tasks |
| Conflicto entre spec y plan | bloquear analyze |
| Conflicto entre código y spec | abrir drift finding |
| Herramienta sin permiso | bloquear tool call |
| Acción irreversible | dry-run + aprobación humana |

---

## 16. Estados cerrados

La fábrica solo puede responder con:

```text
complete
needs_user_input
not_answerable
error
```

Reglas:

- `complete`: todos los gates críticos pasan.
- `needs_user_input`: falta decisión del usuario para avanzar.
- `not_answerable`: no hay evidencia suficiente para una decisión factual.
- `error`: falló herramienta, validación o ejecución no recuperable.

---

## 17. Checklist de constitución

- [x] Objetivo definido.
- [x] Alcance definido.
- [x] Stakeholders definidos.
- [x] Principios no negociables definidos.
- [x] Source-of-truth definido.
- [x] Definición de éxito definida.
- [x] Requerimientos funcionales definidos.
- [x] Requerimientos no funcionales definidos.
- [x] Restricciones definidas.
- [x] Criterios de aceptación definidos.
- [x] Matriz de trazabilidad definida.
- [x] Política de no improvisación definida.
