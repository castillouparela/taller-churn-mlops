"""Carga del modelo y lógica de puntuación: probabilidad, nivel de riesgo y acción."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from churn import config

# Recomendaciones por nivel de riesgo (las define el área de retención, no el modelo)
ACCIONES = {
    "alto": "Contactar en 48 h con asesor de retención y ofrecer beneficio personalizado.",
    "medio": "Incluir en campaña digital de fidelización y revisar reclamos abiertos.",
    "bajo": "Sin acción de retención; mantener comunicación habitual.",
}


class ModeloNoDisponible(RuntimeError):
    """El artefacto del modelo no existe o no se pudo cargar."""


@lru_cache(maxsize=1)
def cargar_modelo(ruta: str = str(config.MODEL_PATH)) -> dict:
    """Carga (una vez) el bundle {pipeline, card} serializado con joblib."""
    if not Path(ruta).exists():
        raise ModeloNoDisponible(f"No existe {ruta}. Ejecute: python -m churn.train")
    try:
        return joblib.load(ruta)
    except Exception as exc:  # archivo corrupto o versión incompatible
        raise ModeloNoDisponible(f"No se pudo cargar el modelo: {exc}") from exc


def nivel_riesgo(prob: float, umbral: float, umbral_alto: float) -> str:
    if prob >= umbral_alto:
        return "alto"
    if prob >= umbral:
        return "medio"
    return "bajo"


def puntuar(registros: list[dict], bundle: dict | None = None) -> list[dict]:
    """Devuelve probabilidad, nivel y recomendación para cada registro."""
    bundle = bundle or cargar_modelo()
    card = bundle["card"]
    df = pd.DataFrame(registros)[config.FEATURES]
    probas = bundle["pipeline"].predict_proba(df)[:, 1]
    salida = []
    for prob in probas:
        nivel = nivel_riesgo(float(prob), card["umbral_decision"], card["umbral_riesgo_alto"])
        salida.append(
            {
                "probabilidad_churn": round(float(prob), 4),
                "nivel_riesgo": nivel,
                "recomendacion": ACCIONES[nivel],
                "version_modelo": card["version"],
            }
        )
    return salida
