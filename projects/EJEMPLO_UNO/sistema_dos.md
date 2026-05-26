# Especificación del sistema web: Gestor de Tareas Personales

## 1. Nombre del sistema

**TaskLiteJota — Gestor Personal de Tareas**

---

## 2. Objetivo general

Desarrollar un sistema web pequeño para que un usuario pueda administrar tareas personales de forma simple.

El sistema debe permitir:

- Crear tareas.
- Ver el listado de tareas.
- Editar tareas.
- Marcar tareas como completadas.
- Eliminar tareas.
- Filtrar tareas por estado.
- Guardar la información en una base de datos **SQLite**.

Este sistema está pensado como un ejercicio académico pequeño, fácil de ejecutar localmente y adecuado para ser desarrollado por una fábrica de agentes de IA.

---

## 3. Alcance del sistema

El sistema será una aplicación web básica con una interfaz sencilla.

Debe incluir:

- Backend web.
- Base de datos SQLite.
- Frontend WEB simple-> REACT + BOOTSTRAP
- Operaciones CRUD sobre tareas.
- Validaciones básicas.
- Estructura clara de archivos.
- Documentación mínima para instalación y ejecución.

No se requiere autenticación de usuarios en esta primera versión.

---

## 4. Tipo de aplicación

Aplicación web monousuario.

El sistema puede ejecutarse localmente en el computador del usuario usando un servidor web de desarrollo.

Tecnologías sugeridas:

- Backend: Python con FASTAPI.
- Base de datos: SQLite.
- Frontend: REACT + BOOTSTRAP

---

# 5. Funcionalidades principales

## 5.1 Crear tarea

El usuario debe poder crear una nueva tarea desde un formulario.

Campos requeridos:

- Título de la tarea.
- Descripción opcional.
- Fecha límite opcional.
- Prioridad.
- Estado inicial.

Reglas:

- El título es obligatorio.
- El título debe tener entre 3 y 100 caracteres.
- La descripción puede estar vacía.
- La prioridad puede ser: baja, media o alta.
- El estado inicial por defecto debe ser pendiente.

---

## 5.2 Listar tareas

El sistema debe mostrar todas las tareas registradas.

Cada tarea debe mostrar:

- ID.
- Título.
- Descripción.
- Fecha límite.
- Prioridad.
- Estado.
- Fecha de creación.
- Botones de acción:
  - Editar.
  - Completar / reabrir.
  - Eliminar.

Las tareas deben mostrarse ordenadas por fecha de creación descendente, mostrando primero las tareas más recientes.

---

## 5.3 Editar tarea

El usuario debe poder modificar una tarea existente.

Campos editables:

- Título.
- Descripción.
- Fecha límite.
- Prioridad.
- Estado.

Reglas:

- No se puede guardar una tarea sin título.
- Si la tarea no existe, se debe mostrar un mensaje de error.
- Al editar una tarea, debe actualizarse el campo `updated_at`.

---

## 5.4 Marcar tarea como completada

El usuario debe poder marcar una tarea pendiente como completada.

Reglas:

- Si la tarea está pendiente, se cambia a completada.
- Si la tarea está completada, puede volver a pendiente.
- Al cambiar el estado, debe actualizarse el campo `updated_at`.

---

## 5.5 Eliminar tarea

El usuario debe poder eliminar una tarea.

Reglas:

- Antes de eliminar, la interfaz debe pedir confirmación.
- Si la tarea existe, se elimina de la base de datos.
- Si la tarea no existe, se muestra un mensaje de error.

---

## 5.6 Filtrar tareas

El usuario debe poder filtrar tareas por estado.

Filtros mínimos:

- Todas.
- Pendientes.
- Completadas.

Opcionalmente se puede agregar filtro por prioridad:

- Baja.
- Media.
- Alta.

---

# 6. Requisitos no funcionales

## RNF-01 Simplicidad

El sistema debe ser fácil de entender, instalar y ejecutar.

## RNF-02 Ejecución local

El sistema debe ejecutarse localmente sin depender de servicios externos.

## RNF-03 Código ordenado

El código debe estar separado por responsabilidades.

## RNF-04 Seguridad básica

El sistema debe validar los datos recibidos desde formularios.

## RNF-05 Usabilidad

La interfaz debe ser clara, simple y usable.

## RNF-06 Compatibilidad

El sistema debe funcionar en un navegador moderno.

---


# 7. Flujo principal del usuario

1. El usuario abre la aplicación en el navegador.
2. El sistema muestra la lista de tareas.
3. El usuario presiona “Nueva tarea”.
4. El usuario completa el formulario.
5. El sistema valida los datos.
6. El sistema guarda la tarea en SQLite.
7. El sistema vuelve a la pantalla principal.
8. El usuario puede editar, completar o eliminar tareas.

---

# 8. Casos de uso

## Caso de uso 1: Crear una tarea

Actor: Usuario.

Flujo:

1. Usuario entra a la pantalla principal.
2. Usuario selecciona “Nueva tarea”.
3. Usuario ingresa título, descripción, fecha límite y prioridad.
4. Usuario presiona “Guardar”.
5. Sistema valida los datos.
6. Sistema guarda la tarea.
7. Sistema muestra mensaje de éxito.

Resultado: La tarea queda registrada como pendiente.

---

## Caso de uso 2: Completar una tarea

Actor: Usuario.

Flujo:

1. Usuario visualiza el listado de tareas.
2. Usuario presiona “Completar” en una tarea pendiente.
3. Sistema cambia el estado a completada.
4. Sistema actualiza la lista.

Resultado: La tarea aparece como completada.

---

## Caso de uso 3: Editar una tarea

Actor: Usuario.

Flujo:

1. Usuario visualiza una tarea.
2. Usuario presiona “Editar”.
3. Sistema muestra formulario con datos actuales.
4. Usuario modifica los datos.
5. Usuario presiona “Guardar”.
6. Sistema actualiza la tarea.

Resultado: La tarea queda actualizada.

---

## Caso de uso 4: Eliminar una tarea

Actor: Usuario.

Flujo:

1. Usuario visualiza una tarea.
2. Usuario presiona “Eliminar”.
3. Sistema solicita confirmación.
4. Usuario confirma.
5. Sistema elimina la tarea.

Resultado: La tarea ya no aparece en el listado.

---

# 9. Criterios de aceptación

El sistema se considera terminado cuando cumple lo siguiente:

- Se puede ejecutar localmente.
- Crea automáticamente la base de datos SQLite si no existe.
- Permite crear tareas.
- Permite listar tareas.
- Permite editar tareas.
- Permite marcar tareas como completadas.
- Permite reabrir tareas completadas.
- Permite eliminar tareas.
- Permite filtrar por estado.
- Valida que el título no esté vacío.
- Guarda los datos correctamente en SQLite.
- Tiene una interfaz simple y entendible.
- Incluye un README con instrucciones de instalación y ejecución.

---

# 10. Checklist de pruebas

```text
[ ] La aplicación inicia sin errores.
[ ] La base de datos SQLite se crea automáticamente.
[ ] Se puede crear una tarea con título válido.
[ ] No se puede crear una tarea sin título.
[ ] Se muestran las tareas creadas.
[ ] Se puede editar una tarea.
[ ] Se puede marcar una tarea como completada.
[ ] Se puede reabrir una tarea completada.
[ ] Se puede eliminar una tarea.
[ ] Se pide confirmación antes de eliminar.
[ ] El filtro “Todas” funciona.
[ ] El filtro “Pendientes” funciona.
[ ] El filtro “Completadas” funciona.
[ ] Los datos persisten al reiniciar la aplicación.
```

---

# 25. Definición final del producto mínimo viable

El producto mínimo viable debe ser una aplicación web local llamada **TaskLiteJota**, desarrollada con **FASTAPI y SQLite**, que permita administrar tareas personales mediante una interfaz simple.

Debe incluir creación, listado, edición, eliminación, cambio de estado y filtrado de tareas.

El sistema debe estar organizado, documentado y listo para ser ejecutado como ejercicio académico.
