# Atajos para macOS/Linux. En Windows use: python tareas.py <tarea>
.PHONY: datos entrenar entrenar-rf probar api trafico drift smoke todo limpiar alumno
datos:       ; python tareas.py datos
entrenar:    ; python tareas.py entrenar
entrenar-rf: ; python tareas.py entrenar-rf
probar:      ; python tareas.py probar
api:         ; python tareas.py api
trafico:     ; python tareas.py trafico
drift:       ; python tareas.py drift
smoke:       ; python tareas.py smoke
todo:        ; python tareas.py todo
limpiar:     ; python tareas.py limpiar
alumno:      ; python tareas.py alumno
