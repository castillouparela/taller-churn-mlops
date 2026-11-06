"""Pruebas del dataset sintético: determinismo, esquema y calidad."""
import pandas as pd
import pytest

from churn import config
from churn.dataset import generar
from churn.features import DataQualityError, validar_calidad


def test_generacion_determinista():
    # Misma semilla => mismo dataset (reproducibilidad)
    pd.testing.assert_frame_equal(generar(n=300), generar(n=300))


def test_esquema_y_tasa_churn():
    df = generar()
    assert set(config.FEATURES + [config.TARGET, config.SENSITIVE_COL]) <= set(df.columns)
    assert 0.15 < df[config.TARGET].mean() < 0.40  # tasa plausible en telco


def test_validacion_detecta_errores():
    df = generar(n=100)
    df.loc[0, "cargo_mensual"] = -5
    df.loc[1, "tipo_plan"] = "ilimitado"
    with pytest.raises(DataQualityError, match="cargo_mensual"):
        validar_calidad(df)


def test_escenario_crisis_cambia_distribucion():
    base, crisis = generar(), generar(seed=config.SEED + 1, escenario="crisis")
    assert crisis["cargo_mensual"].mean() > base["cargo_mensual"].mean() + 5
    assert crisis["reclamos_ult_3m"].mean() > 2 * base["reclamos_ult_3m"].mean()
