"""API de churn: /predict, /predict/lote, /health, /metrics y /dashboard.

Ejecutar:
    uvicorn churn.api:app --reload --port 8000
Documentación interactiva: http://localhost:8000/docs
"""
from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from churn import config
from churn.monitoring import Monitor
from churn.predict import ModeloNoDisponible, cargar_modelo, puntuar

log = logging.getLogger("churn.api")
estado: dict = {"bundle": None, "error_carga": None}
monitor = Monitor()


# ---------- Contratos de entrada/salida (validación estricta) ----------
class Cliente(BaseModel):
    """Datos de un cliente-mes. Rechaza campos extra para evitar datos no autorizados."""

    model_config = ConfigDict(extra="forbid", json_schema_extra={"example": {
        "id_cliente": "C4200001", "antiguedad_meses": 6, "tipo_plan": "prepago",
        "cargo_mensual": 45.5, "reclamos_ult_3m": 3, "uso_datos_gb": 2.1,
        "metodo_pago": "efectivo", "renovo_contrato": "no"}})

    id_cliente: str | None = Field(None, max_length=40, pattern=r"^[A-Za-z0-9_-]+$")
    antiguedad_meses: int = Field(..., ge=0, le=600, description="Meses como cliente")
    tipo_plan: Literal["prepago", "pospago_basico", "pospago_premium"]
    cargo_mensual: float = Field(..., ge=0, le=1000, description="Facturación mensual (USD)")
    reclamos_ult_3m: int = Field(..., ge=0, le=100)
    uso_datos_gb: float = Field(..., ge=0, le=2000)
    metodo_pago: Literal["tarjeta_credito", "debito_automatico", "efectivo", "transferencia"]
    renovo_contrato: Literal["si", "no"]


class Prediccion(BaseModel):
    id_cliente: str | None
    probabilidad_churn: float
    nivel_riesgo: Literal["alto", "medio", "bajo"]
    recomendacion: str
    version_modelo: str
    aviso: str = "Apoyo a la decisión: requiere revisión humana antes de acciones que afecten al cliente."


class Lote(BaseModel):
    clientes: list[Cliente] = Field(..., min_length=1, max_length=1000)


# ---------- Ciclo de vida ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        estado["bundle"] = cargar_modelo()
    except ModeloNoDisponible as exc:  # la API arranca, pero /health lo reporta
        estado["error_carga"] = str(exc)
        log.error(exc)
    yield


app = FastAPI(
    title="API de Churn Telco",
    version=config.MODEL_VERSION,
    description="Probabilidad de abandono, nivel de riesgo y acción recomendada.",
    lifespan=lifespan,
)


def _bundle() -> dict:
    if estado["bundle"] is None:
        raise HTTPException(status_code=503, detail=f"Modelo no disponible: {estado['error_carga']}")
    return estado["bundle"]


# ---------- Manejo de errores ----------
@app.exception_handler(RequestValidationError)
async def error_validacion(request: Request, exc: RequestValidationError):
    errores = [
        {"campo": ".".join(str(x) for x in e["loc"][1:]) or "body", "mensaje": e["msg"]}
        for e in exc.errors()
    ]
    monitor.registrar_error("validacion", str(errores))
    return JSONResponse(status_code=422, content={"error": "Entrada inválida", "detalle": errores})


@app.exception_handler(Exception)
async def error_inesperado(request: Request, exc: Exception):
    monitor.registrar_error("interno", repr(exc))
    log.exception("Error no controlado")
    return JSONResponse(status_code=500, content={"error": "Error interno. Revise logs/predicciones.jsonl"})


# ---------- Endpoints ----------
@app.get("/health")
def health():
    ok = estado["bundle"] is not None
    card = estado["bundle"]["card"] if ok else {}
    return {
        "status": "ok" if ok else "degradado",
        "modelo_cargado": ok,
        "version_modelo": card.get("version"),
        "aprobado_para_despliegue": card.get("aprobado_para_despliegue"),
        "error": estado["error_carga"],
    }


@app.post("/predict", response_model=Prediccion)
def predict(cliente: Cliente):
    bundle = _bundle()
    inicio = time.perf_counter()
    entrada = cliente.model_dump()
    resultado = puntuar([entrada], bundle)[0]
    monitor.registrar(entrada, resultado, (time.perf_counter() - inicio) * 1000)
    return {"id_cliente": cliente.id_cliente, **resultado}


@app.post("/predict/lote", response_model=list[Prediccion])
def predict_lote(lote: Lote):
    bundle = _bundle()
    inicio = time.perf_counter()
    entradas = [c.model_dump() for c in lote.clientes]
    resultados = puntuar(entradas, bundle)
    lat = (time.perf_counter() - inicio) * 1000 / len(entradas)
    for e, r in zip(entradas, resultados):
        monitor.registrar(e, r, lat)
    return [{"id_cliente": e["id_cliente"], **r} for e, r in zip(entradas, resultados)]


@app.get("/metrics")
def metrics():
    card = estado["bundle"]["card"] if estado["bundle"] else None
    return monitor.resumen(card)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    ruta = config.ROOT / "dashboard" / "index.html"
    if not ruta.exists():
        raise HTTPException(status_code=404, detail="dashboard/index.html no encontrado")
    return ruta.read_text(encoding="utf-8")
