---
name: api-security-review
description: Revisa y endurece APIs FastAPI de modelos: validación de entradas, manejo de errores, privacidad en logs y riesgos de uso indebido. Úsala al crear o revisar endpoints.
license: MIT
compatibility: opencode
metadata:
  origen: taller-churn-mlops
  inspirado_en: everything-claude-code (ECC)
---
# Skill: revisión de seguridad de la API (estilo ECC · security-review)

## Checklist obligatorio
- [ ] **Validación estricta** con Pydantic: tipos, rangos (`ge`/`le`), dominios (`Literal`), `extra="forbid"`.
- [ ] **Límites de tamaño**: lotes con `max_length`; strings con `max_length` y `pattern`.
- [ ] **Errores controlados**: 422 con detalle por campo, 503 si el modelo no está cargado,
      500 genérico sin *stack trace* al cliente (el detalle va al log).
- [ ] **Privacidad**: no registrar IDs ni datos personales en claro (hash); no aceptar datos sensibles
      (cédula, nombre, edad) en el contrato.
- [ ] **Sin secretos** en el código ni en el repositorio.
- [ ] **Dependencias** mínimas y conocidas.
- [ ] **Uso responsable**: la respuesta incluye un aviso de que es apoyo a la decisión y requiere revisión humana.

## Formato de salida de la revisión
Tabla: `Hallazgo | Severidad (alta/media/baja) | Archivo:línea | Corrección propuesta`.
