> **Repositorio del alumno**: el código de `src/churn/`, las pruebas y las especificaciones se construyen durante el taller con OpenCode y Spec Kit. Empieza por `plantillas/ASUM-DM_plantilla.md` y `prompts/PROMPTS_OPENCODE.md`. La solución está en `referencia/`.

# Taller · Churn Telco con ASUM-DM + SDD + ECC + OpenCode + MLOps

Repositorio plantilla del taller **"Integración de ASUM-DM, MLOps, Spec-Driven Development, skills ECC y modelos
abiertos con OpenCode en Visual Studio Code"**. Todo corre en tu laptop: **sin tokens, sin cuentas, sin nube**.

**Resultado**: una API que recibe datos de un cliente y devuelve probabilidad de churn, nivel de riesgo y acción
recomendada, con pruebas, métricas de negocio, dashboard, detección de drift y trazabilidad de especificaciones.

```
ASUM-DM (negocio) → Spec Kit (constitución, spec, plan, tareas) → OpenCode + skills ECC + Ollama (código)
→ FastAPI + pytest → /health /metrics /dashboard + drift (MLOps) → gobernanza
```

## Contenido
| Ruta | Qué es |
|---|---|
| `business/ASUM-DM.md` | Entendimiento de negocio completo (referencia) |
| `.specify/memory/constitution.md`, `specs/001-api-churn/` | Constitución, spec, plan, tareas y checklist (referencia SDD) |
| `src/churn/` | Código: dataset, features, train, evaluate, predict, api, monitoring, drift |
| `tests/` | 18 pruebas pytest (datos, modelo, API, drift, privacidad) |
| `data/raw/churn_telco.csv` | Dataset sintético determinista (5.000 clientes, semilla 42) |
| `models/` | Modelo serializado + `model_card.json` |
| `dashboard/index.html` | Panel de métricas sin dependencias externas |
| `.opencode/skills/` | 6 skills estilo ECC: ML, testing, seguridad, arquitectura, docs, revisión vs spec |
| `opencode.json`, `Modelfile`, `AGENTS.md` | Configuración de OpenCode + Ollama local y reglas del agente |
| `prompts/PROMPTS_OPENCODE.md` | Prompts en español, listos para copiar |
| `plantillas/` | Plantillas ASUM-DM, spec, plan, tasks |
| `docs/` | Guion del facilitador, gobernanza, ética, rúbrica, plan B, checklist previo, reto |
| `scripts/` | Instaladores por SO, smoke test, simulador de tráfico, generador de repo alumno |

## 1. Requisitos
- 16 GB de RAM recomendado (8 GB con el modelo 3B), 15 GB de disco libre.
- VS Code, Python 3.11+, Git, Node.js LTS, uv, Ollama, OpenCode, Spec Kit.

## 2. Instalación automática (recomendada)
Desde la raíz del repositorio:

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\instalar_windows.ps1        # laptop >= 16 GB
powershell -ExecutionPolicy Bypass -File scripts\instalar_windows.ps1 -Mini  # laptop de 8 GB
```
**macOS** (requiere [Homebrew](https://brew.sh))
```bash
bash scripts/instalar_macos.sh          # o: bash scripts/instalar_macos.sh --mini
```
**Linux (Ubuntu/Debian)**
```bash
bash scripts/instalar_linux.sh          # o: bash scripts/instalar_linux.sh --mini
```

## 3. Instalación manual paso a paso
| Paso | Windows (PowerShell) | macOS | Linux |
|---|---|---|---|
| VS Code | `winget install -e --id Microsoft.VisualStudioCode` | `brew install --cask visual-studio-code` | `sudo snap install code --classic` |
| Python 3.12 | `winget install -e --id Python.Python.3.12` | `brew install python@3.12` | `sudo apt install python3 python3-venv` |
| Git | `winget install -e --id Git.Git` | `brew install git` | `sudo apt install git` |
| Node.js | `winget install -e --id OpenJS.NodeJS.LTS` | `brew install node` | `sudo apt install nodejs npm` |
| uv | `winget install -e --id astral-sh.uv` | `brew install uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Ollama | `winget install -e --id Ollama.Ollama` | `brew install --cask ollama` | `curl -fsSL https://ollama.com/install.sh \| sh` |
| OpenCode | `npm install -g opencode-ai` | `curl -fsSL https://opencode.ai/install \| bash` | `curl -fsSL https://opencode.ai/install \| bash` |
| Spec Kit | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` | igual | igual |

**Modelo local** (todos los SO):
```bash
ollama pull qwen2.5-coder:7b
ollama create taller-coder -f Modelfile        # contexto 16k y temperatura baja para OpenCode
# Laptop de 8 GB:
ollama pull qwen2.5-coder:3b && ollama create taller-coder-mini -f Modelfile.mini
```

**Extensiones de VS Code**: busca **OpenCode** y **Python** en el Marketplace e instálalas
(o `code --install-extension ms-python.python`). La extensión de OpenCode se activa al ejecutar `opencode`
en la terminal integrada (atajo: `Ctrl+Esc` en Windows/Linux, `Cmd+Esc` en macOS).

**Entorno del proyecto**
```bash
# macOS / Linux
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```
```powershell
# Windows
py -3.12 -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

**Spec Kit en este repo** (crea `.opencode/commands/speckit.*`):
```bash
specify integration install opencode
# Si tu versión no lo reconoce: specify init --here --integration opencode
```

## 4. Smoke test
```bash
python scripts/smoke_test.py            # verifica herramientas, Ollama, modelo y API
python scripts/smoke_test.py --sin-ia   # sólo la parte Python (Plan B)
```
Salida esperada al final: `Todo listo para el taller.`

## 5. Configuración de OpenCode con Ollama
`opencode.json` (ya incluido) apunta a `http://localhost:11434/v1` con el proveedor `@ai-sdk/openai-compatible`:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "ollama/taller-coder",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": { "taller-coder": { "name": "Taller - Qwen2.5-Coder 7B (ctx 16k)" } }
    }
  }
}
```
Abre VS Code en la carpeta, terminal integrada → `opencode` → `/models` → **taller-coder**.
Alternativa: `ollama launch opencode` (configura OpenCode con Ollama sin editar archivos).

> **Contexto**: la documentación de Ollama recomienda 64k de contexto para OpenCode. En laptops usamos 16k
> (`Modelfile`) con prompts cortos; si tienes ≥ 32 GB de RAM sube `num_ctx` a 32768 o más.

### Skills ECC
Las skills de `.opencode/skills/<nombre>/SKILL.md` siguen el formato estándar (`name`, `description`) y OpenCode
las descubre automáticamente; el agente las carga con su herramienta `skill`. Están inspiradas en
[Everything Claude Code (ECC)](https://github.com/affaan-m/ECC). Para usar el catálogo completo de ECC
(opcional, requiere internet) sigue su guía para OpenCode o copia skills de su carpeta `skills/` a `.opencode/skills/`.

## 6. Uso
```bash
python -m churn.dataset                   # 1. datos  -> data/raw/churn_telco.csv (5000 filas, churn ~25 %)
python -m churn.train                     # 2. modelo -> models/ (ROC-AUC ~0,81, recall ~0,73, precision ~0,49)
pytest                                    # 3. pruebas -> 18 passed
uvicorn churn.api:app --reload            # 4. API en http://localhost:8000/docs
python scripts/simular_trafico.py         # 5. (otra terminal) tráfico -> http://localhost:8000/dashboard
python -m churn.drift --escenario crisis  # 6. drift -> reports/metrics/drift.json
python scripts/simular_trafico.py --escenario crisis --n 500   # el dashboard pasa a "critico"
```
Atajos: `python tareas.py <datos|entrenar|probar|api|trafico|drift|smoke|todo>` (o `make <tarea>` en macOS/Linux).

**Ejemplo de consulta**
```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"antiguedad_meses\": 6, \"tipo_plan\": \"prepago\", \"cargo_mensual\": 45.5, \"reclamos_ult_3m\": 3, \"uso_datos_gb\": 2.1, \"metodo_pago\": \"efectivo\", \"renovo_contrato\": \"no\"}"
```
```json
{"id_cliente": null, "probabilidad_churn": 0.97, "nivel_riesgo": "alto",
 "recomendacion": "Contactar en 48 h con asesor de retención y ofrecer beneficio personalizado.",
 "version_modelo": "1.0.0", "aviso": "Apoyo a la decisión: requiere revisión humana antes de acciones que afecten al cliente."}
```

| Endpoint | Propósito |
|---|---|
| `POST /predict` | Un cliente → probabilidad, nivel, recomendación, versión |
| `POST /predict/lote` | Hasta 1.000 clientes |
| `GET /health` | Estado del servicio y versión del modelo |
| `GET /metrics` | Operación, negocio (clientes/ingresos en riesgo, priorizados) y drift (PSI) |
| `GET /dashboard` | Panel visual que lee `/metrics` cada 5 s |

## 7. Repo del alumno
`python scripts/crear_repo_alumno.py` genera `../taller-churn-mlops-alumno/`: misma estructura y dataset, pero sin
el código de `src/churn/`, sin pruebas y sin specs (los construyen en el taller). La solución queda en `referencia/`
como red de seguridad.

## 8. Uso responsable
Este modelo **apoya** decisiones de retención: no debe usarse para negar servicios, cambiar precios ni tomar decisiones
automatizadas sin revisión humana. No usa la edad para predecir y audita el impacto por grupo; los logs guardan IDs con hash.
Los datos son sintéticos. Ver [docs/ETICA.md](docs/ETICA.md) y [docs/GOBERNANZA.md](docs/GOBERNANZA.md).
