# Tareas: API de riesgo de churn

**Entrada**: `spec.md`, `plan.md` · Formato: `- [ ] T0xx [P?] [Historia] descripción (archivo)` · `[P]` = paralelizable

## Fase 1 · Preparación
- [x] T001 Crear estructura de carpetas y `pyproject.toml` (raíz)
- [x] T002 [P] Configuración central: rutas, semilla, columnas, umbrales (`src/churn/config.py`)
- [x] T003 [P] Reglas del agente para OpenCode (`AGENTS.md`)

## Fase 2 · Fundamentos (bloquean todas las historias)
- [x] T004 Generador sintético determinista con escenarios base y crisis (`src/churn/dataset.py`) → SC-008
- [x] T005 Prueba de determinismo y esquema (`tests/test_dataset.py`)
- [x] T006 Validación de calidad, partición estratificada y preprocesador (`src/churn/features.py`)
- [x] T007 Métricas técnicas, de negocio y de equidad (`src/churn/evaluate.py`) → SC-001..003, SC-006, SC-007
- [x] T008 Entrenamiento baseline, calibración de umbral y model card (`src/churn/train.py`) → FR-009
- [x] T009 Prueba de criterios de éxito y trazabilidad del model card (`tests/test_modelo.py`)

## Fase 3 · Historia 1 (P1) · Consultar riesgo  🎯 MVP
- [x] T010 [H1] Carga del modelo y puntuación con nivel y recomendación (`src/churn/predict.py`) → FR-001, FR-010
- [x] T011 [H1] Contrato Pydantic con rangos, dominios y `extra="forbid"` (`src/churn/api.py`) → FR-002, FR-003
- [x] T012 [H1] Endpoint `POST /predict` con versión y aviso (`src/churn/api.py`) → FR-001, FR-005
- [x] T013 [H1] Manejadores de error 422/503/500 en español (`src/churn/api.py`)
- [x] T014 [H1] Pruebas: caso feliz, rango, categoría, campo extra, campo faltante, orden de riesgo (`tests/test_api.py`) → SC-005

## Fase 4 · Historia 2 (P2) · Priorizar campaña
- [x] T015 [H2] Endpoint `POST /predict/lote` (1..1000) (`src/churn/api.py`) → FR-004
- [x] T016 [H2] Métricas de negocio con presupuesto (`src/churn/evaluate.py`) → SC-006
- [x] T017 [H2] Prueba de presupuesto y de lote (`tests/test_modelo.py`, `tests/test_api.py`)

## Fase 5 · Historia 3 (P3) · Confiar en el tiempo (MLOps)
- [x] T018 [H3] `GET /health` (`src/churn/api.py`) → FR-006
- [x] T019 [H3] Logging estructurado JSONL con hash de ID (`src/churn/monitoring.py`) → FR-008
- [x] T020 [H3] `GET /metrics` operación + negocio + drift (`src/churn/monitoring.py`) → FR-007
- [x] T021 [H3] PSI y simulación de escenario crisis (`src/churn/drift.py`) → SC-008
- [x] T022 [H3] Pruebas de drift y de privacidad en logs (`tests/test_drift.py`, `tests/test_api.py`)
- [x] T023 [P] [H3] Dashboard HTML sin dependencias (`dashboard/index.html`)

## Fase 6 · Cierre
- [x] T024 [P] README ejecutable multiplataforma (`README.md`)
- [x] T025 [P] Gobernanza y ética (`docs/GOBERNANZA.md`, `docs/ETICA.md`)
- [x] T026 Ejecutar `/speckit.converge` y resolver brechas hasta estado `Converged`

## Dependencias
Fase 1 → Fase 2 → (H1 → H2) y H3 en paralelo tras T012 → Fase 6.
