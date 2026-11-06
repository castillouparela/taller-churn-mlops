"""Detección de drift con PSI y simulación de un escenario de cambio de mercado.

Uso:
    python -m churn.drift --escenario crisis
"""
from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd

from churn import config
from churn.dataset import generar
from churn.evaluate import metricas_negocio, metricas_tecnicas
from churn.predict import cargar_modelo


def psi_numerica(actual: pd.Series, cortes: list[float], proporciones: list[float]) -> float:
    """PSI de una variable numérica usando los bins (deciles) de referencia."""
    bordes = [-np.inf, *cortes, np.inf]
    esperado = np.clip(np.asarray(proporciones, dtype=float), 1e-4, None)
    obs = np.histogram(actual, bins=bordes)[0] / max(len(actual), 1)
    obs = np.clip(obs, 1e-4, None)
    return round(float(np.sum((obs - esperado) * np.log(obs / esperado))), 4)


def psi_categorica(actual: pd.Series, ref: dict) -> float:
    """PSI de una variable categórica con las frecuencias de referencia."""
    obs = actual.value_counts(normalize=True)
    total = 0.0
    for cat in set(ref) | set(obs.index):
        e = max(ref.get(cat, 0.0), 1e-4)
        a = max(float(obs.get(cat, 0.0)), 1e-4)
        total += (a - e) * np.log(a / e)
    return round(float(total), 4)


def estado_psi(valor: float) -> str:
    if valor >= config.PSI_CRITICO:
        return "critico"
    if valor >= config.PSI_ALERTA:
        return "alerta"
    return "estable"


def calcular_drift(df: pd.DataFrame, perfil: dict) -> dict:
    """PSI por feature y estado global (el peor de todos)."""
    resultado = {}
    for col, info in perfil["numericas"].items():
        if col in df:
            resultado[col] = psi_numerica(df[col], info["cortes"], info["proporciones"])
    for col, ref in perfil["categoricas"].items():
        if col in df:
            resultado[col] = psi_categorica(df[col], ref)
    detalle = {c: {"psi": v, "estado": estado_psi(v)} for c, v in resultado.items()}
    peor = max(resultado.values()) if resultado else 0.0
    return {"features": detalle, "psi_max": peor, "estado_global": estado_psi(peor)}


def simular(escenario: str = "crisis") -> dict:
    """Compara desempeño y métricas de negocio entre datos base y escenario alterado."""
    bundle = cargar_modelo()
    card = bundle["card"]
    umbral = card["umbral_decision"]
    comparacion = {}
    for nombre, df in {
        "base": pd.read_csv(config.DATA_RAW),
        escenario: generar(seed=config.SEED + 1, escenario=escenario),
    }.items():
        proba = bundle["pipeline"].predict_proba(df[config.FEATURES])[:, 1]
        comparacion[nombre] = {
            "tecnicas": metricas_tecnicas(df[config.TARGET], proba, umbral),
            "negocio": metricas_negocio(proba, df["cargo_mensual"], umbral, df[config.TARGET]),
            "drift": calcular_drift(df, card["perfil_referencia"]),
        }
        if nombre != "base":
            config.DATA_DRIFT.mkdir(parents=True, exist_ok=True)
            df.to_csv(config.DATA_DRIFT / f"churn_telco_{nombre}.csv", index=False)

    alerta = comparacion[escenario]["drift"]["estado_global"]
    reporte = {
        "version_modelo": card["version"],
        "escenario": escenario,
        "comparacion": comparacion,
        "decision": (
            "Reentrenar y revalidar antes de seguir usando el modelo"
            if alerta == "critico" else "Monitorear de cerca" if alerta == "alerta" else "Sin acción"
        ),
    }
    config.DRIFT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    config.DRIFT_REPORT_PATH.write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
    return reporte


def main() -> None:
    parser = argparse.ArgumentParser(description="Simula drift y mide su impacto")
    parser.add_argument("--escenario", default="crisis")
    args = parser.parse_args()
    r = simular(args.escenario)
    print(f"{'métrica':<32}{'base':>12}{args.escenario:>12}")
    b, c = r["comparacion"]["base"], r["comparacion"][args.escenario]
    filas = [
        ("ROC-AUC", b["tecnicas"]["roc_auc"], c["tecnicas"]["roc_auc"]),
        ("Precision", b["tecnicas"]["precision"], c["tecnicas"]["precision"]),
        ("Recall", b["tecnicas"]["recall"], c["tecnicas"]["recall"]),
        ("Tasa churn real", b["negocio"]["tasa_churn_real"], c["negocio"]["tasa_churn_real"]),
        ("% clientes en riesgo", b["negocio"]["pct_en_riesgo"], c["negocio"]["pct_en_riesgo"]),
        ("Ingresos/mes en riesgo", b["negocio"]["ingresos_mensuales_en_riesgo"], c["negocio"]["ingresos_mensuales_en_riesgo"]),
        ("PSI máximo", b["drift"]["psi_max"], c["drift"]["psi_max"]),
    ]
    for nombre, vb, vc in filas:
        print(f"{nombre:<32}{vb:>12}{vc:>12}")
    print(f"\nEstado drift: {c['drift']['estado_global'].upper()} -> {r['decision']}")
    print(f"Reporte: {config.DRIFT_REPORT_PATH.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
