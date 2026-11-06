"""Pruebas del modelo: criterios de éxito de ASUM-DM y trazabilidad."""
import json

from churn import config
from churn.evaluate import metricas_negocio


def test_model_card_cumple_criterios():
    card = json.loads(config.MODEL_CARD_PATH.read_text(encoding="utf-8"))
    m = card["metricas_test"]
    assert m["roc_auc"] >= config.MIN_ROC_AUC
    assert m["recall"] >= config.MIN_RECALL
    assert m["precision"] >= config.MIN_PRECISION
    assert card["aprobado_para_despliegue"] is True


def test_model_card_trazabilidad():
    card = json.loads(config.MODEL_CARD_PATH.read_text(encoding="utf-8"))
    for campo in ("version", "entrenado_en", "dataset", "umbral_decision", "perfil_referencia"):
        assert campo in card
    assert len(card["dataset"]["sha256"]) == 16
    assert config.SENSITIVE_COL not in card["features"]  # atributo sensible excluido


def test_metricas_negocio_respetan_presupuesto():
    r = metricas_negocio([0.9] * 1000, [50.0] * 1000, umbral=0.5)
    assert r["costo_campana"] <= config.PRESUPUESTO_CAMPANA
    assert r["clientes_en_riesgo"] == 1000
    assert r["clientes_priorizados"] == int(config.PRESUPUESTO_CAMPANA // config.COSTO_CONTACTO)
