# Guion del facilitador · minuto a minuto

**Taller**: Integración de ASUM-DM, MLOps, Spec-Driven Development, skills ECC y modelos abiertos con OpenCode en VS Code
**Duración**: 180 minutos exactos · **Modalidad**: presencial · **Grupo ideal**: 12–24 personas en parejas
**Caso**: predicción de churn en telecomunicaciones

## Ajuste de tiempos (léelo antes)
La estructura original suma 220 min (15+20+25+30+35+45+30+20). Para respetar el máximo de 3 horas:
1. **La instalación se hace antes del taller** con `docs/CHECKLIST_PREVIO.md`; en sala sólo se **verifica** (10 min en vez de 25).
2. Se recortan 5 min a apertura, fundamentos, Bloque 1, Bloque 2 y cierre.
3. Bloques 3 (45 min) y 4 (30 min) conservan su tiempo completo: son el corazón práctico.

| Hora | Min | Bloque | Lámina |
|---|---|---|---|
| 0:00 | 10 | 1. Apertura y motivación | 1–4 |
| 0:10 | 15 | 2. Fundamentos rápidos | 5–10 |
| 0:25 | 10 | 3. Verificación de instalación | 11 |
| 0:35 | 25 | 4. Bloque 1 · Negocio con ASUM-DM | 12–13 |
| 1:00 | 30 | 5. Bloque 2 · SDD con Spec Kit | 14–16 |
| 1:30 | 45 | 6. Bloque 3 · OpenCode + ECC + modelo local | 17–19 |
| 2:15 | 30 | 7. Bloque 4 · MLOps mínimo viable | 20–22 |
| 2:45 | 15 | 8. Cierre, demo y evaluación | 23–25 |

## Preparación del facilitador (día anterior)
- [ ] Ejecutar `python tareas.py todo` y `pytest` en el **repo solución** (deben pasar 18 pruebas).
- [ ] Tener abiertas 3 ventanas: VS Code (repo alumno), VS Code (repo solución), navegador con `/docs` y `/dashboard`.
- [ ] `ollama run taller-coder "hola"` una vez para que el modelo quede cargado en memoria.
- [ ] USB / carpeta compartida con: instaladores, `ollama` + modelo exportado, wheels de Python (ver `docs/PLAN_B.md`).
- [ ] Imprimir la rúbrica (1 por pareja) y la tarjeta de prompts (`prompts/PROMPTS_OPENCODE.md`).
- [ ] Definir parejas mezclando perfiles (negocio + técnico) y una pareja "de rescate" con laptop potente.

**Regla didáctica del Bloque 3** (anúnciala y repítela): **Muestro → Ejecutan → Revisamos contra la spec → Convergemos.**

---

## 0:00–0:10 · Apertura y motivación (10 min)
| Min | Qué hace el facilitador | Qué hacen los asistentes | Lámina |
|---|---|---|---|
| 0:00–0:02 | Bienvenida. Pregunta a mano alzada: "¿Quién ha visto un modelo que nunca llegó a producción?" | Responden | 1 |
| 0:02–0:05 | Cuenta la historia: el modelo con AUC 0,92 que nadie usó porque predecía algo que el negocio no podía accionar, no tenía API y nadie vio que los datos cambiaron. Mensaje: **los proyectos fallan por desconexión, no por el algoritmo.** | Escuchan | 2 |
| 0:05–0:07 | Mapa del día: ASUM-DM → SDD → ECC → OpenCode → MLOps. Cada pieza conecta la anterior con la siguiente. | – | 3 |
| 0:07–0:10 | **Demo del resultado final** (repo solución, ya corriendo): `/docs` → un `POST /predict` → `/dashboard` → `specs/001-api-churn/checklists/requirements.md` (trazabilidad). "En 3 horas ustedes construyen esto." | Observan | 4 |

**Frase clave**: "Hoy no aprendemos un algoritmo nuevo; aprendemos a que un modelo sobreviva al lunes."

## 0:10–0:25 · Fundamentos rápidos (15 min)
| Min | Contenido | Lámina |
|---|---|---|
| 0:10–0:13 | **ASUM-DM** (IBM): 6 fases + gestión de proyecto. Diferencia con CRISP-DM: incluye despliegue y operación explícitos. | 5 |
| 0:13–0:16 | **MLOps**: ciclo de vida, despliegue, monitoreo, gobernanza, drift (de datos y de concepto), reentrenamiento, trazabilidad. | 6 |
| 0:16–0:19 | **SDD**: la especificación es el artefacto principal; el código es su consecuencia. Constitución → specify → clarify → plan → tasks → implement → converge. | 7 |
| 0:19–0:21 | **ECC / skills**: instrucciones reutilizables que el agente carga cuando aplican (ML, testing, seguridad, arquitectura, docs, revisión). | 8 |
| 0:21–0:23 | **OpenCode + Ollama**: agente open source, modelo local, sin tokens ni cuentas. Privacidad: el código no sale de la laptop. | 9 |
| 0:23–0:25 | Advertencia ética temprana: sesgo, privacidad, decisiones automatizadas. "Lo retomamos en cada bloque." | 10 |

**Pregunta de control** (0:24): "¿En qué fase de ASUM-DM se define el umbral de decisión?" → Evaluación, pero se acuerda con negocio desde el entendimiento del negocio.

## 0:25–0:35 · Verificación de instalación (10 min)
| Min | Acción |
|---|---|
| 0:25–0:27 | Todos abren VS Code en la carpeta `taller-churn-mlops` y la terminal integrada. Ejecutan `uv sync --extra dev` si aún no sincronizaron el entorno; no hace falta activarlo. |
| 0:27–0:31 | Ejecutan `uv run python scripts/smoke_test.py`. Levantan la mano verde (todo OK) o roja. |
| 0:31–0:33 | `opencode` en la terminal integrada → `/models` → seleccionar **Ollama (local) · taller-coder**. Escribir `Hola, responde en español en una línea.` |
| 0:33–0:35 | Triage: quien falle se empareja con alguien verde **ya**, y el asistente técnico lo atiende en paralelo (ver `docs/PLAN_B.md`). **No detener al grupo.** |

## 0:35–1:00 · Bloque 1 · Negocio con ASUM-DM (25 min)
| Min | Actividad |
|---|---|
| 0:35–0:38 | Explicar la plantilla `plantillas/ASUM-DM_plantilla.md`. Copiarla a `business/ASUM-DM.md`. |
| 0:38–0:50 | **Trabajo en parejas** (12 min): completar secciones 1, 2, 6 (objetivo, KPIs, problema de ML, unidad de análisis, criterios de éxito y umbral). Dato de apoyo en la pizarra: presupuesto USD 2.000, contacto USD 8, éxito 30 %. |
| 0:50–0:55 | Completar secciones 3, 7, 8 (datos, riesgos, despliegue). Opcional: prompt **P1.2** para riesgos. |
| 0:55–1:00 | **Revisión por pares cruzada**: cada pareja revisa el ASUM-DM de la pareja vecina con 3 preguntas: ¿el objetivo es medible? ¿el criterio de éxito justifica recall vs precisión con costos? ¿hay un riesgo de uso indebido con mitigación? Firman la casilla "Revisado por pares". |

**Debate de 1 min (si hay tiempo)**: "¿Por qué recall ≥ 0,70 y no 0,95?" → porque cada falso positivo consume presupuesto.
**Entregable**: `business/ASUM-DM.md` completo y revisado por pares. Referencia: el del repo solución.

## 1:00–1:30 · Bloque 2 · SDD con Spec Kit (30 min)
| Min | Actividad |
|---|---|
| 1:00–1:03 | Si no se hizo antes (debió hacerse con el checklist): `specify integration install opencode` dentro del repo; si su versión de Spec Kit no lo reconoce, `specify init --here --integration opencode`. Reiniciar OpenCode y mostrar `.opencode/commands/` y `.specify/`. Verificar que `/speckit.` autocompleta. |
| 1:03–1:07 | Facilitador ejecuta **P2.1** (`/speckit.constitution`). Asistentes repiten. Mostrar `.specify/memory/constitution.md`. |
| 1:07–1:14 | **P2.2** (`/speckit.specify`). Mientras genera: explicar historias, FR, SC. Abrir `specs/001-*/spec.md`. |
| 1:14–1:18 | **Ejercicio "solución prematura"**: prompt **P2.4**. Buscar en la spec palabras como FastAPI, scikit-learn, JSON, regresión. Reescribirlas como necesidad de negocio. Mostrar el contraejemplo de la lámina 15. |
| 1:18–1:21 | **P2.3** (`/speckit.clarify`): responder 2–3 preguntas en voz alta, decidir en grupo. |
| 1:21–1:26 | **P2.5** (`/speckit.plan`): ahora sí entra la tecnología. Verificar la tabla "Constitución" del plan. |
| 1:26–1:30 | **P2.6** (`/speckit.tasks`) + **P2.7** (`/speckit.checklist`). Revisar que cada tarea tenga archivo y FR. |

**Si el modelo local es lento**: el facilitador proyecta la generación y los asistentes copian los archivos de referencia (`specs/001-api-churn/` y `.specify/memory/constitution.md`) desde `referencia/`. Lo importante es **leerlos y criticarlos**, no esperar.

## 1:30–2:15 · Bloque 3 · Desarrollo con OpenCode + ECC + modelo local (45 min)
Regla: **Muestro (1 min) → Ejecutan (3–4 min) → Revisamos contra spec (1 min)**.

| Min | Paso | Prompt | Verificación |
|---|---|---|---|
| 1:30–1:33 | Contexto: `ls .opencode/skills`, abrir una SKILL.md. Explicar que OpenCode las descubre y carga con la herramienta `skill`. | P3.0 | El agente lista el orden de trabajo |
| 1:33–1:39 | a. Dataset sintético | P3.a | `python -m churn.dataset` → 5000 filas, churn ≈ 25 % |
| 1:39–1:44 | b. Preparación de datos | P3.b | `python -c "from churn.features import *"` |
| 1:44–1:50 | c+d. Entrenamiento y evaluación | P3.c, P3.d | `python -m churn.train` → AUC ≥ 0,75 |
| 1:50–1:53 | e. Serialización y model card | P3.e | abrir `models/model_card.json` |
| 1:53–2:01 | f. API FastAPI | P3.f | `uv run uvicorn churn.api:app --reload` → `/docs` → probar cargo negativo (422) |
| 2:01–2:07 | g. Pruebas pytest | P3.g | `pytest` en verde |
| 2:07–2:09 | h. README | P3.h | leer sección de instalación |
| 2:09–2:15 | **Revisión y convergencia**: P3.r (skill spec-code-review) y `/speckit.converge`. Discutir 1–2 brechas reales del grupo. | P3.r, P3.c2 | Matriz requisito→código→prueba |

**Puntos de rescate**: si una pareja se atrasa más de un paso, copia el archivo equivalente desde `referencia/src/churn/` y sigue. Mensaje: "El objetivo es el método, no teclear".
**Observa y comenta en voz alta** errores típicos de modelos pequeños: columnas inventadas, olvidar `extra="forbid"`, umbral calibrado en test (fuga), archivos truncados.

## 2:15–2:45 · Bloque 4 · MLOps mínimo viable (30 min)
| Min | Actividad | Prompt / comando |
|---|---|---|
| 2:15–2:19 | `/health` y versión del modelo (mostrar `model_card.json`: versión, hash del dataset, `aprobado_para_despliegue`) | P4.1 |
| 2:19–2:24 | Logging estructurado: abrir `logs/predicciones.jsonl`; mostrar que el ID va con hash | P4.2 |
| 2:24–2:29 | `/metrics` y métricas de negocio; abrir `/dashboard`; `python scripts/simular_trafico.py` | P4.3 |
| 2:29–2:37 | **Simulación de drift** (momento "wow"): `python -m churn.drift --escenario crisis` → tabla base vs crisis. Luego `python scripts/simular_trafico.py --escenario crisis --n 500` y ver el dashboard pasar a **crítico**. Preguntar: "¿Qué decisión toman? ¿Quién la aprueba?" | P4.4 |
| 2:37–2:45 | Gobernanza: leer `docs/GOBERNANZA.md` (RACI, evidencias, versionado). Cada pareja escribe en 3 líneas su política de reentrenamiento. | P4.5 |

**Lectura de la tabla de drift** (para explicar): la tasa real de churn se duplica (25 % → 56 %), el ROC-AUC baja (0,80 → 0,77), el PSI supera 0,25 y los ingresos en riesgo se duplican, pero el presupuesto sólo alcanza para 250 contactos. **El modelo no "se rompe" con un error: se degrada en silencio.**

## 2:45–3:00 · Cierre y evaluación (15 min)
| Min | Actividad |
|---|---|
| 2:45–2:51 | **Demo final** de una pareja voluntaria (o del facilitador): negocio → spec → código → API → prueba → métricas → drift, en 6 minutos. |
| 2:51–2:56 | (Lámina 24) Autoevaluación con la rúbrica (`docs/RUBRICA.md`), 5 criterios. Las parejas se puntúan y comparan con la pareja vecina. |
| 2:56–2:58 | Advertencia ética final (lámina 25) y reto para casa (`docs/RETO_CASA.md`). |
| 2:58–3:00 | Encuesta de salida de 2 preguntas: "¿Qué usarás el lunes?" y "¿Qué quitarías?" |

---

## Gestión del tiempo
- Lleva un temporizador visible. Si vas 5 min atrasado al inicio del Bloque 3, **salta P3.h (README)** y usa el de referencia.
- Si vas 10 min atrasado, en el Bloque 4 haz P4.1–P4.3 sólo como demo del facilitador y deja que todos ejecuten el drift.
- Nunca recortes la simulación de drift ni la advertencia ética.

## Preguntas frecuentes de los asistentes
- **"¿Por qué no usar GPT/Claude?"** → El taller demuestra el método sin tokens ni cuentas; con un modelo más grande el método es el mismo y el resultado mejora.
- **"El modelo local escribe código malo."** → Precisamente por eso existen la spec, las pruebas y la convergencia: la calidad la garantiza el proceso, no el modelo.
- **"¿Por qué no MLflow?"** → Se puede agregar luego; el model card JSON + logs JSONL enseñan los mismos conceptos sin infraestructura.
- **"¿Spec Kit funciona sin internet?"** → El scaffolding usa recursos incluidos; la instalación sí requiere red (ver Plan B).
