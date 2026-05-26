# Plan de Pruebas del Proyecto

## 1. Pruebas Unitarias (Backend)
- **test_validate_item_schema:** Valida que Pydantic rechace precios negativos.
- **test_validate_quantity:** Valida que la cantidad no sea negativa.

## 2. Pruebas de API e Integración
- **test_create_item:** Crea un item y valida código 201 y persistencia.
- **test_get_items:** Consulta la API y valida formato JSON and código 200.
- **test_delete_item:** Borra un item por ID y valida respuesta.