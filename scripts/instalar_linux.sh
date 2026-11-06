#!/usr/bin/env bash
# Instalación del entorno del taller en Linux (Ubuntu/Debian; adapte el gestor de paquetes en otras distros)
# Uso: bash scripts/instalar_macos.sh [--mini]   (--mini = modelo 3B para equipos de 8 GB)
set -euo pipefail
MODELO="qwen2.5-coder:7b"; MF="Modelfile"; NOMBRE="taller-coder"
if [[ "${1:-}" == "--mini" ]]; then MODELO="qwen2.5-coder:3b"; MF="Modelfile.mini"; NOMBRE="taller-coder-mini"; fi

echo "==> 1/7 Python, Git, Node.js, uv, Ollama y VS Code"
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip git curl nodejs npm
python3 -c 'import sys; assert sys.version_info >= (3, 11), "Se requiere Python 3.11+"'
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
command -v ollama >/dev/null || curl -fsSL https://ollama.com/install.sh | sh
command -v code >/dev/null || sudo snap install code --classic || echo "   Instale VS Code desde https://code.visualstudio.com"

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
uv sync --extra dev

echo "==> 7/7 Smoke test"
uv run python scripts/smoke_test.py
