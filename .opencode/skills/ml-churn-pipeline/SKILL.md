---
name: ml-churn-pipeline
description: Construye pipelines de ML tabular reproducibles (datos sintéticos, preparación, baseline, evaluación, serialización) para clasificación binaria de churn. Úsala al crear o modificar dataset, features, entrenamiento o evaluación.
license: MIT
compatibility: opencode
metadata:
  origen: taller-churn-mlops
  inspirado_en: everything-claude-code (ECC)
---
# Skill: pipeline de ML para churn (estilo ECC · machine learning)

## Cuándo usarla
Al generar datos, preparar features, entrenar, evaluar o serializar el modelo.

## Reglas
1. **Reproducibilidad**: toda aleatoriedad usa `config.SEED`. Mismo input → mismo output.
2. **Sin fuga de datos**: el preprocesamiento vive dentro de un `sklearn.pipeline.Pipeline`;
   el umbral se calibra con validación cruzada en *train*, nunca con *test*.
3. **Baseline primero**: Regresión Logística con `class_weight="balanced"` antes de modelos complejos.
4. **Métricas obligatorias**: ROC-AUC, precision, recall, F1, matriz de confusión **y** métricas de negocio
   (clientes en riesgo, ingresos en riesgo, clientes priorizados según presupuesto).
5. **Umbral de negocio**: elegir el umbral con mayor precisión que cumpla `MIN_RECALL` de ASUM-DM.
6. **Equidad**: excluir `rango_edad` de las features y reportar tasa de selección y recall por grupo.
7. **Trazabilidad**: serializar `{pipeline, card}` con joblib; el *model card* incluye versión, fecha,
   hash del dataset, métricas, criterios cumplidos y perfil de referencia para drift.
8. **Validación de calidad** antes de entrenar: esquema, nulos, rangos y dominios; fallar con mensaje claro.

## Lista de verificación
- [ ] ¿El código usa sólo columnas de `config.FEATURES`?
- [ ] ¿Hay prueba de determinismo del dataset?
- [ ] ¿Las métricas se comparan contra los criterios de éxito de ASUM-DM?
- [ ] ¿Se guardan `models/model_card.json` y `reports/metrics/evaluacion.json`?
