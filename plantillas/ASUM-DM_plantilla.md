# ASUM-DM · <Nombre del proyecto>

| Campo | Valor |
|---|---|
| Proyecto | |
| Versión / fecha | |
| Patrocinador de negocio | |
| Dueño del modelo | |
| Revisado por pares | ☐ Par 1: ______ ☐ Par 2: ______ |

## 1. Entendimiento del negocio
### 1.1 Objetivo de negocio
<!-- Una frase: verbo + resultado + plazo. Ej.: "Reducir la cancelación mensual en 3 pp en 6 meses". -->

### 1.2 KPIs de negocio
| KPI | Definición (fórmula) | Línea base | Meta |
|---|---|---|---|
| Tasa de cancelación | | | |
| Ingresos retenidos | | | |
| Costo de campaña de retención | | | |

### 1.3 Supuestos (presupuesto, costo por contacto, tasa de éxito de la campaña)

## 2. Traducción a problema de ML
| Elemento | Definición |
|---|---|
| Tipo de problema | |
| Variable objetivo (definición exacta y horizonte) | |
| Unidad de análisis | |
| Frecuencia de scoring | |
| Salida esperada | |

## 3. Entendimiento de los datos
| Variable | Tipo | Descripción | Hipótesis de negocio |
|---|---|---|---|
| antiguedad_meses | | | |
| tipo_plan | | | |
| cargo_mensual | | | |
| reclamos_ult_3m | | | |
| uso_datos_gb | | | |
| metodo_pago | | | |
| renovo_contrato | | | |
| (sensible) | | | ¿Se usa para predecir? ¿Para auditar? |

Reglas de calidad mínimas:

## 4. Preparación de datos (pasos y controles)

## 5. Modelado (baseline y alternativa)

## 6. Evaluación · Criterios de éxito
| Criterio | Umbral mínimo | Justificación de negocio |
|---|---|---|
| Recall clase churn | | ¿Cuánto cuesta un falso negativo? |
| Precision clase churn | | ¿Cuánto cuesta un falso positivo? |
| ROC-AUC | | |
| Métrica de negocio (ROI / ingresos retenidos) | | |
| Umbral de decisión | | ¿Cómo se elige? |

## 7. Riesgos y mitigaciones
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Sesgo | | |
| Calidad de datos | | |
| Drift | | |
| Uso indebido | | |
| Privacidad | | |

## 8. Plan de despliegue
| Aspecto | Decisión |
|---|---|
| Modalidad (batch / tiempo real) | |
| Responsables (RACI) | |
| Monitoreo | |
| Frecuencia y disparadores de reentrenamiento | |
| Criterio de salida a producción | |

## 9. Uso responsable
<!-- ¿Qué NO se puede hacer con este modelo? ¿Quién revisa las decisiones? -->
