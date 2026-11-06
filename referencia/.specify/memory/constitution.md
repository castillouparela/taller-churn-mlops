# Constitución del proyecto · Churn Telco

**Versión**: 1.0.0 · **Ratificada**: 2026-10 · **Última enmienda**: 2026-10

> Referencia del facilitador. En el taller se genera con `/speckit.constitution` y se compara con esta.

## Principios

### I. El negocio manda (no negociable)
Todo requisito se rastrea a un objetivo o KPI de `business/ASUM-DM.md`. No se construye nada que no tenga
un requisito asociado. Las métricas técnicas se reportan junto con métricas de negocio.

### II. Calidad verificable
Cada requisito funcional tiene al menos una prueba automática. `pytest` debe pasar antes de cualquier entrega.
Los criterios de éxito (recall ≥ 0,70, precision ≥ 0,40, ROC-AUC ≥ 0,75) se verifican por código, no por opinión.

### III. Reproducibilidad
Mismos datos + mismo código + misma semilla = mismo resultado. Dependencias declaradas; sin servicios que requieran
cuentas. Cualquier persona debe poder reconstruir el modelo en su laptop siguiendo el README.

### IV. Seguridad y privacidad por diseño
Validación estricta de toda entrada; rechazo de campos no previstos. No se aceptan ni registran datos identificativos
en claro. Errores controlados sin exponer detalles internos.

### V. Explicabilidad y equidad
Se prefiere el modelo más simple que cumpla los criterios. Cada predicción devuelve nivel de riesgo y acción comprensible.
Los atributos sensibles no se usan como predictores y se audita el impacto por grupo (ratio ≥ 0,80).

### VI. Gobernanza y trazabilidad
Cada modelo tiene versión semántica y *model card* (datos, métricas, fecha, criterios). Cada predicción queda registrada
con versión del modelo. Ningún modelo pasa a producción sin aprobación documentada.

### VII. Supervisión humana
El sistema apoya decisiones; no las toma. No se usa para negar servicios ni modificar precios.

## Restricciones técnicas
Ejecución local; Python 3.11+; sin Kubernetes, servicios cloud pagos ni plataformas que requieran cuentas.

## Gobernanza de esta constitución
Las enmiendas requieren justificación escrita, aprobación del dueño del modelo y aumento de versión
(MAJOR: se elimina/redefine un principio; MINOR: se agrega; PATCH: redacción).
