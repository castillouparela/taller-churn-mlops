# Plan de implementación: API de riesgo de churn

**Rama**: `001-api-churn` · **Spec**: [spec.md](spec.md) · **Fecha**: 2026-10

## Resumen
Servicio local que entrena un clasificador binario sobre datos sintéticos deterministas y lo expone vía API con
validación estricta, registro auditable y métricas de operación, negocio y drift.

## Contexto técnico
| Aspecto | Decisión | Justificación |
|---|---|---|
| Lenguaje | Python 3.11+ | Estándar de ciencia de datos |
| Datos | pandas + numpy, CSV en `data/raw/` | Simple y reproducible |
| Modelo | scikit-learn: `Pipeline(ColumnTransformer → LogisticRegression)`; alternativa `RandomForestClassifier` | Baseline explicable (Principio V) |
| Serialización | joblib: `{pipeline, card}` + `models/model_card.json` | Versión y trazabilidad juntas |
| API | FastAPI + Pydantic v2 + Uvicorn | Validación declarativa y docs `/docs` automáticas |
| Pruebas | pytest + TestClient (httpx) | Rápidas, sin red |
| Métricas | JSON en `reports/metrics/`, JSONL en `logs/` | Sin servidores ni cuentas |
| Drift | PSI con deciles de entrenamiento | Fácil de explicar |
| Contenedor | Docker **opcional** (no requerido en el taller) | Restricción de recursos |
| Objetivo de desempeño | p95 < 300 ms por consulta | SC-004 |

## Verificación contra la constitución
| Principio | ¿Cumple el plan? | Evidencia |
|---|---|---|
| I. Negocio manda | ✅ | Métricas de negocio en `/metrics` y en el model card |
| II. Calidad verificable | ✅ | Prueba por cada FR (ver tasks.md) |
| III. Reproducibilidad | ✅ | `config.SEED`, dataset determinista, dependencias en `pyproject.toml` |
| IV. Seguridad/privacidad | ✅ | `extra="forbid"`, rangos, hash de IDs |
| V. Explicabilidad/equidad | ✅ | Regresión logística, exclusión de `rango_edad`, ratio de impacto |
| VI. Gobernanza | ✅ | Versionado semántico, `aprobado_para_despliegue`, `docs/GOBERNANZA.md` |
| VII. Supervisión humana | ✅ | Aviso en cada respuesta |

## Estructura del proyecto (Cookiecutter Data Science simplificado)
```
business/ASUM-DM.md          # entendimiento de negocio
data/raw | processed | drift # datos (deterministas)
models/                      # artefactos + model card
reports/metrics/             # evaluación y drift
logs/                        # predicciones JSONL
src/churn/
  config.py                  # rutas, semillas, umbrales
  dataset.py                 # generador sintético (base y crisis)
  features.py                # calidad, partición, preprocesamiento, perfil de referencia
  evaluate.py                # métricas técnicas, de negocio y de equidad
  train.py                   # entrenamiento, umbral, serialización
  predict.py                 # carga y puntuación
  monitoring.py              # logging estructurado y agregación de métricas
  drift.py                   # PSI y simulación de escenario
  api.py                     # FastAPI
tests/                       # pytest
dashboard/index.html         # panel de métricas sin dependencias
```

## Contrato de la API
| Método | Ruta | Entrada | Salida | Errores |
|---|---|---|---|---|
| POST | `/predict` | `Cliente` | `Prediccion` | 422 validación, 503 sin modelo |
| POST | `/predict/lote` | `{clientes: [Cliente] (1..1000)}` | `[Prediccion]` | 422, 503 |
| GET | `/health` | – | estado, versión | – |
| GET | `/metrics` | – | operación, negocio, drift | – |
| GET | `/dashboard` | – | HTML | 404 |

`Cliente`: `antiguedad_meses` int [0,600] · `tipo_plan` {prepago, pospago_basico, pospago_premium} · `cargo_mensual` float [0,1000] ·
`reclamos_ult_3m` int [0,100] · `uso_datos_gb` float [0,2000] · `metodo_pago` {tarjeta_credito, debito_automatico, efectivo, transferencia} ·
`renovo_contrato` {si, no} · `id_cliente` opcional (alfanumérico ≤ 40). Campos extra ⇒ 422.

## Riesgos técnicos
- Modelos locales pequeños pueden generar código incompleto ⇒ pasos cortos + revisión contra spec + `/speckit.converge`.
- Laptops con poca RAM ⇒ modelo 3B (`Modelfile.mini`) y Plan B en `docs/PLAN_B.md`.
