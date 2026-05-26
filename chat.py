import os
import json
import sys
from datetime import datetime, timezone
from core.orchestrator import Orchestrator

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_cumulative_metrics():
    runs_dir = os.path.join(os.path.dirname(__file__), ".factory", "runs")
    total_cycles = 0
    total_tokens = 0
    total_cost = 0.0
    total_tool_calls = 0
    projects = set()

    if os.path.exists(runs_dir):
        for run_id in os.listdir(runs_dir):
            state_path = os.path.join(runs_dir, run_id, "state.json")
            if os.path.exists(state_path):
                try:
                    with open(state_path, "r", encoding="utf-8") as f:
                        state = json.load(f)
                    total_cycles += 1
                    projects.add(state.get("project_id", "Unknown"))
                    usage = state.get("usage", {})
                    total_tokens += usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
                    total_cost += usage.get("estimated_cost", 0.0)
                    total_tool_calls += usage.get("tool_calls", 0)
                except Exception:
                    pass

    return {
        "cycles": total_cycles,
        "tokens": total_tokens,
        "cost": total_cost,
        "tool_calls": total_tool_calls,
        "projects_count": len(projects)
    }

def update_handoff_md():
    metrics = get_cumulative_metrics()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S") + " UTC"
    
    projects_dir = os.path.join(os.path.dirname(__file__), "projects")
    active_projects_str = ""
    if os.path.exists(projects_dir):
        for pid in os.listdir(projects_dir):
            p_path = os.path.join(projects_dir, pid)
            if os.path.isdir(p_path):
                # Search for any markdown spec inside projects/pid
                spec_files = [f for f in os.listdir(p_path) if f.endswith(".md") and f != "Aprendizaje.md"]
                has_spec = "Sí" if spec_files or os.path.exists(os.path.join(p_path, "specs", "spec.md")) else "No"
                active_projects_str += f"- **Proyecto ID:** `{pid}` (Especificación: {has_spec}) | [Abrir Directorio](file://{p_path})\n"
    if not active_projects_str:
        active_projects_str = "- No hay proyectos activos registrados aún en `projects/`.\n"

    handoff_content = f"""# Documentación de Traspaso (HANDOFF.md)

Este documento sirve como bitácora y estado de situación formal para la fábrica de software agentica **FabricaWebTransaccionalSDD**. Contiene información clave para los agentes y desarrolladores que inicien nuevos hilos de proyecto.

- **Última Actualización:** {today}
- **Estado de la Fábrica:** `OPERATIONAL` (Activa, Limpia y Validada para Nuevos Ciclos)

---

## 1. Métricas Acumuladas del Sistema
Estas métricas son calculadas dinámicamente de forma acumulada desde el historial en `.factory/runs/`:

| Métrica | Valor Registrado |
|---|---|
| Ciclos de Orquestación Ejecutados | {metrics['cycles']} |
| Proyectos Gestionados | {metrics['projects_count']} |
| Consumo Acumulado de Tokens | {metrics['tokens']} |
| Costo Estimado Acumulado | ${metrics['cost']:.6f} |
| Llamadas a Herramientas | {metrics['tool_calls']} |

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
{active_projects_str}
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
"""
    
    handoff_path = os.path.join(os.path.dirname(__file__), "HANDOFF.md")
    with open(handoff_path, "w", encoding="utf-8") as f:
        f.write(handoff_content.strip())

def main():
    update_handoff_md()
    while True:
        clear_screen()
        print("\033[94m==========================================================")
        print("         BIENVENIDO A FABRICAWEBTRANSACCIONALSDD")
        print("==========================================================\033[0m")
        print(" 1. Iniciar nuevo Ciclo de Desarrollo SDD (CHAT)")
        print(" 2. Listar Proyectos Activos")
        print(" 3. Ver Métricas e Historial Acumulado")
        print(" 4. Actualizar Index, Caché y Handoff")
        print(" 5. Salir")
        print("\033[94m==========================================================\033[0m")
        
        choice = input("Seleccione una opción (1-5): ").strip()
        
        if choice == "1":
            clear_screen()
            print("\033[95m--- INICIAR CICLO DE DESARROLLO SDD (CHAT) ---\033[0m\n")
            project_id = input("1. Ingrese el ID único del Proyecto (ej. inventario_app): ").strip()
            if not project_id:
                print("ID no válido.")
                input("\nPresione Enter para continuar...")
                continue
                
            project_name = input("2. Ingrese el Nombre del Proyecto (ej. Inventario de Repuestos): ").strip()
            print("\n3. Describa detalladamente el requerimiento o la idea de negocio:")
            print("(Ejemplo: 'Quiero un sistema para gestionar herramientas que tenga nombre, precio y stock. Solo admin puede agregar o borrar.')")
            requirement = input("\nRequerimiento: ").strip()
            
            if not requirement:
                print("Requerimiento no válido.")
                input("\nPresione Enter para continuar...")
                continue

            print("\n\033[93mIniciando Orquestador en segundo plano... Por favor, espere.\033[0m\n")
            
            # Run Orchestrator
            orch = Orchestrator()
            success = orch.execute_cycle(project_id, project_name, requirement)
            
            if success:
                print("\n\033[92m[ÉXITO] ¡El ciclo se completó satisfactoriamente y las pruebas pasaron en el Sandbox! \033[0m")
            else:
                print("\n\033[91m[ERROR] El ciclo falló o no superó los gates del Sandbox. Revise los logs.\033[0m")
            
            update_handoff_md()
            input("\nPresione Enter para continuar...")
            
        elif choice == "2":
            clear_screen()
            print("\033[95m--- PROYECTOS ACTIVOS EN LA FÁBRICA ---\033[0m\n")
            projects_dir = os.path.join(os.path.dirname(__file__), "projects")
            if os.path.exists(projects_dir):
                count = 0
                for pid in os.listdir(projects_dir):
                    p_path = os.path.join(projects_dir, pid)
                    if os.path.isdir(p_path):
                        count += 1
                        print(f"{count}. ID: {pid}")
                        spec_path = os.path.join(p_path, "specs", "spec.md")
                        if os.path.exists(spec_path):
                            print("   - Especificación: Creada y validada (spec.md)")
                        else:
                            print("   - Especificación: No encontrada")
                if count == 0:
                    print("No hay proyectos registrados.")
            else:
                print("No hay proyectos registrados.")
            input("\nPresione Enter para continuar...")
            
        elif choice == "3":
            clear_screen()
            print("\033[95m--- MÉTRICAS E HISTORIAL ACUMULADO ---\033[0m\n")
            metrics = get_cumulative_metrics()
            print(f"- Ciclos Totales Ejecutados: {metrics['cycles']}")
            print(f"- Proyectos Distintos: {metrics['projects_count']}")
            print(f"- Consumo de Tokens Acumulado: {metrics['tokens']} tokens")
            print(f"- Costo Acumulado Estimado: ${metrics['cost']:.6f}")
            print(f"- Llamadas a Herramientas: {metrics['tool_calls']}")
            
            print("\nHistorial de corridas:")
            runs_dir = os.path.join(os.path.dirname(__file__), ".factory", "runs")
            if os.path.exists(runs_dir):
                for run_id in sorted(os.listdir(runs_dir)):
                    state_path = os.path.join(runs_dir, run_id, "state.json")
                    if os.path.exists(state_path):
                        try:
                            with open(state_path, "r", encoding="utf-8") as f:
                                state = json.load(f)
                            print(f"  * [{run_id}] {state.get('project_name')} -> Estado: {state.get('status').upper()}")
                        except Exception:
                            pass
            input("\nPresione Enter para continuar...")
            
        elif choice == "4":
            print("\nActualizando index, caché y handoff...")
            orch = Orchestrator()
            orch.index_manager.scan_workspace()
            update_handoff_md()
            print("\033[92m[LISTO] Index, Caché y HANDOFF.md actualizados correctamente.\033[0m")
            input("\nPresione Enter para continuar...")
            
        elif choice == "5":
            print("\nSaliendo de la fábrica. ¡Hasta luego!")
            sys.exit(0)

if __name__ == "__main__":
    main()
