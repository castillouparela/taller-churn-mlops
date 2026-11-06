"""Métricas técnicas, de negocio y de equidad para el modelo de churn."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)

from churn import config


def elegir_umbral(y_true, proba, min_recall: float = config.MIN_RECALL) -> float:
    """Umbral con mayor precisión que aún cumple el recall mínimo de negocio."""
    precision, recall, umbrales = precision_recall_curve(y_true, proba)
    validos = [(p, t) for p, r, t in zip(precision[:-1], recall[:-1], umbrales) if r >= min_recall]
    if not validos:
        return config.UMBRAL_DECISION_DEFAULT
    return round(float(max(validos)[1]), 4)


def metricas_tecnicas(y_true, proba, umbral: float) -> dict:
    """ROC-AUC, precision, recall, F1 y matriz de confusión."""
    y_pred = (np.asarray(proba) >= umbral).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "roc_auc": round(float(roc_auc_score(y_true, proba)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "umbral": umbral,
        "matriz_confusion": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


def metricas_negocio(proba, cargo_mensual, umbral: float, y_true=None) -> dict:
    """Clientes e ingresos en riesgo y priorización según presupuesto de campaña."""
    proba = np.asarray(proba, dtype=float)
    cargo = np.asarray(cargo_mensual, dtype=float)
    en_riesgo = proba >= umbral
    perdida_esperada = proba * cargo  # ingreso mensual esperado que se perdería

    # Priorizar por pérdida esperada hasta agotar el presupuesto
    max_contactos = int(config.PRESUPUESTO_CAMPANA // config.COSTO_CONTACTO)
    orden = np.argsort(-perdida_esperada)
    candidatos = [i for i in orden if en_riesgo[i]][:max_contactos]
    ingreso_retenido_esperado = float(perdida_esperada[candidatos].sum() * config.TASA_EXITO_CAMPANA)
    costo = len(candidatos) * config.COSTO_CONTACTO

    resultado = {
        "clientes_evaluados": int(len(proba)),
        "clientes_en_riesgo": int(en_riesgo.sum()),
        "pct_en_riesgo": round(float(en_riesgo.mean()), 4) if len(proba) else 0.0,
        "ingresos_mensuales_en_riesgo": round(float(cargo[en_riesgo].sum()), 2),
        "clientes_priorizados": len(candidatos),
        "costo_campana": round(costo, 2),
        "ingreso_retenido_esperado": round(ingreso_retenido_esperado, 2),
        "roi_esperado": round((ingreso_retenido_esperado - costo) / costo, 3) if costo else None,
    }
    if y_true is not None:
        y = np.asarray(y_true)
        resultado["tasa_churn_real"] = round(float(y.mean()), 4)
    return resultado


def metricas_equidad(y_true, proba, grupos, umbral: float) -> dict:
    """Recall y tasa de selección por grupo sensible (auditoría de sesgo)."""
    df = pd.DataFrame({"y": np.asarray(y_true), "p": np.asarray(proba), "g": np.asarray(grupos)})
    df["pred"] = (df["p"] >= umbral).astype(int)
    por_grupo = {}
    for g, sub in df.groupby("g"):
        positivos = sub[sub["y"] == 1]
        por_grupo[str(g)] = {
            "n": int(len(sub)),
            "tasa_seleccion": round(float(sub["pred"].mean()), 4),
            "recall": round(float(positivos["pred"].mean()), 4) if len(positivos) else None,
        }
    tasas = [v["tasa_seleccion"] for v in por_grupo.values()]
    return {
        "por_grupo": por_grupo,
        # Ratio de impacto dispar: < 0.8 sugiere revisar (regla de los 4/5)
        "ratio_impacto_dispar": round(min(tasas) / max(tasas), 4) if max(tasas) > 0 else None,
    }


def cumple_criterios(m: dict) -> dict:
    """Compara contra los criterios de éxito de ASUM-DM."""
    return {
        "roc_auc": m["roc_auc"] >= config.MIN_ROC_AUC,
        "recall": m["recall"] >= config.MIN_RECALL,
        "precision": m["precision"] >= config.MIN_PRECISION,
    }
