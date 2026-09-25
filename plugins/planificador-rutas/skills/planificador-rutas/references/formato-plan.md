# Formato de `plan.json`

Un solo archivo alimenta el generador. Todo campo no listado como obligatorio puede omitirse.

## Esqueleto

```json
{
  "titulo_pagina": "Cundinamarca · 17 municipios en 5 días",
  "eyebrow": "Gualivá · Rionegro · Magdalena Centro",
  "h1": "Diecisiete<br>municipios",
  "h1_sub": "en cinco<br>días hábiles",
  "lede": "Párrafo de apertura que resume el plan y su restricción principal.",
  "cifras": [["17","municipios"], ["5","días hábiles"], ["83'","promedio por parada"]],

  "origen": "manizales",
  "perfil": true,
  "lugares": { "villeta": {"nombre":"Villeta","lon":-74.4706,"lat":5.0128,"alt":842} },

  "banda_titulo": "Cómo cabe el día",
  "banda": [["rodar","6–8 · rodar",2], ["abierto","8–12 · 240 min",4]],

  "dias": [ { ... } ],
  "corredor": { ... },
  "notas": {"banda":"…","mapa":"…","perfil":"…","corredor":"…"},
  "avisos": [{"titulo":"Tramo crítico","texto":"…","alerta":true}],
  "pie": "Nota al pie, admite <br>"
}
```

## Campos

**`lugares`** (obligatorio) — diccionario `clave: {nombre, lon, lat}` y opcionalmente `alt`.
La clave es un identificador corto sin tildes ni espacios; el resto del archivo se refiere a
los lugares por esa clave. Todo lugar mencionado en algún `circuito` debe existir aquí o el
generador se detiene con el listado de los que faltan.

**`alt` y `perfil`** — la altitud es opcional y solo sirve para el perfil de altitudes.
Pregúntale al usuario si lo quiere antes de salir a buscar altitudes una por una. Si no lo
quiere, omite `alt` y pon `"perfil": false`; la sección desaparece del documento. Si pides
el perfil pero falta la altitud de alguna parada, el generador avisa por consola y omite la
sección en lugar de fallar.

**`origen`** — clave del punto de partida y regreso. Se dibuja en los extremos del perfil
de altitudes, en gris. Omítelo si el viaje no empieza y termina en el mismo sitio.

**`dias`** (obligatorio) — lista ordenada:

```json
{
  "n": 1,
  "titulo": "El corredor de Tobia",
  "base": "Noche en Villeta",
  "meta": "4 visitas · 5 h 30 en pueblo · ~70 km",
  "color": "#C0562B",
  "traslado": false,
  "circuito": ["villeta","quebradanegra","tobia","nimaima","nocaima","villeta"],
  "paradas": ["villeta","quebradanegra","nimaima","nocaima"],
  "filas": [
    ["08:00","Villeta","Se empieza a pie desde el hotel","visita",90],
    ["11:55","Tobia","Almuerzo; el traslado va dentro del descanso","traslado"],
    ["17:20","Villeta","Pernocta, 20 min de regreso","pernocta"]
  ]
}
```

- `circuito` es el recorrido completo del día, incluidos los puntos por los que solo pasa y
  los tramos que se devuelven sobre sí mismos. Repite una clave si el día pasa dos veces
  por ahí.
- `paradas` son las visitas de verdad, en el orden en que ocurren. De aquí sale la
  numeración 1..N del mapa y del perfil, así que el orden importa.
- `traslado: true` dibuja la línea del día punteada. Úsalo en los días sin visitas.
- `color` es opcional; si falta, se asigna de la paleta.
- Cada fila es `[hora, lugar, nota, tipo]` y, si el tipo es `visita`, un quinto elemento con
  los minutos reales. Tipos: `visita`, `traslado`, `pernocta`, `llegada`.

**`banda`** — franjas del día: `[clase, texto, peso]`, con clase `abierto` para las ventanas
de visita y `rodar` para el resto. El peso es la proporción de ancho.

**`corredor`** — opcional, para el traslado inicial y el regreso cuando son largos:

```json
{
  "titulo": "Traslado y regreso",
  "subtitulo": "Día 0 por Letras · tarde del día 5 por Cambao",
  "comun": ["manizales","letras","fresno","mariquita"],
  "ida": ["mariquita","honda","guaduas","villeta"],
  "vuelta": ["viani","sanjuan","cambao","armero","mariquita"],
  "color_ida": "#6B7F86", "color_vuelta": "#A9781F",
  "dia_ida": 0, "dia_vuelta": 5,
  "titulo_ida": "Día 0 · traslado, 6 h 30",
  "titulo_vuelta": "Día 5 · regreso, 6 h 15",
  "ida_lista": [["Manizales",""],["Alto de Letras","1 h 50"]],
  "vuelta_lista": [["Vianí",""],["San Juan de Rioseco","45 min"]],
  "anclas": ["villeta","viani"],
  "rio": [[-74.80,5.35],[-74.744,5.207]],
  "rio_rotulo": [-74.72,5.05,"Río Magdalena"],
  "leyenda": "gris = tramo compartido · punteado = regreso"
}
```

`comun` es el tramo que ida y regreso recorren igual; se dibuja una sola vez en gris, si no
las dos líneas se tapan entre sí. Las `*_lista` alimentan la versión móvil, que es una línea
de tiempo vertical con la duración de cada tramo — más útil en un teléfono que un mapa
aplastado.

**`navegar`** — opcional; la sección de enlaces sale aunque el campo no exista.

- Ausente o `true`: se arma sola. Un bloque por día con paradas, cada parada con su enlace de
  Waze y como detalle la hora y los minutos de su fila `visita`; un enlace de Google Maps por
  día; y un bloque final de regreso al `origen`.
- `false`: se omite la sección.
- Diccionario: igual que `true`, pero admite ajustes:

```json
"navegar": {
  "titulo": "Navegar con Waze",
  "sub": "Un enlace por parada, en orden de visita",
  "intro": "Texto de apertura; por defecto explica que Waze admite una sola parada.",
  "nota": "Texto de cierre; por defecto aclara a dónde llevan los enlaces.",
  "detalles": {"paime": "desde La Palma · 2 h 30, pasando por Villagómez"},
  "gmaps": true,
  "regreso": true,
  "detalle_regreso": "6 h 30 por Vianí y Cambao",
  "nota_regreso": "Waze puede proponer otra vía; la sugerida es por Cambao"
}
```

`detalles` reemplaza el texto bajo el nombre de una parada, por clave de lugar. Si además
viene `grupos`, el generador no arma nada y usa esos grupos tal cual:
`[{"titulo", "color", "detalle", "items": [[num, nombre, url_waze, detalle]], "gmaps": url o lista}]`.

## Campos de ajuste fino

Rara vez hacen falta: el generador coloca las etiquetas y separa los marcadores solo.

- `etiquetas`: `{"villeta": [-9, 4, "end"]}` fuerza el desplazamiento y anclaje de una
  etiqueta concreta.
- `separar`: `{"bituima": [0, 12]}` fuerza el apartado de un marcador en la versión móvil.
- `rotular_paso`: lista de claves que no son parada pero merecen nombre en el mapa.
- `nombres_cortos`: `{"Guayabal de Síquima": "Guayabal de Síq."}` para el perfil móvil,
  donde el espacio de la etiqueta es fijo.

## Comprobación rápida

```bash
python3 scripts/generar_documento.py plan.json salida.html
python3 scripts/html_a_pdf.py salida.html salida.pdf "Pie de página"
```

El generador imprime el tamaño y confirma que no quedó JavaScript. Si el PDF sale con más
páginas de las esperadas o algún gráfico se ve cortado, rasteriza una página y míralo antes
de entregar.
