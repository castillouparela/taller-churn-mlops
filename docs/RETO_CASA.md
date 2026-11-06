# Reto opcional para casa: adapta el pipeline a otro caso

Elige **uno**. Reutiliza el mismo método: ASUM-DM → constitución → spec → plan → tareas → OpenCode → converge → MLOps.

| Caso | Unidad de análisis | Objetivo | Variables sugeridas | Métrica clave | Riesgo ético principal |
|---|---|---|---|---|---|
| **Fraude en pagos** | Transacción | Bloquear o revisar transacciones fraudulentas | monto, hora, país, canal, intentos fallidos, antigüedad de la tarjeta | Recall alto con tasa de falsos positivos acotada | Bloquear injustamente a grupos (país, zona) |
| **Quiebre de inventario** | SKU-tienda-semana | Predecir quiebre de stock | ventas 4 semanas, stock, lead time, promoción, estacionalidad | Recall de quiebres, costo de sobrestock | Bajo; cuidado con decisiones de surtido por zona |
| **Deserción estudiantil** | Estudiante-semestre | Acompañar a quien está en riesgo de desertar | promedio, asistencia, materias reprobadas, créditos, beca, trabajo | Recall con capacidad de tutores | **Alto**: estigmatización; nunca para excluir |

## Pasos (≈ 3 horas)
1. Copia el repo y renombra el paquete (`src/churn` → `src/<caso>`).
2. Reescribe `business/ASUM-DM.md` con la plantilla.
3. `/speckit.constitution` (reutiliza principios) → `/speckit.specify` con tu nueva historia.
4. Adapta `config.py` y `dataset.py` (escenario base y uno con drift).
5. Usa los prompts del Bloque 3 cambiando nombres de columnas.
6. Ajusta métricas de negocio en `evaluate.py` (costo de revisar vs costo de no detectar).
7. Entrega: repo + demo de 5 minutos + autoevaluación con `docs/RUBRICA.md`.
