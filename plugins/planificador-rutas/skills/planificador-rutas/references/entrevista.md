# Guion de entrevista

Objetivo: salir con datos suficientes para calcular el itinerario sin volver a preguntar.
Pregunta en tandas de dos o tres, no todas de golpe. Si la conversación ya contiene una
respuesta, no la repitas: resume y confirma.

## Bloque 1 — lo que no se puede calcular sin saber

1. **¿Desde dónde sale y a dónde regresa?** Si el origen queda lejos de la zona a visitar,
   el traslado se lleva un día entero y hay que decidir si cuenta o no.
2. **¿Qué lugares quiere visitar?** Pide la lista completa. Verifica ortografía y
   homónimos: hay municipios con el mismo nombre en departamentos distintos.
3. **¿Cuántos días tiene?** Y en seguida: **¿son días de visita o incluyen los traslados?**
   Esta distinción cambia el plan más que ninguna otra.
4. **¿En qué horario puede visitar?** No asumas jornada completa. Alcaldías, museos y
   oficinas suelen cerrar al mediodía, y mucha gente planifica alrededor de eso.
5. **¿Cuánto quiere estar en cada lugar?** Pregunta el deseado y también el mínimo que
   consideraría aceptable. El mínimo es la palanca que permite salvar un día completo.
6. **¿En qué se mueve?** Carro propio, moto, transporte público, conductor contratado.
7. **¿Puede salir la tarde anterior? ¿Puede regresar al día siguiente?** Dos preguntas
   distintas; a veces una sí y la otra no.

## Bloque 1b — qué debe traer el documento

Pregúntalo antes de buscar datos, no después: la altitud obliga a consultar cada cabecera
una por una y no siempre aporta.

- **¿Quiere el perfil de altitudes?** Tiene sentido cuando la ruta cruza cordillera y el
  clima cambia varias veces al día — sirve para saber qué ropa empacar. En terreno plano
  no aporta nada. Si dice que no, deja `"perfil": false` en el plan y omite el campo `alt`
  de los lugares; el generador se salta la sección completa.
- **¿Quiere el esquema de traslado y regreso?** Solo vale la pena si el trayecto de entrada
  o de salida pasa de dos o tres horas.
- **¿Va a ver el documento en el celular, imprimirlo, o ambos?** Por defecto se entregan
  las dos versiones, HTML y PDF.
- **¿Necesita llegar a una dirección exacta en cada parada** (juzgado, alcaldía, cliente)?
  El documento trae un enlace de Waze por parada que lleva a las coordenadas del lugar.
  Si basta con el centro del pueblo, sirven las de la cabecera; si no, pide o busca las
  del sitio exacto antes de escribir `lugares`.

## Bloque 2 — condicionales

Dispara cada una solo cuando aplique.

- **Si el origen queda a más de tres horas** → ¿prefiere gastar la primera mañana en
  carretera o dormir la noche anterior en el primer lugar de la ruta?
- **Si va en carro propio o moto** → ¿conduce de noche? ¿A qué hora quiere estar llegando?
  En zona de montaña la respuesta suele ser antes del anochecer, y eso fija la hora de
  salida del último día.
- **Si va en transporte público** → ¿ya sabe las frecuencias? Los horarios de flota mandan
  sobre las ventanas de visita y muchas rutas veredales tienen dos salidas al día.
- **Si la ruta toca zona rural** → ¿en qué temporada viaja? En temporada de lluvias las
  vías terciarias cambian el plan de un día para otro; conviene dejar un tramo alterno.
- **Si hay más lugares que días cómodos** → ¿prefiere recortar el tiempo por parada,
  agregar un día o sacar lugares de la lista? No decidas por él.
- **Si algún lugar tiene día u hora fija** (mercado campesino, feria, misa, una oficina que
  atiende solo por la mañana) → anótalo como restricción dura y arma el resto alrededor.
- **Si menciona acompañantes** → ¿viajan niños o adultos mayores? Eso acorta las jornadas
  útiles y obliga a paradas más frecuentes.
- **Si el alojamiento en la zona es escaso** → ¿reserva con anticipación o prefiere pueblos
  con oferta segura aunque impliquen más carretera?
- **Si pide el documento** → ¿lo va a ver en el celular, imprimirlo, o ambos? Por defecto
  se entregan las dos versiones.

## Bloque 3 — cierre

Antes de calcular, devuelve un resumen corto de lo entendido y pide confirmación. Un
malentendido en la lista de lugares o en las ventanas horarias se paga rehaciendo todo.

## Cuando ya crees saber la respuesta

Puede que el contexto —la conversación misma, o lo que tengas recordado de este usuario—
ya contenga el origen, las ventanas horarias o la lista de lugares. Eso ahorra preguntas,
pero **nunca lo apliques en silencio**: un dato viejo o de otro viaje produce un plan que
se ve correcto y no lo es.

Enúncialo y pide confirmación en una sola frase:

> "Voy con lo que ya tengo: sale de Manizales, visita de 8 a 12 y de 2 a 5, y viaja en
> carro propio. ¿Sigue igual para este viaje?"

Si el usuario lanza solo el comando, sin dar detalles, esa frase es la primera respuesta:
enumera lo que estás dando por sentado antes de calcular nada. Y si dice que arranque de
cero o que ignore lo anterior, haz la entrevista completa sin reutilizar nada.

## Cómo preguntar

- Una idea por pregunta. "¿Cuántos días y en qué horario?" produce respuestas a medias.
- Si tienes una herramienta de opciones tocables, úsala para las preguntas cerradas
  (días, transporte, horarios típicos). El usuario suele estar en el celular.
- Ofrece un valor por defecto razonable cuando la pregunta sea técnica: "por defecto asumo
  que no quiere manejar de noche, ¿le sirve?" es mejor que dejarlo en blanco.
