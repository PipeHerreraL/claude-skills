---
name: planificador-rutas
description: Planifica rutas de viaje por carretera entre varios municipios o ciudades mediante una entrevista guiada, y entrega el itinerario como documento HTML estático más PDF imprimible con mapa del circuito, perfil de altitudes y horarios día por día. Úsala SIEMPRE que alguien pida planear una ruta, un recorrido, una gira o un itinerario que toque varios pueblos, municipios, ciudades o sitios, o que mencione ventanas de horario para visitar, tiempo máximo por parada, días disponibles, salida desde una ciudad base o entrega del plan en HTML/PDF — aunque no nombre la skill ni pida explícitamente un documento. También aplica cuando pidan ajustar, recortar o rebalancear un itinerario que ya existe, o llevar un recorrido a Waze o Google Maps.
---

# Planificador de rutas por municipios

Convierte una necesidad de viaje en un itinerario factible y en un documento entregable.
El valor está en dos cosas que se hacen mal si se improvisan:

1. **Detectar temprano si el viaje cabe.** Las ventanas horarias, no la distancia, son
   las que fijan cuántas paradas caben por día. Descubrirlo al final obliga a rehacer todo.
2. **Entregar algo que abra en cualquier parte.** El documento se lee sobre todo en el
   celular, muchas veces desde un visor que no ejecuta JavaScript.

## Flujo

1. **Entrevista** al usuario con el guion de `references/entrevista.md`. No inventes lo
   que no te dijo: los supuestos silenciosos son la causa habitual de un plan inservible.
2. **Verifica la capacidad** antes de ordenar nada, con la aritmética de
   `references/planificacion.md`. Si no cabe, dilo de una vez y ofrece las palancas.
3. **Arma el itinerario** agrupando por cercanía y respetando las ventanas.
4. **Escribe `plan.json`** siguiendo `references/formato-plan.md`.
5. **Genera el documento**: `python3 scripts/generar_documento.py plan.json salida.html`
   y luego `python3 scripts/html_a_pdf.py salida.html salida.pdf`.
6. **Revisa el resultado** rasterizando alguna página del PDF antes de entregarlo, y
   entrega ambos archivos con la herramienta de presentación de archivos que tengas.

## La entrevista

Pregunta de a poco, no en un cuestionario de veinte puntos. Si estás en una interfaz con
botones de selección, úsalos: el usuario suele responder desde el celular.

Las siete que nunca puedes saltarte, porque sin ellas el plan no se puede calcular:

- Origen y destino final del viaje
- Lista de lugares por visitar
- Días disponibles, y si son corridos o hábiles
- Ventanas horarias en las que puede visitar
- Cuánto quiere estar en cada lugar, y cuál es el mínimo aceptable
- Medio de transporte
- Si puede trasladarse la tarde anterior y si puede regresar al día siguiente

El resto de preguntas, incluidas las condicionales que se disparan según las respuestas
(no conducir de noche, temporada de lluvias, ferias con fecha fija, alojamiento escaso),
está en `references/entrevista.md`. Léelo antes de empezar a preguntar.

Cuando la conversación ya trae parte de la información, no la vuelvas a pedir: resume lo
que entendiste, pregunta solo los huecos y confirma antes de calcular.

Lo mismo vale para lo que tengas recordado de este usuario de conversaciones anteriores.
Reutilizarlo está bien y ahorra preguntas, pero enúncialo antes de usarlo: "voy con lo que
ya tengo — origen, ventanas y transporte, ¿sigue igual?". Un dato de otro viaje produce un
plan que se ve correcto y no lo es, y el usuario no tiene cómo notarlo.

## La regla que más se olvida

Una ventana de la tarde de tres horas **no admite dos visitas de 90 minutos**: 90 + traslado
+ 90 se pasa del cierre. Una mañana de cuatro horas sí admite dos si los pueblos quedan a
menos de una hora. Ese detalle cambia el número de días del viaje, así que calcúlalo antes
de proponer cualquier orden de visita, con el procedimiento de `references/planificacion.md`.

Si los lugares no caben en los días disponibles, no recortes por tu cuenta: presenta las
palancas (bajar minutos por parada, agregar un día de traslado, sacar lugares de la lista)
con el costo de cada una, y deja que el usuario escoja.

## El documento

`scripts/generar_documento.py` produce **HTML estático sin una sola línea de JavaScript**.
Esto no es una preferencia estética:

- Safari en iOS no soporta variables CSS en atributos de presentación de SVG
  (`fill="var(--x)"` sale sin color), así que el generador escribe colores literales.
- Los visores de archivos de iOS y de muchos clientes de correo no ejecutan JavaScript,
  así que los gráficos van dibujados dentro del archivo y los filtros por día funcionan
  con CSS puro.
- Cada gráfico se genera dos veces, en versión móvil y de escritorio, y se muestra una u
  otra por consulta de medios. El PDF siempre usa la de escritorio.

El documento incluye portada con cifras, banda de ventanas horarias, mapa del circuito con
paradas numeradas, perfil de altitudes, esquema de traslado y regreso, itinerario día por
día con los minutos reales de cada parada, sección **Navegar con Waze** y bloque de avisos.

## Navegar con Waze

Si el usuario pide "exportar la ruta a Waze", dile de una vez que no se puede cargar
completa: Waze solo admite **una parada por ruta** y sus enlaces profundos aceptan un único
destino, y no importa GPX ni KML. Lo que sí se puede, y el generador arma solo a partir de
`dias` y `lugares`:

- **Un enlace de Waze por parada**, en orden de visita y agrupado por día, más uno final de
  regreso al `origen`. Al terminar en una parada, el usuario toca la siguiente y Waze
  navega desde donde esté. Son enlaces `https://www.waze.com/ul?ll=lat,lon&navigate=yes`,
  que funcionan en el HTML y también en el PDF.
- **Un enlace de Google Maps por día** con todas sus paradas. Google admite hasta 9
  paradas intermedias en la app, pero solo 3 si el enlace se abre en el navegador del
  celular; el generador parte en varios enlaces los días que pasan de 10 paradas.

Los enlaces apuntan a las coordenadas de `lugares`, normalmente el centro de la cabecera.
Si el usuario necesita llegar a una dirección exacta (un juzgado, una alcaldía, una
bodega), usa las coordenadas de ese sitio y no las del pueblo. La sección sale por
defecto; `"navegar": false` la quita. Los campos para ajustarla están en
`references/formato-plan.md`.

Los scripts colocan solos las etiquetas del mapa evitando choques y separan los marcadores
que quedan demasiado juntos. No hace falta ajustar coordenadas a mano.

## Coordenadas y tiempos

Cada lugar necesita longitud y latitud. **La altitud es opcional**: solo alimenta el perfil
de altitudes, que tiene sentido en ruta de montaña y ninguno en terreno plano. Pregúntale
al usuario si lo quiere antes de ponerte a buscar altitudes cabecera por cabecera; si dice
que no, `"perfil": false` y listo. Para Cundinamarca y el eje cafetero ya están verificados en
`references/datos-cundinamarca.md`. Para otras regiones, búscalos y
advierte al usuario que los tiempos de recorrido son estimados.

Los tiempos de manejo en vía de montaña salen a 30–45 km/h promedio, no a la velocidad que
sugiere la distancia en línea recta. Un tramo de 15 km entre dos cabeceras vecinas puede
tomar 40 minutos.

## Archivos

- `references/entrevista.md` — guion completo, con las preguntas condicionales
- `references/planificacion.md` — aritmética de capacidad, agrupación y reglas de armado
- `references/formato-plan.md` — estructura de `plan.json` campo por campo
- `references/datos-cundinamarca.md` — coordenadas, altitudes y tiempos ya validados
- `assets/ejemplo-plan.json` — un plan completo y funcional, útil como plantilla
- `scripts/generar_documento.py` — `plan.json` → HTML estático, incluidos los enlaces de Waze y Google Maps
- `scripts/html_a_pdf.py` — HTML → PDF A4 con encabezado de página
- `scripts/svg_mapas.py` — módulo de dibujo, no se ejecuta directo
