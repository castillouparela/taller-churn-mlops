# ASUM-DM · Predicción de churn en telecomunicaciones

> Documento de referencia del facilitador (versión completa). Los asistentes parten de
> `plantillas/ASUM-DM_plantilla.md` y lo comparan con este al final del Bloque 1.

| Campo | Valor |
|---|---|
| Proyecto | Retención proactiva de clientes móviles |
| Versión | 1.0 · 2026-10 |
| Patrocinador | Gerencia de Retención y Fidelización |
| Dueño del modelo | Líder de Analítica |
| Revisado por pares | ☐ Par 1: ________ ☐ Par 2: ________ |

---

## 1. Entendimiento del negocio

### 1.1 Objetivo de negocio
Reducir la cancelación voluntaria (churn) de clientes móviles identificando **cada mes** a los clientes con mayor
probabilidad de abandonar, para que el equipo de retención actúe **antes** de que cancelen, dentro de un presupuesto fijo.

### 1.2 KPIs de negocio
| KPI | Definición | Línea base | Meta a 6 meses |
|---|---|---|---|
| Tasa de cancelación mensual | clientes que cancelan / clientes activos al inicio del mes | 25,5 % (dataset del taller) | −3 pp |
| Ingresos retenidos | Σ cargo mensual de clientes contactados que no cancelan | n/d | ≥ 2× costo de campaña |
| Costo de campaña de retención | n.º clientes contactados × costo por contacto (USD 8) | USD 2.000/mes (tope) | ≤ presupuesto |
| ROI de campaña | (ingreso retenido − costo) / costo | n/d | > 0,5 |

### 1.3 Situación actual y supuestos
- Hoy la campaña contacta clientes al azar o por intuición; la tasa de éxito estimada de un contacto es **30 %**.
- El presupuesto alcanza para **250 contactos/mes** (2.000 / 8).
- El área de retención define las acciones; el modelo **sólo prioriza**.

## 2. Traducción a problema de ML

| Elemento | Definición |
|---|---|
| Tipo de problema | Clasificación binaria con salida probabilística |
| Variable objetivo | `churn` = 1 si el cliente cancela en los 30 días siguientes al corte; 0 si no |
| Unidad de análisis | **Cliente-mes** (una fila por cliente activo en el corte mensual) |
| Horizonte de predicción | 30 días |
| Frecuencia de scoring | Mensual en lote + consulta en tiempo real para el asesor |
| Salida esperada | Probabilidad de churn, nivel de riesgo (alto/medio/bajo) y acción recomendada |

## 3. Entendimiento de los datos (simulados)

| Variable | Tipo | Descripción | Hipótesis de negocio |
|---|---|---|---|
| `antiguedad_meses` | numérica | Meses como cliente | Más antigüedad ⇒ menos churn |
| `tipo_plan` | categórica | prepago / pospago_basico / pospago_premium | Prepago ⇒ más churn |
| `cargo_mensual` | numérica | Facturación mensual (USD) | Cargo alto ⇒ más churn |
| `reclamos_ult_3m` | numérica | Reclamos en los últimos 3 meses | Más reclamos ⇒ más churn |
| `uso_datos_gb` | numérica | Consumo de datos mensual | Uso alto ⇒ más vínculo |
| `metodo_pago` | categórica | tarjeta, débito automático, efectivo, transferencia | Efectivo ⇒ más churn |
| `renovo_contrato` | categórica | si / no | Renovar ⇒ menos churn |
| `rango_edad` | categórica **sensible** | 18-25, 26-40, 41-60, 60+ | **No se usa para predecir**; sólo para auditar sesgo |

Calidad mínima exigida: sin nulos en features, rangos válidos, dominios cerrados, IDs únicos.
Fuente del taller: `data/raw/churn_telco.csv` (5.000 filas, semilla 42, generado con `python -m churn.dataset`).

## 4. Preparación de datos
- Validación de calidad automática (`churn.features.validar_calidad`) antes de entrenar; si falla, el pipeline se detiene.
- Partición estratificada 75/25 con semilla fija.
- Escalado de numéricas y one-hot de categóricas **dentro del pipeline** (evita fuga de datos).
- Se guarda un perfil de referencia (deciles y frecuencias) para medir drift.

## 5. Modelado
- Baseline: Regresión Logística con `class_weight="balanced"`. Alternativa: Random Forest.
- El umbral de decisión se calibra por validación cruzada en entrenamiento: **máxima precisión con recall ≥ 0,70**.

## 6. Evaluación · Criterios de éxito

| Criterio | Umbral mínimo | Resultado baseline (test) | ¿Cumple? |
|---|---|---|---|
| Recall clase churn (detectar a quien se va) | ≥ 0,70 | 0,73 | ✅ |
| Precision clase churn | ≥ 0,40 | 0,49 | ✅ |
| ROC-AUC | ≥ 0,75 | 0,81 | ✅ |
| ROI esperado de la campaña priorizada | > 0,5 | 1,13 | ✅ |
| Ratio de impacto dispar por rango de edad | ≥ 0,80 | 0,90 | ✅ |

**Por qué priorizamos recall:** dejar ir a un cliente (falso negativo) cuesta ~12 meses de facturación;
contactar a uno que no se iba (falso positivo) cuesta USD 8. Aun así exigimos precisión mínima para no agotar el presupuesto.

**Umbral de decisión:** calibrado ≈ 0,54 (se guarda en `models/model_card.json`). Nivel **alto** ≥ 0,70; **medio** entre umbral y 0,70; **bajo** por debajo del umbral.

## 7. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **Sesgo**: variables proxy (prepago, efectivo) correlacionadas con edad o ingreso | Trato desigual a grupos | Excluir `rango_edad`; reportar tasa de selección y recall por grupo; revisar si ratio < 0,8 |
| **Mala calidad de datos** | Predicciones erróneas | Validación automática que detiene el pipeline; pruebas de esquema |
| **Drift** (precios, competidor, crisis) | Pérdida de desempeño silenciosa | PSI por variable en `/metrics`; alerta ≥ 0,10, crítico ≥ 0,25 ⇒ reentrenar |
| **Uso indebido** (negar servicio, subir precio a "riesgosos") | Daño al cliente, reputacional y legal | Uso exclusivo para ofrecer beneficios; aviso en cada respuesta; revisión humana |
| **Privacidad** | Exposición de datos personales | No aceptar datos identificativos; IDs con hash en logs; minimización de datos |

## 8. Plan de despliegue

| Aspecto | Decisión |
|---|---|
| Modalidad | API FastAPI: `/predict` (tiempo real para asesor) y `/predict/lote` (scoring mensual) |
| Infraestructura | Local / servidor interno; sin servicios pagos ni Kubernetes |
| Monitoreo | `/health`, `/metrics`, `/dashboard`; logs JSONL de cada predicción |
| Frecuencia de reentrenamiento | Mensual programado **o** inmediato si PSI crítico o recall < 0,70 en datos etiquetados |
| Responsables | Analítica (modelo y monitoreo) · Retención (acciones y feedback) · TI (operación de la API) · Riesgo/Cumplimiento (aprobación) |
| Criterio de salida a producción | `aprobado_para_despliegue = true` en el model card + aprobación documentada en `docs/GOBERNANZA.md` |

## 9. Uso responsable (advertencia ética)
Este modelo **apoya** decisiones de retención; **no** debe usarse para negar servicios, cambiar precios ni
tomar decisiones automatizadas con efectos significativos sobre la persona sin revisión humana.
Los clientes tienen derecho a saber cómo se usan sus datos (en Colombia, Ley 1581 de 2012 de protección de datos personales).
Ver `docs/ETICA.md`.
