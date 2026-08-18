# -*- coding: utf-8 -*-
"""plan.json -> documento HTML estatico (sin JavaScript).

    python3 generar_documento.py plan.json salida.html

El HTML resultante abre en cualquier visor, incluidos los de iOS que no ejecutan
JavaScript, y trae version movil y de escritorio de cada grafico.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svg_mapas import mapa, perfil, corredor, esc, PAPEL2, TINTA, TINTA2, LINEA, SEPIA

PALETA = ["#6B7F86", "#C0562B", "#8A3A5E", "#2F6E5A", "#3B5C96", "#A9781F", "#5B4B8A", "#4E7A3F"]
ETIQ = {"pernocta": "pernocta", "llegada": "llegada"}


def preparar(plan):
    for i, d in enumerate(plan["dias"]):
        d.setdefault("color", PALETA[i % len(PALETA)])
        d.setdefault("paradas", [])
        d.setdefault("circuito", [])
    orden, idx = [], {}
    for d in plan["dias"]:
        for k in d["paradas"]:
            orden.append((k, d["n"], d["color"]))
            idx[k] = len(orden)
    plan["_orden"] = orden; plan["_idx"] = idx
    con_alt = [k for k, _, _ in orden if plan["lugares"][k].get("alt") is not None]
    plan["_perfil"] = bool(plan.get("perfil", True)) and len(con_alt) == len(orden) and len(orden) > 1
    if plan.get("perfil") and not plan["_perfil"]:
        sin = [plan["lugares"][k]["nombre"] for k, _, _ in orden if plan["lugares"][k].get("alt") is None]
        print("Aviso: se pidió perfil de altitudes pero faltan altitudes en: %s. Se omite la sección."
              % ", ".join(sin))
    faltan = [k for d in plan["dias"] for k in d["circuito"] if k not in plan["lugares"]]
    if faltan:
        raise SystemExit("Faltan coordenadas para: %s" % ", ".join(sorted(set(faltan))))
    return plan


def bloque_dias(plan):
    out = []
    for d in plan["dias"]:
        out.append('<article class="dia" data-dia="%s" style="border-top-color:%s">' % (d["n"], d["color"]))
        out.append('<div class="dia-cab"><div class="dia-num" style="color:%s">%s</div>' % (d["color"], d["n"]))
        out.append('<div><div class="dia-tit">%s</div><div class="det">%s</div></div>' % (esc(d["titulo"]), esc(d.get("base", ""))))
        out.append('<div class="dia-meta">%s</div></div><table><tbody>' % esc(d.get("meta", "")))
        for f in d["filas"]:
            hora, lugar, nota, tipo = f[0], f[1], f[2], f[3]
            mins = f[4] if len(f) > 4 else 0
            cls = "parada" if tipo == "visita" else "paso"
            tag = ("%d min" % mins) if tipo == "visita" else ETIQ.get(tipo)
            out.append('<tr class="%s"><td class="hora">%s</td><td class="lugar">%s' % (cls, esc(hora), esc(lugar)))
            if tag:
                out.append('<span class="tag" style="color:%s">%s</span>' % (d["color"] if tipo == "visita" else TINTA2, tag))
            out.append('</td><td class="det">%s</td></tr>' % esc(nota))
        out.append('</tbody></table></article>')
    return "\n".join(out)


def construir(plan):
    plan = preparar(plan)
    L = plan["lugares"]; dias = plan["dias"]

    radios = '<input class="rf" type="radio" name="filtro" id="f-todo" checked>'
    radios += "".join('<input class="rf" type="radio" name="filtro" id="f-%s">' % d["n"] for d in dias)
    chips = '<label class="chip" for="f-todo">Todo</label>' + "".join(
        '<label class="chip" for="f-%s">Día %s</label>' % (d["n"], d["n"]) for d in dias)
    reglas = ['#f-todo:checked ~ .app-cuerpo .chip[for="f-todo"]{background:%s;border-color:%s;color:%s}' % (TINTA, TINTA, PAPEL2)]
    for d in dias:
        n = d["n"]
        reglas += ['#f-%s:checked ~ .app-cuerpo .grupo:not([data-dia="%s"]){opacity:.13}' % (n, n),
                   '#f-%s:checked ~ .app-cuerpo .dia:not([data-dia="%s"]){opacity:.34}' % (n, n),
                   '#f-%s:checked ~ .app-cuerpo .mleg-dia:not([data-dia="%s"]){opacity:.3}' % (n, n),
                   '#f-%s:checked ~ .app-cuerpo .chip[for="f-%s"]{background:%s;border-color:%s;color:%s}' % (n, n, TINTA, TINTA, PAPEL2)]

    leyenda = "".join('<span><i style="background:%s"></i>Día %s · %s</span>' % (d["color"], d["n"], esc(d["titulo"])) for d in dias)
    mleg = "".join('<div class="mleg-dia" data-dia="%s"><i style="background:%s"></i><b>Día %s</b><span>%s</span></div>'
                   % (d["n"], d["color"], d["n"],
                      esc(" · ".join("%d %s" % (plan["_idx"][k], L[k]["nombre"]) for k in d["paradas"]) or d.get("sin_visitas", "traslado, sin visitas")))
                   for d in dias)
    facts = "".join('<div class="fact"><b>%s</b><i>%s</i></div>' % (esc(a), esc(b)) for a, b in plan.get("cifras", []))
    banda = "".join('<div class="%s" style="flex:%s">%s</div>' % (c, f, esc(t)) for c, t, f in plan.get("banda", []))
    avisos = "".join('<div class="aviso%s"><h3>%s</h3><p>%s</p></div>'
                     % (" alerta" if a.get("alerta") else "", esc(a["titulo"]), esc(a["texto"]))
                     for a in plan.get("avisos", []))
    notas = plan.get("notas", {})
    sec_corr = ""
    if plan.get("corredor"):
        sec_corr = ('<section id="sec-corredor"><h2>%s</h2><p class="sub">%s</p>'
                    '<div class="lienzo solo-desktop">%s</div><div class="lienzo solo-movil">%s</div>'
                    '<p class="nota">%s</p></section>') % (
            esc(plan["corredor"].get("titulo", "Traslado y regreso")),
            esc(plan["corredor"].get("subtitulo", "")),
            corredor(plan, False), corredor(plan, True), esc(notas.get("corredor", "")))

    sec_perfil = ""
    if plan["_perfil"]:
        sec_perfil = ('<section id="sec-perfil"><h2>%s</h2><p class="sub">%s</p>'
                      '<div class="lienzo solo-desktop">%s</div><div class="lienzo solo-movil">%s</div>'
                      '<p class="nota">%s</p></section>') % (
            esc(plan.get("titulo_perfil", "Lo que sube y lo que baja")),
            esc(plan.get("sub_perfil", "Altitud de cada parada, en orden de visita")),
            perfil(plan, False), perfil(plan, True), esc(notas.get("perfil", "")))

    sec_banda = ""
    if banda:
        sec_banda = ('<section id="sec-reloj"><h2>%s</h2><p class="sub">%s</p><div class="banda">%s</div>'
                     '<p class="nota">%s</p></section>') % (
            esc(plan.get("banda_titulo", "Cómo cabe el día")),
            esc(plan.get("banda_subtitulo", "Ventanas de visita contra tiempo de rodaje")),
            banda, esc(notas.get("banda", "")))

    return PLANTILLA % dict(
        titulo=esc(plan.get("titulo_pagina", "Itinerario")),
        eyebrow=esc(plan.get("eyebrow", "")),
        h1=plan.get("h1", ""), h1sub=plan.get("h1_sub", ""),
        lede=esc(plan.get("lede", "")), facts=facts,
        css_filtros="\n    ".join(reglas), radios=radios, chips=chips,
        mapa_d=mapa(plan, False), mapa_m=mapa(plan, True),
        leyenda=leyenda, mleg=mleg,
        sec_banda=sec_banda, sec_corr=sec_corr, sec_perfil=sec_perfil,
        titulo_mapa=esc(plan.get("titulo_mapa", "El circuito")),
        sub_mapa=esc(plan.get("sub_mapa", "Trazado esquemático · toca un día para aislarlo")),
        nota_mapa=esc(notas.get("mapa", "")),
        sub_itinerario=esc(plan.get("sub_itinerario", "Cada parada muestra sus minutos reales de visita")),
        dias=bloque_dias(plan),
        titulo_avisos=esc(plan.get("titulo_avisos", "Antes de arrancar")),
        sub_avisos=esc(plan.get("sub_avisos", "")), avisos=avisos,
        pie=plan.get("pie", ""))


PLANTILLA = u"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light">
<title>%(titulo)s</title>
<style>
  :root{--papel:#E7EAE3;--papel-2:#F3F5EF;--tinta:#16221E;--tinta-2:#4E5C56;--sepia:#A08C63;--linea:#C7CDC2;
    --mono:Menlo,Consolas,"DejaVu Sans Mono",monospace;
    --disp:-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;
    --body:Georgia,"Times New Roman",serif}
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:#E7EAE3;color:#16221E;font-family:Georgia,"Times New Roman",serif;font-size:16px;line-height:1.6;-webkit-text-size-adjust:100%%}
  .wrap{max-width:1040px;margin:0 auto;padding:0 22px 80px}
  svg{max-width:100%%}
  .top{padding:48px 0 26px;border-bottom:1px solid var(--linea)}
  .eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--sepia);margin:0 0 14px}
  h1{font-family:var(--disp);font-weight:800;letter-spacing:-.03em;line-height:.92;font-size:46px;text-transform:uppercase;margin:0 0 6px}
  h1 span{display:block;color:var(--sepia)}
  .lede{max-width:58ch;color:var(--tinta-2);margin:18px 0 0}
  .facts{display:flex;flex-wrap:wrap;margin:26px 0 0;border-top:1px solid var(--linea);border-left:1px solid var(--linea)}
  .fact{flex:1 1 150px;padding:12px 14px;border-right:1px solid var(--linea);border-bottom:1px solid var(--linea)}
  .fact b{display:block;font-family:var(--disp);font-size:26px;font-weight:800;letter-spacing:-.02em;line-height:1}
  .fact i{font-style:normal;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--tinta-2);display:block;margin-top:6px}
  section{padding-top:52px}
  h2{font-family:var(--disp);font-weight:800;text-transform:uppercase;letter-spacing:-.01em;font-size:22px;margin:0 0 4px}
  .sub{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--sepia);margin:0 0 20px}
  .rf{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
  .filtros{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 16px}
  .chip{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;background:transparent;border:1px solid var(--linea);color:var(--tinta-2);padding:9px 12px;cursor:pointer;display:inline-block;-webkit-user-select:none;user-select:none}
  .grupo,.dia,.mleg-dia{transition:opacity .18s}
  %(css_filtros)s
  .lienzo{background:var(--papel-2);border:1px solid var(--linea);padding:6px}
  .lienzo svg{display:block;width:100%%;height:auto}
  .solo-movil{display:none}
  .leyenda{display:flex;flex-wrap:wrap;gap:14px;margin:14px 0 0;font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--tinta-2)}
  .leyenda i{display:inline-block;width:20px;height:3px;vertical-align:middle;margin-right:6px}
  .nota{font-size:13.5px;color:var(--tinta-2);margin:12px 0 0;max-width:70ch}
  .mleg{display:none;margin-top:12px}
  .mleg-dia{display:flex;align-items:baseline;gap:8px;padding:9px 0;border-bottom:1px solid var(--linea)}
  .mleg-dia:last-child{border-bottom:0}
  .mleg-dia i{flex:0 0 auto;width:12px;height:12px;border-radius:50%%;margin-top:2px}
  .mleg-dia b{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;white-space:nowrap}
  .mleg-dia span{font-size:13px;color:var(--tinta-2);line-height:1.45}
  .banda{display:flex;height:30px;border:1px solid var(--linea);font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;align-items:center;background:var(--papel-2)}
  .banda div{height:100%%;display:flex;align-items:center;justify-content:center;border-right:1px solid var(--linea);color:var(--tinta-2)}
  .banda div:last-child{border-right:0}
  .banda .abierto{background:#DCE6E1;color:var(--tinta);font-weight:700}
  .banda .rodar{background:#EDEAE0}
  .dia{border-top:2px solid var(--tinta);margin-top:34px;padding-top:14px}
  .dia-cab{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
  .dia-num{font-family:var(--disp);font-size:44px;font-weight:800;line-height:.8;letter-spacing:-.04em}
  .dia-tit{font-family:var(--disp);font-size:17px;font-weight:800;text-transform:uppercase;letter-spacing:-.01em}
  .dia-meta{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--tinta-2);margin-left:auto}
  table{width:100%%;border-collapse:collapse;margin-top:12px}
  td{padding:9px 8px;border-bottom:1px solid var(--linea);vertical-align:top}
  tr.parada td{background:#EFEBE0}
  .hora{font-family:var(--mono);font-size:12px;white-space:nowrap;width:64px;color:var(--tinta-2)}
  .lugar{font-family:var(--disp);font-weight:700;font-size:15px}
  tr.paso .lugar{font-weight:400;font-family:var(--body);color:var(--tinta-2);font-size:14.5px}
  .det{font-size:14px;color:var(--tinta-2)}
  .tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;border:1px solid currentColor;padding:2px 5px;margin-left:8px;white-space:nowrap;display:inline-block}
  .avisos{display:flex;flex-wrap:wrap;gap:1px;background:var(--linea);border:1px solid var(--linea);margin-top:10px}
  .aviso{background:var(--papel-2);padding:18px;flex:1 1 260px}
  .aviso h3{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 8px;color:var(--sepia)}
  .aviso p{margin:0;font-size:14.5px;color:var(--tinta-2)}
  .aviso.alerta{background:#F4EAE4}
  .aviso.alerta h3{color:#C0562B}
  footer{margin-top:56px;padding-top:18px;border-top:1px solid var(--linea);font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;color:var(--tinta-2);line-height:1.9}
  @media (min-width:760px){h1{font-size:70px}}
  @media (max-width:700px){
    .wrap{padding:0 16px 60px}
    .top{padding:32px 0 22px}
    h1{font-size:38px}
    .lede{font-size:15px}
    section{padding-top:38px}
    .solo-desktop{display:none}
    .solo-movil{display:block}
    .leyenda{display:none}
    .mleg{display:block}
    .chip{padding:10px 13px;font-size:10.5px}
    .lienzo{padding:4px}
    .banda{display:block;height:auto}
    .banda div{height:32px;width:100%%;border-right:0;border-bottom:1px solid var(--linea);justify-content:flex-start;padding-left:12px;font-size:10px}
    .banda div:last-child{border-bottom:0}
    .fact{flex:1 1 44%%;padding:10px 12px}
    .fact b{font-size:22px}
    .dia{margin-top:26px}
    .dia-num{font-size:34px}
    .dia-meta{margin-left:0;width:100%%;margin-top:6px;font-size:9.5px}
    table,tbody,tr,td{display:block;width:auto}
    table{margin-top:8px}
    tr{border-bottom:1px solid var(--linea);padding:9px 0}
    tr.parada{background:#EFEBE0;padding:9px 10px;border-bottom:0;margin-bottom:2px}
    tr.parada td{background:transparent}
    td{border:0;padding:0}
    .hora{display:inline-block;width:auto;margin-right:9px;color:var(--tinta);font-weight:700}
    .lugar{display:inline;font-size:14.5px}
    .det{font-size:13px;margin-top:4px;line-height:1.45}
    .aviso{padding:15px;flex:1 1 100%%}
    .nota{font-size:13px}
  }
  @page{size:A4;margin:13mm 12mm 12mm}
  @media print{
    *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
    body{background:#fff;font-size:10.3pt;line-height:1.5}
    .wrap{max-width:none;padding:0}
    .filtros{display:none}
    .grupo,.dia,.mleg-dia{opacity:1 !important}
    .solo-desktop{display:block !important}
    .solo-movil{display:none !important}
    .leyenda{display:flex !important}
    .mleg{display:none !important}
    .top{padding:0 0 20px;min-height:132mm}
    h1{font-size:50pt}
    .lede{font-size:11pt;max-width:64ch}
    .fact{flex:1 1 105px}
    .fact b{font-size:20pt}
    section{padding-top:26px}
    #sec-reloj,#itinerario,#sec-avisos{break-before:page;page-break-before:always;padding-top:0}
    h2,.sub{break-after:avoid;page-break-after:avoid}
    h2{font-size:16pt;margin-bottom:2px}
    .lienzo,.avisos,.aviso,.dia,footer,.leyenda,.banda{break-inside:avoid;page-break-inside:avoid}
    .dia{margin-top:18px}
    .dia-num{font-size:28pt}
    td{padding:5.5px 7px}
    .nota{font-size:9.5pt}
  }
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <p class="eyebrow">%(eyebrow)s</p>
    <h1>%(h1)s<span>%(h1sub)s</span></h1>
    <p class="lede">%(lede)s</p>
    <div class="facts">%(facts)s</div>
  </header>
  %(sec_banda)s
  <div class="app">
  %(radios)s
  <div class="app-cuerpo">
  <section id="sec-circuito">
    <h2>%(titulo_mapa)s</h2>
    <p class="sub">%(sub_mapa)s</p>
    <div class="filtros">%(chips)s</div>
    <div class="lienzo solo-desktop">%(mapa_d)s</div>
    <div class="lienzo solo-movil">%(mapa_m)s</div>
    <div class="leyenda">%(leyenda)s</div>
    <div class="mleg">%(mleg)s</div>
    <p class="nota">%(nota_mapa)s</p>
  </section>
  %(sec_perfil)s
  %(sec_corr)s
  <section id="itinerario">
    <h2>Itinerario</h2>
    <p class="sub">%(sub_itinerario)s</p>
    %(dias)s
  </section>
  </div>
  </div>
  <section id="sec-avisos">
    <h2>%(titulo_avisos)s</h2>
    <p class="sub">%(sub_avisos)s</p>
    <div class="avisos">%(avisos)s</div>
  </section>
  <footer>%(pie)s</footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("uso: generar_documento.py plan.json salida.html")
    with open(sys.argv[1], encoding="utf-8") as fh:
        plan = json.load(fh)
    html = construir(plan)
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(html)
    print("HTML escrito: %s (%d KB, sin JavaScript: %s)" % (
        sys.argv[2], len(html.encode("utf-8")) // 1024, "<script" not in html.lower()))
