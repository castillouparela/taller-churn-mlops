"""Pruebas de drift: el PSI debe ser bajo en base y crítico en el escenario de crisis."""
import json

from churn import config
from churn.dataset import generar
from churn.drift import calcular_drift


def _perfil():
    return json.loads(config.MODEL_CARD_PATH.read_text(encoding="utf-8"))["perfil_referencia"]


def test_sin_drift_en_datos_similares():
    r = calcular_drift(generar(seed=7), _perfil())
    assert r["estado_global"] == "estable"


def test_drift_critico_en_crisis():
    r = calcular_drift(generar(seed=8, escenario="crisis"), _perfil())
    assert r["estado_global"] == "critico"
    assert r["features"]["cargo_mensual"]["estado"] == "critico"
