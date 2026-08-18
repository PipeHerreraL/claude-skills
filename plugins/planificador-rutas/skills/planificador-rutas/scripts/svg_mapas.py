# -*- coding: utf-8 -*-
"""Dibujo de los graficos SVG del documento de ruta.

Todos los colores se escriben literales: Safari en iOS no resuelve var(--x)
dentro de atributos de presentacion de SVG y los graficos saldrian sin color.
"""

MONO = "Menlo,Consolas,'DejaVu Sans Mono',monospace"
PAPEL2 = "#F3F5EF"; TINTA = "#16221E"; TINTA2 = "#4E5C56"
SEPIA = "#A08C63"; LINEA = "#C7CDC2"; GRIS = "#8E9A93"

CANDIDATOS = [(11, 4, "start"), (-11, 4, "end"), (0, -13, "middle"), (0, 17, "middle"),
              (12, -9, "start"), (-12, -9, "end"), (12, 16, "start"), (-12, 16, "end"),
              (0, -25, "middle"), (0, 29, "middle")]


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;")


def proyeccion(pts, W, H, pad):
    lo = [p[0] for p in pts]; la = [p[1] for p in pts]
    lo0, lo1, la0, la1 = min(lo), max(lo), min(la), max(la)
    dlo = max(lo1 - lo0, 1e-6); dla = max(la1 - la0, 1e-6)
    s = min((W - 2 * pad) / dlo, (H - 2 * pad) / dla)
    ox = (W - dlo * s) / 2; oy = (H - dla * s) / 2
    return (lambda lon, lat: (ox + (lon - lo0) * s, oy + (la1 - lat) * s)), (lo0, lo1, la0, la1)


def estilos(movil):
    a, b, c = (7, 11, 9.5) if movil else (8, 9.5, 8.5)
    return ("<style>"
            ".grat{font-family:%s;font-size:%spx;fill:%s}"
            ".rot{font-family:%s;font-size:%spx;letter-spacing:.06em;text-transform:uppercase;"
            "fill:%s;paint-order:stroke;stroke:%s;stroke-width:3.5px;stroke-linejoin:round}"
            ".rot2{font-family:%s;font-size:%spx;letter-spacing:.04em;fill:%s;"
            "paint-order:stroke;stroke:%s;stroke-width:3px;stroke-linejoin:round}"
            ".num{font-family:%s;font-size:%spx;font-weight:700;fill:%s;text-anchor:middle}"
            "</style>") % (MONO, a, LINEA, MONO, b, TINTA, PAPEL2,
                           MONO, c, TINTA2, PAPEL2, MONO, c, PAPEL2)


def graticula(p, caja, W, H, paso):
    o = []; lo0, lo1, la0, la1 = caja
    v = (int(lo0 / paso)) * paso
    while v <= lo1:
        if v >= lo0:
            x, _ = p(v, la1)
            o.append('<line x1="%.1f" y1="0" x2="%.1f" y2="%d" stroke="%s" stroke-width="0.6" stroke-dasharray="2 5"/>' % (x, x, H, LINEA))
            o.append('<text x="%.1f" y="12" class="grat">%.1f°O</text>' % (x + 3, abs(v)))
        v += paso
    v = (int(la0 / paso) + 1) * paso
    while v <= la1:
        if v >= la0:
            _, y = p(lo0, v)
            o.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="0.6" stroke-dasharray="2 5"/>' % (y, W, y, LINEA))
            o.append('<text x="4" y="%.1f" class="grat">%.1f°N</text>' % (y - 4, v))
        v += paso
    return "".join(o)


def _rect(x, y, dx, dy, anc, texto, fs):
    ancho = len(texto) * fs * 0.62; alto = fs * 1.15
    cx = x + dx
    if anc == "end": x0 = cx - ancho
    elif anc == "middle": x0 = cx - ancho / 2
    else: x0 = cx
    return (x0, y + dy - alto, x0 + ancho, y + dy + alto * 0.25)


def _solape(r, o):
    ax = min(r[2], o[2]) - max(r[0], o[0])
    ay = min(r[3], o[3]) - max(r[1], o[1])
    return ax * ay if ax > 0 and ay > 0 else 0.0


def colocar_etiquetas(nodos, manual, fs, W, H, extra=()):
    """Devuelve {clave:(dx,dy,anclaje)} escogiendo, para cada etiqueta, la posicion
    con menos solape contra marcadores, puntos de paso y etiquetas ya ubicadas."""
    ocupados = [(x - 11, y - 11, x + 11, y + 11) for _, x, y, _ in nodos]
    ocupados += [(x - 6, y - 6, x + 6, y + 6) for x, y in extra]
    salida = {}
    for clave, x, y, texto in nodos:
        if clave in manual:
            dx, dy, anc = manual[clave]
            salida[clave] = (dx, dy, anc)
            ocupados.append(_rect(x, y, dx, dy, anc, texto, fs))
            continue
        mejor, mejor_costo = None, None
        for i, (dx, dy, anc) in enumerate(CANDIDATOS):
            r = _rect(x, y, dx, dy, anc, texto, fs)
            costo = sum(_solape(r, o) for o in ocupados) + i * 12.0
            if r[0] < 2 or r[2] > W - 2 or r[1] < 2 or r[3] > H - 2:
                costo += 8000.0
            if mejor_costo is None or costo < mejor_costo:
                mejor, mejor_costo = (dx, dy, anc, r), costo
            if costo <= i * 12.0:
                break
        salida[clave] = mejor[:3]
        ocupados.append(mejor[3])
    return salida


def separar_marcadores(posiciones, radio):
    """Aparta verticalmente los marcadores que quedan encimados. {clave:(dx,dy)}"""
    minimo = radio * 2.15
    grupos = []
    for clave, (x, y) in posiciones.items():
        for g in grupos:
            if any((x - posiciones[k][0]) ** 2 + (y - posiciones[k][1]) ** 2 < minimo ** 2 for k in g):
                g.append(clave); break
        else:
            grupos.append([clave])
    ajuste = {}
    for g in grupos:
        if len(g) < 2: continue
        g.sort(key=lambda k: posiciones[k][0])
        for i, clave in enumerate(g):
            paso = (radio + 5) * (1 if i % 2 else -1) * (1 + i // 2)
            ajuste[clave] = (0, paso)
    return ajuste


# --------------------------------------------------------------- mapa
def mapa(plan, movil):
    L = plan["lugares"]; dias = plan["dias"]
    W, H, pad = (380, 408, 30) if movil else (700, 690, 58)
    claves = []
    for d in dias:
        for k in d["circuito"]:
            if k not in claves: claves.append(k)
    p, caja = proyeccion([(L[k]["lon"], L[k]["lat"]) for k in claves], W, H, pad)
    idx = plan["_idx"]

    pos = {}
    for d in dias:
        for k in d["paradas"]:
            pos[k] = p(L[k]["lon"], L[k]["lat"])
    radio = 8 if movil else 8.5
    ajuste = separar_marcadores(pos, radio) if movil else {}
    ajuste.update({k: tuple(v) for k, v in plan.get("separar", {}).items()} if movil else {})

    o = [estilos(movil), '<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPEL2),
         graticula(p, caja, W, H, 0.2 if movil else 0.1)]

    def trazo(keys):
        d = ""
        for i, k in enumerate(keys):
            x, y = p(L[k]["lon"], L[k]["lat"])
            d += ("L" if i else "M") + "%.1f %.1f " % (x, y)
        return d

    for d in dias:
        g = ['<g class="grupo" data-dia="%s">' % d["n"]]
        dash = "9 5" if d.get("traslado") else "0"
        g.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"/>' % (trazo(d["circuito"]), PAPEL2, 5.5 if movil else 7))
        g.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="%s"/>' % (trazo(d["circuito"]), d["color"], 2.4 if movil else 3, dash))
        for k in d["circuito"]:
            if k in d["paradas"]: continue
            x, y = p(L[k]["lon"], L[k]["lat"])
            g.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, 2.2 if movil else 2.6, SEPIA))
        o.append("".join(g) + "</g>")

    etiquetas = {}
    if not movil:
        rotular = list(plan.get("rotular_paso", []))
        nodos = [(k, pos[k][0], pos[k][1], L[k]["nombre"]) for d in dias for k in d["paradas"]]
        nodos += [(k, p(L[k]["lon"], L[k]["lat"])[0], p(L[k]["lon"], L[k]["lat"])[1], L[k]["nombre"])
                  for k in rotular if k not in pos]
        pasos = [p(L[k]["lon"], L[k]["lat"]) for d in dias for k in d["circuito"] if k not in pos]
        etiquetas = colocar_etiquetas(nodos, plan.get("etiquetas", {}), 9.5, W, H, pasos)

    for d in dias:
        if not d["paradas"]: continue
        g = ['<g class="grupo" data-dia="%s">' % d["n"]]
        for k in d["paradas"]:
            cx, cy = pos[k]
            if k in ajuste:
                nx, ny = cx + ajuste[k][0], cy + ajuste[k][1]
                g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (cx, cy, nx, ny, d["color"]))
                cx, cy = nx, ny
            g.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.6"/>' % (cx, cy, radio, d["color"], PAPEL2))
            g.append('<text x="%.1f" y="%.1f" class="num">%d</text>' % (cx, cy + 3.2, idx[k]))
            if not movil:
                dx, dy, anc = etiquetas[k]
                g.append('<text x="%.1f" y="%.1f" text-anchor="%s" class="rot">%s</text>' % (pos[k][0] + dx, pos[k][1] + dy, anc, esc(L[k]["nombre"])))
        o.append("".join(g) + "</g>")

    if movil:
        o.append('<text x="%d" y="%d" text-anchor="end" class="rot2">N ↑ · números = orden de visita</text>' % (W - 10, H - 10))
    else:
        for k in plan.get("rotular_paso", []):
            if k in pos: continue
            x, y = p(L[k]["lon"], L[k]["lat"])
            dx, dy, anc = etiquetas.get(k, (10, 4, "start"))
            o.append('<text x="%.1f" y="%.1f" text-anchor="%s" class="rot2">%s</text>' % (x + dx, y + dy, anc, esc(L[k]["nombre"])))
        o.append('<text x="%d" y="%d" text-anchor="end" class="rot2">N ↑ · punteado = traslado</text>' % (W - 14, H - 14))
    return '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mapa del circuito">%s</svg>' % (W, H, "".join(o))


# --------------------------------------------------------------- perfil
def _puntos(plan):
    L = plan["lugares"]; origen = plan.get("origen")
    alt = lambda k: int(L[k].get("alt") or 0)
    pts = []
    if origen:
        pts.append(dict(nombre=L[origen]["nombre"], alt=alt(origen), color=GRIS, dia=None, i=0))
    for k, dia, color in plan["_orden"]:
        pts.append(dict(nombre=L[k]["nombre"], alt=alt(k), color=color, dia=dia, i=plan["_idx"][k]))
    if origen:
        pts.append(dict(nombre=L[origen]["nombre"], alt=alt(origen), color=GRIS, dia=None, i=0))
    return pts


def perfil(plan, movil):
    pts = _puntos(plan); n = len(pts)
    maxA = max(200, int(max(p["alt"] for p in pts) * 1.09 / 100.0 + 1) * 100)
    corto = plan.get("nombres_cortos", {})
    if movil:
        W = 380; fila = 25; T = 34; H = int(T + n * fila + 14); x0 = 126; x1 = W - 44
        o = [estilos(movil), '<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPEL2)]
        for a in (0, maxA // 2, maxA):
            x = x0 + (float(a) / maxA) * (x1 - x0)
            o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="0.7"/>' % (x, T - 8, x, H - 10, LINEA))
            o.append('<text x="%.1f" y="%d" text-anchor="middle" class="grat" style="fill:%s">%d</text>' % (x, T - 14, SEPIA, a))
        o.append('<text x="6" y="%d" class="rot2">altitud, m</text>' % (T - 14))
        for i, pt in enumerate(pts):
            y = T + i * fila + fila / 2.0
            x = x0 + (float(pt["alt"]) / maxA) * (x1 - x0)
            nom = corto.get(pt["nombre"], pt["nombre"])
            o.append('<g class="grupo" data-dia="%s">' % (pt["dia"] if pt["dia"] is not None else ""))
            o.append('<text x="6" y="%.1f" class="rot2">%s</text>' % (y + 3.5, esc(("%d  " % pt["i"] if pt["i"] else "") + nom)))
            o.append('<line x1="%d" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-linecap="round" opacity="%s"/>' % (x0, y, x, y, pt["color"], 5 if pt["dia"] is not None else 3, 1 if pt["dia"] is not None else .6))
            o.append('<text x="%.1f" y="%.1f" class="rot2">%d</text>' % (x + 7, y + 3.5, pt["alt"]))
            o.append('</g>')
        return '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Perfil de altitudes">%s</svg>' % (W, H, "".join(o))

    W, H, Lm, R, T, B = 960, 372, 54, 22, 30, 132
    dx = (W - Lm - R) / float(n - 1)
    X = lambda i: Lm + i * dx
    Y = lambda a: T + (1 - float(a) / maxA) * (H - T - B)
    o = [estilos(movil), '<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPEL2)]
    paso = maxA // 4
    for a in range(0, maxA, paso):
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="0.7"/>' % (Lm, Y(a), W - R, Y(a), LINEA))
        o.append('<text x="%d" y="%.1f" text-anchor="end" class="grat" style="fill:%s">%d</text>' % (Lm - 8, Y(a) + 3, SEPIA, a))
    area = "M%.1f %.1f" % (X(0), Y(pts[0]["alt"]))
    for i, pt in enumerate(pts):
        if i: area += "L%.1f %.1f" % (X(i), Y(pt["alt"]))
    area += "L%.1f %.1fL%.1f %.1fZ" % (X(n - 1), Y(0), X(0), Y(0))
    o.append('<path d="%s" fill="%s" opacity=".1"/>' % (area, SEPIA))
    for i, pt in enumerate(pts):
        if i == 0: continue
        pv = pts[i - 1]
        o.append('<g class="grupo" data-dia="%s"><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.4" stroke-linecap="round"/></g>' % (pt["dia"] if pt["dia"] is not None else "", X(i - 1), Y(pv["alt"]), X(i), Y(pt["alt"]), pt["color"]))
    for i, pt in enumerate(pts):
        o.append('<g class="grupo" data-dia="%s">' % (pt["dia"] if pt["dia"] is not None else ""))
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.8"/>' % (X(i), Y(pt["alt"]), X(i), Y(0), LINEA))
        o.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (X(i), Y(pt["alt"]), 4.2 if pt["dia"] is not None else 3, pt["color"]))
        o.append('<text x="%.1f" y="%.1f" text-anchor="middle" class="rot2">%d</text>' % (X(i), Y(pt["alt"]) - 10, pt["alt"]))
        o.append('<text transform="translate(%.1f,%.1f) rotate(-52)" text-anchor="end" class="rot2">%s</text>' % (X(i), Y(0) + 12, esc(("%d " % pt["i"] if pt["i"] else "") + pt["nombre"])))
        o.append('</g>')
    o.append('<text x="%d" y="16" class="rot2">metros sobre el nivel del mar</text>' % Lm)
    return '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Perfil de altitudes">%s</svg>' % (W, H, "".join(o))


# --------------------------------------------------------------- corredor
def _tira(lista, y0, color, dash, dia, titulo):
    fila = 34; xl = 104
    o = ['<text x="6" y="%d" class="rot" style="fill:%s">%s</text>' % (y0 - 14, color, esc(titulo))]
    o.append('<g class="grupo" data-dia="%s">' % dia)
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4" stroke-dasharray="%s"/>' % (xl, y0, xl, y0 + (len(lista) - 1) * fila, color, dash))
    for i, par in enumerate(lista):
        nombre, tramo = par[0], (par[1] if len(par) > 1 else "")
        y = y0 + i * fila
        if tramo:
            o.append('<text x="%d" y="%d" text-anchor="end" class="rot2">%s</text>' % (xl - 12, y - fila / 2 + 4, esc(tramo)))
        extremo = (i == 0 or i == len(lista) - 1)
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (xl, y, 6 if extremo else 4, TINTA if extremo else color))
        o.append('<text x="%d" y="%d" class="rot2" style="font-size:11px;fill:%s">%s</text>' % (xl + 14, y + 4, TINTA, esc(nombre)))
    return "".join(o) + "</g>"


def corredor(plan, movil):
    c = plan.get("corredor")
    if not c: return ""
    L = plan["lugares"]
    if movil:
        fila = 34; ni = len(c["ida_lista"]); nv = len(c["vuelta_lista"])
        W = 380; y0 = 54; y1 = y0 + (ni - 1) * fila + 72; H = int(y1 + (nv - 1) * fila + 24)
        o = [estilos(movil), '<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPEL2)]
        o.append(_tira(c["ida_lista"], y0, c["color_ida"], "0", c["dia_ida"], c["titulo_ida"]))
        o.append(_tira(c["vuelta_lista"], y1, c["color_vuelta"], "9 5", c["dia_vuelta"], c["titulo_vuelta"]))
        return '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Traslado y regreso">%s</svg>' % (W, H, "".join(o))

    W, H = 960, 400
    claves = []
    for k in c.get("comun", []) + c["ida"] + c["vuelta"]:
        if k not in claves: claves.append(k)
    p, caja = proyeccion([(L[k]["lon"], L[k]["lat"]) for k in claves], W, H, 64)
    o = [estilos(movil), '<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPEL2), graticula(p, caja, W, H, 0.1)]

    def trazo(keys):
        d = ""
        for i, k in enumerate(keys):
            x, y = p(L[k]["lon"], L[k]["lat"])
            d += ("L" if i else "M") + "%.1f %.1f " % (x, y)
        return d

    rio = c.get("rio")
    if rio:
        d = ""
        for i, pt in enumerate(rio):
            x, y = p(pt[0], pt[1]); d += ("L" if i else "M") + "%.1f %.1f " % (x, y)
        o.append('<path d="%s" fill="none" stroke="#3E6E8E" stroke-width="4" opacity=".45" stroke-linecap="round"/>' % d)
        if c.get("rio_rotulo"):
            rx, ry = p(c["rio_rotulo"][0], c["rio_rotulo"][1])
            o.append('<text x="%.1f" y="%.1f" class="rot2" style="fill:#3E6E8E">%s</text>' % (rx + 8, ry, esc(c["rio_rotulo"][2])))
    if c.get("comun"):
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="7.5" stroke-linejoin="round"/>' % (trazo(c["comun"]), PAPEL2))
        o.append('<path d="%s" fill="none" stroke="#A7AFA9" stroke-width="3" stroke-linejoin="round"/>' % trazo(c["comun"]))
    for seg, color, dia, dash in ((c["ida"], c["color_ida"], c["dia_ida"], "0"),
                                  (c["vuelta"], c["color_vuelta"], c["dia_vuelta"], "9 5")):
        o.append('<g class="grupo" data-dia="%s">' % dia)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="7.5" stroke-linejoin="round"/>' % (trazo(seg), PAPEL2))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round" stroke-dasharray="%s"/>' % (trazo(seg), color, dash))
        o.append('</g>')
    anclas = set(c.get("anclas", []))
    nodos = [(k, p(L[k]["lon"], L[k]["lat"])[0], p(L[k]["lon"], L[k]["lat"])[1], L[k]["nombre"]) for k in claves]
    et = colocar_etiquetas(nodos, plan.get("etiquetas", {}), 9, W, H)
    for k in claves:
        x, y = p(L[k]["lon"], L[k]["lat"]); a = k in anclas
        o.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, 6 if a else 3.4, TINTA if a else SEPIA))
        dx, dy, anc = et[k]
        o.append('<text x="%.1f" y="%.1f" text-anchor="%s" class="%s">%s</text>' % (x + dx, y + dy, anc, "rot" if a else "rot2", esc(L[k]["nombre"])))
    o.append('<text x="%d" y="%d" text-anchor="end" class="rot2">%s</text>' % (W - 14, H - 14, esc(c.get("leyenda", ""))))
    return '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Traslado y regreso">%s</svg>' % (W, H, "".join(o))
