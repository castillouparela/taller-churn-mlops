"""Fixtures compartidas: garantizan datos y modelo antes de probar."""
import pytest
from fastapi.testclient import TestClient

from churn import config


@pytest.fixture(scope="session", autouse=True)
def artefactos():
    # Si faltan datos o modelo, se generan de forma determinista
    if not config.DATA_RAW.exists():
        from churn.dataset import generar
        config.DATA_RAW.parent.mkdir(parents=True, exist_ok=True)
        generar().to_csv(config.DATA_RAW, index=False)
    if not config.MODEL_PATH.exists():
        from churn.train import entrenar
        entrenar()


@pytest.fixture(scope="session")
def client(artefactos):
    from churn.api import app
    with TestClient(app) as c:
        yield c


@pytest.fixture
def cliente_valido():
    return {
        "id_cliente": "C4200001", "antiguedad_meses": 6, "tipo_plan": "prepago",
        "cargo_mensual": 45.5, "reclamos_ult_3m": 3, "uso_datos_gb": 2.1,
        "metodo_pago": "efectivo", "renovo_contrato": "no",
    }
