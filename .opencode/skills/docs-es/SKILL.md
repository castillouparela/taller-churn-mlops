---
name: docs-es
description: Redacta documentación técnica en español clara y ejecutable: README con comandos copiables, docstrings breves y documentos de gobernanza. Úsala al documentar.
license: MIT
compatibility: opencode
metadata:
  origen: taller-churn-mlops
  inspirado_en: everything-claude-code (ECC)
---
# Skill: documentación en español (estilo ECC · doc-updater)

## Reglas
- Escribe para alguien que llega mañana: qué es, cómo instalar, cómo ejecutar, cómo verificar.
- Cada comando en un bloque copiable, separado por sistema operativo cuando difiera
  (Windows PowerShell / macOS / Linux).
- Incluye la **salida esperada** de los comandos clave.
- Docstrings de una línea en español; comentarios sólo donde el *porqué* no es obvio.
- Enlaza la trazabilidad: requisito (`FR-xxx`) → tarea (`T0xx`) → archivo → prueba.
- Incluye siempre la sección **Uso responsable** (sesgo, privacidad, decisiones automatizadas).
