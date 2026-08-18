# -*- coding: utf-8 -*-
"""HTML -> PDF A4 usando Chromium sin interfaz.

    python3 html_a_pdf.py salida.html salida.pdf ["pie de pagina"]

Renderiza con un viewport ancho para que se aplique la version de escritorio de
los graficos, no la movil.
"""
import sys, os, pathlib


def con_playwright(src, dst, pie):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1100, "height": 1400})
        pg.goto(pathlib.Path(src).absolute().as_uri(), wait_until="load")
        pg.wait_for_timeout(600)
        pg.emulate_media(media="print")
        pg.pdf(path=dst, format="A4", print_background=True, prefer_css_page_size=True,
               display_header_footer=True, header_template="<div></div>",
               footer_template=('<div style="width:100%%;font-family:monospace;font-size:7pt;'
                                'color:#7a857f;padding:0 12mm"><table style="width:100%%"><tr>'
                                '<td style="text-align:left">%s</td>'
                                '<td style="text-align:right"><span class="pageNumber"></span>'
                                ' / <span class="totalPages"></span></td></tr></table></div>') % pie)
        b.close()


def con_wkhtmltopdf(src, dst):
    import subprocess
    subprocess.check_call(["wkhtmltopdf", "--enable-local-file-access", "--page-size", "A4",
                           "--print-media-type", src, dst])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("uso: html_a_pdf.py entrada.html salida.pdf [pie]")
    src, dst = sys.argv[1], sys.argv[2]
    pie = sys.argv[3] if len(sys.argv) > 3 else ""
    try:
        con_playwright(src, dst, pie)
    except Exception as err:
        print("Playwright no disponible (%s); intento con wkhtmltopdf" % err)
        con_wkhtmltopdf(src, dst)
    print("PDF escrito: %s (%d KB)" % (dst, os.path.getsize(dst) // 1024))
