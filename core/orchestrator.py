import os
import json
from datetime import datetime, timezone
from core.logger import FactoryLogger
from core.usage_ledger import UsageLedger
from core.index_manager import IndexManager
from core.cache_manager import CacheManager
from core.sandbox import SandboxManager

# Import Agents
from agents.sdd_spec_agent import SDDSpecAgent
from agents.clarifier_qa_agent import ClarifierQAAgent
from agents.architect_agent import ArchitectAgent
from agents.task_analyzer_agent import TaskAnalyzerAgent
from agents.implementer_agent import ImplementerAgent
from agents.validation_agent import ValidationAgent
from agents.ops_security_agent import OpsSecurityAgent

class Orchestrator:
    def __init__(self, workspace_path=None):
        self.workspace_path = workspace_path or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.logger = FactoryLogger()
        self.usage_ledger = UsageLedger()
        self.index_manager = IndexManager(self.workspace_path)
        self.cache_manager = CacheManager(self.workspace_path)
        self.cycle_id = None
        self.state = {}

    def initialize_cycle(self, project_id, project_name, requirement):
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        self.cycle_id = f"CYCLE-{timestamp_str}"
        
        self.logger.set_cycle_id(self.cycle_id)
        self.usage_ledger.set_cycle_id(self.cycle_id)
        
        # Setup paths
        self.project_dir = os.path.join(self.workspace_path, "projects", project_id)
        self.specs_dir = os.path.join(self.project_dir, "specs")
        os.makedirs(self.project_dir, exist_ok=True)
        os.makedirs(self.specs_dir, exist_ok=True)

        self.state = {
            "cycle_id": self.cycle_id,
            "trace_id": f"TRACE-{timestamp_str}",
            "work_order_id": f"WO-{timestamp_str}",
            "project_id": project_id,
            "project_name": project_name,
            "status": "running",
            "objective": requirement,
            "current_phase": "INIT",
            "stack": {
                "backend": "Python3/FastAPI",
                "frontend": "React/Bootstrap",
                "database": "LiteSQL (SQLite)"
            },
            "gates": {
                "sdd_spec_first": "pending",
                "requirements_quality": "pending",
                "plan_valid": "pending",
                "analyze": "pending",
                "validation": "pending",
                "security": "pending",
                "budget": "pending"
            },
            "artifacts": {},
            "budget": {
                "max_tokens": 100000,
                "max_tool_calls": 50,
                "max_duration_minutes": 10
            },
            "usage": {},
            "decisions": [],
            "risks": [],
            "errors": []
        }
        self.save_state()

    def save_state(self):
        if self.cycle_id:
            state_path = os.path.join(self.workspace_path, ".factory", "runs", self.cycle_id, "state.json")
            os.makedirs(os.path.dirname(state_path), exist_ok=True)
            with open(state_path, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)

    def execute_cycle(self, project_id, project_name, requirement):
        self.initialize_cycle(project_id, project_name, requirement)
        self.logger.log_event("orchestrator", "plan", f"Ciclo de Orquestador iniciado: {self.cycle_id}", "success")
        
        try:
            # --- Paso 1. Planifica ciclo ---
            self.state["current_phase"] = "PLAN_CYCLE"
            self.save_state()
            self.logger.log_event("orchestrator", "plan", "Paso 1: Planificando ciclo y guardando Work Order", "success")
            
            work_order = {
                "work_order_id": self.state["work_order_id"],
                "project_id": project_id,
                "project_name": project_name,
                "requirement": requirement,
                "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }
            wo_path = os.path.join(self.specs_dir, "work_order.json")
            with open(wo_path, "w", encoding="utf-8") as f:
                json.dump(work_order, f, ensure_ascii=False, indent=2)
            self.state["artifacts"]["work_order"] = os.path.relpath(wo_path, self.workspace_path)
            self.save_state()

            # --- Paso 2. Index y Cache de Contexto ---
            self.state["current_phase"] = "LOAD_INDEX_CACHE"
            self.save_state()
            self.logger.log_event("orchestrator", "context", "Paso 2: Cargando Index e inicializando Cache de Contexto", "success")
            
            self.index_manager.scan_workspace()
            spec_hash = self.cache_manager.generate_hash(requirement)
            cached_plan = self.cache_manager.get_cache("plan_cache", spec_hash)
            if cached_plan:
                self.logger.log_event("orchestrator", "context", "Cache hit detectado para especificaciones de requerimiento similar", "success")
            
            # --- Paso 3. Analiza Aprendizaje.md ---
            self.state["current_phase"] = "READ_LEARNING"
            self.save_state()
            self.logger.log_event("orchestrator", "context", "Paso 3: Analizando Aprendizaje.md global y específico", "success")
            
            learning_path = os.path.join(self.workspace_path, "Aprendizaje.md")
            if not os.path.exists(learning_path):
                # Create empty template if not exists
                with open(learning_path, "w", encoding="utf-8") as f:
                    f.write("# Aprendizaje de Fábrica\n\n- No se han registrado fallas previas aún.\n")
            
            proj_learning_path = os.path.join(self.project_dir, "Aprendizaje.md")
            if not os.path.exists(proj_learning_path):
                with open(proj_learning_path, "w", encoding="utf-8") as f:
                    f.write(f"# Aprendizaje del Proyecto: {project_name}\n\n- Repositorio inicializado.\n")
            
            self.state["artifacts"]["learning_fabrica"] = os.path.relpath(learning_path, self.workspace_path)
            self.state["artifacts"]["learning_proyecto"] = os.path.relpath(proj_learning_path, self.workspace_path)
            self.save_state()

            # --- Paso 4 y 5. Logs y Usage ya inicializados en INIT ---
            self.logger.log_event("orchestrator", "logs", "Paso 4: Trazas e inicio de logs por agente LISTO", "success")
            self.logger.log_event("orchestrator", "budget", "Paso 5: Usage ledger inicializado y hora de inicio registrada", "success")

            # --- Paso 6. Informar plan al usuario ---
            self.state["current_phase"] = "INFORM_USER_PLAN"
            self.save_state()
            self.logger.log_event("orchestrator", "communication", "Paso 6: Informando plan del ciclo al usuario", "success")
            
            plan_message = f"""Inicio de Ciclo Operativo {self.cycle_id}
- ID de Proyecto: {project_id}
- Nombre de Proyecto: {project_name}
- Requerimiento: {requirement}
- Agentes involucrados: sdd_spec_agent, clarifier_qa_agent, architect_agent, task_analyzer_agent, implementer_agent, validation_agent, ops_security_agent
- Entorno de Validación: SANDBOX aislado ({os.path.join("sandbox", project_id)})
- Stack Técnico: FastAPI, React (Bootstrap), SQLite
- Gates Activos: Spec_exists, Trazabilidad_matrix, Pytest_run, Security_scan
- Circuit Breaker: Reintentos máximos = 1 por fase
"""
            self.logger.log_user_update(plan_message)

            # --- Paso 7. Ejecución de flujo SDD ---
            self.state["current_phase"] = "EXECUTE_SDD"
            self.save_state()
            self.logger.log_event("orchestrator", "sdd", "Paso 7: Iniciando Flujo Spec-Driven Development", "success")

            # A. Especificador SDD (Siempre Primero)
            spec_agent = SDDSpecAgent(self.logger, self.usage_ledger)
            spec_path = spec_agent.execute(project_id, project_name, requirement, self.specs_dir)
            self.state["artifacts"]["spec"] = os.path.relpath(spec_path, self.workspace_path)
            self.state["gates"]["sdd_spec_first"] = "pass"
            self.save_state()

            # B. Clarificador y Checklist
            clarifier = ClarifierQAAgent(self.logger, self.usage_ledger)
            clarifications_path, checklist_path = clarifier.execute(project_id, self.specs_dir)
            self.state["artifacts"]["clarifications"] = os.path.relpath(clarifications_path, self.workspace_path)
            self.state["artifacts"]["checklist"] = os.path.relpath(checklist_path, self.workspace_path)
            self.state["gates"]["requirements_quality"] = "pass"
            self.save_state()

            # C. Arquitecto
            architect = ArchitectAgent(self.logger, self.usage_ledger)
            plan_path, data_model_path, test_plan_path = architect.execute(project_id, self.specs_dir)
            self.state["artifacts"]["plan"] = os.path.relpath(plan_path, self.workspace_path)
            self.state["artifacts"]["data_model"] = os.path.relpath(data_model_path, self.workspace_path)
            self.state["artifacts"]["test_plan"] = os.path.relpath(test_plan_path, self.workspace_path)
            self.state["gates"]["plan_valid"] = "pass"
            self.save_state()

            # D. Tareas y Análisis
            analyzer = TaskAnalyzerAgent(self.logger, self.usage_ledger)
            tasks_path, analyze_path, traceability_path = analyzer.execute(project_id, self.specs_dir)
            self.state["artifacts"]["tasks"] = os.path.relpath(tasks_path, self.workspace_path)
            self.state["artifacts"]["analyze"] = os.path.relpath(analyze_path, self.workspace_path)
            self.state["artifacts"]["traceability"] = os.path.relpath(traceability_path, self.workspace_path)
            self.state["gates"]["analyze"] = "pass"
            self.save_state()

            # E. Implementación
            implementer = ImplementerAgent(self.logger, self.usage_ledger)
            backend_dir, frontend_dir = implementer.execute(project_id, self.project_dir)
            self.state["artifacts"]["backend"] = os.path.relpath(backend_dir, self.workspace_path)
            self.state["artifacts"]["frontend"] = os.path.relpath(frontend_dir, self.workspace_path)
            self.save_state()

            # F. Validación de Pruebas (Paso 8 integrado)
            self.state["current_phase"] = "EXECUTE_TESTS"
            self.save_state()
            self.logger.log_event("orchestrator", "validation", "Paso 8: Iniciando validación automatizada de pruebas en Sandbox", "success")
            
            validator = ValidationAgent(self.logger, self.usage_ledger)
            test_report_path, validation_path, tests_passed = validator.execute(project_id, self.project_dir, self.specs_dir)
            
            self.state["artifacts"]["test_report"] = os.path.relpath(test_report_path, self.workspace_path)
            self.state["artifacts"]["validation"] = os.path.relpath(validation_path, self.workspace_path)
            
            if not tests_passed:
                self.state["gates"]["validation"] = "fail"
                self.state["status"] = "error"
                self.save_state()
                # --- Paso 9: Si no cumple, registra aprendizaje y bloquea ---
                self.logger.log_event("orchestrator", "validation", "Fase de pruebas FALLÓ en el Sandbox. Registrando lección...", "error")
                with open(proj_learning_path, "a", encoding="utf-8") as lf:
                    lf.write(f"\n## LEARN-{datetime.now(timezone.utc).strftime('%Y%m%d')}-001\n- Tipo: test_failure\n- Causa: Falla al ejecutar suite de pytest en sandbox.\n")
                self.logger.log_user_update("CERRANDO CICLO CON ERROR: Suite de pruebas en Sandbox falló. Deteniendo pipeline.")
                return False
                
            self.state["gates"]["validation"] = "pass"
            self.save_state()

            # G. Seguridad y Operación
            security_agent = OpsSecurityAgent(self.logger, self.usage_ledger)
            security_path, deployment_path, rollback_path = security_agent.execute(project_id, self.specs_dir)
            self.state["artifacts"]["security"] = os.path.relpath(security_path, self.workspace_path)
            self.state["artifacts"]["deployment_plan"] = os.path.relpath(deployment_path, self.workspace_path)
            self.state["artifacts"]["rollback_plan"] = os.path.relpath(rollback_path, self.workspace_path)
            self.state["gates"]["security"] = "pass"
            self.save_state()

            # --- Paso 10. Actualizar Index e Cache ---
            self.state["current_phase"] = "UPDATE_INDEX_CACHE"
            self.save_state()
            self.logger.log_event("orchestrator", "context", "Paso 10: Actualizando índices y caché de compilación", "success")
            
            self.index_manager.scan_workspace()
            self.cache_manager.cache_context(spec_hash, "v1", requirement)
            
            # --- Paso 11. Informar resultado ---
            self.state["current_phase"] = "INFORM_RESULT"
            self.state["status"] = "complete"
            self.save_state()
            self.logger.log_event("orchestrator", "communication", "Paso 11: Enviando reporte de éxito al usuario", "success")
            
            totals = self.usage_ledger.get_totals()
            result_message = f"""Ciclo {self.cycle_id} COMPLETADO CON ÉXITO!
- Resultados: Código e interfaz generados en 'projects/{project_id}'
- Calidad: 100% de las pruebas pasaron en Sandbox
- Artefactos Creados: spec.md, plan.md, data-model.md, test-plan.md, tasks.md, traceability-matrix.md, test-report.md, security-review.md
- Costo operativo estimado: ${totals['estimated_cost']:.6f}
- Consumo de Tokens: Input={totals['input_tokens']}, Output={totals['output_tokens']}
"""
            self.logger.log_user_update(result_message)

            # --- Paso 12. Cierre y Tokens Ledger ---
            self.state["current_phase"] = "CLOSE"
            self.state["usage"] = totals
            self.save_state()
            
            final_report_path = os.path.join(self.workspace_path, ".factory", "runs", self.cycle_id, "final-report.md")
            with open(final_report_path, "w", encoding="utf-8") as f:
                f.write(f"""# Reporte Final de Ciclo: {self.cycle_id}

- **Estado:** Exitoso
- **Inicio:** {self.state['work_order_id']}
- **Tokens Totales:** {totals['input_tokens'] + totals['output_tokens']}
- **Costo de Ejecución:** ${totals['estimated_cost']:.6f}
- **Pruebas en Sandbox:** Completas (PASS)
""")
            
            self.logger.log_event("orchestrator", "close", f"Paso 12: Ciclo cerrado formalmente. Reporte guardado en Runs.", "success")
            return True

        except Exception as e:
            self.state["status"] = "error"
            self.state["errors"].append(str(e))
            self.save_state()
            self.logger.log_event("orchestrator", "error", f"Fallo catastrófico en el orquestador: {str(e)}", "error")
            return False
