# Especificación del feature: API de riesgo de churn

**Rama**: `001-api-churn` · **Estado**: Aprobada para plan · **Creada**: 2026-10
**Entrada**: "Como analista de retención, quiero una API que reciba datos del cliente y devuelva probabilidad de churn,
nivel de riesgo y recomendación de acción."

> Esta especificación describe **qué** y **por qué**. No menciona lenguajes, librerías ni frameworks:
> eso pertenece a `plan.md`.

## Escenarios de usuario y pruebas

### Historia 1 · Consultar el riesgo de un cliente (Prioridad: P1)
Como analista de retención, durante una llamada o revisión de cuenta, quiero consultar el riesgo de un cliente para
decidir si le ofrezco un beneficio.

**Por qué P1**: es el valor mínimo del producto; sin esto no hay retención proactiva.
**Prueba independiente**: enviar los datos de un cliente y recibir probabilidad, nivel y recomendación.

**Escenarios de aceptación**
1. **Dado** un cliente con datos completos y válidos, **cuando** consulto su riesgo, **entonces** recibo una probabilidad entre 0 y 1, un nivel (alto/medio/bajo) y una recomendación.
2. **Dado** un cliente con un dato fuera de rango (p. ej., cargo negativo), **cuando** consulto, **entonces** recibo un error que indica qué campo es inválido y por qué.
3. **Dado** un cliente nuevo con muchos reclamos, pago en efectivo y sin renovación, **cuando** consulto, **entonces** su probabilidad es mayor que la de un cliente antiguo, sin reclamos y con renovación.

### Historia 2 · Priorizar la campaña mensual (Prioridad: P2)
Como líder de retención, quiero puntuar la base completa del mes y saber cuántos clientes e ingresos están en riesgo y
a quiénes contactar con el presupuesto disponible.

**Escenarios de aceptación**
1. **Dado** un lote de clientes, **cuando** lo envío, **entonces** recibo una respuesta por cliente en el mismo orden.
2. **Dado** el presupuesto mensual, **cuando** consulto las métricas, **entonces** veo clientes en riesgo, ingresos en riesgo y clientes priorizados sin exceder el presupuesto.

### Historia 3 · Confiar en el modelo en el tiempo (Prioridad: P3)
Como dueño del modelo, quiero saber si el servicio está sano y si los datos que llegan se parecen a los de entrenamiento.

**Escenarios de aceptación**
1. **Dado** el servicio en ejecución, **cuando** consulto su estado, **entonces** sé si el modelo está cargado y qué versión es.
2. **Dado** que cambian las condiciones del mercado, **cuando** reviso las métricas, **entonces** veo una alerta de drift por variable.

### Casos límite
- ¿Qué pasa si falta un campo obligatorio? → error claro por campo.
- ¿Qué pasa si llega un campo no previsto (p. ej., número de documento)? → se rechaza.
- ¿Qué pasa si el modelo no está disponible? → el servicio lo informa sin caerse.
- ¿Qué pasa con un lote vacío o demasiado grande? → se rechaza con mensaje.

## Requisitos

### Funcionales
- **FR-001**: El sistema DEBE recibir los datos de un cliente-mes (antigüedad, tipo de plan, cargo mensual, reclamos de los últimos 3 meses, uso de datos, método de pago, renovación de contrato) y devolver probabilidad de churn, nivel de riesgo y recomendación de acción.
- **FR-002**: El sistema DEBE validar tipos, rangos y valores permitidos de cada dato y rechazar entradas inválidas indicando el campo y el motivo.
- **FR-003**: El sistema DEBE rechazar datos no previstos en el contrato, en particular datos personales identificativos.
- **FR-004**: El sistema DEBE permitir puntuar lotes de hasta 1.000 clientes.
- **FR-005**: Cada respuesta DEBE incluir la versión del modelo que la generó y un aviso de que requiere revisión humana.
- **FR-006**: El sistema DEBE exponer su estado de salud (servicio activo, modelo cargado, versión).
- **FR-007**: El sistema DEBE exponer métricas operativas (volumen, errores, latencia), de negocio (clientes en riesgo, ingresos en riesgo, clientes priorizados según presupuesto) y de drift por variable.
- **FR-008**: El sistema DEBE registrar cada predicción de forma auditable sin almacenar identificadores en claro.
- **FR-009**: El sistema NO DEBE usar el rango de edad para predecir; DEBE reportar el impacto por rango de edad.
- **FR-010**: Las recomendaciones DEBEN ser acciones de retención definidas por el negocio, nunca negación de servicio ni cambios de precio.

### Entidades clave
- **Cliente-mes**: foto mensual del cliente con las 7 variables de entrada.
- **Predicción**: probabilidad, nivel de riesgo, recomendación, versión de modelo, aviso.
- **Versión de modelo**: identificador, fecha, datos usados, métricas y estado de aprobación.

## Criterios de éxito (medibles y agnósticos de tecnología)
- **SC-001**: El modelo detecta al menos el **70 %** de los clientes que realmente cancelan (recall) en datos de prueba.
- **SC-002**: Al menos el **40 %** de los clientes marcados en riesgo realmente cancelan (precision).
- **SC-003**: Capacidad de discriminación ROC-AUC ≥ **0,75**.
- **SC-004**: Una consulta individual responde en menos de **300 ms** (p95) en una laptop.
- **SC-005**: El **100 %** de entradas inválidas se rechaza con mensaje por campo.
- **SC-006**: La campaña priorizada nunca supera el presupuesto mensual y su ROI esperado es > **0,5**.
- **SC-007**: Ratio de impacto dispar por rango de edad ≥ **0,80**.
- **SC-008**: Un cambio fuerte en la distribución de datos se reporta como drift crítico.

## Supuestos
- Presupuesto mensual USD 2.000; costo por contacto USD 8; éxito de contacto 30 %.
- Los datos del taller son sintéticos; no hay datos reales de clientes.

## Fuera de alcance
- Interfaz gráfica para asesores, integración con CRM, autenticación corporativa, reentrenamiento automático.
