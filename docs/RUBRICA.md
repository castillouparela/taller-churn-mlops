# Rúbrica de evaluación (por pareja)

Puntaje: 1 = inicial · 2 = en desarrollo · 3 = logrado · 4 = destacado. **Aprobado: ≥ 12/20 y ningún criterio en 1.**

| Criterio | 1 · Inicial | 2 · En desarrollo | 3 · Logrado | 4 · Destacado | Pts |
|---|---|---|---|---|---|
| **1. Alineación negocio-ML** | Objetivo vago, sin KPI | KPI sin línea base ni meta; criterios técnicos sin justificar | Objetivo medible, KPIs con fórmula, criterios de éxito y umbral justificados con costos | Además, ROI y presupuesto conectados al umbral; revisión por pares incorporada | |
| **2. Calidad de la especificación** | Spec con tecnología, sin criterios | Historias sin escenarios Dado/Cuando/Entonces o SC no medibles | Spec sin solución técnica, FR verificables, SC medibles, casos límite; plan y tareas coherentes | Clarificaciones resueltas, checklist en verde, tareas trazadas a FR/SC | |
| **3. Calidad y pruebas del código** | No ejecuta | Ejecuta, sin pruebas o pruebas fallando | API con validación y manejo de errores; `pytest` en verde; README ejecutable | Pruebas de casos límite y privacidad; código comentado; converge = Converged | |
| **4. Trazabilidad MLOps** | Sin versión ni métricas | Versión o métricas, pero no ambas | `/health`, `/metrics`, logs JSONL, model card con versión y hash; drift simulado | Política de reentrenamiento y RACI escritas; decisión argumentada ante drift | |
| **5. Uso responsable de IA** | Sin consideración ética | Menciona riesgos genéricos | Atributo sensible excluido y auditado; IDs con hash; aviso de revisión humana | Analiza proxies de sesgo; revisa críticamente el código generado por IA | |
| | | | | **Total** | **/20** |

## Evidencias a mostrar en la demo final (6 min)
1. `business/ASUM-DM.md` con firma de revisión por pares.
2. `spec.md` (sin tecnología) → `plan.md` → `tasks.md`.
3. `pytest` en verde.
4. `POST /predict` válido y uno inválido (422).
5. `/dashboard` antes y después del escenario crisis.
6. Resultado de `/speckit.converge`.
