"""Entrenamiento del baseline, evaluación y serialización con trazabilidad.

Uso:
    python -m churn.train                       # Regresión Logística (default)
    python -m churn.train --algoritmo rf        # Random Forest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone

import joblib
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline

from churn import config
from churn.evaluate import (
    cumple_criterios,
    elegir_umbral,
    metricas_equidad,
    metricas_negocio,
    metricas_tecnicas,
)
from churn.features import (
    cargar_datos,
    construir_preprocesador,
    particionar,
    perfil_referencia,
    validar_calidad,
)


def construir_modelo(algoritmo: str = "logreg") -> Pipeline:
    """Pipeline preprocesamiento + clasificador (class_weight balanceado)."""
    if algoritmo == "logreg":
        clf = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=config.SEED)
    elif algoritmo == "rf":
        clf = RandomForestClassifier(
            n_estimators=200, max_depth=8, min_samples_leaf=20,
            class_weight="balanced", random_state=config.SEED, n_jobs=-1,
        )
    else:
        raise ValueError("algoritmo debe ser 'logreg' o 'rf'")
    return Pipeline([("prep", construir_preprocesador()), ("clf", clf)])


def hash_archivo(ruta) -> str:
    """Huella SHA-256 del dataset para trazabilidad de datos."""
    return hashlib.sha256(open(ruta, "rb").read()).hexdigest()[:16]


def entrenar(algoritmo: str = "logreg") -> dict:
    df = cargar_datos()
    calidad = validar_calidad(df)
    X_train, X_test, y_train, y_test = particionar(df)

    modelo = construir_modelo(algoritmo)
    # El umbral se calibra con validación cruzada en train (nunca con test)
    proba_cv = cross_val_predict(modelo, X_train, y_train, cv=5, method="predict_proba")[:, 1]
    umbral = elegir_umbral(y_train, proba_cv)

    modelo.fit(X_train, y_train)
    proba_test = modelo.predict_proba(X_test)[:, 1]

    tecnicas = metricas_tecnicas(y_test, proba_test, umbral)
    negocio = metricas_negocio(proba_test, X_test["cargo_mensual"], umbral, y_test)
    equidad = metricas_equidad(
        y_test, proba_test, df.loc[X_test.index, config.SENSITIVE_COL], umbral
    )
    criterios = cumple_criterios(tecnicas)

    card = {
        "modelo": "churn-telco",
        "version": config.MODEL_VERSION,
        "algoritmo": algoritmo,
        "entrenado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "dataset": {"ruta": str(config.DATA_RAW.relative_to(config.ROOT)), "sha256": hash_archivo(config.DATA_RAW), **calidad},
        "features": config.FEATURES,
        "atributo_sensible_excluido": config.SENSITIVE_COL,
        "umbral_decision": umbral,
        "umbral_riesgo_alto": max(config.UMBRAL_RIESGO_ALTO, umbral),
        "metricas_test": tecnicas,
        "metricas_negocio_test": negocio,
        "equidad_test": equidad,
        "criterios_exito": criterios,
        "aprobado_para_despliegue": all(criterios.values()),
        "entorno": {"python": platform.python_version(), "sklearn": sklearn.__version__},
        "perfil_referencia": perfil_referencia(X_train),
    }

    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": modelo, "card": card}, config.MODEL_PATH)
    config.MODEL_CARD_PATH.write_text(json.dumps(card, indent=2, ensure_ascii=False), encoding="utf-8")
    config.METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    config.METRICS_PATH.write_text(
        json.dumps({"tecnicas": tecnicas, "negocio": negocio, "equidad": equidad, "criterios": criterios},
                   indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return card


def main() -> None:
    parser = argparse.ArgumentParser(description="Entrena el modelo de churn")
    parser.add_argument("--algoritmo", default="logreg", choices=["logreg", "rf"])
    args = parser.parse_args()
    card = entrenar(args.algoritmo)
    m = card["metricas_test"]
    print(f"[ok] modelo v{card['version']} ({card['algoritmo']}) umbral={card['umbral_decision']}")
    print(f"     ROC-AUC={m['roc_auc']} precision={m['precision']} recall={m['recall']} F1={m['f1']}")
    print(f"     matriz={m['matriz_confusion']}")
    print(f"     criterios={card['criterios_exito']} -> aprobado={card['aprobado_para_despliegue']}")
    print(f"     impacto dispar por edad={card['equidad_test']['ratio_impacto_dispar']}")


if __name__ == "__main__":
    main()
