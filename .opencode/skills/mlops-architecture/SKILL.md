---
name: mlops-architecture
description: Diseña la arquitectura MLOps mínima viable local: versionado del modelo, endpoints health/metrics, logging estructurado, métricas de negocio, drift (PSI) y gobernanza sin Kubernetes ni servicios pagos.
license: MIT
compatibility: opencode
metadata:
  origen: taller-churn-mlops
  inspirado_en: everything-claude-code (ECC)
---
# Skill: arquitectura MLOps mínima viable (estilo ECC · architect)

## Principios
- Local primero, cero cuentas: archivos JSON/JSONL como almacén de métricas y logs.
- Cada predicción es auditable: timestamp, versión de modelo, features, probabilidad, nivel y latencia.
- Monitoreo en tres capas: **operación** (volumen, errores, latencia), **modelo** (distribución de scores,
  PSI por feature) y **negocio** (clientes e ingresos en riesgo, priorizados, ROI esperado).

## Componentes
| Componente | Implementación del taller |
|---|---|
| Registro de modelo | `models/churn_model.joblib` + `models/model_card.json` (versión semántica) |
| Servicio | FastAPI: `/predict`, `/predict/lote`, `/health`, `/metrics`, `/dashboard` |
| Logs | `logs/predicciones.jsonl` (una línea JSON por evento) |
| Drift | PSI con deciles de entrenamiento; alerta ≥ 0.10, crítico ≥ 0.25 |
| Gobernanza | `docs/GOBERNANZA.md`: aprobadores, evidencias y política de versiones |

## Reglas de decisión
- PSI crítico o caída de recall bajo el mínimo ⇒ reentrenar y revalidar antes de seguir.
- Un modelo nuevo sólo se despliega si `aprobado_para_despliegue = true` en su *model card*.
