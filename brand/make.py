"""Render the CAD Lifeboat org avatar and profile banner (SVG, and PNG with cairosvg)."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
BG, BG2 = '#0f1720', '#16212d'
INK, MUTED, ORANGE, WHITE, LINE, TEAL = '#eef3f8', '#9fb0c2', '#f08a24', '#f4f6f8', '#2a3a4c', '#3fb6c8'
FONT = "'Noto Sans', 'Helvetica Neue', Arial, sans-serif"


def cube(x, y, s, top='#e9eff5', left='#aebccb', right='#8194a8'):
    """An isometric CAD part (steel grey, so it reads as cargo, not as part of the boat)."""
    h = s * 0.5
    edge = f'stroke="#f7fafc" stroke-width="{max(s / 40, 1):.1f}" stroke-linejoin="round"'
    return (f'<path d="M{x},{y} l{s},{h} l-{s},{h} l-{s},-{h} z" fill="{top}" {edge}/>'
            f'<path d="M{x - s},{y + h} l{s},{h} v{s} l-{s},-{h} z" fill="{left}"/>'
            f'<path d="M{x + s},{y + h} l-{s},{h} v{s} l{s},-{h} z" fill="{right}"/>'
            f'<path d="M{x},{y + s} v{s}" stroke="#d5dee8" stroke-width="{max(s / 50, 1):.1f}"/>')


def boat(cx, cy, k, uid):
    """A lifeboat: curved sheer, shaded orange hull, grab-line rope, sitting in two waves."""
    def P(x, y):
        return '%.1f,%.1f' % (cx + x * k, cy + y * k)
    defs = (f'<linearGradient id="hull-{uid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#f7983a"/><stop offset="1" stop-color="#d4670f"/></linearGradient>'
            f'<clipPath id="above-{uid}"><rect x="{cx - 260 * k:.1f}" y="{cy - 420 * k:.1f}" '
            f'width="{520 * k:.1f}" height="{466 * k:.1f}"/></clipPath>')
    # Deck line rises at bow (right) and stern (left).
    hull = (f'<path d="M{P(-178, -40)} Q{P(-150, -28)} {P(-100, -28)} L{P(100, -28)} Q{P(150, -28)} {P(182, -44)} '
            f'L{P(134, 52)} Q{P(0, 80)} {P(-132, 52)} Z" fill="url(#hull-{uid})"/>'
            f'<path d="M{P(-178, -40)} Q{P(-150, -28)} {P(-100, -28)} L{P(100, -28)} Q{P(150, -28)} {P(182, -44)}" '
            f'fill="none" stroke="#ffb469" stroke-width="{4 * k:.1f}" stroke-linecap="round"/>'
            )
    xs = list(range(-120, 121, 40))
    rope = ''.join(f'<path d="M{P(x, -6)} Q{P(x + 20, 14)} {P(x + 40, -6)}" fill="none" stroke="{WHITE}" '
                   f'stroke-width="{5 * k:.1f}" stroke-linecap="round"/>' for x in xs[:-1])
    rope += ''.join(f'<circle cx="{cx + x * k:.1f}" cy="{cy - 6 * k:.1f}" r="{4.5 * k:.1f}" fill="#b45410"/>' for x in xs)

    def wave(y, color, opacity, width):
        return (f'<path d="M{P(-220, y)} q{26 * k:.1f},{-14 * k:.1f} {52 * k:.1f},0 ' + ' '.join(
            f't{52 * k:.1f},0' for _ in range(7)) + f'" fill="none" stroke="{color}" stroke-width="{width * k:.1f}" '
            f'stroke-linecap="round" opacity="{opacity}"/>')
    back = wave(30, '#2a8fa0', 0.9, 7)
    front = wave(48, TEAL, 1, 9) + wave(84, TEAL, 0.45, 7)
    # The inside of the boat: far rim and a darker interior, drawn behind the cargo.
    inside = (f'<path d="M{P(-170, -40)} Q{P(-140, -50)} {P(-100, -50)} L{P(100, -50)} Q{P(140, -50)} {P(174, -46)} '
              f'L{P(182, -44)} Q{P(150, -28)} {P(100, -28)} L{P(-100, -28)} Q{P(-150, -28)} {P(-178, -40)} Z" '
              f'fill="#9c4a0e"/>')
    return (f'<defs>{defs}</defs>' + back + inside,
            f'<g clip-path="url(#above-{uid})">' + hull + rope + '</g>' + front)


def mark(cx, cy, k, uid='m'):
    """The logo: your CAD part riding in a lifeboat (inside, cargo, then the near side of the hull)."""
    behind, front = boat(cx, cy, k, uid)
    return behind + cube(cx, cy - 146 * k, 84 * k) + front


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
