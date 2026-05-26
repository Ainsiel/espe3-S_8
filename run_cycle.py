"""Script temporal para ejecutar el ciclo del orquestador para TaskLiteJota."""
import time
import json
import os
from core.orchestrator import Orchestrator

start = time.time()

orch = Orchestrator()
result = orch.execute_cycle(
    "DOS",
    "TaskLiteJota - Gestor Personal de Tareas",
    "Desarrollar un sistema web para administrar tareas personales: crear, listar, editar, completar/reabrir, eliminar y filtrar tareas. Backend FastAPI con SQLite, frontend React + Bootstrap. Validar titulo 3-100 chars, prioridades baja/media/alta, estados pendiente/completada. Orden descendente por fecha de creacion."
)

elapsed = time.time() - start

print("\n")
print("=" * 60)
if result:
    print("  RESULTADO: EXITO - Ciclo completado satisfactoriamente")
else:
    print("  RESULTADO: FALLO - El ciclo no paso los gates")
print("=" * 60)
print(f"  Cycle ID: {orch.cycle_id}")
print(f"  Tiempo total: {elapsed:.2f} segundos")

# Print usage metrics
totals = orch.usage_ledger.get_totals()
print(f"  Input Tokens: {totals['input_tokens']}")
print(f"  Output Tokens: {totals['output_tokens']}")
print(f"  Cached Input Tokens: {totals['cached_input_tokens']}")
print(f"  Tool Calls: {totals['tool_calls']}")
print(f"  Costo Estimado: ${totals['estimated_cost']:.6f}")
print("=" * 60)
