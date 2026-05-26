# Especificación del sistema web: Gestión Avanzada de Inventario ERP

## 1. Nombre del sistema

**StockMaster ERP Lite — Sistema Web Avanzado de Inventario, Dashboard y Reportes**

---

## 2. Objetivo general

Desarrollar una aplicación web responsiva para gestionar inventario avanzado con lógica tipo ERP, permitiendo controlar productos, bodegas, ubicaciones, stock, movimientos, compras, ventas, transferencias, ajustes, conteos físicos, alertas, dashboard ejecutivo y reportes operacionales.

El sistema debe permitir:

- Administrar productos, categorías, marcas, unidades de medida, proveedores, clientes, bodegas y ubicaciones.
- Controlar stock disponible, reservado, comprometido, en tránsito y mínimo.
- Registrar entradas, salidas, transferencias, ajustes, compras, recepciones y despachos.
- Mantener trazabilidad mediante Kardex, lotes, series y auditoría.
- Generar reportes exportables y dashboard con indicadores clave.
- Operar desde escritorio, tablet y móvil mediante interfaz responsiva.
- Guardar información en base de datos **MySQL o MariaDB**.

Este sistema está pensado para una fábrica de agentes de IA que deba construir software web transaccional, modular, validable, documentado y fácil de mantener.

---

## 3. Alcance del sistema

El sistema será una aplicación web multiusuario para gestión integral de inventario.

Debe incluir:

- Backend web con API REST.
- Base de datos MySQL o MariaDB.
- Frontend web responsivo con React + Bootstrap.
- Autenticación, roles y permisos.
- CRUD completo de maestros.
- Gestión de stock por producto, bodega y ubicación.
- Registro de movimientos de inventario.
- Kardex completo por producto.
- Dashboard con indicadores.
- Reportes exportables a Excel/CSV/PDF.
- Validaciones de negocio.
- Auditoría de acciones críticas.
- Estructura clara de archivos.
- Documentación de instalación, ejecución y pruebas.

No se incluyen en esta primera versión:

- Contabilidad completa.
- Facturación electrónica real.
- Integración directa con SII u organismos tributarios.
- Integración con hardware físico como lectores RFID o balanzas industriales.
- Aplicación móvil nativa.
- Inteligencia artificial predictiva avanzada.

---

## 4. Tipo de aplicación

Aplicación web transaccional multiusuario.

El sistema puede ejecutarse localmente o en un servidor privado usando backend, frontend y base de datos separados.

Tecnologías sugeridas:

- Backend: Python 3 con FASTAPI.
- Base de datos: MySQL o MariaDB.
- ORM: SQLAlchemy.
- Migraciones: Alembic.
- Frontend: React + Bootstrap.
- Cliente HTTP: Axios o Fetch API.
- Autenticación: JWT.
- Reportes: generación CSV/XLSX/PDF.
- Documentación API: Swagger/OpenAPI automático de FastAPI.

Arquitectura mínima:

```text
frontend-react-bootstrap/
backend-fastapi/
database-mysql-mariadb/
docs/
tests/
```

---

# 5. Funcionalidades principales

## 5.1 Autenticación y usuarios

El sistema debe permitir acceso seguro por usuario y contraseña.

Campos mínimos de usuario:

- ID.
- Nombre.
- Email.
- Contraseña encriptada.
- Rol.
- Estado.
- Fecha de creación.
- Fecha de actualización.

Roles mínimos:

- Administrador.
- Jefe de inventario.
- Operador de bodega.
- Compras.
- Ventas.
- Auditor / solo lectura.

Reglas:

- El email debe ser único.
- La contraseña no debe almacenarse en texto plano.
- Un usuario inactivo no puede iniciar sesión.
- Cada acción crítica debe registrar usuario, fecha, entidad y acción.

---

## 5.2 Dashboard principal

El sistema debe mostrar un dashboard inicial con visión ejecutiva del inventario.

Indicadores mínimos:

- Total de productos activos.
- Valor total estimado del inventario.
- Stock total por bodega.
- Productos bajo stock mínimo.
- Productos sin stock.
- Movimientos del día.
- Entradas del mes.
- Salidas del mes.
- Transferencias pendientes.
- Compras pendientes de recepción.
- Productos con mayor rotación.
- Productos sin movimiento.

Visualizaciones mínimas:

- Tarjetas KPI.
- Gráfico de stock por categoría.
- Gráfico de movimientos por período.
- Tabla de alertas críticas.
- Tabla de últimos movimientos.

Reglas:

- El dashboard debe cargar datos reales desde la API.
- Los indicadores deben actualizarse al registrar movimientos.
- El usuario solo debe ver información permitida por su rol.

---

## 5.3 Gestión de productos

El usuario autorizado debe poder crear, listar, editar, activar/desactivar y consultar productos.

Campos mínimos:

- SKU.
- Código de barras opcional.
- Nombre.
- Descripción.
- Categoría.
- Marca.
- Unidad de medida.
- Costo unitario.
- Precio de venta opcional.
- Stock mínimo.
- Stock máximo.
- Controla lote: sí/no.
- Controla serie: sí/no.
- Estado.
- Imagen opcional.

Reglas:

- El SKU es obligatorio y único.
- El nombre es obligatorio y debe tener entre 3 y 150 caracteres.
- El costo no puede ser negativo.
- El stock mínimo no puede ser negativo.
- Un producto con movimientos no debe eliminarse físicamente; debe desactivarse.
- Si controla serie, cada unidad debe tener número de serie único.
- Si controla lote, los movimientos deben indicar lote cuando aplique.

---

## 5.4 Gestión de categorías, marcas y unidades de medida

El sistema debe permitir administrar catálogos maestros.

Catálogos mínimos:

- Categorías.
- Subcategorías.
- Marcas.
- Unidades de medida.
- Familias de productos.

Reglas:

- El nombre de cada catálogo debe ser obligatorio.
- No se deben permitir duplicados activos.
- No se debe eliminar un catálogo asociado a productos; debe desactivarse.

---

## 5.5 Gestión de bodegas y ubicaciones

El sistema debe permitir controlar inventario por bodega y ubicación física.

Campos mínimos de bodega:

- Código.
- Nombre.
- Dirección.
- Responsable.
- Estado.

Campos mínimos de ubicación:

- Bodega.
- Pasillo.
- Estante.
- Nivel.
- Posición.
- Código interno.
- Estado.

Reglas:

- Una bodega puede tener múltiples ubicaciones.
- El código de bodega debe ser único.
- La ubicación debe ser única dentro de una bodega.
- Una ubicación con stock no puede desactivarse sin mover el inventario.

---

## 5.6 Gestión de proveedores

El usuario autorizado debe poder crear, listar, editar, activar/desactivar y consultar proveedores.

Campos mínimos:

- RUT o identificador fiscal.
- Razón social.
- Nombre comercial.
- Email.
- Teléfono.
- Dirección.
- Contacto principal.
- Condición de pago.
- Estado.

Reglas:

- El identificador fiscal debe ser único.
- Un proveedor con compras asociadas no debe eliminarse físicamente.
- El email debe tener formato válido si se informa.

---

## 5.7 Gestión de clientes internos o externos

El sistema debe permitir registrar clientes para salidas, despachos o consumo interno.

Campos mínimos:

- Código.
- Nombre.
- Tipo: interno o externo.
- Email opcional.
- Teléfono opcional.
- Dirección opcional.
- Estado.

Reglas:

- El código debe ser único.
- Un cliente con movimientos asociados no debe eliminarse físicamente.

---

## 5.8 Consulta de inventario actual

El sistema debe mostrar el stock actual por producto, bodega, ubicación, lote y serie.

Cada registro debe mostrar:

- Producto.
- SKU.
- Bodega.
- Ubicación.
- Lote, si aplica.
- Serie, si aplica.
- Stock disponible.
- Stock reservado.
- Stock comprometido.
- Stock en tránsito.
- Costo promedio.
- Valor estimado.
- Fecha del último movimiento.

Filtros mínimos:

- Producto.
- SKU.
- Categoría.
- Bodega.
- Ubicación.
- Stock bajo mínimo.
- Sin stock.
- Lote.
- Serie.

Reglas:

- El inventario debe calcularse a partir de movimientos válidos.
- No se debe permitir stock negativo salvo configuración explícita autorizada.
- El stock disponible debe considerar reservas y compromisos.

---

## 5.9 Kardex de producto

El sistema debe mostrar el historial completo de movimientos de un producto.

Cada movimiento debe mostrar:

- Fecha.
- Tipo de movimiento.
- Documento origen.
- Bodega origen.
- Bodega destino.
- Cantidad entrada.
- Cantidad salida.
- Saldo posterior.
- Costo unitario.
- Costo total.
- Usuario responsable.
- Observación.

Reglas:

- El Kardex no debe poder editarse directamente.
- Cada movimiento debe mantener trazabilidad del documento origen.
- El saldo posterior debe ser consistente con la secuencia de movimientos.

---

## 5.10 Entradas de inventario

El sistema debe permitir registrar entradas manuales o por recepción de compra.

Campos mínimos:

- Producto.
- Bodega destino.
- Ubicación destino.
- Cantidad.
- Costo unitario.
- Proveedor opcional.
- Documento referencia.
- Lote, si aplica.
- Serie, si aplica.
- Observación.

Reglas:

- La cantidad debe ser mayor que cero.
- El costo unitario no puede ser negativo.
- Si el producto controla lote, el lote es obligatorio.
- Si el producto controla serie, se debe registrar una serie por unidad.
- Al confirmar la entrada, se actualiza el stock y se registra Kardex.

---

## 5.11 Salidas de inventario

El sistema debe permitir registrar salidas por venta, consumo interno, merma, devolución o ajuste autorizado.

Campos mínimos:

- Producto.
- Bodega origen.
- Ubicación origen.
- Cantidad.
- Tipo de salida.
- Cliente o área solicitante.
- Documento referencia.
- Lote, si aplica.
- Serie, si aplica.
- Observación.

Reglas:

- La cantidad debe ser mayor que cero.
- No se puede retirar más stock del disponible.
- Si el producto controla serie, se deben seleccionar las series exactas.
- Al confirmar la salida, se descuenta stock y se registra Kardex.

---

## 5.12 Transferencias entre bodegas o ubicaciones

El sistema debe permitir transferir productos entre bodegas o ubicaciones.

Estados mínimos:

- Borrador.
- En tránsito.
- Recibida.
- Cancelada.

Campos mínimos:

- Bodega origen.
- Ubicación origen.
- Bodega destino.
- Ubicación destino.
- Producto.
- Cantidad.
- Fecha de envío.
- Fecha de recepción.
- Usuario emisor.
- Usuario receptor.
- Observación.

Reglas:

- Origen y destino no pueden ser iguales.
- La cantidad debe ser mayor que cero.
- Al enviar, el stock pasa a estado en tránsito.
- Al recibir, el stock se suma al destino.
- Una transferencia recibida no puede editarse.

---

## 5.13 Ajustes de inventario

El sistema debe permitir ajustar stock por diferencias detectadas.

Tipos mínimos:

- Ajuste positivo.
- Ajuste negativo.
- Corrección por conteo físico.
- Merma.
- Pérdida.
- Daño.

Reglas:

- Todo ajuste debe requerir motivo obligatorio.
- Los ajustes negativos deben validar stock disponible.
- Los ajustes deben quedar en auditoría.
- Opcionalmente, ajustes superiores a un umbral requieren aprobación.

---

## 5.14 Órdenes de compra y recepción

El sistema debe permitir crear órdenes de compra y recepcionar productos.

Estados mínimos de orden de compra:

- Borrador.
- Emitida.
- Parcialmente recibida.
- Recibida.
- Cancelada.

Campos mínimos:

- Número de orden.
- Proveedor.
- Fecha de emisión.
- Fecha esperada.
- Productos.
- Cantidades solicitadas.
- Costos unitarios.
- Total estimado.
- Estado.

Reglas:

- Una orden emitida puede recibir productos parcial o totalmente.
- La recepción genera entrada de inventario.
- No se debe recepcionar más de lo solicitado salvo permiso especial.
- Una orden recibida no debe modificarse sin autorización.

---

## 5.15 Reservas y compromisos de stock

El sistema debe permitir reservar productos para ventas, pedidos internos o proyectos.

Campos mínimos:

- Producto.
- Cantidad reservada.
- Bodega.
- Cliente o área solicitante.
- Fecha de expiración.
- Estado.

Estados mínimos:

- Activa.
- Consumida.
- Liberada.
- Vencida.

Reglas:

- No se puede reservar más que el stock disponible.
- La reserva reduce el stock disponible, pero no el stock físico.
- Al despachar, la reserva se consume.
- Las reservas vencidas pueden liberarse automáticamente o manualmente.

---

## 5.16 Inventario físico y conteo cíclico

El sistema debe permitir realizar conteos físicos por bodega, ubicación, categoría o producto.

Estados mínimos:

- Planificado.
- En conteo.
- Cerrado.
- Ajustado.

Campos mínimos:

- Nombre del conteo.
- Bodega.
- Ubicación opcional.
- Productos incluidos.
- Stock teórico.
- Stock contado.
- Diferencia.
- Responsable.
- Fecha.

Reglas:

- Un conteo cerrado no puede editarse.
- Las diferencias deben generar propuesta de ajuste.
- El ajuste debe ser confirmado por usuario autorizado.
- Debe quedar evidencia de stock teórico versus stock contado.

---

## 5.17 Reportes

El sistema debe permitir consultar y exportar reportes.

Reportes mínimos:

- Inventario actual.
- Kardex por producto.
- Movimientos por período.
- Stock bajo mínimo.
- Productos sin stock.
- Productos sin movimiento.
- Valorización de inventario.
- Rotación de productos.
- Entradas por proveedor.
- Salidas por cliente o área.
- Transferencias por estado.
- Ajustes por motivo.
- Diferencias de inventario físico.

Formatos mínimos:

- Vista web.
- CSV.
- Excel/XLSX.
- PDF simple.

Reglas:

- Todo reporte debe permitir filtros por fecha cuando aplique.
- Los reportes exportados deben respetar los filtros aplicados.
- Los usuarios solo pueden exportar reportes permitidos por su rol.

---

## 5.18 Alertas y notificaciones internas

El sistema debe mostrar alertas operacionales.

Alertas mínimas:

- Producto bajo stock mínimo.
- Producto sin stock.
- Producto sobre stock máximo.
- Compra pendiente de recepción.
- Transferencia pendiente de recepción.
- Reserva próxima a vencer.
- Producto sin movimiento por más de X días.

Reglas:

- Las alertas deben mostrarse en dashboard.
- Deben poder filtrarse por severidad.
- Deben poder marcarse como revisadas.

---

## 5.19 Búsqueda avanzada

El sistema debe permitir búsqueda rápida y avanzada.

Búsqueda rápida:

- SKU.
- Nombre.
- Código de barras.
- Lote.
- Serie.

Búsqueda avanzada:

- Categoría.
- Marca.
- Bodega.
- Proveedor.
- Estado de stock.
- Rango de fechas.

Reglas:

- La búsqueda debe responder en tiempo razonable.
- Los resultados deben poder ordenarse y paginarse.

---

## 5.20 Importación y exportación de datos

El sistema debe permitir cargar maestros mediante archivo.

Importaciones mínimas:

- Productos.
- Proveedores.
- Clientes.
- Stock inicial.
- Ubicaciones.

Reglas:

- El archivo debe validarse antes de importar.
- Debe mostrarse resumen de errores.
- No deben insertarse datos inválidos.
- La importación debe registrar auditoría.
- Debe existir plantilla descargable por tipo de importación.

---

## 5.21 Auditoría

El sistema debe registrar acciones relevantes.

Eventos mínimos:

- Inicio de sesión.
- Creación de producto.
- Edición de producto.
- Desactivación de producto.
- Entrada de inventario.
- Salida de inventario.
- Transferencia.
- Ajuste.
- Conteo físico.
- Exportación de reporte.

Campos mínimos:

- Usuario.
- Fecha y hora.
- Módulo.
- Acción.
- Entidad afectada.
- ID de entidad.
- Valores anteriores, cuando aplique.
- Valores nuevos, cuando aplique.
- IP o identificador de sesión opcional.

Reglas:

- La auditoría no debe ser editable desde la interfaz normal.
- Solo administradores o auditores pueden consultarla.

---

## 5.22 Configuración general

El administrador debe poder configurar parámetros del sistema.

Parámetros mínimos:

- Permitir stock negativo: sí/no.
- Moneda por defecto.
- Decimales de cantidad.
- Decimales de costo.
- Método de costo: promedio ponderado inicial.
- Umbral de aprobación para ajustes.
- Días para producto sin movimiento.
- Formato de código interno.

Reglas:

- Los cambios de configuración deben quedar auditados.
- Configuraciones críticas deben requerir rol administrador.

---

# 6. Requisitos no funcionales

## RNF-01 Simplicidad operativa

El sistema debe ser entendible, instalable y ejecutable con instrucciones claras.

## RNF-02 Modularidad

El código debe separarse por responsabilidades: rutas, servicios, modelos, esquemas, repositorios, componentes, páginas y utilidades.

## RNF-03 Rendimiento

Las consultas de inventario y reportes deben usar paginación, filtros e índices en base de datos.

## RNF-04 Seguridad básica

El sistema debe validar entrada de datos, proteger rutas, encriptar contraseñas y aplicar permisos por rol.

## RNF-05 Trazabilidad

Todo movimiento que afecte stock debe quedar registrado en Kardex y auditoría.

## RNF-06 Usabilidad

La interfaz debe ser clara, rápida y usable por personal operativo.

## RNF-07 Responsividad

El sistema debe funcionar correctamente en escritorio, tablet y móvil.

## RNF-08 Compatibilidad

Debe funcionar en navegadores modernos: Chrome, Edge, Firefox y Safari.

## RNF-09 Integridad de datos

La base de datos debe usar claves primarias, claves foráneas, restricciones únicas e índices.

## RNF-10 Escalabilidad básica

El diseño debe permitir agregar módulos futuros de ventas, compras, contabilidad o integraciones externas.

## RNF-11 Disponibilidad local o servidor

El sistema debe poder ejecutarse en ambiente local, QA o producción privada.

## RNF-12 Documentación

Debe incluir README, documentación técnica, endpoints principales, modelo de datos y guía de pruebas.

---

# 7. Flujo principal del usuario

1. El usuario abre la aplicación web.
2. El sistema muestra pantalla de login.
3. El usuario inicia sesión.
4. El sistema valida credenciales y permisos.
5. El sistema muestra dashboard principal.
6. El usuario consulta alertas de stock.
7. El usuario revisa inventario actual.
8. El usuario registra una entrada, salida, transferencia o ajuste.
9. El sistema valida reglas de negocio.
10. El sistema registra movimiento, actualiza stock, genera Kardex y auditoría.
11. El usuario consulta reportes.
12. El usuario exporta información si tiene permisos.

---

# 8. Casos de uso

## Caso de uso 1: Iniciar sesión

Actor: Usuario.

Flujo:

1. Usuario abre la aplicación.
2. Usuario ingresa email y contraseña.
3. Sistema valida credenciales.
4. Sistema genera token de sesión.
5. Sistema muestra dashboard.

Resultado: Usuario accede al sistema según su rol.

---

## Caso de uso 2: Crear producto

Actor: Administrador o jefe de inventario.

Flujo:

1. Usuario entra al módulo Productos.
2. Usuario presiona “Nuevo producto”.
3. Usuario ingresa SKU, nombre, categoría, unidad, costo y reglas de control.
4. Sistema valida campos obligatorios y SKU único.
5. Sistema guarda producto.
6. Sistema registra auditoría.
7. Sistema muestra mensaje de éxito.

Resultado: Producto queda creado y disponible para movimientos.

---

## Caso de uso 3: Consultar inventario actual

Actor: Usuario autorizado.

Flujo:

1. Usuario entra al módulo Inventario.
2. Usuario aplica filtros por producto, bodega o categoría.
3. Sistema consulta stock consolidado.
4. Sistema muestra stock disponible, reservado y valorizado.

Resultado: Usuario visualiza estado actual del inventario.

---

## Caso de uso 4: Registrar entrada de inventario

Actor: Operador de bodega o compras.

Flujo:

1. Usuario entra a Movimientos > Entrada.
2. Usuario selecciona producto, bodega, ubicación y cantidad.
3. Usuario informa costo y documento de referencia.
4. Sistema valida cantidad, costo, lote o serie si aplica.
5. Usuario confirma entrada.
6. Sistema actualiza stock.
7. Sistema registra Kardex y auditoría.

Resultado: Inventario aumenta en la bodega indicada.

---

## Caso de uso 5: Registrar salida de inventario

Actor: Operador de bodega o ventas.

Flujo:

1. Usuario entra a Movimientos > Salida.
2. Usuario selecciona producto, bodega, ubicación y cantidad.
3. Sistema valida stock disponible.
4. Usuario informa motivo y documento de referencia.
5. Usuario confirma salida.
6. Sistema descuenta stock.
7. Sistema registra Kardex y auditoría.

Resultado: Inventario disminuye de forma controlada.

---

## Caso de uso 6: Transferir stock entre bodegas

Actor: Operador de bodega.

Flujo:

1. Usuario crea transferencia.
2. Selecciona bodega origen y destino.
3. Agrega productos y cantidades.
4. Sistema valida stock disponible.
5. Usuario confirma envío.
6. Sistema mueve stock a estado en tránsito.
7. Usuario receptor confirma recepción.
8. Sistema suma stock en destino.

Resultado: Stock queda transferido con trazabilidad.

---

## Caso de uso 7: Ajustar inventario

Actor: Jefe de inventario.

Flujo:

1. Usuario entra a Ajustes.
2. Selecciona producto, bodega y ubicación.
3. Informa cantidad de ajuste y motivo.
4. Sistema valida permisos y stock disponible.
5. Usuario confirma ajuste.
6. Sistema actualiza stock, Kardex y auditoría.

Resultado: Stock queda corregido con motivo documentado.

---

## Caso de uso 8: Crear orden de compra

Actor: Compras.

Flujo:

1. Usuario entra a Compras.
2. Crea orden de compra.
3. Selecciona proveedor y productos.
4. Informa cantidades y costos.
5. Sistema calcula total.
6. Usuario emite la orden.

Resultado: Orden queda emitida y pendiente de recepción.

---

## Caso de uso 9: Recepcionar orden de compra

Actor: Compras u operador de bodega.

Flujo:

1. Usuario abre orden emitida.
2. Selecciona productos a recepcionar.
3. Informa cantidades recibidas.
4. Sistema valida contra cantidades solicitadas.
5. Usuario confirma recepción.
6. Sistema genera entrada de inventario.
7. Sistema actualiza estado de la orden.

Resultado: Compra queda parcial o totalmente recibida.

---

## Caso de uso 10: Realizar conteo físico

Actor: Jefe de inventario u operador autorizado.

Flujo:

1. Usuario crea conteo físico.
2. Selecciona bodega, ubicación o productos.
3. Sistema congela stock teórico de referencia.
4. Usuario registra cantidades contadas.
5. Sistema calcula diferencias.
6. Usuario cierra conteo.
7. Usuario autorizado genera ajustes si corresponde.

Resultado: Diferencias quedan registradas y corregidas.

---

## Caso de uso 11: Consultar dashboard

Actor: Usuario autorizado.

Flujo:

1. Usuario entra al dashboard.
2. Sistema carga KPIs y gráficos.
3. Usuario revisa alertas y últimos movimientos.
4. Usuario accede a detalle desde una tarjeta o alerta.

Resultado: Usuario obtiene visión ejecutiva del inventario.

---

## Caso de uso 12: Generar reporte

Actor: Usuario autorizado.

Flujo:

1. Usuario entra a Reportes.
2. Selecciona tipo de reporte.
3. Define filtros.
4. Sistema muestra vista previa.
5. Usuario exporta si tiene permisos.

Resultado: Reporte queda disponible en pantalla o archivo.

---

# 9. Criterios de aceptación

El sistema se considera terminado cuando cumple lo siguiente:

- Se puede ejecutar localmente o en servidor de desarrollo.
- Backend FASTAPI inicia sin errores.
- Frontend React + Bootstrap inicia sin errores.
- Base de datos MySQL/MariaDB se conecta correctamente.
- Migraciones crean las tablas necesarias.
- Permite iniciar sesión con usuario válido.
- Aplica roles y permisos básicos.
- Permite crear, listar, editar y desactivar productos.
- Permite administrar categorías, marcas y unidades.
- Permite administrar bodegas y ubicaciones.
- Permite administrar proveedores y clientes.
- Permite consultar inventario actual.
- Permite registrar entradas de inventario.
- Permite registrar salidas de inventario.
- Permite transferir stock entre bodegas o ubicaciones.
- Permite registrar ajustes con motivo.
- Permite crear y recepcionar órdenes de compra.
- Permite gestionar reservas de stock.
- Permite ejecutar conteo físico.
- Actualiza stock correctamente después de cada movimiento.
- Registra Kardex por producto.
- Registra auditoría de acciones críticas.
- Muestra dashboard con KPIs reales.
- Muestra alertas de stock mínimo y sin stock.
- Permite generar reportes filtrados.
- Permite exportar reportes a CSV/XLSX/PDF.
- Valida campos obligatorios.
- Evita duplicidad de SKU.
- Evita salidas mayores al stock disponible.
- Es responsivo en escritorio, tablet y móvil.
- Incluye README con instalación, ejecución y pruebas.

---

# 10. Checklist de pruebas

```text
[ ] La aplicación inicia sin errores.
[ ] El backend FASTAPI responde en /docs.
[ ] El frontend React carga correctamente.
[ ] La conexión a MySQL/MariaDB funciona.
[ ] Las migraciones crean tablas correctamente.
[ ] Se puede crear usuario administrador inicial.
[ ] Se puede iniciar sesión con credenciales válidas.
[ ] No se puede iniciar sesión con credenciales inválidas.
[ ] Un usuario inactivo no puede iniciar sesión.
[ ] Se aplica control de permisos por rol.
[ ] Se puede crear un producto con SKU válido.
[ ] No se puede crear producto sin nombre.
[ ] No se puede crear producto con SKU duplicado.
[ ] Se puede editar un producto existente.
[ ] Se puede desactivar un producto.
[ ] Se puede crear categoría.
[ ] Se puede crear marca.
[ ] Se puede crear unidad de medida.
[ ] Se puede crear proveedor.
[ ] Se puede crear cliente.
[ ] Se puede crear bodega.
[ ] Se puede crear ubicación dentro de bodega.
[ ] Se puede registrar entrada de inventario.
[ ] La entrada aumenta el stock disponible.
[ ] La entrada genera Kardex.
[ ] La entrada genera auditoría.
[ ] No se puede registrar entrada con cantidad cero.
[ ] Se puede registrar salida de inventario.
[ ] La salida disminuye el stock disponible.
[ ] La salida genera Kardex.
[ ] La salida genera auditoría.
[ ] No se puede registrar salida mayor al stock disponible.
[ ] Se puede transferir stock entre bodegas.
[ ] La transferencia descuenta origen y suma destino al recibir.
[ ] No se puede transferir a la misma ubicación.
[ ] Se puede registrar ajuste positivo.
[ ] Se puede registrar ajuste negativo.
[ ] No se puede registrar ajuste sin motivo.
[ ] Se puede crear orden de compra.
[ ] Se puede recepcionar orden de compra parcial.
[ ] Se puede recepcionar orden de compra total.
[ ] La recepción genera entrada de inventario.
[ ] Se puede crear reserva de stock.
[ ] La reserva reduce stock disponible.
[ ] Se puede liberar reserva.
[ ] Se puede ejecutar conteo físico.
[ ] El conteo calcula diferencias.
[ ] El conteo cerrado no se puede editar.
[ ] Se muestra inventario actual por producto y bodega.
[ ] Se muestra Kardex por producto.
[ ] El dashboard muestra KPIs reales.
[ ] Se muestran alertas de bajo stock.
[ ] Se muestran productos sin stock.
[ ] Se puede filtrar inventario por producto.
[ ] Se puede filtrar inventario por bodega.
[ ] Se puede buscar por SKU.
[ ] Se puede buscar por código de barras.
[ ] Se puede buscar por lote.
[ ] Se puede buscar por serie.
[ ] Se puede generar reporte de inventario actual.
[ ] Se puede generar reporte de movimientos.
[ ] Se puede generar reporte de Kardex.
[ ] Se puede exportar reporte a CSV.
[ ] Se puede exportar reporte a XLSX.
[ ] Se puede exportar reporte a PDF.
[ ] La interfaz se adapta a escritorio.
[ ] La interfaz se adapta a tablet.
[ ] La interfaz se adapta a móvil.
[ ] Los datos persisten al reiniciar la aplicación.
[ ] Las acciones críticas quedan en auditoría.
```

---

# 11. Módulos del sistema

Módulos mínimos:

1. Autenticación y usuarios.
2. Roles y permisos.
3. Dashboard.
4. Productos.
5. Categorías, marcas y unidades.
6. Proveedores.
7. Clientes o áreas solicitantes.
8. Bodegas.
9. Ubicaciones.
10. Inventario actual.
11. Movimientos de inventario.
12. Kardex.
13. Compras.
14. Recepciones.
15. Reservas.
16. Transferencias.
17. Ajustes.
18. Conteo físico.
19. Reportes.
20. Alertas.
21. Importación/exportación.
22. Auditoría.
23. Configuración.

---

# 12. Modelo de datos mínimo

Tablas mínimas sugeridas:

```text
users
roles
permissions
role_permissions
categories
subcategories
brands
units
products
warehouses
locations
suppliers
customers
inventory_stock
inventory_movements
inventory_movement_details
product_lots
product_serials
purchase_orders
purchase_order_details
purchase_receipts
purchase_receipt_details
stock_reservations
stock_transfers
stock_transfer_details
stock_adjustments
stock_adjustment_details
physical_counts
physical_count_details
alerts
audit_logs
system_settings
import_jobs
export_jobs
```

Relaciones principales:

- Un producto pertenece a una categoría, marca y unidad.
- Una bodega tiene muchas ubicaciones.
- El stock se controla por producto, bodega, ubicación, lote y serie cuando aplique.
- Todo movimiento tiene cabecera y detalle.
- Todo movimiento confirmado afecta stock y Kardex.
- Una compra puede tener varias recepciones.
- Una reserva afecta disponibilidad pero no stock físico.
- La auditoría registra operaciones críticas por usuario.

---

# 13. Campos principales por tabla

## 13.1 Tabla `products`

```text
id
sku
barcode
name
description
category_id
subcategory_id
brand_id
unit_id
cost_price
sale_price
min_stock
max_stock
tracks_lot
tracks_serial
image_url
status
created_at
updated_at
```

## 13.2 Tabla `inventory_stock`

```text
id
product_id
warehouse_id
location_id
lot_id
serial_id
physical_qty
reserved_qty
committed_qty
in_transit_qty
available_qty
average_cost
last_movement_at
created_at
updated_at
```

## 13.3 Tabla `inventory_movements`

```text
id
movement_number
movement_type
source_document_type
source_document_id
warehouse_origin_id
warehouse_destination_id
status
movement_date
created_by
confirmed_by
confirmed_at
notes
created_at
updated_at
```

## 13.4 Tabla `inventory_movement_details`

```text
id
movement_id
product_id
location_origin_id
location_destination_id
lot_id
serial_id
quantity
unit_cost
total_cost
balance_after
created_at
```

## 13.5 Tabla `audit_logs`

```text
id
user_id
module
action
entity_name
entity_id
old_values_json
new_values_json
ip_address
created_at
```

---

# 14. Endpoints API mínimos

## 14.1 Autenticación

```text
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
POST   /api/auth/refresh
```

## 14.2 Usuarios y roles

```text
GET    /api/users
POST   /api/users
GET    /api/users/{id}
PUT    /api/users/{id}
PATCH  /api/users/{id}/status
GET    /api/roles
POST   /api/roles
PUT    /api/roles/{id}
```

## 14.3 Productos y maestros

```text
GET    /api/products
POST   /api/products
GET    /api/products/{id}
PUT    /api/products/{id}
PATCH  /api/products/{id}/status
GET    /api/categories
POST   /api/categories
GET    /api/brands
POST   /api/brands
GET    /api/units
POST   /api/units
```

## 14.4 Bodegas y ubicaciones

```text
GET    /api/warehouses
POST   /api/warehouses
GET    /api/warehouses/{id}
PUT    /api/warehouses/{id}
GET    /api/locations
POST   /api/locations
PUT    /api/locations/{id}
```

## 14.5 Inventario y movimientos

```text
GET    /api/inventory/stock
GET    /api/inventory/kardex/{product_id}
POST   /api/inventory/entries
POST   /api/inventory/exits
POST   /api/inventory/transfers
PATCH  /api/inventory/transfers/{id}/send
PATCH  /api/inventory/transfers/{id}/receive
POST   /api/inventory/adjustments
GET    /api/inventory/movements
GET    /api/inventory/movements/{id}
```

## 14.6 Compras y recepciones

```text
GET    /api/purchase-orders
POST   /api/purchase-orders
GET    /api/purchase-orders/{id}
PUT    /api/purchase-orders/{id}
PATCH  /api/purchase-orders/{id}/issue
POST   /api/purchase-orders/{id}/receipts
GET    /api/purchase-receipts
```

## 14.7 Reservas y conteos

```text
GET    /api/reservations
POST   /api/reservations
PATCH  /api/reservations/{id}/release
PATCH  /api/reservations/{id}/consume
GET    /api/physical-counts
POST   /api/physical-counts
PUT    /api/physical-counts/{id}
PATCH  /api/physical-counts/{id}/close
POST   /api/physical-counts/{id}/generate-adjustments
```

## 14.8 Dashboard, reportes y auditoría

```text
GET    /api/dashboard/summary
GET    /api/dashboard/movements-chart
GET    /api/dashboard/stock-by-category
GET    /api/alerts
PATCH  /api/alerts/{id}/review
GET    /api/reports/current-stock
GET    /api/reports/kardex
GET    /api/reports/movements
GET    /api/reports/valuation
GET    /api/reports/low-stock
GET    /api/audit-logs
```

---

# 15. Reglas de negocio críticas

- Todo producto debe tener SKU único.
- Todo movimiento confirmado debe afectar stock.
- Todo movimiento confirmado debe generar Kardex.
- Todo movimiento confirmado debe generar auditoría.
- No se permite salida mayor al stock disponible.
- No se permite transferencia mayor al stock disponible.
- No se permite desactivar ubicación con stock físico.
- No se permite eliminar físicamente entidades con movimientos asociados.
- El stock disponible se calcula como stock físico menos reservado y comprometido.
- El stock en tránsito no debe estar disponible para venta o salida.
- Los productos con serie deben registrar una serie por unidad.
- Los productos con lote deben registrar lote en entradas y salidas.
- Una orden de compra recibida completamente debe cambiar a estado recibida.
- Una transferencia recibida no debe modificarse.
- Un conteo físico cerrado no debe editarse.
- Los ajustes requieren motivo obligatorio.

---

# 16. Pantallas principales

Pantallas mínimas:

1. Login.
2. Dashboard.
3. Menú principal lateral o superior.
4. Productos.
5. Formulario de producto.
6. Categorías, marcas y unidades.
7. Proveedores.
8. Clientes.
9. Bodegas.
10. Ubicaciones.
11. Inventario actual.
12. Kardex de producto.
13. Entrada de inventario.
14. Salida de inventario.
15. Transferencias.
16. Ajustes.
17. Órdenes de compra.
18. Recepciones.
19. Reservas.
20. Conteo físico.
21. Reportes.
22. Alertas.
23. Auditoría.
24. Usuarios y roles.
25. Configuración general.

---

# 17. Diseño responsivo

El sistema debe adaptarse a los siguientes tamaños:

```text
Móvil:      320px a 767px
Tablet:     768px a 1023px
Escritorio: 1024px o superior
```

Reglas de interfaz:

- En móvil, el menú debe colapsar.
- Las tablas deben permitir scroll horizontal o transformarse en tarjetas.
- Los formularios deben usar una columna en móvil y dos o más en escritorio.
- Los botones críticos deben tener confirmación.
- Los filtros deben poder ocultarse o desplegarse.
- El dashboard debe reorganizar tarjetas y gráficos según pantalla.
- Las acciones frecuentes deben ser visibles y fáciles de usar.

---

# 18. Estructura sugerida del backend

```text
backend/
  app/
    main.py
    config.py
    database.py
    auth/
    users/
    roles/
    products/
    warehouses/
    inventory/
    purchases/
    reservations/
    reports/
    dashboard/
    audit/
    settings/
    shared/
  migrations/
  tests/
  requirements.txt
  README.md
```

Reglas:

- Cada módulo debe tener rutas, modelos, esquemas y servicios.
- La lógica de negocio no debe quedar directamente en los endpoints.
- Las validaciones deben aplicarse en esquemas y servicios.
- Las operaciones críticas deben usar transacciones de base de datos.

---

# 19. Estructura sugerida del frontend

```text
frontend/
  src/
    api/
    auth/
    components/
    layouts/
    pages/
      dashboard/
      products/
      inventory/
      purchases/
      reports/
      users/
      settings/
    routes/
    hooks/
    utils/
    styles/
  public/
  package.json
  README.md
```

Reglas:

- Usar componentes reutilizables.
- Separar páginas, servicios API y componentes visuales.
- Manejar estados de carga, error y éxito.
- Validar formularios antes de enviar al backend.
- Proteger rutas según autenticación y rol.

---

# 20. Validaciones mínimas

Validaciones de frontend y backend:

- Campos obligatorios no vacíos.
- Longitud mínima y máxima de textos.
- SKU único.
- Email válido.
- Cantidades mayores que cero.
- Costos no negativos.
- Fechas válidas.
- Bodega activa.
- Ubicación activa.
- Producto activo.
- Stock suficiente para salidas y transferencias.
- Lote obligatorio cuando producto controla lote.
- Serie obligatoria cuando producto controla serie.
- Motivo obligatorio para ajustes.
- Permisos suficientes para acciones críticas.

---

# 21. Reportes y métricas del dashboard

KPIs mínimos:

- Valor total del inventario.
- Cantidad total de SKUs activos.
- Productos bajo stock mínimo.
- Productos sin stock.
- Productos sobre stock máximo.
- Entradas del mes.
- Salidas del mes.
- Rotación promedio.
- Top 10 productos con mayor salida.
- Top 10 productos sin movimiento.
- Órdenes de compra pendientes.
- Transferencias pendientes.

Gráficos mínimos:

- Stock por categoría.
- Movimientos por mes.
- Entradas versus salidas.
- Valor de inventario por bodega.
- Productos críticos por categoría.

---

# 22. Seguridad y permisos

Permisos mínimos por módulo:

```text
products.read
products.create
products.update
products.disable
inventory.read
inventory.entry
inventory.exit
inventory.transfer
inventory.adjust
purchases.read
purchases.create
purchases.receive
reports.read
reports.export
users.manage
settings.manage
audit.read
```

Reglas:

- Todo endpoint protegido debe validar token JWT.
- Todo endpoint crítico debe validar permiso específico.
- Las contraseñas deben almacenarse con hash seguro.
- No se deben exponer errores técnicos al usuario final.
- Las acciones críticas deben quedar auditadas.

---

# 23. Casos de prueba funcionales mínimos

## CP-01 Crear producto válido

Datos:

- SKU: PROD-001.
- Nombre: Producto prueba.
- Costo: 1000.
- Stock mínimo: 5.

Resultado esperado:

- Producto creado correctamente.
- SKU queda único.
- Auditoría registrada.

## CP-02 Crear producto con SKU duplicado

Resultado esperado:

- Sistema rechaza la operación.
- Muestra mensaje claro.
- No crea registro duplicado.

## CP-03 Entrada de inventario válida

Datos:

- Producto: PROD-001.
- Cantidad: 10.
- Bodega: Principal.

Resultado esperado:

- Stock aumenta en 10.
- Kardex registra entrada.
- Auditoría registra acción.

## CP-04 Salida con stock suficiente

Datos:

- Stock disponible: 10.
- Salida: 3.

Resultado esperado:

- Stock final disponible: 7.
- Kardex registra salida.

## CP-05 Salida sin stock suficiente

Datos:

- Stock disponible: 2.
- Salida: 5.

Resultado esperado:

- Sistema rechaza la operación.
- Stock no cambia.
- Muestra mensaje claro.

## CP-06 Transferencia válida

Resultado esperado:

- Stock se descuenta del origen al enviar.
- Stock queda en tránsito.
- Stock se suma al destino al recibir.

## CP-07 Ajuste sin motivo

Resultado esperado:

- Sistema rechaza la operación.
- Stock no cambia.

## CP-08 Conteo físico con diferencia

Resultado esperado:

- Sistema calcula diferencia.
- Sistema permite generar ajuste controlado.

## CP-09 Reporte con filtros

Resultado esperado:

- Reporte muestra solo datos filtrados.
- Exportación respeta los mismos filtros.

## CP-10 Acceso sin permiso

Resultado esperado:

- Sistema bloquea acción.
- Muestra mensaje de autorización insuficiente.

---

# 24. Entregables técnicos mínimos

El proyecto debe entregar:

- Código backend FASTAPI.
- Código frontend React + Bootstrap.
- Scripts de base de datos o migraciones Alembic.
- Archivo `.env.example`.
- README de instalación.
- README de ejecución local.
- Documentación de endpoints principales.
- Modelo de datos resumido.
- Checklist de pruebas.
- Datos iniciales de ejemplo.
- Usuario administrador inicial.
- Guía breve de uso del sistema.

---

# 25. Definición final del producto mínimo viable

El producto mínimo viable debe ser una aplicación web llamada **StockMaster ERP Lite**, desarrollada con **FASTAPI, React, Bootstrap y MySQL/MariaDB**, que permita gestionar inventario avanzado con lógica tipo ERP.

Debe incluir autenticación, usuarios, roles, productos, bodegas, ubicaciones, proveedores, clientes, inventario actual, entradas, salidas, transferencias, ajustes, órdenes de compra, recepciones, reservas, conteo físico, Kardex, dashboard, alertas, reportes exportables, auditoría y diseño responsivo.

El sistema debe estar organizado, documentado, validado y listo para ser implementado por una fábrica de agentes de IA como software web transaccional pequeño, robusto y ampliable.
