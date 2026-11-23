"""Hand-built SVG line vignettes for the book edition. Each returns an SVG string (viewBox 0 0 600 220)."""
import math

W, H = 600, 220


def svg(body, label, uid):
    return (f'<svg class="vg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="{uid}-t">'
            f'<title id="{uid}-t">{label}</title>{body}</svg>')


# ---------- building blocks ----------
def house(x, base, w, h, step=11, steps=2, door=True, windows=2, door_at=0.5):
    """Hui-style house: white wall with stepped 'horse-head' gables capped in dark tile."""
    n = 2 * steps + 1
    seg = w / n
    ys = [base - h - min(i, n - 1 - i) * step for i in range(n)]
    pts = [(x, base)]
    for i, y in enumerate(ys):
        pts += [(x + i * seg, y), (x + (i + 1) * seg, y)]
    pts.append((x + w, base))
    poly = ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts)
    out = [f'<polygon class="wall" points="{poly}"/>']
    for i, y in enumerate(ys):
        x0, x1 = x + i * seg - 3, x + (i + 1) * seg + 3
        out.append(f'<line class="cap" x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}"/>')
        # upturned tips where the wall steps down
        if i <= steps:
            out.append(f'<path class="line" d="M{x0:.1f} {y:.1f} l-4 -4"/>')
        if i >= steps:
            out.append(f'<path class="line" d="M{x1:.1f} {y:.1f} l4 -4"/>')
    wy = base - h * 0.62
    for k in range(windows):
        wx = x + w * (k + 1) / (windows + 1) - 4
        if door and abs((wx + 4) - (x + w * door_at)) < 14:
            continue
        out.append(f'<rect class="dark" x="{wx:.1f}" y="{wy:.1f}" width="8" height="10" rx="1"/>')
    if door:
        dx = x + w * door_at - 7
        out.append(f'<path class="line" d="M{dx - 5:.1f} {base - 30:.1f} h24"/>')
        out.append(f'<rect class="dark" x="{dx:.1f}" y="{base - 25:.1f}" width="14" height="25" rx="1"/>')
    return '\n'.join(out)


def water(y, uid, scene, ripples):
    """Mirror `scene` below the waterline, clipped, with ripple strokes."""
    r = [f'<line class="ripple" x1="{x1}" y1="{yy}" x2="{x2}" y2="{yy}"/>' for x1, x2, yy in ripples]
    return (f'<clipPath id="{uid}-w"><rect x="0" y="{y}" width="{W}" height="{H - y}"/></clipPath>'
            f'<rect class="water" x="0" y="{y}" width="{W}" height="{H - y}"/>'
            f'<g clip-path="url(#{uid}-w)"><g opacity=".3" transform="translate(0 {2 * y}) scale(1 -1)">{scene}</g></g>'
            f'<line class="line" x1="0" y1="{y}" x2="{W}" y2="{y}"/>' + ''.join(r))


def pad(cx, cy, rx, ry):
    """A flat-bottomed pine needle pad, the way Huangshan pines grow in layers."""
    return (f'<path class="pine" d="M{cx - rx} {cy} '
            f'Q{cx - rx * .75} {cy - ry * .9} {cx - rx * .3} {cy - ry * .75} '
            f'Q{cx - rx * .05} {cy - ry * 1.25} {cx + rx * .35} {cy - ry * .85} '
            f'Q{cx + rx * .8} {cy - ry * 1.0} {cx + rx} {cy} Z"/>')


def far_ridge(points, cls='far'):
    return f'<polyline class="{cls}" points="{" ".join(f"{a},{b}" for a, b in points)}"/>'


# ---------- scenes ----------
def nanhu_bridge():
    """宏村 · 南湖画桥: arched stone bridge across South Lake, houses behind."""
    wl = 168
    houses = ''.join([
        house(10, wl, 86, 58, windows=2, door=False),
        house(90, wl, 84, 76, windows=2, door=False),
        house(424, wl, 80, 70, windows=1, door=False),
        house(498, wl, 96, 56, windows=2, door=False),
    ])
    # bridge: a low deck with one round arch
    bridge = (f'<path class="wall" d="M184 {wl} L190 146 Q300 100 410 146 L416 {wl} L336 {wl} '
              f'A36 36 0 0 0 264 {wl} Z"/>'
              f'<path class="line" d="M184 144 Q300 98 416 144"/>'
              + ''.join(f'<line class="line" x1="{x}" y1="{144 - (1 - ((x - 300) / 116) ** 2) * 23:.1f}" x2="{x}" y2="{136 - (1 - ((x - 300) / 116) ** 2) * 23:.1f}"/>' for x in range(200, 410, 22))
              + f'<path class="line" d="M190 136 Q300 90 410 136"/>')
    scene = houses + bridge
    willow = ''
    rip = [(40, 90, 182), (220, 270, 190), (330, 380, 184), (450, 520, 196), (110, 150, 204)]
    return svg(far_ridge([(0, 92), (70, 74), (130, 86), (220, 60), (300, 80), (380, 66), (470, 84), (540, 70), (600, 86)])
               + scene + willow + water(wl, 'nh', scene, rip), '宏村南湖画桥线描', 'vg-nh')


def moon_pond():
    """宏村 · 月沼: houses wrapped around the half-moon pond."""
    wl = 150
    houses = ''.join([
        house(10, wl, 80, 66, windows=2, door=False),
        house(84, wl, 96, 82, steps=2, windows=2),
        house(174, wl, 72, 60, windows=1, door=False),
        house(240, wl, 120, 92, steps=3, step=10, windows=3, door=True),  # 汪氏宗祠-like hall
        house(354, wl, 76, 64, windows=1, door=False),
        house(424, wl, 92, 78, windows=2),
        house(510, wl, 84, 60, windows=2, door=False),
    ])
    pond = (f'<clipPath id="mp-p"><path d="M30 {wl} Q300 236 570 {wl} Z"/></clipPath>'
            f'<path class="water" d="M30 {wl} Q300 236 570 {wl} Z"/>'
            f'<g clip-path="url(#mp-p)"><g opacity=".3" transform="translate(0 {2 * wl}) scale(1 -1)">{houses}</g></g>'
            f'<path class="line" d="M30 {wl} Q300 236 570 {wl}"/>'
            f'<line class="line" x1="0" y1="{wl}" x2="{W}" y2="{wl}"/>'
            + ''.join(f'<line class="ripple" x1="{a}" y1="{y}" x2="{b}" y2="{y}"/>'
                      for a, b, y in [(150, 210, 164), (300, 360, 172), (420, 470, 162), (240, 280, 182)]))
    # paved ground in front of the pond edge
    stones = ''.join(f'<line class="far" x1="{x}" y1="{wl + 4}" x2="{x - 6}" y2="{wl + 10}"/>' for x in range(20, 600, 36))
    return svg(houses + pond + stones, '宏村月沼线描', 'vg-mp')


def welcome_pine():
    """黄山 · 迎客松: an old pine on granite, one long branch held out."""
    rock = ('<path class="rock" d="M0 220 L0 150 L40 128 L78 138 L112 112 L150 126 L196 150 L232 186 L260 220 Z"/>'
            + ''.join(f'<path class="line" d="{d}"/>' for d in
                      ['M60 140 l-6 40', 'M110 118 l4 50', 'M150 130 l-8 46', 'M196 152 l-10 40']))
    peaks = (far_ridge([(250, 220), (300, 120), (330, 150), (372, 70), (404, 128), (440, 96), (488, 160), (540, 110), (600, 150)])
             + far_ridge([(372, 70), (378, 120)]) + far_ridge([(440, 96), (436, 140)]))
    trunk = ('<path class="wood" d="M118 116 C116 96 124 82 136 72 C148 62 150 52 146 40 L154 38 '
             'C160 54 156 68 144 80 C134 90 128 102 128 118 Z"/>'
             '<path class="line" d="M118 116 C116 96 124 82 136 72 C148 62 150 52 146 40 M154 38 '
             'C160 54 156 68 144 80 C134 90 128 102 128 118"/>')
    arm = ('<path class="line wood-line" d="M138 76 C190 70 240 82 300 76 C330 73 352 78 372 86"/>'
           '<path class="line wood-line" d="M144 58 C170 50 190 54 212 48"/>')
    pads = ''.join(pad(*p) for p in [
        (150, 40, 34, 14), (196, 50, 30, 12), (176, 34, 24, 10),
        (236, 80, 30, 12), (290, 76, 34, 13), (346, 82, 34, 12), (382, 92, 22, 9),
    ])
    return svg(peaks + rock + trunk + arm + pads, '黄山迎客松线描', 'vg-wp')


def sunrise_peaks():
    """黄山 · 始信峰日出: granite pillars standing out of the sea of clouds."""
    sun = ('<circle class="sun" cx="430" cy="118" r="34"/>'
           + ''.join(f'<line class="ray" x1="{430 + 46 * math.cos(a):.1f}" y1="{118 - 46 * math.sin(a):.1f}" '
                     f'x2="{430 + 62 * math.cos(a):.1f}" y2="{118 - 62 * math.sin(a):.1f}"/>'
                     for a in [math.radians(d) for d in range(20, 170, 20)]))
    peaks = ('<path class="rock" d="M70 220 L84 92 L100 70 L118 88 L126 150 L150 120 L170 60 L186 40 L202 58 L214 132 L240 220 Z"/>'
             '<path class="rock" d="M300 220 L318 120 L340 104 L356 128 L372 220 Z"/>'
             + ''.join(f'<path class="line" d="{d}"/>' for d in
                       ['M100 80 l-4 60', 'M186 48 l2 70', 'M170 70 l-6 60', 'M340 112 l-2 50']))
    pine = pad(186, 42, 18, 8) + pad(100, 70, 14, 6) + '<path class="line" d="M186 42 v-4 M100 70 v-3"/>'
    clouds = ''.join(
        f'<path class="cloud" d="M{x} {y} q{w * .15} -{h} {w * .3} 0 q{w * .15} -{h * 1.3} {w * .35} 0 '
        f'q{w * .1} -{h * .8} {w * .35} 0 Z"/>'
        for x, y, w, h in [(0, 176, 220, 16), (160, 186, 260, 18), (380, 172, 240, 15), (-20, 202, 300, 14), (260, 206, 360, 16)])
    base = f'<rect class="cloud" x="0" y="200" width="{W}" height="20" style="stroke:none"/>'
    return svg(sun + peaks + pine + clouds + base, '黄山始信峰云海日出线描', 'vg-sr')


def aoyu_lantern():
    """唐模 · 鳌鱼灯: a lit dragon-headed carp lantern raised on poles over the night crowd, chasing a pearl."""
    O = 'stroke="#3a1e16" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"'
    defs = ('<defs>'
            '<radialGradient id="ay-glow" cx="52%" cy="45%" r="55%">'
            '<stop offset="0" stop-color="#f3c66a" stop-opacity=".55"/>'
            '<stop offset=".45" stop-color="#e08a3c" stop-opacity=".18"/>'
            '<stop offset="1" stop-color="#e08a3c" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="ay-body" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#f08a5c"/><stop offset=".55" stop-color="#d4573c"/>'
            '<stop offset="1" stop-color="#a83a28"/></linearGradient>'
            '<clipPath id="ay-clip"><path d="M200 104 C240 64 300 52 350 62 C400 72 430 90 452 100 '
            'L456 124 C430 132 400 140 350 138 C290 136 236 140 200 136 Z"/></clipPath>'
            '</defs>')
    sky = ('<rect x="0" y="0" width="600" height="220" rx="10" fill="#1f2a33"/>'
           '<rect x="0" y="0" width="600" height="220" rx="10" fill="url(#ay-glow)"/>'
           + ''.join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#e9e4d6" opacity=".6"/>'
                     for x, y in [(40, 30), (130, 18), (250, 24), (420, 20), (560, 34), (580, 100), (20, 120)]))
    bursts = ''
    for cx, cy, r, c in [(70, 52, 40, '#e3b552'), (540, 46, 36, '#f0d2c6'), (500, 150, 22, '#e3b552'), (30, 150, 18, '#f0d2c6')]:
        for i in range(18):
            a = i * math.pi / 9
            bursts += (f'<line x1="{cx + r * .3 * math.cos(a):.1f}" y1="{cy + r * .3 * math.sin(a):.1f}" '
                       f'x2="{cx + r * math.cos(a):.1f}" y2="{cy + r * math.sin(a):.1f}" stroke="{c}" '
                       f'stroke-width="1.5" stroke-linecap="round" opacity=".85"/>')
            bursts += f'<circle cx="{cx + r * 1.15 * math.cos(a):.1f}" cy="{cy + r * 1.15 * math.sin(a):.1f}" r="1.4" fill="{c}"/>'
    # stepped gable rooftops behind the square
    roof = '<path fill="#2b3842" d="M0 220 V184 H14 V176 H30 V168 H58 V176 H74 V184 H96 V172 H112 V162 H140 V172 H156 V180 ' \
           'H440 V170 H456 V160 H486 V170 H502 V178 H520 V168 H536 V158 H566 V168 H582 V176 H600 V220 Z"/>'
    roof += ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="3" fill="#121a20"/>' for x, y, w in
                    [(10, 182, 24), (26, 174, 24), (54, 166, 24), (108, 160, 36), (452, 158, 38), (532, 156, 38)])
    roof += ''.join(f'<rect x="{x}" y="{y}" width="7" height="8" fill="#f3c66a" opacity=".8"/>' for x, y in [(40, 190), (122, 184), (466, 182), (548, 180)])
    poles = (f'<path d="M262 138 L244 220 M372 140 L392 220" stroke="#5a4230" stroke-width="4" stroke-linecap="round"/>'
             f'<path d="M300 136 L304 220" stroke="#5a4230" stroke-width="3" stroke-linecap="round"/>')
    small = ''
    for x, y, flip in [(170, 178, 1), (440, 184, -1), (520, 196, 1)]:
        small += (f'<g transform="translate({x} {y}) scale({flip} 1)">'
                  f'<line x1="0" y1="6" x2="2" y2="34" stroke="#5a4230" stroke-width="2"/>'
                  f'<path d="M-14 0 C-8 -9 8 -9 14 0 L22 -7 L20 0 L22 7 L14 0 C8 9 -8 9 -14 0 Z" fill="#e3b552" {O}/>'
                  f'<circle cx="-8" cy="-1" r="1.4" fill="#3a1e16"/></g>')
    crowd = ''.join(f'<circle cx="{x}" cy="{206 - (x * 7) % 6}" r="8" fill="#121a20"/>'
                    f'<rect x="{x - 12}" y="{212 - (x * 7) % 6}" width="24" height="14" rx="8" fill="#121a20"/>'
                    for x in range(10, 600, 26))
    fins = (f'<path d="M246 76 L258 52 L270 70 L288 46 L300 64 L318 42 L332 62 L348 46 L360 64 L376 54 L390 76 Z" fill="#e3b552" {O}/>'
            f'<path d="M250 138 C252 162 272 172 292 168 C282 158 278 148 282 138 Z" fill="#e3b552" {O}/>'
            f'<path d="M372 140 C378 160 396 168 414 162 C402 154 398 146 400 136 Z" fill="#e3b552" {O}/>')
    tail = (f'<path d="M450 100 C480 92 510 74 540 54 C532 82 514 100 502 112 C516 124 534 140 552 154 '
            f'C520 148 486 134 456 124 Z" fill="#e3b552" {O}/>'
            + ''.join(f'<path d="M458 112 L{x} {y}" stroke="#b9842c" stroke-width="1.2" fill="none"/>' for x, y in [(526, 70), (508, 104), (512, 124), (534, 146)]))
    body = f'<path d="M200 104 C240 64 300 52 350 62 C400 72 430 90 452 100 L456 124 C430 132 400 140 350 138 C290 136 236 140 200 136 Z" fill="url(#ay-body)"/>'
    scales = ''
    for row, y in enumerate(range(66, 146, 16)):
        for x in range(206 + (row % 2) * 11, 460, 22):
            scales += f'<path d="M{x} {y} a11 11 0 0 0 22 0" fill="none" stroke="#f7c08f" stroke-width="1.3" opacity=".75"/>'
    body += f'<g clip-path="url(#ay-clip)">{scales}<path d="M210 112 C270 88 360 84 448 108" stroke="#ffe1b0" stroke-width="5" opacity=".35" fill="none"/></g>'
    body += f'<path d="M200 104 C240 64 300 52 350 62 C400 72 430 90 452 100 L456 124 C430 132 400 140 350 138 C290 136 236 140 200 136 Z" fill="none" {O}/>'
    mane = (f'<path d="M188 84 C198 64 214 66 222 50 C226 66 238 70 246 60 C250 80 240 98 214 108 Z" fill="#e3b552" {O}/>'
            f'<path d="M200 136 C196 152 182 160 170 156 C180 150 184 144 182 136 Z" fill="#e3b552" {O}/>')
    head = (f'<path d="M208 100 C192 80 164 74 142 80 L108 88 Q102 95 112 98 L146 102 L154 110 L116 122 '
            f'Q110 131 120 133 C150 140 184 144 208 138 Z" fill="#e3b552" {O}/>'
            f'<path d="M112 98 l6 5 l5 -4 l6 5 l5 -4 l6 5 M120 121 l6 -5 l5 4 l6 -5 l5 4" fill="none" stroke="#f7f3e8" stroke-width="1.6"/>'
            f'<path d="M150 104 L154 110 L130 118 Z" fill="#a83a28"/>'
            f'<path d="M160 86 C168 80 180 80 188 88" fill="none" {O}/>'
            f'<circle cx="174" cy="94" r="6" fill="#f7f3e8" {O}/><circle cx="172" cy="94" r="3" fill="#1f2a33"/>'
            f'<path d="M184 80 C190 62 204 52 222 46 M196 64 C204 62 210 66 214 72" fill="none" stroke="#e3b552" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M172 80 C176 64 186 56 200 52" fill="none" stroke="#e3b552" stroke-width="3.5" stroke-linecap="round"/>'
            f'<path d="M118 90 C104 58 84 52 62 34" fill="none" stroke="#e3b552" stroke-width="2.4" stroke-linecap="round"/>'
            f'<path d="M124 130 C100 150 80 140 60 162" fill="none" stroke="#e3b552" stroke-width="2.4" stroke-linecap="round"/>')
    pearl = ('<circle cx="80" cy="108" r="11" fill="#fff2c6"/>'
             '<path d="M70 104 C64 94 70 86 74 82 C74 90 80 92 80 97 C84 92 88 90 90 84 C94 92 92 100 90 104" fill="none" stroke="#f3c66a" stroke-width="2"/>'
             '<circle cx="80" cy="108" r="17" fill="#f3c66a" opacity=".25"/>')
    return svg(defs + sky + bursts + roof + poles + small + crowd + fins + tail + body + mane + head + pearl,
               '唐模鳌鱼灯线描：夜里人群举起龙头鱼身的鳌鱼灯，前面是一颗宝珠，四周有烟花', 'vg-ay')


def langqiao():
    """唐模 · 高阳廊桥: a covered bridge with a small pavilion over Tangan stream."""
    wl = 170
    deck = (f'<path class="wall" d="M120 {wl} L120 132 L480 132 L480 {wl} L332 {wl} A32 32 0 0 0 268 {wl} Z"/>'
            f'<path class="line" d="M263 {wl} A37 37 0 0 1 337 {wl}"/>')
    gallery = ('<rect class="wall" x="140" y="96" width="320" height="36"/>'
               + ''.join(f'<rect class="dark" x="{x}" y="104" width="16" height="14" rx="2"/>' for x in range(160, 450, 34)))
    roof = ('<path class="dark" d="M124 98 L476 98 L486 90 L456 82 L144 82 L114 90 Z"/>'
            '<path class="line" d="M114 90 l-8 -6 M486 90 l8 -6"/>'
            # pavilion in the middle of the gallery
            '<rect class="wall" x="262" y="58" width="76" height="26"/>'
            '<path class="dark" d="M252 60 L348 60 L358 52 L330 42 L270 42 L242 52 Z"/>'
            '<path class="line" d="M242 52 l-8 -6 M358 52 l8 -6"/>')
    scene = deck + gallery + roof
    side = house(500, wl, 90, 60, windows=1, door=False) + house(0, wl, 110, 52, windows=2, door=False)
    tree = pad(60, 100, 46, 22) + '<path class="line wood-line" d="M60 100 L58 140"/>'
    rip = [(30, 90, 182), (180, 240, 190), (360, 410, 186), (470, 540, 196)]
    return svg(tree + side + scene + water(wl, 'lq', side + scene, rip), '唐模高阳廊桥线描', 'vg-lq')


SCENES = {
    'd1': (nanhu_bridge, '宏村 · 南湖画桥'),
    'd2': (moon_pond, '宏村 · 月沼'),
    'd3': (welcome_pine, '黄山 · 迎客松'),
    'd4': (sunrise_peaks, '黄山 · 始信峰日出'),
    'lantern': (aoyu_lantern, '唐模 · 鳌鱼灯'),
    'd5': (langqiao, '唐模 · 高阳廊桥'),
}


def vignette(pid):
    if pid not in SCENES:
        return ''
    fn, cap = SCENES[pid]
    return f'<figure class="vignette">{fn()}<figcaption>{cap}</figcaption></figure>'


if __name__ == '__main__':
    import sys
    pid = sys.argv[1]
    print(f'<html><body style="background:#eeebe3">{vignette(pid)}</body></html>')
