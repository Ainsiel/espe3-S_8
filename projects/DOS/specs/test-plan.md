# Plan de Pruebas del Proyecto (TaskLiteJota)

## 1. Pruebas Unitarias y API (Backend)
- `test_create_task_success`: Valida que se crea una tarea con datos correctos.
- `test_create_task_invalid_title`: Valida que falle la creación con título menor a 3 o mayor a 100 caracteres.
- `test_get_tasks_sorting`: Valida el listado y ordenamiento descendente por creación.
- `test_edit_task_success`: Modifica una tarea y comprueba actualización de `updated_at`.
- `test_toggle_status`: Completa y reabre una tarea, validando los estados correspondientes.
- `test_delete_task_success`: Elimina una tarea y valida que ya no exista.
- `test_delete_non_existent`: Valida código 404 al intentar borrar un ID inexistente.