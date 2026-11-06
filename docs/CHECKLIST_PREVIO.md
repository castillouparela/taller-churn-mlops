# Checklist previo al taller

## Para el facilitador
### Dos semanas antes
- [ ] Confirmar sala: enchufes para todos, proyector, red Wi-Fi (o plan sin internet), mesas para parejas.
- [ ] Enviar a los asistentes este checklist y el repositorio (`taller-churn-mlops-alumno.zip`).
- [ ] Solicitar permisos de administrador o software preinstalado a TI (VS Code, Python, Git, Node, Ollama).
- [ ] Definir si habrá servidor Ollama compartido (ver `PLAN_B.md`, sección B2).

### Una semana antes
- [ ] Probar la instalación completa en Windows, macOS y Linux con los scripts de `scripts/`.
- [ ] Preparar el kit offline en USB (`PLAN_B.md`, sección A).
- [ ] Ensayar el guion completo con cronómetro (objetivo: 170 min, 10 min de colchón).
- [ ] Recoger el resultado del smoke test de cada asistente (captura de pantalla).

### El día del taller (60 min antes)
- [ ] Repo solución: `python tareas.py todo` y `pytest` en verde.
- [ ] `ollama run taller-coder "hola"` para precargar el modelo.
- [ ] API corriendo en el repo solución para la demo inicial (`uvicorn churn.api:app`).
- [ ] Rúbricas y tarjetas de prompts impresas.
- [ ] Temporizador visible y diapositivas abiertas.

## Para cada asistente (antes de llegar)
### Equipo
- [ ] RAM: **16 GB recomendado** (8 GB mínimo con modelo 3B). Disco libre: **15 GB**.
- [ ] Windows 10/11, macOS 12+ o Linux (Ubuntu 22.04+). Permisos para instalar software.

### Software (o ejecute el script de su SO en `scripts/`)
- [ ] VS Code instalado → `code --version`
- [ ] Python 3.11+ → `python --version` (Windows: `py -3.12 --version`)
- [ ] Git → `git --version`
- [ ] Node.js LTS → `node --version`
- [ ] uv → `uv --version`
- [ ] Ollama → `ollama --version` y la app/servicio corriendo
- [ ] Modelo descargado → `ollama pull qwen2.5-coder:7b` (≈ 4,7 GB) **o** `qwen2.5-coder:3b` (≈ 1,9 GB)
- [ ] Modelo del taller creado → `ollama create taller-coder -f Modelfile` (o `taller-coder-mini -f Modelfile.mini`)
- [ ] OpenCode → `opencode --version`
- [ ] Extensión **OpenCode** en VS Code (Marketplace) y extensión **Python**
- [ ] Spec Kit → `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
- [ ] Integración de Spec Kit en el repo → `specify integration install opencode`

### Proyecto
- [ ] Repositorio descomprimido o clonado y abierto en VS Code
- [ ] Entorno virtual creado y activado; `pip install -e ".[dev]"`
- [ ] `python scripts/smoke_test.py` termina con **"Todo listo para el taller."**
- [ ] En OpenCode, `/models` muestra **Ollama (local) → taller-coder** y responde a "Hola"

> Si algo falla, no se preocupe: traiga la captura del error. Hay Plan B para todos los casos.
