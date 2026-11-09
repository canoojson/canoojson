#!/usr/bin/env python3
"""Genera los SVG con estética synthwave roja del README: títulos de sección, «Sobre mí»,
stack y tarjetas de proyectos, en castellano e inglés.

GitHub no deja poner CSS propio en un README, así que el estilo va dentro de imágenes SVG.
La fuente (Orbitron) y los iconos van incrustados: GitHub sirve las imágenes sin dejarles
cargar recursos externos.

Uso: python3 tools/cards.py  (desde la raíz del repo)
"""
import base64
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "tools" / "vendor"
OUT = ROOT / "assets"

RED = "#ff2a4d"
ORANGE = "#ff6b3d"
TEXT = "#fff1f3"
MUTED = "#ffb3be"
DIM = "#9a6a74"
BODY_FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"

FONT = base64.b64encode((VENDOR / "orbitron-700.woff2").read_bytes()).decode()

W = 900  # ancho de diseño; en el README se escalan al 100 %


def defs(extra=""):
    return f"""<defs>
    <style>
      @font-face {{ font-family: 'Orbitron'; font-weight: 700; src: url(data:font/woff2;base64,{FONT}) format('woff2'); }}
      .o {{ font-family: 'Orbitron', 'Arial Black', sans-serif; font-weight: 700; }}
      .b {{ font-family: {BODY_FONT}; }}
    </style>
    <linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14060c"/><stop offset="1" stop-color="#07030a"/></linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{RED}" stroke-opacity=".07"/></pattern>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    {extra}
  </defs>"""


def panel(w, h):
    """Fondo de tarjeta: degradado oscuro, rejilla tenue y borde de neón."""
    return f"""<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="16" fill="url(#bg)"/>
  <rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="16" fill="url(#grid)"/>
  <rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="16" fill="none" stroke="url(#neon)" stroke-width="2" filter="url(#glow)"/>"""


def svg(w, h, body, label, extra_defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
  {defs(extra_defs)}
  {body}
</svg>
"""


def wrap(text, max_chars):
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > max_chars:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line] if line else lines


def write(name, content):
    (OUT / name).write_text(content)
    print(f"assets/{name}")


# ---------- títulos de sección ----------

HEADERS = {
    "about": ("SOBRE MÍ", "ABOUT ME"),
    "stack": ("CON QUÉ TRABAJO", "TECH STACK"),
    "projects": ("PROYECTOS DESTACADOS", "FEATURED PROJECTS"),
    "music": ("QUÉ ESTOY ESCUCHANDO", "WHAT I'M LISTENING TO"),
    "games": ("A QUÉ JUEGO", "WHAT I PLAY"),
    "fandoms": ("MUNDOS DE LOS QUE SOY FAN", "WORLDS I'M A FAN OF"),
    "contrib": ("MIS CONTRIBUCIONES", "MY CONTRIBUTIONS"),
}


def header(title):
    h = 64
    body = f"""<linearGradient id="line" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset=".6" stop-color="{RED}" stop-opacity=".25"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>"""
    content = f"""<rect x="4" y="16" width="5" height="30" rx="2" fill="url(#neon)" filter="url(#glow)"/>
  <text class="o" x="26" y="42" font-size="25" letter-spacing="4" fill="{TEXT}" filter="url(#glow)">{escape(title)}</text>
  <rect x="4" y="57" width="{W - 4}" height="2" fill="url(#line)"/>"""
    return svg(W, h, content, title, body)


# ---------- sobre mí ----------

ABOUT = {
    "es": [
        ("TRABAJO", "Desarrollador en AHORA"),
        ("ESTUDIOS", "Desarrollo de Aplicaciones Multiplataforma (DAM)"),
        ("ME GUSTA", "Android con Kotlin + Jetpack Compose y backend con Spring Boot"),
        ("TIEMPO LIBRE", "Herramientas para el día a día, como un asistente de voz o los AirPods en Linux"),
        ("SCOUTS", "Desarrollador web del grupo Impeesa 243 de Burjassot"),
    ],
    "en": [
        ("WORK", "Developer at AHORA"),
        ("STUDIES", "Multiplatform Application Development (DAM)"),
        ("I ENJOY", "Android with Kotlin + Jetpack Compose and backend with Spring Boot"),
        ("FREE TIME", "Tools for everyday use, like a voice assistant or AirPods on Linux"),
        ("SCOUTS", "Web developer for the Impeesa 243 Scout group in Burjassot"),
    ],
}


def about(rows):
    row_h, top = 46, 30
    h = top * 2 + row_h * len(rows) - 12
    parts = [panel(W, h)]
    for i, (label, value) in enumerate(rows):
        y = top + i * row_h + 20
        parts.append(f'<circle cx="38" cy="{y - 5}" r="3.5" fill="{RED}" filter="url(#glow)"/>')
        parts.append(f'<text class="o" x="56" y="{y}" font-size="13" letter-spacing="2.5" fill="{RED}">{escape(label)}</text>')
        parts.append(f'<text class="b" x="230" y="{y + 1}" font-size="17" fill="{TEXT}">{escape(value)}</text>')
        if i < len(rows) - 1:
            parts.append(f'<rect x="56" y="{y + 18}" width="{W - 92}" height="1" fill="{RED}" fill-opacity=".12"/>')
    return svg(W, h, "\n  ".join(parts), "Sobre mí / About me")


# ---------- stack ----------

ICONS = ["kotlin", "java", "cs", "py", "ts", "js", "react", "html", "css",
         "spring", "androidstudio", "mysql", "sqlite", "cloudflare", "git", "bash", "linux", "arch"]
WORK_STACK = ["SQL Server · T-SQL", "DevExpress", "Crystal Reports", "Qlik Sense", "FlexyGo"]


def chip(x, y, label, size=13):
    w = len(label) * size * 0.58 + 26
    return w, f"""<rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="{RED}" fill-opacity=".1" stroke="{RED}" stroke-opacity=".7"/>
  <text class="b" x="{x + w / 2:.0f}" y="{y + 20}" font-size="{size}" font-weight="600" text-anchor="middle" fill="{MUTED}">{escape(label)}</text>"""


def stack(work_label):
    per_row, size, gap = 9, 64, 18
    grid_w = per_row * size + (per_row - 1) * gap
    x0 = (W - grid_w) / 2
    parts = []
    for i, name in enumerate(ICONS):
        data = base64.b64encode((VENDOR / f"icon-{name}.svg").read_bytes()).decode()
        x = x0 + (i % per_row) * (size + gap)
        y = 32 + (i // per_row) * (size + gap)
        parts.append(f'<image href="data:image/svg+xml;base64,{data}" x="{x:.0f}" y="{y}" width="{size}" height="{size}"/>')
    rows = (len(ICONS) + per_row - 1) // per_row
    y = 32 + rows * (size + gap) + 14
    parts.append(f'<text class="o" x="{W / 2}" y="{y}" font-size="12" letter-spacing="3" text-anchor="middle" fill="{RED}">{escape(work_label)}</text>')
    # chips centrados
    widths = [len(c) * 13 * 0.58 + 26 for c in WORK_STACK]
    total = sum(widths) + 10 * (len(WORK_STACK) - 1)
    x = (W - total) / 2
    for c in WORK_STACK:
        w, s = chip(x, y + 14, c)
        parts.append(s)
        x += w + 10
    h = y + 14 + 30 + 30
    return svg(W, h, panel(W, h) + "\n  " + "\n  ".join(parts), "Stack")


# ---------- proyectos ----------

PROJECTS = [
    ("airpods", "AirPods en Linux", "AirPods on Linux",
     "Batería de los AirPods (también con la caja cerrada) y popup estilo iOS al abrir la caja.",
     "AirPods battery (even with the case closed) and an iOS-style popup when you open the case.",
     ["Python", "BLE", "BlueZ"]),
    ("finanzas", "Finanzas", "Finances",
     "PWA de finanzas personales autoalojada en Cloudflare.",
     "Self-hosted personal finance PWA on Cloudflare.",
     ["TypeScript", "Workers", "D1"]),
    ("portfolio", "Portfolio", "Portfolio",
     "Mi web personal: proyectos, música y juegos. canoojson.dev",
     "My personal site: projects, music and games. canoojson.dev",
     ["React", "Vite", "TypeScript"]),
    ("scouts", "Web Scouts", "Scouts website",
     "La web del grupo scout Impeesa 243 de Burjassot.",
     "Website for the Impeesa 243 Scout group in Burjassot.",
     ["HTML", "CSS", "JavaScript"]),
]


def project(title, desc, tags):
    w, h = 440, 170
    parts = [panel(w, h)]
    parts.append(f'<text class="o" x="26" y="46" font-size="19" letter-spacing="1.5" fill="{TEXT}" filter="url(#glow)">{escape(title)}</text>')
    parts.append(f'<path d="M{w - 44} 30h14v14M{w - 30} 30l-14 14" fill="none" stroke="{RED}" stroke-width="2.2" stroke-linecap="round" filter="url(#glow)"/>')
    for i, line in enumerate(wrap(desc, 56)[:3]):
        parts.append(f'<text class="b" x="26" y="{76 + i * 21}" font-size="14.5" fill="{MUTED}">{escape(line)}</text>')
    x = 26
    for t in tags:
        cw, s = chip(x, h - 46, t, 12)
        parts.append(s)
        x += cw + 8
    return svg(w, h, "\n  ".join(parts), title)


def main():
    OUT.mkdir(exist_ok=True)
    for key, (es, en) in HEADERS.items():
        write(f"h-{key}.svg", header(es))
        write(f"h-{key}.en.svg", header(en))
    write("about.svg", about(ABOUT["es"]))
    write("about.en.svg", about(ABOUT["en"]))
    write("stack.svg", stack("EN EL TRABAJO"))
    write("stack.en.svg", stack("AT WORK"))
    for key, t_es, t_en, d_es, d_en, tags in PROJECTS:
        write(f"p-{key}.svg", project(t_es, d_es, tags))
        write(f"p-{key}.en.svg", project(t_en, d_en, tags))


if __name__ == "__main__":
    main()
