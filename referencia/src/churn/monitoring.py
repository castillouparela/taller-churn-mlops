"""Monitoreo operativo: logging estructurado de predicciones y agregación de métricas."""
from __future__ import annotations

import hashlib
import json
import logging
import threading
import time
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from churn import config
from churn.drift import calcular_drift
from churn.evaluate import metricas_negocio


def _logger_json() -> logging.Logger:
    """Logger que escribe una línea JSON por evento en logs/predicciones.jsonl."""
    logger = logging.getLogger("churn.predicciones")
    if not logger.handlers:
        config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(config.PREDICTIONS_LOG, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


def seudonimizar(id_cliente: str | None) -> str | None:
    """Nunca registramos el ID en claro (privacidad): sólo un hash corto."""
    if not id_cliente:
        return None
    return hashlib.sha256(id_cliente.encode()).hexdigest()[:12]


class Monitor:
    """Acumula métricas en memoria (ventana deslizante) y registra cada predicción."""

    def __init__(self, ventana: int = 5000):
        self.inicio = time.time()
        self.lock = threading.Lock()
        self.total = 0
        self.errores = 0
        self.niveles: Counter = Counter()
        self.latencias_ms: deque = deque(maxlen=1000)
        self.entradas: deque = deque(maxlen=ventana)
        self.probas: deque = deque(maxlen=ventana)
        self.logger = _logger_json()

    def registrar(self, entrada: dict, salida: dict, latencia_ms: float) -> None:
        evento = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "evento": "prediccion",
            "id_cliente_hash": seudonimizar(entrada.get("id_cliente")),
            "features": {k: entrada[k] for k in config.FEATURES},
            "probabilidad_churn": salida["probabilidad_churn"],
            "nivel_riesgo": salida["nivel_riesgo"],
            "version_modelo": salida["version_modelo"],
            "latencia_ms": round(latencia_ms, 2),
        }
        self.logger.info(json.dumps(evento, ensure_ascii=False))
        with self.lock:
            self.total += 1
            self.niveles[salida["nivel_riesgo"]] += 1
            self.latencias_ms.append(latencia_ms)
            self.entradas.append(evento["features"])
            self.probas.append(salida["probabilidad_churn"])

    def registrar_error(self, tipo: str, detalle: str) -> None:
        with self.lock:
            self.errores += 1
        self.logger.info(json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "evento": "error", "tipo": tipo, "detalle": detalle[:300],
        }, ensure_ascii=False))

    def resumen(self, card: dict | None) -> dict:
        """Métricas operativas + negocio + drift sobre la ventana de predicciones."""
        with self.lock:
            entradas = list(self.entradas)
            probas = list(self.probas)
            lat = sorted(self.latencias_ms)
            niveles = dict(self.niveles)
            total, errores = self.total, self.errores

        out = {
            "uptime_s": round(time.time() - self.inicio, 1),
            "predicciones_totales": total,
            "errores_totales": errores,
            "distribucion_riesgo": niveles,
            "probabilidad_media": round(sum(probas) / len(probas), 4) if probas else None,
            "latencia_p50_ms": round(lat[len(lat) // 2], 2) if lat else None,
            "latencia_p95_ms": round(lat[int(len(lat) * 0.95) - 1], 2) if lat else None,
        }
        if card:
            out["modelo"] = {
                "version": card["version"],
                "algoritmo": card["algoritmo"],
                "entrenado_en": card["entrenado_en"],
                "umbral_decision": card["umbral_decision"],
                "metricas_offline": {k: card["metricas_test"][k] for k in ("roc_auc", "precision", "recall", "f1")},
            }
            if probas:
                df = pd.DataFrame(entradas)
                out["negocio"] = metricas_negocio(probas, df["cargo_mensual"], card["umbral_decision"])
            # Drift sólo con una muestra mínima para que el PSI sea estable
            if len(entradas) >= 200:
                out["drift"] = calcular_drift(pd.DataFrame(entradas), card["perfil_referencia"])
            else:
                out["drift"] = {"estado_global": "muestra_insuficiente", "minimo_requerido": 200, "actual": len(entradas)}
        return out


def leer_log(ruta: Path = config.PREDICTIONS_LOG, n: int = 20) -> list[dict]:
    """Últimos n eventos del log (para auditoría rápida)."""
    if not ruta.exists():
        return []
    lineas = ruta.read_text(encoding="utf-8").strip().splitlines()[-n:]
    return [json.loads(x) for x in lineas if x]
