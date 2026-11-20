"""Render the CAD Lifeboat org avatar and profile banner (SVG, and PNG with cairosvg)."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
BG, BG2 = '#0f1720', '#16212d'
INK, MUTED, ORANGE, WHITE, LINE, TEAL = '#eef3f8', '#9fb0c2', '#f08a24', '#f4f6f8', '#2a3a4c', '#3fb6c8'
FONT = "'Noto Sans', 'Helvetica Neue', Arial, sans-serif"


def cube(x, y, s, top='#e4ebf2', left='#a9b8c8', right='#7f91a5'):
    """An isometric CAD part (steel grey, so it reads as cargo, not as part of the boat)."""
    h = s * 0.5
    return (f'<path d="M{x},{y} l{s},{h} l-{s},{h} l-{s},-{h} z" fill="{top}"/>'
            f'<path d="M{x - s},{y + h} l{s},{h} v{s} l-{s},-{h} z" fill="{left}"/>'
            f'<path d="M{x + s},{y + h} l-{s},{h} v{s} l{s},-{h} z" fill="{right}"/>')


def boat(cx, cy, k):
    """A lifeboat: orange hull with a rope line along its side, sitting on two waves."""
    def P(x, y):
        return '%.1f,%.1f' % (cx + x * k, cy + y * k)
    hull = (f'<path d="M{P(-170, -30)} L{P(170, -30)} L{P(128, 52)} Q{P(0, 78)} {P(-128, 52)} Z" '
            f'fill="{ORANGE}"/>'
            f'<path d="M{P(-170, -30)} L{P(170, -30)} L{P(164, -18)} L{P(-164, -18)} Z" fill="#c4600f"/>')
    rope = ''.join(f'<path d="M{P(x, -4)} Q{P(x + 17, 12)} {P(x + 34, -4)}" fill="none" stroke="{WHITE}" '
                   f'stroke-width="{5 * k:.1f}" stroke-linecap="round"/>' for x in range(-136, 136, 34))
    waves = ''.join(f'<path d="M{P(-210, y)} q{26 * k:.1f},{-14 * k:.1f} {52 * k:.1f},0 t{52 * k:.1f},0 '
                    f't{52 * k:.1f},0 t{52 * k:.1f},0 t{52 * k:.1f},0 t{52 * k:.1f},0 t{52 * k:.1f},0 t{52 * k:.1f},0" '
                    f'fill="none" stroke="{TEAL}" stroke-width="{8 * k:.1f}" stroke-linecap="round" opacity="{o}"/>'
                    for y, o in ((50, 1), (86, 0.55)))
    # The hull is cut at the waterline, so the boat sits in the water on any background.
    clip = (f'<clipPath id="above-water"><rect x="{cx - 240 * k:.1f}" y="{cy - 400 * k:.1f}" '
            f'width="{480 * k:.1f}" height="{450 * k:.1f}"/></clipPath>')
    return clip + '<g clip-path="url(#above-water)">' + hull + rope + '</g>' + waves


def mark(cx, cy, k):
    """The logo: your CAD part riding in a lifeboat."""
    return cube(cx, cy - 150 * k, 78 * k) + boat(cx, cy, k)


def avatar(size=512):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512">'
            f'<rect width="512" height="512" fill="{BG}"/>{mark(256, 300, 1.05)}</svg>')


def banner(w=1280, h=320):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG2}"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/><rect width="{w}" height="6" fill="{ORANGE}"/>
{mark(165, 205, 0.55)}
<text x="320" y="150" font-family="{FONT}" font-size="72" font-weight="800" fill="{INK}">CAD Lifeboat</text>
<text x="322" y="205" font-family="{FONT}" font-size="28" fill="{MUTED}">Get your designs out of the cloud and onto your own disk.</text>
<text x="322" y="250" font-family="{FONT}" font-size="20" fill="{MUTED}">Free, open-source tools · MIT licensed · nothing leaves your computer</text>
</svg>
'''


def social(w=1280, h=640):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG2}"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/><rect width="{w}" height="6" fill="{ORANGE}"/>
{mark(1000, 380, 1.0)}
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
