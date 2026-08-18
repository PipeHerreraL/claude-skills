#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Empaqueta una skill en un archivo .skill para subirla a claude.ai.

    python3 scripts/empaquetar.py plugins/planificador-rutas/skills/planificador-rutas

El .skill es un zip cuya raiz es la carpeta de la skill. Los archivos quedan en dist/.
En Claude Code no hace falta: alli las skills se instalan desde el marketplace.
"""
import sys, zipfile
from pathlib import Path

EXCLUIR = {"__pycache__", ".git", ".DS_Store", "node_modules", ".pytest_cache"}


def empaquetar(carpeta, destino="dist"):
    carpeta = Path(carpeta).resolve()
    if not (carpeta / "SKILL.md").exists():
        raise SystemExit("No hay SKILL.md en %s" % carpeta)
    salida = Path(destino).resolve()
    salida.mkdir(parents=True, exist_ok=True)
    archivo = salida / ("%s.skill" % carpeta.name)
    n = 0
    with zipfile.ZipFile(archivo, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(carpeta.rglob("*")):
            if not f.is_file():
                continue
            rel = f.relative_to(carpeta.parent)
            if any(p in EXCLUIR or p.endswith(".pyc") for p in rel.parts):
                continue
            z.write(f, rel)
            n += 1
    print("%s  (%d archivos, %d KB)" % (archivo, n, archivo.stat().st_size // 1024))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("uso: empaquetar.py <carpeta-de-la-skill> [destino]")
    empaquetar(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "dist")
