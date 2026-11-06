# Checklist de validación · 001-api-churn

## Calidad de la especificación (antes de /speckit.plan)
- [x] No contiene detalles de implementación (lenguajes, frameworks, librerías)
- [x] Se centra en valor para el usuario y el negocio
- [x] Escrita para personas no técnicas
- [x] Sin marcadores `[NEEDS CLARIFICATION]` pendientes
- [x] Requisitos verificables y sin ambigüedad
- [x] Criterios de éxito medibles y agnósticos de tecnología
- [x] Casos límite identificados
- [x] Alcance delimitado (incluye "Fuera de alcance")
- [x] Supuestos explícitos

## Trazabilidad requisito → código → prueba (antes de cerrar)
| Req. | Implementación | Prueba | Estado |
|---|---|---|---|
| FR-001 | `api.predict`, `predict.puntuar` | `test_predict_ok` | ✅ |
| FR-002 | `api.Cliente` (Field ge/le, Literal) | `test_rechaza_valores_fuera_de_rango`, `test_rechaza_campo_faltante` | ✅ |
| FR-003 | `ConfigDict(extra="forbid")` | `test_rechaza_categoria_invalida_y_campos_extra` | ✅ |
| FR-004 | `api.predict_lote` | `test_lote` | ✅ |
| FR-005 | `Prediccion.version_modelo`, `aviso` | `test_predict_ok` | ✅ |
| FR-006 | `api.health` | `test_health` | ✅ |
| FR-007 | `monitoring.Monitor.resumen` | `test_metrics_reporta_operacion_y_negocio` | ✅ |
| FR-008 | `monitoring.seudonimizar` | `test_log_no_guarda_id_en_claro` | ✅ |
| FR-009 | `config.SENSITIVE_COL`, `evaluate.metricas_equidad` | `test_model_card_trazabilidad` | ✅ |
| FR-010 | `predict.ACCIONES` | revisión manual | ✅ |
| SC-001..003 | `train.entrenar` | `test_model_card_cumple_criterios` | ✅ |
| SC-006 | `evaluate.metricas_negocio` | `test_metricas_negocio_respetan_presupuesto` | ✅ |
| SC-008 | `drift.calcular_drift` | `test_drift_critico_en_crisis` | ✅ |
