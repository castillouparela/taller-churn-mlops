---
name: python-testing
description: Escribe pruebas pytest pequeñas, deterministas y legibles (TDD) para datos, modelo y API FastAPI. Úsala al crear o revisar tests.
license: MIT
compatibility: opencode
metadata:
  origen: taller-churn-mlops
  inspirado_en: everything-claude-code (ECC)
---
# Skill: pruebas con pytest (estilo ECC · tdd-workflow / python-testing)

## Flujo
1. **Rojo**: escribe la prueba que expresa un criterio de aceptación (cita `SC-xxx` o `FR-xxx`).
2. **Verde**: implementa lo mínimo para que pase.
3. **Refactor**: limpia sin romper pruebas.

## Reglas
- Una idea por prueba; nombre descriptivo en español (`test_rechaza_valores_fuera_de_rango`).
- Usa `fastapi.testclient.TestClient` dentro de `with` para que se ejecute el `lifespan`.
- Fixtures en `tests/conftest.py`; nada de rutas absolutas ni dependencias de red.
- Cubre: camino feliz, entradas inválidas (422), campos extra, campo faltante, modelo ausente (503),
  criterios de negocio (recall, precision, AUC) y drift (estable vs crítico).
- Las pruebas deben correr en < 30 s en una laptop.

## Plantilla
```python
def test_<comportamiento>(client, cliente_valido):
    # Arrange
    datos = {**cliente_valido, "cargo_mensual": -10}
    # Act
    r = client.post("/predict", json=datos)
    # Assert
    assert r.status_code == 422
```
