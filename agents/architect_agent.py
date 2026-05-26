import os

class ArchitectAgent:
    def __init__(self, logger, usage_ledger):
        self.logger = logger
        self.usage_ledger = usage_ledger

    def execute(self, project_id, specs_dir):
        self.logger.log_event("architect_agent", "plan", "Iniciando diseño arquitectónico y plan técnico", "success")
        
        # Simulate LLM usage
        self.usage_ledger.record_usage(
            agent_id="architect_agent",
            phase="plan",
            skill_id="write_plan_artifact",
            input_tokens=2200,
            output_tokens=1800
        )

        if project_id.strip().upper() in ["UNO", "DOS", "TRES"]:
            plan_content = """# Plan Técnico y de Diseño Arquitectónico (TaskLiteJota)

## 1. Resumen de Arquitectura
Se propone un monolito estructurado modular pequeño:
- **Backend:** FastAPI (Python 3.9+) estructurado en modelos y controladores de tareas.
- **Frontend:** React + Bootstrap servido estáticamente en página única interactiva.
- **Base de Datos:** SQLite local (`db.sqlite3`) en modo archivo persistente.

## 2. Estructura de Módulos (Backend)
- `main.py`: Entrada del servidor, base de datos SQLite con SQLAlchemy, esquemas Pydantic y endpoints de API integrados.
- `tests/test_main.py`: Suite de pruebas Pytest utilizando `TestClient` de FastAPI.

## 3. Política de Dependencias Aprobada
- FastAPI (v0.95.0+)
- Uvicorn (v0.22.0+)
- SQLAlchemy (v2.0.0+)
- Pydantic (v1.10.0+)
"""
            
            data_model_content = """# Modelo de Datos (TaskLiteJota)

## 1. Entidades
| Entidad | Propósito | Almacenamiento | Sensible | Owner |
|---|---|---|---|---|
| Task | Almacena las tareas personales del usuario | SQLite | No | PO de Fábrica |

## 2. Campos
| Entidad | Campo | Tipo | Requerido | Validación | Sensible |
|---|---|---|---|---|---|
| Task | id | INTEGER | Sí (PK, Auto) | Autoincrementado | No |
| Task | titulo | VARCHAR(100)| Sí | len(x) >= 3 and len(x) <= 100 | No |
| Task | descripcion | TEXT | No | Opcional | No |
| Task | fecha_limite | VARCHAR(50) | No | Opcional (ISO Date string) | No |
| Task | prioridad | VARCHAR(20) | Sí | En enum: baja, media, alta | No |
| Task | estado | VARCHAR(20) | Sí | En enum: pendiente, completada | No |
| Task | created_at | DATETIME | Sí | Seteado en inserción | No |
| Task | updated_at | DATETIME | Sí | Actualizado en edición/estado | No |

## 3. Comportamiento ante Fallo
- Toda escritura sobre `Task` debe ser atómica. Ante excepciones se ejecuta rollback de la sesión.
"""
            
            test_plan_content = """# Plan de Pruebas del Proyecto (TaskLiteJota)

## 1. Pruebas Unitarias y API (Backend)
- `test_create_task_success`: Valida que se crea una tarea con datos correctos.
- `test_create_task_invalid_title`: Valida que falle la creación con título menor a 3 o mayor a 100 caracteres.
- `test_get_tasks_sorting`: Valida el listado y ordenamiento descendente por creación.
- `test_edit_task_success`: Modifica una tarea y comprueba actualización de `updated_at`.
- `test_toggle_status`: Completa y reabre una tarea, validando los estados correspondientes.
- `test_delete_task_success`: Elimina una tarea y valida que ya no exista.
- `test_delete_non_existent`: Valida código 404 al intentar borrar un ID inexistente.
"""
        elif project_id.strip().upper() == "CUATRO":
            plan_content = """# Plan Técnico y de Diseño Arquitectónico (StockMaster ERP Lite)

## 1. Resumen de Arquitectura
Se propone un monolito estructurado modular pequeño:
- **Backend:** FastAPI (Python 3) con SQLAlchemy para modelos y controladores integrados.
- **Frontend:** React + Bootstrap servido estáticamente en página única interactiva.
- **Base de Datos:** SQLite local (`db.sqlite3`) en modo archivo persistente.

## 2. Estructura de Módulos (Backend)
- `main.py`: Entrada del servidor, base de datos SQLite con SQLAlchemy, esquemas Pydantic y endpoints de API integrados.
- `tests/test_main.py`: Suite de pruebas Pytest utilizando `TestClient` de FastAPI.

## 3. Política de Dependencias Aprobada
- FastAPI (v0.95.0+)
- Uvicorn (v0.22.0+)
- SQLAlchemy (v2.0.0+)
- Pydantic (v1.10.0+)
"""
            
            data_model_content = """# Modelo de Datos (StockMaster ERP Lite)

## 1. Entidades
- `Product`: Tabla de productos del catálogo.
- `Warehouse`: Tabla de bodegas de almacenamiento.
- `StockMovement`: Historial de transacciones de inventario.

## 2. Campos
### Product
- `id` (INTEGER, PK, Auto)
- `sku` (VARCHAR(50), unique, required)
- `nombre` (VARCHAR(150), required)
- `descripcion` (TEXT, optional)
- `costo` (FLOAT, required, ge=0)
- `precio` (FLOAT, required, ge=0)
- `stock_disponible` (INTEGER, required, ge=0)
- `stock_minimo` (INTEGER, required, ge=0)
- `categoria` (VARCHAR(100))
- `marca` (VARCHAR(100))
- `unidad_medida` (VARCHAR(50))

### Warehouse
- `id` (INTEGER, PK, Auto)
- `codigo` (VARCHAR(20), unique, required)
- `nombre` (VARCHAR(100), required)
- `direccion` (VARCHAR(200))
- `encargado` (VARCHAR(100))

### StockMovement
- `id` (INTEGER, PK, Auto)
- `product_id` (INTEGER, FK to Product)
- `warehouse_id` (INTEGER, FK to Warehouse)
- `cantidad` (INTEGER, required, >0)
- `tipo` (VARCHAR(20)) -- entrada, salida, transferencia
- `documento_referencia` (VARCHAR(50))
- `usuario` (VARCHAR(100))
- `fecha` (DATETIME)
- `observacion` (TEXT)

## 3. Comportamiento ante Fallo
- Toda escritura de movimientos debe realizarse dentro de transacciones SQL atómicas para evitar inconsistencias en el cálculo del stock global de productos.
"""
            
            test_plan_content = """# Plan de Pruebas del Proyecto (StockMaster ERP Lite)

## 1. Pruebas Unitarias y API (Backend)
- `test_create_product_success`: Valida creación de producto con valores correctos.
- `test_create_product_duplicate_sku`: Valida código 400 ante SKU duplicado.
- `test_create_product_invalid_values`: Valida que costo o precio negativo devuelva 422.
- `test_create_warehouse`: Valida la creación de bodegas físicas.
- `test_movement_stock_in`: Valida registro de entrada y actualización de stock disponible.
- `test_movement_stock_out_insufficient`: Valida rechazo 400 ante salida superior al stock disponible (prevención stock negativo).
- `test_movement_transfer`: Valida el movimiento dual entre bodegas.
- `test_dashboard_kpis`: Valida agregación de KPIs en tiempo real.
"""
        else:
            plan_content = """# Plan Técnico y de Diseño Arquitectónico

## 1. Resumen de Arquitectura
Se propone un monolito estructurado modular pequeño:
- **Backend:** FastAPI (Python 3.9+) estructurado en controladores, modelos y esquemas de validación.
- **Frontend:** React + Bootstrap servido estáticamente o a través de servidor local de desarrollo.
- **Base de Datos:** SQLite local en modo archivo para asegurar persistencia transaccional simple.

## 2. Estructura de Módulos (Backend)
- `main.py`: Entrada del servidor y configuración de CORS.
- `db.py`: Inicialización de base de datos y sesión de SQLite.
- `models.py`: Modelo SQLAlchemy para la persistencia.
- `schemas.py`: Esquemas Pydantic para validación y serialización.
- `routes.py`: Rutas de la API FastAPI.

## 3. Estructura de Componentes (Frontend)
- `index.html`: Estructura HTML base que enlaza Bootstrap.
- `app.js`: Lógica interactiva en Vanilla JS/React para manejar la tabla, creación y borrado.

## 4. Política de Dependencias Aprobada
- FastAPI (v0.95.0+)
- Uvicorn (v0.22.0+)
- SQLAlchemy (v2.0.0+)
- Pydantic (v1.10.0+)
"""
            
            data_model_content = """# Modelo de Datos

## 1. Entidades
| Entidad | Propósito | Almacenamiento | Sensible | Owner |
|---|---|---|---|---|
| Item | Datos de los registros transaccionales | SQLite | No | PO de Fábrica |

## 2. Campos
| Entidad | Campo | Tipo | Requerido | Validación | Sensible |
|---|---|---|---|---|---|
| Item | id | INTEGER | Sí (PK, Auto) | Autoincrementado | No |
| Item | nombre | VARCHAR(100)| Sí | len(x) > 0 | No |
| Item | descripcion | TEXT | No | Ninguna | No |
| Item | cantidad | INTEGER | Sí | x >= 0 | No |
| Item | precio | FLOAT | Sí | x >= 0.0 | No |

## 3. Comportamiento ante Fallo
- Toda escritura sobre `Item` debe ser atómica. Ante cualquier excepción en SQLite, se ejecutará rollback de la sesión.
"""
            
            test_plan_content = """# Plan de Pruebas del Proyecto

## 1. Pruebas Unitarias (Backend)
- **test_validate_item_schema:** Valida que Pydantic rechace precios negativos.
- **test_validate_quantity:** Valida que la cantidad no sea negativa.

## 2. Pruebas de API e Integración
- **test_create_item:** Crea un item y valida código 201 y persistencia.
- **test_get_items:** Consulta la API y valida formato JSON and código 200.
- **test_delete_item:** Borra un item por ID y valida respuesta.
"""

        plan_path = os.path.join(specs_dir, "plan.md")
        with open(plan_path, "w", encoding="utf-8") as f:
            f.write(plan_content.strip())

        data_model_path = os.path.join(specs_dir, "data-model.md")
        with open(data_model_path, "w", encoding="utf-8") as f:
            f.write(data_model_content.strip())

        test_plan_path = os.path.join(specs_dir, "test-plan.md")
        with open(test_plan_path, "w", encoding="utf-8") as f:
            f.write(test_plan_content.strip())
            
        self.logger.log_event("architect_agent", "plan", f"Artefactos arquitectónicos creados en {specs_dir}", "success")
        return plan_path, data_model_path, test_plan_path
