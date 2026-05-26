# Modelo de Datos

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