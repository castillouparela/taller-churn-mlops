#!/usr/bin/env bash
# Instalación del entorno del taller en macOS (requiere Homebrew: https://brew.sh)
# Uso: bash scripts/instalar_macos.sh [--mini]   (--mini = modelo 3B para equipos de 8 GB)
set -euo pipefail
MODELO="qwen2.5-coder:7b"; MF="Modelfile"; NOMBRE="taller-coder"
if [[ "${1:-}" == "--mini" ]]; then MODELO="qwen2.5-coder:3b"; MF="Modelfile.mini"; NOMBRE="taller-coder-mini"; fi

command -v brew >/dev/null || { echo "Instale Homebrew primero: https://brew.sh"; exit 1; }
echo "==> 1/7 VS Code, Ollama, Python 3.12, Git, Node.js, uv"
brew install --cask visual-studio-code ollama || true
brew install python@3.12 git node uv

echo "==> 2/7 OpenCode"
command -v opencode >/dev/null || curl -fsSL https://opencode.ai/install | bash

echo "==> 3/7 Spec Kit (specify-cli)"
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git || uv tool upgrade specify-cli

echo "==> 4/7 Extensiones de VS Code"
code --install-extension ms-python.python || true
code --install-extension sst-dev.opencode || echo "   Instale 'OpenCode' desde el Marketplace de VS Code"

echo "==> 5/7 Modelo local ($MODELO)"
(pgrep -x ollama >/dev/null || (ollama serve >/dev/null 2>&1 &)); sleep 3
ollama pull "$MODELO"
ollama create "$NOMBRE" -f "$MF"

echo "==> 6/7 Entorno Python del proyecto"
python3.12 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip && pip install -e ".[dev]"

echo "==> 7/7 Smoke test"
python scripts/smoke_test.py
