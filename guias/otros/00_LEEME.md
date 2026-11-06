# Taller: Integración de ASUM-DM, MLOps, SDD, skills ECC y modelos abiertos con OpenCode en VS Code

Capacitación presencial de **3 horas** · caso de negocio: **churn en telecomunicaciones** · 100 % local
(OpenCode + Ollama), sin tokens ni cuentas de proveedores comerciales.

**Objetivo de aprendizaje**: al finalizar, el asistente podrá traducir un objetivo de negocio en un sistema de ML
operable, especificado con SDD, desarrollado con IA local y monitoreado desde una perspectiva MLOps.

## Contenido del paquete
| # | Entregable | Ubicación |
|---|---|---|
| 1 | Repositorio plantilla completo y ejecutable (solución) | `01_repo_solucion/taller-churn-mlops/` |
| 1b | Repositorio del alumno (sin código; solución en `referencia/`) | `02_repo_alumno/taller-churn-mlops-alumno/` |
| 2 | README con instalación para Windows, macOS y Linux + scripts | `01_repo_solucion/.../README.md`, `scripts/instalar_*` |
| 3 | Diapositivas (25 láminas, con notas del orador) | `03_diapositivas/` (.pptx y .pdf) |
| 4 | Guion minuto a minuto del facilitador | `04_guia_y_documentos/GUION_FACILITADOR.md` |
| 5 | Dataset sintético determinista (5.000 clientes, semilla 42) | `data/raw/churn_telco.csv` + `src/churn/dataset.py` |
| 6 | Prompts listos para OpenCode, en español | `04_guia_y_documentos/PROMPTS_OPENCODE.md` |
| 7 | Plantillas ASUM-DM, spec.md, plan.md, tasks.md (+ ejemplos resueltos) | `04_guia_y_documentos/plantillas/` |
| 8 | Rúbrica de evaluación | `04_guia_y_documentos/RUBRICA.md` |
| 9 | Plan B (sin internet / pocos recursos) | `04_guia_y_documentos/PLAN_B.md` |
| 10 | Checklist previo al taller | `04_guia_y_documentos/CHECKLIST_PREVIO.md` |
| + | Gobernanza, ética, reto para casa, ASUM-DM de referencia | `04_guia_y_documentos/` |

## Agenda (180 min)
| Hora | Min | Bloque |
|---|---|---|
| 0:00 | 10 | Apertura y motivación |
| 0:10 | 15 | Fundamentos rápidos |
| 0:25 | 10 | Verificación de instalación (la instalación se hace antes con el checklist) |
| 0:35 | 25 | Bloque 1 · Negocio con ASUM-DM |
| 1:00 | 30 | Bloque 2 · SDD con Spec Kit |
| 1:30 | 45 | Bloque 3 · OpenCode + ECC + modelo local |
| 2:15 | 30 | Bloque 4 · MLOps mínimo viable |
| 2:45 | 15 | Cierre, demo y evaluación |

> La estructura solicitada sumaba 220 min; para respetar el máximo de 3 h la instalación pasa a ser previa
> (en sala sólo se verifica) y se recortan 5 min a apertura, fundamentos, bloques 1–2 y cierre.
> Los bloques prácticos 3 y 4 conservan su tiempo completo.

## Inicio rápido (repo solución)
```bash
cd 01_repo_solucion/taller-churn-mlops
uv sync --extra dev             # crea .venv e instala dependencias de proyecto y desarrollo
uv run python tareas.py todo    # datos -> modelo -> 18 pruebas -> drift
uv run uvicorn churn.api:app --reload  # http://localhost:8000/docs y /dashboard
```

## Stack verificado
Python 3.11+ · pandas · scikit-learn · FastAPI · pytest · Ollama (`qwen2.5-coder:7b` / `3b`) · OpenCode (proveedor
`@ai-sdk/openai-compatible` → `http://localhost:11434/v1`) · Spec Kit (`specify-cli`, integración `opencode`) ·
skills en `.opencode/skills/<nombre>/SKILL.md` inspiradas en Everything Claude Code (ECC).

## Uso responsable
Datos sintéticos. El modelo apoya decisiones de retención; no debe usarse para negar servicios ni cambiar precios.
Ver `04_guia_y_documentos/ETICA.md`.
