# Instalación del entorno del taller en Windows 10/11 (PowerShell, usa winget)
# Uso:  powershell -ExecutionPolicy Bypass -File scripts\instalar_windows.ps1 [-Mini]
param([switch]$Mini)
$ErrorActionPreference = "Stop"
$Modelo = "qwen2.5-coder:7b"; $MF = "Modelfile"; $Nombre = "taller-coder"
if ($Mini) { $Modelo = "qwen2.5-coder:3b"; $MF = "Modelfile.mini"; $Nombre = "taller-coder-mini" }

function Refrescar-Path { $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User") }

Write-Host "==> 1/7 VS Code, Python 3.12, Git, Node.js, Ollama, uv (winget)"
$paquetes = "Microsoft.VisualStudioCode","Python.Python.3.12","Git.Git","OpenJS.NodeJS.LTS","Ollama.Ollama","astral-sh.uv"
foreach ($p in $paquetes) { winget install -e --id $p --accept-source-agreements --accept-package-agreements --silent; }
Refrescar-Path

Write-Host "==> 2/7 OpenCode"
npm install -g opencode-ai

Write-Host "==> 3/7 Spec Kit (specify-cli)"
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
if ($LASTEXITCODE -ne 0) { uv tool upgrade specify-cli }
Refrescar-Path

Write-Host "==> 4/7 Extensiones de VS Code"
code --install-extension ms-python.python
code --install-extension sst-dev.opencode
if ($LASTEXITCODE -ne 0) { Write-Host "   Instale 'OpenCode' desde el Marketplace de VS Code" }

Write-Host "==> 5/7 Modelo local ($Modelo)"
if (-not (Get-Process ollama -ErrorAction SilentlyContinue)) { Start-Process ollama -ArgumentList "serve" -WindowStyle Hidden; Start-Sleep 4 }
ollama pull $Modelo
ollama create $Nombre -f $MF

Write-Host "==> 6/7 Entorno Python del proyecto"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"

Write-Host "==> 7/7 Smoke test"
python scripts\smoke_test.py
