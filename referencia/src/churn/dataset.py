"""Generador determinista de un dataset sintético de churn en telecomunicaciones.

Uso:
    python -m churn.dataset                     # escenario base -> data/raw/churn_telco.csv
    python -m churn.dataset --escenario crisis  # escenario con drift -> data/drift/
"""
from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from churn import config

# Escenarios: "base" refleja la operación normal; "crisis" simula un cambio de mercado
ESCENARIOS = {
    "base": {
        "p_plan": [0.40, 0.40, 0.20],
        "cargo_shift": 0.0,
        "lambda_reclamos": 0.8,
        "p_efectivo": 0.20,
        "uso_shift": 0.0,
        "coef_uso": -0.06,       # en operación normal, más uso = más fidelidad
        "coef_renovo": -1.50,
    },
    "crisis": {  # subida de precios, más reclamos y migración a prepago
        "p_plan": [0.60, 0.30, 0.10],
        "cargo_shift": 18.0,
        "lambda_reclamos": 2.0,
        "p_efectivo": 0.40,
        "uso_shift": -2.0,
        # Drift de concepto: un competidor capta a los usuarios intensivos de datos
        "coef_uso": 0.08,
        "coef_renovo": -0.60,
    },
}


def generar(n: int = config.N_CLIENTES, seed: int = config.SEED, escenario: str = "base") -> pd.DataFrame:
    """Genera n clientes-mes con relaciones causales plausibles y semilla fija."""
    if escenario not in ESCENARIOS:
        raise ValueError(f"Escenario desconocido: {escenario}. Use {list(ESCENARIOS)}")
    p = ESCENARIOS[escenario]
    rng = np.random.default_rng(seed)

    # La edad no entra al modelo, pero se correlaciona con el plan (proxy de sesgo)
    rango_edad = rng.choice(config.RANGOS_EDAD, size=n, p=[0.20, 0.40, 0.30, 0.10])
    sesgo_joven = np.where(rango_edad == "18-25", 0.20, np.where(rango_edad == "60+", -0.10, 0.0))
    u = rng.random(n)
    p_prepago = np.clip(p["p_plan"][0] + sesgo_joven, 0.05, 0.95)
    p_basico = (1 - p_prepago) * p["p_plan"][1] / (p["p_plan"][1] + p["p_plan"][2])
    tipo_plan = np.where(u < p_prepago, "prepago",
                         np.where(u < p_prepago + p_basico, "pospago_basico", "pospago_premium"))
    # Cargo base según plan + ruido + desplazamiento del escenario
    base_cargo = np.select(
        [tipo_plan == "prepago", tipo_plan == "pospago_basico"], [25.0, 55.0], default=95.0
    )
    cargo = np.clip(base_cargo + rng.normal(0, 12, n) + p["cargo_shift"], 10, 200).round(2)

    antiguedad = np.clip(rng.gamma(2.0, 14.0, n), 1, 120).round().astype(int)
    reclamos = rng.poisson(p["lambda_reclamos"], n)
    uso_datos = np.clip(rng.lognormal(1.8, 0.6, n) + p["uso_shift"], 0, 80).round(2)

    resto = (1 - p["p_efectivo"]) / 3
    metodo_pago = rng.choice(
        config.METODOS_PAGO, size=n, p=[resto, resto, p["p_efectivo"], resto]
    )
    # Clientes antiguos y pospago renuevan más
    p_renueva = np.clip(0.25 + antiguedad / 200 + (tipo_plan != "prepago") * 0.2, 0, 0.95)
    renovo = np.where(rng.random(n) < p_renueva, "si", "no")

    # Modelo latente de abandono (la "verdad" que el modelo debe aprender)
    logit = (
        -0.20
        - 0.045 * antiguedad
        + 0.65 * reclamos
        + 0.022 * (cargo - 60)
        + p["coef_uso"] * (uso_datos - 6)
        + 0.90 * (tipo_plan == "prepago")
        + 0.70 * (metodo_pago == "efectivo")
        + p["coef_renovo"] * (renovo == "si")
    )
    prob = 1 / (1 + np.exp(-logit))
    churn = (rng.random(n) < prob).astype(int)

    return pd.DataFrame(
        {
            config.ID_COL: [f"C{seed:02d}{i:05d}" for i in range(n)],
            "periodo": "2026-09" if escenario == "base" else "2026-10",
            "antiguedad_meses": antiguedad,
            "tipo_plan": tipo_plan,
            "cargo_mensual": cargo,
            "reclamos_ult_3m": reclamos,
            "uso_datos_gb": uso_datos,
            "metodo_pago": metodo_pago,
            "renovo_contrato": renovo,
            config.SENSITIVE_COL: rango_edad,
            config.TARGET: churn,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera el dataset sintético de churn")
    parser.add_argument("--escenario", default="base", choices=list(ESCENARIOS))
    parser.add_argument("--n", type=int, default=config.N_CLIENTES)
    parser.add_argument("--seed", type=int, default=config.SEED)
    args = parser.parse_args()

    # El escenario alterado usa otra semilla para simular un mes distinto
    seed = args.seed if args.escenario == "base" else args.seed + 1
    df = generar(args.n, seed, args.escenario)
    if args.escenario == "base":
        destino = config.DATA_RAW
    else:
        destino = config.DATA_DRIFT / f"churn_telco_{args.escenario}.csv"
    destino.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destino, index=False)
    print(f"[ok] {len(df)} filas -> {destino.relative_to(config.ROOT)} | churn={df[config.TARGET].mean():.1%}")


if __name__ == "__main__":
    main()
