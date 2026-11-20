"""Render the CAD Lifeboat org avatar and profile banner (SVG, and PNG with cairosvg)."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
BG, BG2 = '#0f1720', '#16212d'
INK, MUTED, ORANGE, WHITE, LINE = '#eef3f8', '#9fb0c2', '#f08a24', '#f4f6f8', '#2a3a4c'
FONT = "'Noto Sans', 'Helvetica Neue', Arial, sans-serif"


def ring(cx, cy, r, w):
    """Life ring: alternating orange and white quarters, with rope notches."""
    import math
    parts = []
    for i in range(8):
        a0, a1 = math.radians(i * 45 - 90), math.radians((i + 1) * 45 - 90)
        ro, ri = r + w / 2, r - w / 2
        p = [(cx + ro * math.cos(a0), cy + ro * math.sin(a0)), (cx + ro * math.cos(a1), cy + ro * math.sin(a1)),
             (cx + ri * math.cos(a1), cy + ri * math.sin(a1)), (cx + ri * math.cos(a0), cy + ri * math.sin(a0))]
        color = ORANGE if i % 2 == 0 else WHITE
        parts.append(f'<path d="M{p[0][0]:.1f},{p[0][1]:.1f} A{ro},{ro} 0 0 1 {p[1][0]:.1f},{p[1][1]:.1f} '
                     f'L{p[2][0]:.1f},{p[2][1]:.1f} A{ri},{ri} 0 0 0 {p[3][0]:.1f},{p[3][1]:.1f} Z" fill="{color}"/>')
    return ''.join(parts)


def cube(x, y, s):
    h = s * 0.5
    return (f'<path d="M{x},{y} l{s},{h} l-{s},{h} l-{s},-{h} z" fill="#f6b26b"/>'
            f'<path d="M{x - s},{y + h} l{s},{h} v{s} l-{s},-{h} z" fill="#d9731a"/>'
            f'<path d="M{x + s},{y + h} l-{s},{h} v{s} l{s},-{h} z" fill="#b85f12"/>')


def mark(cx, cy, k):
    """The logo: a CAD part inside a life ring."""
    return ring(cx, cy, 150 * k, 56 * k) + cube(cx, cy - 64 * k, 64 * k)


def avatar(size=512):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512">'
            f'<rect width="512" height="512" fill="{BG}"/>{mark(256, 256, 1.15)}</svg>')


def banner(w=1280, h=320):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG2}"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/><rect width="{w}" height="6" fill="{ORANGE}"/>
{mark(170, 163, 0.62)}
<text x="320" y="150" font-family="{FONT}" font-size="72" font-weight="800" fill="{INK}">CAD Lifeboat</text>
<text x="322" y="205" font-family="{FONT}" font-size="28" fill="{MUTED}">Get your designs out of the cloud and onto your own disk.</text>
<text x="322" y="250" font-family="{FONT}" font-size="20" fill="{MUTED}">Free, open-source tools · MIT licensed · nothing leaves your computer</text>
</svg>
'''


def social(w=1280, h=640):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG2}"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/><rect width="{w}" height="6" fill="{ORANGE}"/>
{mark(1000, 320, 1.0)}
<text x="80" y="290" font-family="{FONT}" font-size="84" font-weight="800" fill="{INK}">CAD Lifeboat</text>
<text x="82" y="350" font-family="{FONT}" font-size="32" fill="{MUTED}">Get your designs out of the cloud</text>
<text x="82" y="392" font-family="{FONT}" font-size="32" fill="{MUTED}">and onto your own disk.</text>
<text x="82" y="460" font-family="{FONT}" font-size="22" fill="{MUTED}">Free, open-source tools · github.com/cad-lifeboat</text>
</svg>
'''


def main():
    import cairosvg
    for name, svg, size in [('avatar', avatar(), None), ('banner', banner(), None), ('social', social(), None)]:
        (HERE / (name + '.svg')).write_text(svg, encoding='utf-8')
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(HERE / (name + '.png')))
    print('ok')


if __name__ == '__main__':
    main()
