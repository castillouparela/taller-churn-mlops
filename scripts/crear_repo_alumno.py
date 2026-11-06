"""Genera el repositorio del alumno a partir de esta solución.

Uso: python scripts/crear_repo_alumno.py [destino]
El alumno recibe estructura, dataset, configuración, skills, prompts y plantillas; el código, las pruebas
y los artefactos SDD que se construyen en el taller se mueven a referencia/ como red de seguridad.
"""
import shutil
import sys
from pathlib import Path

ORIGEN = Path(__file__).resolve().parents[1]
DESTINO = Path(sys.argv[1]) if len(sys.argv) > 1 else ORIGEN.parent / "taller-churn-mlops-alumno"

IGNORAR = shutil.ignore_patterns(".venv", "__pycache__", "*.egg-info", ".pytest_cache", "*.jsonl", "referencia")
# Lo que el alumno construye durante el taller (se mueve a referencia/)
A_REFERENCIA = [
    "src/churn/dataset.py", "src/churn/features.py", "src/churn/evaluate.py", "src/churn/train.py",
    "src/churn/predict.py", "src/churn/api.py", "src/churn/monitoring.py", "src/churn/drift.py",
    "tests", "specs", ".specify", "business/ASUM-DM.md", "models/churn_model.joblib",
    "models/model_card.json", "reports/metrics/evaluacion.json", "reports/metrics/drift.json",
    "docs/GOBERNANZA.md",
]
# Material sólo para el facilitador
EXCLUIR = ["docs/GUION_FACILITADOR.md", "data/drift"]


def main() -> None:
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    shutil.copytree(ORIGEN, DESTINO, ignore=IGNORAR)
    ref = DESTINO / "referencia"
    for rel in A_REFERENCIA:
        src = DESTINO / rel
        if not src.exists():
            continue
        dst = ref / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
    for rel in EXCLUIR:
        p = DESTINO / rel
        shutil.rmtree(p) if p.is_dir() else p.unlink(missing_ok=True)
    # Carpetas vacías que el alumno llenará
    for carpeta in ["business", "tests", "models", "reports/metrics", "logs", "data/drift"]:
        (DESTINO / carpeta).mkdir(parents=True, exist_ok=True)
        (DESTINO / carpeta / ".gitkeep").touch()
    (ref / "LEEME.md").write_text(
        "# Referencia (red de seguridad)\n\nVersión final de cada archivo que se construye en el taller.\n"
        "Úsala sólo si te atrasas o el modelo local falla: copia el archivo al mismo lugar fuera de `referencia/`.\n"
        "Primero intenta generarlo con OpenCode y compáralo con la especificación.\n",
        encoding="utf-8",
    )
    readme = DESTINO / "README.md"
    readme.write_text(
        "> **Repositorio del alumno**: el código de `src/churn/`, las pruebas y las especificaciones se construyen "
        "durante el taller con OpenCode y Spec Kit. Empieza por `plantillas/ASUM-DM_plantilla.md` y "
        "`prompts/PROMPTS_OPENCODE.md`. La solución está en `referencia/`.\n\n" + readme.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    print(f"[ok] repo alumno creado en {DESTINO}")


if __name__ == "__main__":
    main()
