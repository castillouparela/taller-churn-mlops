"""Envía clientes de un CSV a la API en ejecución para poblar /metrics y el dashboard.

Uso:
    python scripts/simular_trafico.py                    # 300 clientes del dataset base
    python scripts/simular_trafico.py --escenario crisis # clientes con drift
"""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request

import pandas as pd

from churn import config
from churn.dataset import generar


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--escenario", default="base", choices=["base", "crisis"])
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--url", default="http://localhost:8000")
    a = ap.parse_args()

    df = pd.read_csv(config.DATA_RAW) if a.escenario == "base" else generar(seed=config.SEED + 1, escenario="crisis")
    muestra = df.sample(n=min(a.n, len(df)), random_state=config.SEED)
    clientes = muestra[[config.ID_COL, *config.FEATURES]].to_dict(orient="records")
    # Enviar en lotes de 100 al endpoint batch
    for i in range(0, len(clientes), 100):
        cuerpo = json.dumps({"clientes": clientes[i:i + 100]}).encode()
        req = urllib.request.Request(f"{a.url}/predict/lote", data=cuerpo, headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=30).read()
        except urllib.error.URLError as exc:
            raise SystemExit(f"No se pudo conectar a {a.url}: {exc}. ¿Está corriendo uvicorn?")
    print(f"[ok] {len(clientes)} clientes ({a.escenario}) enviados. Abra {a.url}/dashboard")


if __name__ == "__main__":
    main()
