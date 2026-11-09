#!/usr/bin/env python3
"""Genera assets/banner.svg: atardecer synthwave rojo con suelo de rejilla animado.

Uso: python3 tools/banner.py  (desde la raíz del repo)
"""
W, H = 1200, 340
HZ = 205            # línea del horizonte
CX = W / 2
N = 12              # líneas horizontales del suelo
DUR = 3.2           # segundos que tarda una línea en llegar abajo

def floor_lines():
    out = []
    # profundidad z de 1 (pegado a la cámara) a 12 (horizonte): y = HZ + k/z
    k = (H - HZ) * 1.0
    steps = 24
    ys = [HZ + k / (12 - 11 * t / steps) for t in range(steps + 1)]
    values = ";".join(f"{y:.1f}" for y in ys)
    for i in range(N):
        begin = -DUR * i / N
        y0 = ys[round(steps * i / N)]  # posición inicial (por si el visor no anima)
        out.append(
            f'<line x1="0" x2="{W}" y1="{y0:.1f}" y2="{y0:.1f}" stroke="#ff2a4d" stroke-width="1.6">'
            f'<animate attributeName="y1" values="{values}" dur="{DUR}s" begin="{begin:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" values="{values}" dur="{DUR}s" begin="{begin:.2f}s" repeatCount="indefinite"/>'
            f'</line>'
        )
    # líneas que fugan al centro del horizonte
    for j in range(-14, 15):
        x = CX + j * 110
        out.append(f'<line x1="{CX + j * 14:.1f}" y1="{HZ}" x2="{x:.1f}" y2="{H}" stroke="#ff2a4d" stroke-width="1.4"/>')
    return "\n    ".join(out)

def sun_stripes():
    # franjas que cortan la parte baja del sol, cada vez más gruesas
    out, y, h = [], 130, 3
    while y < HZ:
        out.append(f'<rect x="0" y="{y}" width="{W}" height="{h:.1f}" fill="black"/>')
        y += h + 9 - h * 0.6
        h += 2.2
    return "\n      ".join(out)

def mountains():
    pts_back = [(0, HZ), (90, 170), (180, 188), (270, 150), (360, 182), (430, 165), (500, HZ),
                (700, HZ), (770, 160), (850, 185), (930, 140), (1020, 178), (1110, 158), (1200, 176), (1200, HZ)]
    return " ".join(f"{x},{y}" for x, y in pts_back)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Sergio Cano · canoojson">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#05020a"/><stop offset=".55" stop-color="#1c0510"/><stop offset="1" stop-color="#3a0716"/>
    </linearGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffd27a"/><stop offset=".45" stop-color="#ff6b3d"/><stop offset="1" stop-color="#ff1744"/>
    </linearGradient>
    <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1a030b"/><stop offset="1" stop-color="#05020a"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ff2a4d" stop-opacity="0"/><stop offset=".25" stop-color="#ff2a4d" stop-opacity="1"/>
    </linearGradient>
    <mask id="sunmask">
      <rect width="{W}" height="{H}" fill="white"/>
      {sun_stripes()}
    </mask>
    <mask id="floormask"><rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#fade)"/></mask>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="halo" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#ff2a4d" stop-opacity=".45"/><stop offset="1" stop-color="#ff2a4d" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <style>
    .name {{ font: 900 76px 'Orbitron', 'Arial Black', 'Segoe UI', sans-serif; letter-spacing: 10px; }}
    .sub {{ font: 600 20px 'Segoe UI', Ubuntu, sans-serif; letter-spacing: 6px; fill: #ffc2cb; }}
    .flicker {{ animation: flicker 6s infinite; }}
    @keyframes flicker {{ 0%, 18%, 22%, 60%, 64%, 100% {{ opacity: 1; }} 20%, 62% {{ opacity: .55; }} }}
    .twinkle {{ animation: tw 3s ease-in-out infinite; }}
    @keyframes tw {{ 50% {{ opacity: .2; }} }}
  </style>

  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <g fill="#ffd6dc">
    <circle class="twinkle" cx="140" cy="40" r="1.4"/><circle cx="260" cy="90" r="1"/><circle class="twinkle" cx="380" cy="30" r="1.2" style="animation-delay:1s"/>
    <circle cx="820" cy="50" r="1.1"/><circle class="twinkle" cx="960" cy="95" r="1.4" style="animation-delay:.5s"/><circle cx="1080" cy="35" r="1"/>
    <circle cx="60" cy="120" r="1"/><circle class="twinkle" cx="1150" cy="130" r="1.2" style="animation-delay:2s"/><circle cx="700" cy="25" r="1"/>
  </g>

  <circle cx="{CX}" cy="{HZ - 10}" r="170" fill="url(#halo)"/>
  <circle cx="{CX}" cy="{HZ - 10}" r="105" fill="url(#sun)" mask="url(#sunmask)" filter="url(#softglow)"/>
  <polygon points="{mountains()}" fill="#0d0207" stroke="#ff2a4d" stroke-width="1.5" stroke-opacity=".7"/>

  <rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floor)"/>
  <g mask="url(#floormask)" filter="url(#softglow)">
    {floor_lines()}
  </g>
  <line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}" stroke="#ff6b7f" stroke-width="2" filter="url(#softglow)"/>

  <g class="flicker" filter="url(#glow)">
    <text class="name" x="{CX}" y="118" text-anchor="middle" fill="none" stroke="#ff2a4d" stroke-width="2.5">SERGIO CANO</text>
  </g>
  <text class="name" x="{CX}" y="118" text-anchor="middle" fill="#fff1f3" fill-opacity=".92">SERGIO CANO</text>
  <text class="sub" x="{CX}" y="300" text-anchor="middle" filter="url(#softglow)">DEV · VALENCIA · ARCH LINUX</text>
</svg>
'''

open("assets/banner.svg", "w").write(svg)
print("assets/banner.svg")
