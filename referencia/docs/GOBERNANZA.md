# Gobernanza del modelo de churn

## 1. Roles (RACI)
| Actividad | Analítica (dueño del modelo) | Retención (negocio) | TI / Operación | Riesgo y Cumplimiento |
|---|---|---|---|---|
| Definir objetivo, KPIs y criterios (ASUM-DM) | R | A | C | C |
| Constitución y especificación (SDD) | R | A | C | C |
| Entrenar y evaluar | A/R | I | I | C |
| Auditoría de sesgo y privacidad | R | C | I | **A** |
| Aprobar paso a producción | R | C | C | **A** |
| Operar la API y los logs | C | I | A/R | I |
| Monitorear drift y métricas | A/R | I | C | I |
| Decidir reentrenamiento o retiro | R | C | C | **A** |

R = responsable · A = aprueba · C = consultado · I = informado

## 2. Evidencias que se guardan por versión
| Evidencia | Ubicación | Quién la genera |
|---|---|---|
| Documento de negocio | `business/ASUM-DM.md` | Analítica + Retención |
| Constitución, spec, plan, tareas, checklist | `.specify/memory/`, `specs/001-api-churn/` | Equipo (Spec Kit) |
| Model card (versión, hash de datos, métricas, equidad, aprobación) | `models/model_card.json` | `python -m churn.train` |
| Métricas de evaluación | `reports/metrics/evaluacion.json` | `python -m churn.train` |
| Reporte de drift | `reports/metrics/drift.json` | `python -m churn.drift` |
| Resultados de pruebas | salida de `pytest` (adjuntar al acta) | CI local |
| Log de predicciones (sin IDs en claro) | `logs/predicciones.jsonl` | API |
| Acta de aprobación | `docs/aprobaciones/vX.Y.Z.md` | Riesgo y Cumplimiento |

## 3. Versionado del modelo (semántico)
- **MAJOR** (2.0.0): cambia la definición del objetivo, las features o el uso del modelo → nueva spec y nueva aprobación completa.
- **MINOR** (1.1.0): reentrenamiento con datos nuevos o cambio de algoritmo con mismas features → revalidar criterios y equidad.
- **PATCH** (1.0.1): cambios que no afectan predicciones (logs, documentación).
- La versión vive en `src/churn/config.py` (`MODEL_VERSION`), se copia al model card y viaja en **cada respuesta** de la API.
- Los artefactos se versionan con Git (o Git LFS si crecen); el hash del dataset en el model card liga modelo ↔ datos.

## 4. Criterios de paso a producción
1. `aprobado_para_despliegue = true` en el model card (recall ≥ 0,70, precision ≥ 0,40, ROC-AUC ≥ 0,75).
2. Ratio de impacto dispar por rango de edad ≥ 0,80 (si no, análisis documentado).
3. `pytest` 100 % en verde.
4. `/speckit.converge` en estado **Converged**.
5. Acta firmada por Riesgo y Cumplimiento.

## 5. Disparadores de reentrenamiento
| Señal | Umbral | Acción |
|---|---|---|
| PSI de cualquier variable | ≥ 0,10 | Alerta: revisar en la reunión semanal |
| PSI de cualquier variable | ≥ 0,25 | Reentrenar y revalidar antes de 5 días hábiles |
| Recall en datos etiquetados del mes | < 0,70 | Reentrenar; si persiste, revisar features |
| Tasa real de churn | cambia > 5 pp | Revisar umbral y presupuesto con Retención |
| Calendario | mensual | Reentrenamiento programado |

## 6. Retiro y vuelta atrás (rollback)
- Se conservan las dos últimas versiones aprobadas en `models/` (o en el historial de Git).
- Si la nueva versión empeora el KPI de negocio dos semanas seguidas, se vuelve a la anterior y se documenta.
- Si se detecta uso indebido, la API se apaga y se notifica a Cumplimiento.
