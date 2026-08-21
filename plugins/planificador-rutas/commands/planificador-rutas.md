---
description: Arranca la entrevista para planificar una ruta por carretera
argument-hint: [origen] [lugares] [dias]
---

Ejecuta la rutina del skill `planificador-rutas`. Lee su SKILL.md antes de
empezar y sigue el guion de `references/entrevista.md`.

Argumentos recibidos: $ARGUMENTS

## No arranques a armar el itinerario

Primero la entrevista, y de a poco: preguntas cortas, no un cuestionario de
veinte puntos. Si la interfaz tiene botones de seleccion, usalos, porque el
usuario suele responder desde el celular.

Aprovecha lo que ya venga en los argumentos y pregunta solo lo que falte. Las
siete sin las cuales el plan no se puede calcular:

- Origen y destino final
- Lista de lugares por visitar
- Dias disponibles, y si son corridos o habiles
- Ventanas horarias de visita
- Cuanto quiere estar en cada lugar, y el minimo aceptable
- Ciudad base, si la hay
- Si hay paradas que no se pueden mover

No inventes lo que no te dijo: un supuesto silencioso es la causa habitual de
un plan inservible.

## Verifica que quepa antes de ordenar nada

Con la aritmetica de `references/planificacion.md`. Lo que fija cuantas
paradas caben por dia son las ventanas horarias, no la distancia. Si no cabe,
dilo de una vez y ofrece las palancas: mas dias, menos lugares, menos tiempo
por parada. Descubrirlo al final obliga a rehacer todo.

## Genera y revisa

1. Escribe `plan.json` segun `references/formato-plan.md`.
2. `scripts/generar_documento.py plan.json salida.html`
3. `scripts/html_a_pdf.py salida.html salida.pdf`
4. Rasteriza alguna pagina del PDF y miralo antes de entregar.
5. Entrega los dos archivos.

El documento se lee sobre todo en el celular, muchas veces en visores que no
ejecutan JavaScript: por eso el HTML es estatico.
