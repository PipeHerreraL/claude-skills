# Reglas de planificación

## 1. Capacidad diaria: calcúlala antes que nada

Con ventanas horarias, el límite de paradas por día no lo pone la distancia sino el reloj.

Para cada ventana:

    minutos_utiles = duracion_ventana - suma_de_traslados_dentro_de_la_ventana
    paradas = piso(minutos_utiles / minutos_por_parada)

Ejemplo con ventanas de 8–12 y 2–5 y paradas de 90 minutos:

- Mañana: 240 min. Dos visitas de 90 dejan 60 min para el traslado intermedio, así que
  caben dos **si los lugares quedan a menos de una hora entre sí**. Tres no caben.
- Tarde: 180 min. Dos visitas de 90 suman 180 sin dejar un solo minuto de traslado, así
  que cabe **una sola**.
- Total: tres paradas al día.

Multiplica por los días disponibles y compara con la lista. Si no alcanza, dilo de una vez.

## 2. Las tres palancas cuando no cabe

Preséntalas con su costo y deja que el usuario escoja:

- **Recortar minutos por parada.** Con paradas de 90 fijas entran tres al día; bajando
  algunas a 65–75 entran cuatro en los días de pueblos vecinos. Cuesta poco tiempo total
  de visita y suele ahorrar un día entero.
- **Agregar un día.** Un traslado la tarde anterior o un regreso al día siguiente no
  consume ventana de visita y descarga las jornadas extremas.
- **Sacar lugares.** La última opción, y quien decide es el usuario.

Recorta primero donde el traslado ya aprieta (tardes con dos paradas, tramos largos entre
dos visitas) y deja completos los lugares aislados, que no tienen con quién compartir el día.

## 3. Las horas fuera de ventana son el recurso más valioso

Todo lo que no sea visita —los traslados largos, el almuerzo, la llegada al hotel— va
antes de que abra la ventana, en el corte del mediodía, o después del cierre. Un traslado
de dos horas metido entre 12 y 2 no cuesta ninguna visita; el mismo traslado a las 10 de
la mañana cuesta una.

De ahí salen las salidas tempranas. Si la primera visita del día queda a una hora de
distancia, la salida es a las 6:45 y no es negociable.

## 4. Agrupación

1. Ubica los lugares por coordenadas y agrúpalos por cercanía real de carretera, no por
   distancia en línea recta: dos pueblos separados por una cordillera pueden estar a 8 km
   y a hora y media de camino.
2. Arma cada día dentro de un grupo. Cruzar entre grupos se hace en las horas muertas.
3. **Duerma en el lugar de la primera visita del día siguiente.** Es la optimización que
   más ventana libera: amanecer en el pueblo significa abrir a las 8:00 sin gastar carretera.
4. Cierra el circuito por una vía distinta a la de ida cuando exista. Evita repetir
   paisaje y suele ahorrar horas.

## 5. Restricciones duras que van antes de optimizar

- **No manejar de noche.** Fija la hora de llegada y, hacia atrás, la de salida del último día.
- **Tramos de vía terciaria.** Van completos en un mismo día, con las paradas de ese día en
  su duración máxima, porque no hay minutos que reacomodar. Marca ese día como el que fija
  el techo del plan y ofrece siempre una alternativa por si llueve.
- **Combustible.** Señala dónde tanquear cuando haya tramos largos sin estaciones.
- **Alojamiento escaso.** Nómbralo como riesgo con un plan B concreto, no como advertencia
  genérica.

## 6. Velocidades de referencia

- Vía principal pavimentada en plano: 60–70 km/h
- Vía principal de montaña: 40–50 km/h
- Vía secundaria de montaña: 30–40 km/h
- Vía terciaria destapada: 20–25 km/h

Siempre redondea hacia arriba y anota que son estimados. Recomienda confirmar el estado de
las vías con la autoridad vial correspondiente antes de salir.

## 7. Qué escribir en el documento

- Cada parada con sus **minutos reales**, no un genérico "90 min": el usuario necesita ver
  dónde tiene holgura.
- Las filas de traslado y de pernocta también, para que el día se lea completo.
- Un bloque de avisos con los riesgos concretos del plan: el tramo crítico, dónde se
  recortó y por qué, las salidas tempranas obligatorias, combustible, alojamiento, vías.
