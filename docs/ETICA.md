# Advertencia ética y uso responsable

> **Este modelo es una herramienta de apoyo a la decisión. No decide sobre personas.**

## Sesgo
- El modelo **no** usa `rango_edad`, pero variables como `tipo_plan` o `metodo_pago` pueden actuar como **proxies** de edad,
  ingreso o zona geográfica. En el dataset del taller los jóvenes son más prepago a propósito, para que lo vean.
- Cada entrenamiento reporta tasa de selección y recall por grupo y el **ratio de impacto dispar** (regla de 4/5: ≥ 0,80).
- Un ratio bajo no se "arregla" ocultando la variable: se analiza la causa, se consulta a Cumplimiento y se documenta.

## Privacidad
- La API **rechaza** campos no previstos (p. ej., documento de identidad o nombre): minimización de datos.
- Los logs guardan un **hash** del ID, nunca el ID en claro.
- Los datos del taller son **sintéticos**. Con datos reales aplique la normativa vigente de protección de datos
  (en Colombia, Ley 1581 de 2012 y sus decretos) y las políticas internas de la organización.
- Con OpenCode + Ollama el código y los datos **no salen de la laptop**: no se envían a proveedores externos.

## Decisiones automatizadas
- Usos permitidos: priorizar a quién **ofrecer** beneficios de retención.
- Usos prohibidos: negar servicios, subir precios, empeorar condiciones o perfilar a personas para fines distintos.
- Toda acción con efecto significativo sobre un cliente requiere **revisión humana**; cada respuesta de la API lo recuerda.
- El cliente debe poder conocer, rectificar y oponerse al tratamiento de sus datos.

## IA generativa en el desarrollo
- El código generado por el modelo local **se revisa** contra la especificación y se valida con pruebas antes de aceptarlo.
- No pegue datos reales de clientes en los prompts, ni siquiera con modelos locales, salvo autorización.
- Registre qué partes fueron generadas con IA en la descripción de cada commit o PR.
