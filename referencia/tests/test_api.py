"""Pruebas de la API: contrato, validación de entradas, errores y MLOps."""


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["version_modelo"]


def test_predict_ok(client, cliente_valido):
    r = client.post("/predict", json=cliente_valido)
    assert r.status_code == 200
    body = r.json()
    assert 0 <= body["probabilidad_churn"] <= 1
    assert body["nivel_riesgo"] in {"alto", "medio", "bajo"}
    assert body["recomendacion"]
    assert body["version_modelo"]


def test_cliente_riesgoso_vs_fiel(client, cliente_valido):
    fiel = {**cliente_valido, "antiguedad_meses": 80, "tipo_plan": "pospago_premium",
            "reclamos_ult_3m": 0, "metodo_pago": "debito_automatico", "renovo_contrato": "si",
            "uso_datos_gb": 15}
    p_riesgo = client.post("/predict", json=cliente_valido).json()["probabilidad_churn"]
    p_fiel = client.post("/predict", json=fiel).json()["probabilidad_churn"]
    assert p_riesgo > p_fiel


def test_rechaza_valores_fuera_de_rango(client, cliente_valido):
    r = client.post("/predict", json={**cliente_valido, "cargo_mensual": -10})
    assert r.status_code == 422
    assert r.json()["error"] == "Entrada inválida"
    assert r.json()["detalle"][0]["campo"] == "cargo_mensual"


def test_rechaza_categoria_invalida_y_campos_extra(client, cliente_valido):
    assert client.post("/predict", json={**cliente_valido, "tipo_plan": "gratis"}).status_code == 422
    assert client.post("/predict", json={**cliente_valido, "cedula": "123"}).status_code == 422


def test_rechaza_campo_faltante(client, cliente_valido):
    datos = dict(cliente_valido)
    datos.pop("antiguedad_meses")
    assert client.post("/predict", json=datos).status_code == 422


def test_lote(client, cliente_valido):
    r = client.post("/predict/lote", json={"clientes": [cliente_valido] * 3})
    assert r.status_code == 200 and len(r.json()) == 3
    assert client.post("/predict/lote", json={"clientes": []}).status_code == 422


def test_metrics_reporta_operacion_y_negocio(client, cliente_valido):
    client.post("/predict", json=cliente_valido)
    m = client.get("/metrics").json()
    assert m["predicciones_totales"] >= 1
    assert m["modelo"]["version"]
    assert "ingresos_mensuales_en_riesgo" in m["negocio"]
    assert "drift" in m


def test_log_no_guarda_id_en_claro(client, cliente_valido):
    from churn.monitoring import leer_log
    client.post("/predict", json=cliente_valido)
    ultimo = [e for e in leer_log() if e["evento"] == "prediccion"][-1]
    assert "id_cliente" not in ultimo
    assert ultimo["id_cliente_hash"] != cliente_valido["id_cliente"]
