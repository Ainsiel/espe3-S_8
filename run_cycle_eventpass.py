"""Script para ejecutar el ciclo del orquestador para EventPass."""
import time
import json
import os
from core.orchestrator import Orchestrator

start = time.time()

orch = Orchestrator()
result = orch.execute_cycle(
    "EJEMPLO_TRES",
    "EventPass — Sistema de Reserva de Entradas a Eventos",
    "Desarrollar un sistema web sencillo para que los usuarios puedan registrarse, iniciar sesión con JWT, explorar un catálogo de eventos disponibles y reservar entradas de forma controlada con persistencia en SQLite, backend FastAPI y frontend React + Bootstrap 5."
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
