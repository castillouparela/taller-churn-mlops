"""Preparación de datos: carga, validación de calidad, partición y preprocesamiento."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from churn import config


class DataQualityError(ValueError):
    """Error de calidad de datos que debe detener el pipeline."""


# Reglas de calidad mínimas (rango permitido por columna numérica)
RANGOS = {
    "antiguedad_meses": (0, 600),
    "cargo_mensual": (0, 1000),
    "reclamos_ult_3m": (0, 100),
    "uso_datos_gb": (0, 2000),
}
DOMINIOS = {
    "tipo_plan": config.PLANES,
    "metodo_pago": config.METODOS_PAGO,
    "renovo_contrato": config.RENOVACION,
}


def cargar_datos(ruta: Path = config.DATA_RAW) -> pd.DataFrame:
    """Lee el CSV y falla con un mensaje claro si no existe."""
    if not Path(ruta).exists():
        raise FileNotFoundError(f"No existe {ruta}. Ejecute: python -m churn.dataset")
    return pd.read_csv(ruta)


def validar_calidad(df: pd.DataFrame, con_target: bool = True) -> dict:
    """Valida esquema, nulos, rangos y dominios. Devuelve un resumen o lanza DataQualityError."""
    requeridas = config.FEATURES + ([config.TARGET] if con_target else [])
    faltantes = [c for c in requeridas if c not in df.columns]
    if faltantes:
        raise DataQualityError(f"Columnas faltantes: {faltantes}")

    errores = []
    nulos = df[requeridas].isna().sum()
    if nulos.any():
        errores.append(f"Nulos: {nulos[nulos > 0].to_dict()}")
    for col, (lo, hi) in RANGOS.items():
        fuera = int(((df[col] < lo) | (df[col] > hi)).sum())
        if fuera:
            errores.append(f"{col}: {fuera} valores fuera de [{lo}, {hi}]")
    for col, dominio in DOMINIOS.items():
        invalidos = sorted(set(df[col].dropna().unique()) - set(dominio))
        if invalidos:
            errores.append(f"{col}: valores no permitidos {invalidos}")
    if con_target and not set(df[config.TARGET].unique()) <= {0, 1}:
        errores.append("La variable objetivo debe ser binaria 0/1")
    if errores:
        raise DataQualityError(" | ".join(errores))

    return {
        "filas": len(df),
        "duplicados_id": int(df[config.ID_COL].duplicated().sum()) if config.ID_COL in df else 0,
        "tasa_churn": round(float(df[config.TARGET].mean()), 4) if con_target else None,
    }


def particionar(df: pd.DataFrame):
    """Partición estratificada y reproducible train/test."""
    X = df[config.FEATURES]
    y = df[config.TARGET]
    return train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.SEED, stratify=y
    )


def construir_preprocesador() -> ColumnTransformer:
    """Escala numéricas y codifica categóricas (ignora categorías nuevas en producción)."""
    return ColumnTransformer(
        [
            ("num", StandardScaler(), config.NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), config.CATEGORICAL_FEATURES),
        ]
    )


def perfil_referencia(df: pd.DataFrame) -> dict:
    """Guarda cuantiles y frecuencias de entrenamiento para detectar drift después."""
    perfil = {"numericas": {}, "categoricas": {}}
    for col in config.NUMERIC_FEATURES:
        # Deciles únicos: variables discretas (p. ej. reclamos) generan cortes repetidos
        cortes = sorted(set(df[col].quantile([i / 10 for i in range(1, 10)]).round(4).tolist()))
        bordes = [-np.inf, *cortes, np.inf]
        proporciones = (np.histogram(df[col], bins=bordes)[0] / len(df)).round(6).tolist()
        perfil["numericas"][col] = {
            "cortes": cortes, "proporciones": proporciones, "media": round(float(df[col].mean()), 4)
        }
    for col in config.CATEGORICAL_FEATURES:
        perfil["categoricas"][col] = df[col].value_counts(normalize=True).round(4).to_dict()
    return perfil
