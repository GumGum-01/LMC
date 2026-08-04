#!/usr/bin/env python3
"""
Erzeugt die SVG-Strukturformeln fuer
"Oxidative Kupplung: vom Catechin zum Benzotropolon (Theaflavin)".

Alle Koordinaten werden gerechnet, nicht geschaetzt:
Bindungslaenge = Sechseck-Umkreisradius = BOND.
"""

import math
from pathlib import Path

BOND = 34.0
HALF = BOND * math.sqrt(3) / 2      # 29.44 = Apothem eines Sechsecks
TRIM = 13.0                          # Freiraum um beschriftete Atome
LBL = 15
NUM = 10.5

# Formeln werden als Liste (Text, Art) gesetzt; Art: "" | "sub" | "sup".
# Keine tspans, keine Sonderzeichen jenseits von ASCII -> in jedem Font gleich.
SC = 0.72      # Groesse von Hoch- und Tiefstellung

# Vorschubbreiten Helvetica/Arial in 1/1000 em – damit sitzen die
# hoch- und tiefgestellten Zeichen exakt, egal welcher Font laedt.
_W = {" ": 278, "(": 333, ")": 333, "+": 584, ",": 278, "-": 333, ".": 278,
      "/": 278, ":": 278, "=": 584}
for _c in "0123456789":
    _W[_c] = 556
for _c, _w in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                  (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
                   722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611)):
    _W[_c] = _w
for _c, _w in zip("abcdefghijklmnopqrstuvwxyz",
                  (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
                   556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500)):
    _W[_c] = _w


def tw(text, size):
    return sum(_W.get(ch, 556) for ch in text) * size / 1000.0


# ---------------------------------------------------------------- Geometrie

def polar(c, r, deg):
    a = math.radians(deg)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def norm(v):
    n = math.hypot(*v) or 1.0
    return (v[0] / n, v[1] / n)


def mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def shift(p, direction, d):
    u = norm(direction)
    return (p[0] + u[0] * d, p[1] + u[1] * d)


def hexagon(c, rot=0.0):
    return [polar(c, BOND, -90 + rot + 60 * i) for i in range(6)]


def bring(c):
    """B-Ring, C1' unten (dort haengt das Flavan-Geruest)."""
    v = hexagon(c)
    return {"4'": v[0], "3'": v[1], "2'": v[2], "1'": v[3], "6'": v[4], "5'": v[5]}


def outward(c, p, d):
    return shift(p, sub(p, c), d)


# ---------------------------------------------------------------- SVG

class Fig:
    def __init__(self, label):
        self.label = label
        self.body = []
        self.xs = []
        self.ys = []

    def box(self, p, w=26, h=26):
        self.xs += [p[0] - w, p[0] + w]
        self.ys += [p[1] - h, p[1] + h]

    def raw(self, s):
        self.body.append(s)

    # -- Bindungen -------------------------------------------------
    def bond(self, p, q, t0=0.0, t1=0.0, w=1.7, cls="bd"):
        a = shift(p, sub(q, p), t0)
        b = shift(q, sub(p, q), t1)
        self.raw(f'<line class="{cls}" x1="{a[0]:.1f}" y1="{a[1]:.1f}" '
                 f'x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke-width="{w}"/>')
        self.box(p, 6, 6); self.box(q, 6, 6)

    def dbl_in(self, p, q, center, t0=0.0, t1=0.0, gap=6.0, inset=7.0):
        self.bond(p, q, t0, t1)
        u = norm(sub(q, p))
        n = (-u[1], u[0])
        if (n[0] * (center[0] - p[0]) + n[1] * (center[1] - p[1])) < 0:
            n = (-n[0], -n[1])
        a = shift(shift(p, sub(q, p), t0 + inset), n, gap)
        b = shift(shift(q, sub(p, q), t1 + inset), n, gap)
        self.raw(f'<line class="bd" x1="{a[0]:.1f}" y1="{a[1]:.1f}" '
                 f'x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke-width="1.7"/>')

    def dbl_sym(self, p, q, t0=0.0, t1=0.0, gap=3.4, cls="bd"):
        u = norm(sub(q, p))
        n = (-u[1], u[0])
        a = shift(p, sub(q, p), t0)
        b = shift(q, sub(p, q), t1)
        for s in (+1, -1):
            a2, b2 = shift(a, n, gap * s), shift(b, n, gap * s)
            self.raw(f'<line class="{cls}" x1="{a2[0]:.1f}" y1="{a2[1]:.1f}" '
                     f'x2="{b2[0]:.1f}" y2="{b2[1]:.1f}" stroke-width="1.7"/>')
        self.box(p, 6, 6); self.box(q, 6, 6)

    def wedge(self, p, q, width=7.0, hashed=False):
        """Keil vom schmalen Ende p zum breiten Ende q."""
        u = norm(sub(q, p))
        n = (-u[1], u[0])
        if not hashed:
            a = (q[0] + n[0] * width / 2, q[1] + n[1] * width / 2)
            b = (q[0] - n[0] * width / 2, q[1] - n[1] * width / 2)
            self.raw(f'<polygon class="wg" points="{p[0]:.1f},{p[1]:.1f} '
                     f'{a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f}"/>')
        else:
            L = math.hypot(*sub(q, p))
            k = 5
            for i in range(1, k + 1):
                t = i / k
                c = (p[0] + u[0] * L * t, p[1] + u[1] * L * t)
                w = width * t / 2
                self.raw(f'<line class="bd" x1="{c[0]-n[0]*w:.1f}" y1="{c[1]-n[1]*w:.1f}" '
                         f'x2="{c[0]+n[0]*w:.1f}" y2="{c[1]+n[1]*w:.1f}" stroke-width="1.5"/>')
        self.box(p, 6, 6); self.box(q, 8, 8)

    def bridge(self, p, q):
        self.bond(p, q, 0, 0, w=3.6, cls="bd bg")

    # -- Text ------------------------------------------------------
    def atom(self, p, text, cls="ox", size=LBL, dy=5.2, chars=None):
        self.raw(f'<text class="at hl mid {cls}" x="{p[0]:.1f}" y="{p[1]+dy:.1f}" '
                 f'font-size="{size}">{text}</text>')
        n = chars if chars is not None else len(text)
        self.box(p, max(12, n * size * 0.34), size * 0.9)

    def pos(self, c, p, text, d=16.0, ang=None):
        q = outward(c, p, d) if ang is None else polar(p, d, ang)
        self.raw(f'<text class="at hl mid nm" x="{q[0]:.1f}" y="{q[1]+3.6:.1f}" '
                 f'font-size="{NUM}">{text}</text>')
        self.box(q, 11, 8)

    def cap(self, p, text, cls="cp", size=12.5, chars=None):
        self.raw(f'<text class="at hl mid {cls}" x="{p[0]:.1f}" y="{p[1]:.1f}" '
                 f'font-size="{size}">{text}</text>')
        self.box(p, tw(text, size) / 2 + 8, size)

    def rich(self, p, parts, size=LBL, cls="ox", dy=5.2):
        """Formel mit Hoch-/Tiefstellung, linksbuendig ausgelegt und dann
        auf p zentriert. Jede Gruppe ist ein eigenes <text>."""
        widths = [tw(t, size * SC if k else size) for t, k in parts]
        W = sum(widths)
        x = p[0] - W / 2
        for (t, k), w in zip(parts, widths):
            t = t.replace(" ", "&#160;") if t.strip() != t else t
            fs = size * SC if k else size
            off = {"": 0.0, "sub": size * 0.20, "sup": -size * 0.42}[k]
            self.raw(f'<text class="at hl {cls}" x="{x:.1f}" '
                     f'y="{p[1]+dy+off:.1f}" font-size="{fs:.1f}">{t}</text>')
            x += w
        self.box(p, W / 2 + 6, size)
        return W

    def anion(self, p, base="O", cls="ox"):
        return self.rich(p, [(base, ""), ("-", "sup")], cls=cls)

    def cation(self, p, base="H", size=12.5, cls="cp em"):
        return self.rich(p, [(base, ""), ("+", "sup")], size=size, cls=cls, dy=4.4)

    def ringplus(self, p, r=7.5):
        self.raw(f'<circle class="pc" cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}"/>')
        self.raw(f'<text class="at hl mid em" x="{p[0]:.1f}" y="{p[1]+4.0:.1f}" '
                 f'font-size="11">+</text>')
        self.box(p, r + 4, r + 4)

    # -- Substituenten ---------------------------------------------
    def oh(self, c, p, label="OH", d=BOND * 0.80, chars=2):
        q = outward(c, p, d)
        self.bond(p, q, 0, TRIM)
        if isinstance(label, list):
            self.rich(q, label)
        else:
            self.atom(q, label, chars=chars)
        return q

    def oxo(self, c, p, d=BOND * 0.82, extra=0.0):
        q = outward(c, p, d + extra)
        self.dbl_sym(p, q, 0, TRIM)
        self.atom(q, "O", chars=1)
        return q

    def stub(self, c, p, text, d=BOND * 0.98):
        q = outward(c, p, d)
        self.bond(p, q, 0, 15)
        self.raw(f'<text class="at hl mid fl" x="{q[0]:.1f}" y="{q[1]+4.6:.1f}" '
                 f'font-size="12.5">{text}</text>')
        self.box(q, len(text) * 4.8 + 8, 12)
        return q

    # -- Pfeile ----------------------------------------------------
    def push(self, p, q, bow=0.45, n=None, t0=0.0, t1=0.0, side=1, lab=13, dash=False):
        a = shift(p, sub(q, p), t0)
        b = shift(q, sub(p, q), t1)
        v = sub(b, a)
        L = math.hypot(*v) or 1.0
        nn = (-v[1] / L * side, v[0] / L * side)
        c1 = (a[0] + v[0] * .25 + nn[0] * L * bow, a[1] + v[1] * .25 + nn[1] * L * bow)
        c2 = (a[0] + v[0] * .75 + nn[0] * L * bow, a[1] + v[1] * .75 + nn[1] * L * bow)
        cls = "ar dsh" if dash else "ar"
        self.raw(f'<path class="{cls}" d="M {a[0]:.1f} {a[1]:.1f} '
                 f'C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} '
                 f'{b[0]:.1f} {b[1]:.1f}" marker-end="url(#hd)"/>')
        self.box(a, 10, 10); self.box(b, 10, 10)
        self.box(((c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2), 8, 8)
        if n is not None:
            m = (a[0] * .125 + c1[0] * .375 + c2[0] * .375 + b[0] * .125,
                 a[1] * .125 + c1[1] * .375 + c2[1] * .375 + b[1] * .125)
            m = shift(m, nn, lab)
            self.raw(f'<circle class="nb" cx="{m[0]:.1f}" cy="{m[1]:.1f}" r="9"/>')
            self.raw(f'<text class="at mid nn" x="{m[0]:.1f}" y="{m[1]+3.7:.1f}" '
                     f'font-size="10.5">{n}</text>')
            self.box(m, 12, 12)

    def rxn(self, p, q, over="", under=""):
        self.raw(f'<line class="rx" x1="{p[0]:.1f}" y1="{p[1]:.1f}" '
                 f'x2="{q[0]:.1f}" y2="{q[1]:.1f}" marker-end="url(#rh)"/>')
        m = mid(p, q)
        if over:
            self.cap((m[0], m[1] - 12), over, size=11.5)
        if under:
            self.cap((m[0], m[1] + 22), under, cls="cp sm", size=11.5)
        self.box(p, 8, 8); self.box(q, 8, 8)

    def equil(self, p, q, gap=4.5):
        """Gleichgewichtspfeile, Richtung beliebig."""
        u = norm(sub(q, p))
        n = (-u[1], u[0])
        for sgn, (a, b) in ((1, (p, q)), (-1, (q, p))):
            a2, b2 = shift(a, n, gap * sgn), shift(b, n, gap * sgn)
            self.raw(f'<line class="rx" x1="{a2[0]:.1f}" y1="{a2[1]:.1f}" '
                     f'x2="{b2[0]:.1f}" y2="{b2[1]:.1f}" marker-end="url(#rh)"/>')
        self.box(p, 12, 12); self.box(q, 12, 12)

    def svg(self, pad=12):
        x0, x1 = min(self.xs) - pad, max(self.xs) + pad
        y0, y1 = min(self.ys) - pad, max(self.ys) + pad
        w, h = x1 - x0, y1 - y0
        return (f'<svg role="img" aria-label="{self.label}" '
                f'viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" '
                f'preserveAspectRatio="xMidYMid meet" '
                f'style="--w:{w:.0f}">{DEFS}{"".join(self.body)}</svg>')


DEFS = ('<defs>'
        '<marker id="hd" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
        'markerHeight="5" orient="auto-start-reverse">'
        '<path d="M 0 0.6 L 10 5 L 0 9.4 z" class="hdf"/></marker>'
        '<marker id="rh" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
        'markerHeight="6" orient="auto-start-reverse">'
        '<path d="M 0 2 L 10 5 L 0 8 z" class="rhf"/></marker>'
        '</defs>')

ORDER = ["1'", "2'", "3'", "4'", "5'", "6'"]
AROM = [("1'", "2'"), ("3'", "4'"), ("5'", "6'")]
QUIN = [("1'", "2'"), ("5'", "6'")]


def draw_ring(f, v, order, doubles, center):
    dbl = [set(d) for d in doubles]
    for i in range(len(order)):
        a, b = order[i], order[(i + 1) % len(order)]
        (f.dbl_in if {a, b} in dbl else f.bond)(v[a], v[b], center) \
            if {a, b} in dbl else f.bond(v[a], v[b])


# ---------------------------------------------------------------- Flavan

def flavan(f, c, tri, title):
    A = hexagon(c)
    C8a, C8, C7, C6, C5, C4a = A[1], A[0], A[5], A[4], A[3], A[2]
    cc = (c[0] + 2 * HALF, c[1])
    Cv = hexagon(cc)
    O1, C2, C3, C4 = Cv[0], Cv[1], Cv[2], Cv[3]

    f.dbl_in(C8a, C8, c); f.bond(C8, C7); f.dbl_in(C7, C6, c)
    f.bond(C6, C5); f.dbl_in(C5, C4a, c); f.bond(C4a, C8a)
    f.bond(C8a, O1, 0, TRIM); f.bond(O1, C2, TRIM, 0)
    f.bond(C2, C3); f.bond(C3, C4); f.bond(C4, C4a)
    f.atom(O1, "O", chars=1)
    f.oh(c, C5); f.oh(c, C7)
    f.cap((c[0], c[1] + 5), "A", cls="cp rg", size=15)
    f.cap((cc[0], cc[1] + 5), "C", cls="cp rg", size=15)

    # 2,3-cis (epi): beide Keile nach vorn
    C1s = shift(C2, (0.5, -math.sqrt(3) / 2), BOND)
    f.wedge(C2, C1s)
    oh3 = outward(cc, C3, BOND * 0.80)
    f.wedge(C3, shift(oh3, sub(C3, oh3), TRIM))
    f.atom(oh3, "OH", chars=2)
    f.cap((C3[0] - 6, C3[1] + 30), "2,3-cis", cls="cp sm", size=10.5)

    bc = (C1s[0], C1s[1] - BOND)
    B = bring(bc)
    draw_ring(f, B, ORDER, AROM, bc)
    f.oh(bc, B["3'"]); f.oh(bc, B["4'"])
    if tri:
        f.oh(bc, B["5'"])
    f.cap((bc[0], bc[1] + 5), "B", cls="cp rg", size=15)
    f.cap((bc[0] - 4, bc[1] - BOND - 52), title, cls="cp nmx", size=13.5)
    return B, bc


# ---------------------------------------------------------------- Panels
# Grundsatz: in der Zeichnung stehen nur kurze Marken.
# Erklaerende Saetze gehoeren in die figcaption, nicht ins SVG.

FIGS = {}


def fig_substrate():
    f = Fig("Strukturformeln von (−)-Epicatechin und (−)-Epigallocatechin")
    flavan(f, (0, 0), False, "(−)-Epicatechin · EC")
    flavan(f, (360, 0), True, "(−)-Epigallocatechin · EGC")
    f.cap((105, 92), "Brenzcatechin · 2 O", cls="cp sm", size=11.5)
    f.cap((465, 92), "Pyrogallol · 3 O", cls="cp sm", size=11.5)
    FIGS["substrate"] = f.svg()


def fig_step0():
    f = Fig("PPO oxidiert den Brenzcatechin-B-Ring zum ortho-Chinon")
    c = (0, 0)
    B = bring(c)
    draw_ring(f, B, ORDER, AROM, c)
    o3 = f.oh(c, B["3'"], label=[("O", ""), ("-", "sup")])
    o4 = f.oh(c, B["4'"], label=[("O", ""), ("-", "sup")])
    f.stub(c, B["1'"], "EC")
    f.pos(c, B["4'"], "4'", d=18, ang=195)
    f.pos(c, B["3'"], "3'", d=18, ang=-15)
    f.pos(c, B["6'"], "6'", d=17)
    f.pos(c, B["5'"], "5'", d=17)

    f.push(polar(o4, 18, 200), shift(B["4'"], sub(o4, B["4'"]), 14),
           bow=0.5, n=1, side=-1, lab=-21)
    f.push(polar(o3, 18, 20), shift(B["3'"], sub(o3, B["3'"]), 14),
           bow=0.5, n=2, side=-1, lab=13)
    f.push(mid(B["3'"], B["4'"]), polar(c, 132, -62), bow=0.16, n=3, t1=6,
           side=-1, lab=16)
    f.rich((140, -128), [("2 e", ""), ("-", "sup"), (" an das Cu-Zentrum", "")],
           size=12, cls="cp em")

    f.rxn((124, 24), (200, 24))
    f.rich((162, 12), [("PPO / 1/2 O", ""), ("2", "sub")], size=11.5, cls="cp")
    f.rich((162, 42), [("- 2 H", ""), ("+", "sup"), (", - H", ""), ("2", "sub"), ("O", "")],
           size=11.5, cls="cp sm")

    c2 = (310, 0)
    Q = bring(c2)
    draw_ring(f, Q, ORDER, QUIN, c2)
    f.oxo(c2, Q["3'"]); f.oxo(c2, Q["4'"])
    f.stub(c2, Q["1'"], "EC")
    f.pos(c2, Q["6'"], "6'", d=17)
    f.pos(c2, Q["2'"], "2'", d=17)
    f.cap((0, 106), "Brenzcatechin", cls="cp sm", size=12)
    f.cap((c2[0], 106), "o-Chinon", cls="cp em", size=12)
    FIGS["step0"] = f.svg()


def fig_step1():
    f = Fig("Redox-Austausch: immer ein oxidierter und ein reduzierter Partner")
    ROW = 268

    c = (0, 0)
    Q = bring(c)
    draw_ring(f, Q, ORDER, QUIN, c)
    f.oxo(c, Q["3'"]); f.oxo(c, Q["4'"]); f.stub(c, Q["1'"], "EC")
    f.cap((0, 108), "EC-Chinon · Elektrophil", cls="cp em", size=12)
    f.cap((128, 6), "+", cls="cp", size=20)
    c2 = (256, 0)
    G = bring(c2)
    draw_ring(f, G, ORDER, AROM, c2)
    f.oh(c2, G["3'"]); f.oh(c2, G["4'"]); f.oh(c2, G["5'"]); f.stub(c2, G["1'"], "EGC")
    f.cap((256, 108), "EGC · Nucleophil", cls="cp nu", size=12)

    f.equil((128, 126), (128, ROW - 70))
    f.rich((198, ROW / 2 - 4), [("2 e", ""), ("-", "sup"), (", 2 H", ""), ("+", "sup")],
           size=12, cls="cp")

    c3 = (0, ROW)
    P = bring(c3)
    draw_ring(f, P, ORDER, AROM, c3)
    f.oh(c3, P["3'"]); f.oh(c3, P["4'"]); f.stub(c3, P["1'"], "EC")
    f.cap((0, ROW + 108), "EC · Nucleophil", cls="cp nu", size=12)
    f.cap((128, ROW + 6), "+", cls="cp", size=20)
    c4 = (256, ROW)
    R = bring(c4)
    draw_ring(f, R, ORDER, QUIN, c4)
    f.oxo(c4, R["3'"]); f.oxo(c4, R["4'"]); f.oh(c4, R["5'"]); f.stub(c4, R["1'"], "EGC")
    f.cap((256, ROW + 108), "EGC-Chinon · Elektrophil", cls="cp em", size=12)
    FIGS["step1"] = f.svg()


# gemeinsame Lage: EGC links, EC rechts. C2'(EGC)–C6'(EC) waagrecht bei y = +17
EC_C = (0.0, 0.0)
LINK = 46.0
EG_C = (-(2 * HALF + LINK), 0.0)


def fig_step2():
    f = Fig("Erste C-C-Kupplung: EGC-C2' greift C6' des EC-Chinons an")
    gc = (-(2 * HALF + LINK + 42), 0.0)
    E = bring(EC_C); G = bring(gc)

    draw_ring(f, E, ORDER, QUIN, EC_C)
    f.oxo(EC_C, E["3'"])
    o4 = f.oxo(EC_C, E["4'"])
    f.stub(EC_C, E["1'"], "EC")
    f.pos(EC_C, E["6'"], "6'", d=17, ang=170)
    f.pos(EC_C, E["4'"], "4'", d=19, ang=-25)

    draw_ring(f, G, ORDER, AROM, gc)
    o3 = f.oh(gc, G["3'"]); f.oh(gc, G["4'"]); f.oh(gc, G["5'"])
    f.stub(gc, G["1'"], "EGC")
    hp = polar(G["2'"], 23, 88)
    f.bond(G["2'"], hp, 0, 10); f.atom(hp, "H", cls="hy", chars=1)
    f.pos(gc, G["2'"], "2'", d=18, ang=-38)
    f.pos(gc, G["3'"], "3'", d=17, ang=10)

    # 1 : +M der 3'-OH schiebt Elektronendichte nach C2'
    f.push(polar(o3, 16, 15), mid(G["3'"], G["2'"]), bow=0.55, n=1, side=-1, lab=12)
    # 2 : pi(C1'=C2') greift den beta-Kohlenstoff C6' an
    f.push(mid(G["1'"], G["2'"]), E["6'"], bow=0.26, n=2, t1=9, side=1, lab=15)
    # 3 : pi(C5'=C6') klappt auf C4' um  ...
    f.push(mid(E["5'"], E["6'"]), mid(E["4'"], E["5'"]), bow=0.9, n=3, side=-1, lab=12)
    # ... und das Carbonyl wird zum Enolat (Pflichtpartner von Pfeil 3)
    f.push(mid(E["4'"], o4), o4, bow=0.8, t1=13, side=-1, lab=11)

    f.cap((gc[0], 112), "Nucleophil", cls="cp nu", size=12)
    f.cap((EC_C[0], 112), "Elektrophil", cls="cp em", size=12)
    FIGS["step2"] = f.svg()


def adduct(f, arrows=False):
    """Addukt nach der Kupplung: links Arenium (EGC), rechts Enolat (EC).
    Beide sp3-Zentren tragen je ein H – 'links und rechts der Bindungsstelle'."""
    E = bring(EC_C); G = bring(EG_C)
    # EC: C3'=O, C4'-O(-), C4'=C5', C6' ist sp3
    draw_ring(f, E, ORDER, [("1'", "2'"), ("4'", "5'")], EC_C)
    f.oxo(EC_C, E["3'"])
    o4 = f.oh(EC_C, E["4'"], label=[("O", ""), ("-", "sup")])
    f.stub(EC_C, E["1'"], "EC")
    hE = polar(E["6'"], 24, 90)
    f.bond(E["6'"], hE, 0, 10); f.atom(hE, "H", cls="hy", chars=1)
    # EGC: Arenium, C2' ist sp3
    draw_ring(f, G, ORDER, [("3'", "4'"), ("5'", "6'")], EG_C)
    f.oh(EG_C, G["3'"]); f.oh(EG_C, G["4'"]); f.oh(EG_C, G["5'"])
    f.stub(EG_C, G["1'"], "EGC")
    f.bond(G["2'"], E["6'"])
    hG = polar(G["2'"], 24, 90)
    f.bond(G["2'"], hG, 0, 10); f.atom(hG, "H", cls="hy", chars=1)
    f.ringplus(polar(G["1'"], 23, -62))
    return E, G, o4, hE, hG


def fig_step3():
    f = Fig("Rearomatisierung: die Protonen links und rechts der Bindungsstelle gehen ab")
    E, G, o4, hE, hG = adduct(f)

    bG = (G["2'"][0] - 62, hG[1] + 22)
    f.atom(bG, "B", cls="hy", chars=1)
    f.push(bG, hG, bow=0.26, n=4, t0=11, t1=11, side=-1, lab=13)
    f.push(mid(G["2'"], hG), mid(G["1'"], G["2'"]), bow=0.95, n=5, side=1, lab=12)

    bE = (E["6'"][0] + 62, hE[1] + 22)
    f.atom(bE, "B", cls="hy", chars=1)
    f.push(bE, hE, bow=0.26, n=6, t0=11, t1=11, side=1, lab=13)
    f.push(mid(E["6'"], hE), mid(E["5'"], E["6'"]), bow=0.95, side=-1, lab=12)
    f.push(polar(o4, 54, -48), o4, bow=0.3, t0=13, t1=15, side=1, lab=12)
    f.cation(polar(o4, 70, -48))
    FIGS["step3"] = f.svg()


def fig_biaryl():
    f = Fig("Farbloses Biaryl nach der ersten Kupplung")
    E = bring(EC_C); G = bring(EG_C)
    draw_ring(f, E, ORDER, AROM, EC_C)
    f.oh(EC_C, E["3'"]); f.oh(EC_C, E["4'"]); f.stub(EC_C, E["1'"], "EC")
    draw_ring(f, G, ORDER, AROM, EG_C)
    f.oh(EG_C, G["3'"]); f.oh(EG_C, G["4'"]); f.oh(EG_C, G["5'"])
    f.stub(EG_C, G["1'"], "EGC")
    f.bond(G["2'"], E["6'"])
    f.cap((EG_C[0] / 2, 106), "Biaryl · beide Ringe aromatisch · farblos",
          cls="cp sm", size=12)
    FIGS["biaryl"] = f.svg()


def fig_step4():
    f = Fig("Dritte Oxidation: der Pyrogallol-Ring wird zum Hydroxy-o-chinon")
    E = bring(EC_C); G = bring(EG_C)
    draw_ring(f, E, ORDER, AROM, EC_C)
    f.oh(EC_C, E["3'"]); f.oh(EC_C, E["4'"]); f.stub(EC_C, E["1'"], "EC")
    draw_ring(f, G, ORDER, QUIN, EG_C)
    f.oxo(EG_C, G["3'"]); f.oxo(EG_C, G["4'"]); f.oh(EG_C, G["5'"])
    f.stub(EG_C, G["1'"], "EGC")
    f.bond(G["2'"], E["6'"])
    f.pos(EG_C, G["4'"], "4'", d=20, ang=-14)
    f.pos(EC_C, E["5'"], "5'", d=18, ang=200)
    f.cap((EG_C[0], 106), "Hydroxy-o-chinon", cls="cp em", size=12)
    FIGS["step4"] = f.svg()


def fig_step5():
    f = Fig("Zweite, intramolekulare Kupplung: 1,2-Addition auf das Carbonyl C4'")
    E = bring(EC_C); G = bring(EG_C)
    draw_ring(f, E, ORDER, AROM, EC_C)
    f.oh(EC_C, E["3'"]); f.oh(EC_C, E["4'"]); f.stub(EC_C, E["1'"], "EC")
    draw_ring(f, G, ORDER, QUIN, EG_C)
    f.oxo(EG_C, G["3'"])
    o4 = f.oxo(EG_C, G["4'"], extra=8)
    f.oh(EG_C, G["5'"]); f.stub(EG_C, G["1'"], "EGC")
    f.bond(G["2'"], E["6'"])
    f.pos(EC_C, E["5'"], "5'", d=18, ang=200)
    f.pos(EG_C, G["4'"], "4'", d=20, ang=-14)

    f.push(mid(E["5'"], E["4'"]), G["4'"], bow=0.62, n=7, t1=11, side=1, lab=15)
    f.push(mid(G["4'"], o4), o4, bow=0.75, n=8, t1=13, side=1, lab=12)
    f.cap((EG_C[0] / 2 - 10, 106), "1,2-Addition auf das C=O", cls="cp em", size=12)
    FIGS["step5"] = f.svg()


# ---- Bicyclo[3.2.1]: Siebenring, unten ans EC-Benzol anelliert, C3'-Bruecke
R7 = BOND / (2 * math.sin(math.pi / 7))
H7 = (0.0, 0.0)
RING7 = ["6'EC", "2'", "1'", "6'", "5'", "4'", "5'EC"]


def sevenring(dx=0.0):
    step = 360 / 7
    a0 = 90 - step / 2
    return {nm: polar((dx, 0.0), R7, a0 - step * i) for i, nm in enumerate(RING7)}


def ec_below(p6, p5):
    c = ((p6[0] + p5[0]) / 2, p6[1] + HALF)
    return ({"6'": p6, "1'": (c[0] + BOND, c[1]), "2'": (c[0] + BOND / 2, c[1] + HALF),
             "3'": (c[0] - BOND / 2, c[1] + HALF), "4'": (c[0] - BOND, c[1]), "5'": p5}, c)


def ec_benzene(f, EC, ecc, fusion_double):
    if fusion_double:
        pat = [("5'", "6'", 1), ("6'", "1'", 0), ("1'", "2'", 1),
               ("2'", "3'", 0), ("3'", "4'", 1), ("4'", "5'", 0)]
    else:
        pat = [("5'", "6'", 0), ("6'", "1'", 1), ("1'", "2'", 0),
               ("2'", "3'", 1), ("3'", "4'", 0), ("4'", "5'", 1)]
    for a, b, d in pat:
        if d:
            f.dbl_in(EC[a], EC[b], ecc)
        else:
            f.bond(EC[a], EC[b])
    f.oh(ecc, EC["3'"]); f.oh(ecc, EC["4'"]); f.stub(ecc, EC["1'"], "EC")


def bicycle(f):
    S = sevenring()
    EC, ecc = ec_below(S["6'EC"], S["5'EC"])
    ec_benzene(f, EC, ecc, fusion_double=False)
    for i in range(6):
        f.bond(S[RING7[i]], S[RING7[i + 1]])
    f.dbl_in(S["2'"], S["1'"], H7)
    f.dbl_in(S["6'"], S["5'"], H7)
    f.stub(H7, S["1'"], "EGC")
    f.oh(H7, S["5'"])
    c3 = (0.0, 15.0)
    f.bridge(S["2'"], c3); f.bridge(S["4'"], c3)
    oq = (0.0, -15.0)
    f.dbl_sym(c3, oq, 0, 12)
    f.atom(oq, "O", chars=1)
    oal = outward(H7, S["4'"], BOND * 1.02)
    f.bond(S["4'"], oal, 0, TRIM + 4)
    f.rich(oal, [("O", ""), ("-", "sup")])
    return S, EC, ecc, c3, oq, oal


def fig_bicycle():
    f = Fig("Tricyclus: bicyclo[3.2.1]-Zwischenstufe mit C3'-Bruecke")
    S, EC, ecc, c3, oq, oal = bicycle(f)
    f.cap((30, 32), "C3'", cls="cp bgl", size=11)
    f.pos(H7, S["4'"], "4'", d=16, ang=-112)
    f.pos(H7, S["2'"], "2'", d=16, ang=-64)
    f.cap((0, -R7 - 34), "Siebenring liegt schon vor", cls="cp em", size=12)
    FIGS["bicycle"] = f.svg()


def fig_step6():
    f = Fig("Retro-Aldol und Decarboxylierung: die Bruecke geht als CO2 ab")
    S, EC, ecc, c3, oq, oal = bicycle(f)
    f.push(polar(oal, 16, 200), mid(S["4'"], oal), bow=0.6, n=9, side=-1, lab=12)
    f.push(mid(S["4'"], c3), S["4'"], bow=0.7, n=10, t1=10, side=1, lab=-16)
    f.push(mid(S["2'"], c3), mid(S["2'"], S["1'"]), bow=0.5, n=11, side=-1, lab=-17)
    f.rich((0, -R7 - 38), [("- CO", ""), ("2", "sub")], size=13, cls="cp em")
    FIGS["step6"] = f.svg()


def fig_product():
    f = Fig("Benzotropolon: das kupferrote Chromophor des Theaflavins")
    S = sevenring()
    EC, ecc = ec_below(S["6'EC"], S["5'EC"])
    ec_benzene(f, EC, ecc, fusion_double=True)
    for i in range(6):
        f.bond(S[RING7[i]], S[RING7[i + 1]])
    f.dbl_in(S["2'"], S["1'"], H7)
    f.dbl_in(S["6'"], S["5'"], H7)
    f.stub(H7, S["1'"], "EGC")
    f.oh(H7, S["5'"])
    oc = f.oxo(H7, S["4'"], extra=6)
    f.cap((0, -R7 - 34), "Tropolon", cls="cp em", size=13)
    f.cap((ecc[0], ecc[1] + HALF + 46), "intramolekularer Charge-Transfer",
          cls="cp sm", size=11.5)
    f.push((-96, 78), (-90, 4), bow=0.22, side=-1, dash=True)
    f.cap((-124, 92), "Donor", cls="cp nu", size=11.5)
    f.cap((-126, -6), "Akzeptor", cls="cp em", size=11.5)
    FIGS["product"] = f.svg()


def fig_chromophore():
    f = Fig("Tropolon: Keto-Form und Tropylium-Kation mit Oxyanion")

    def seven(dx, charged):
        P = sevenring(dx)
        ctr = (dx, 0.0)
        for i in range(6):
            f.bond(P[RING7[i]], P[RING7[i + 1]])
        f.dbl_in(P["5'EC"], P["6'EC"], ctr)
        f.dbl_in(P["2'"], P["1'"], ctr)
        f.dbl_in(P["6'"], P["5'"], ctr)
        f.oh(ctr, P["5'"])
        if charged:
            o = outward(ctr, P["4'"], BOND * 0.88)
            f.bond(P["4'"], o, 0, TRIM + 2)
            f.rich(o, [("O", ""), ("-", "sup")])
            f.ringplus((dx, 2), r=9)
        else:
            f.oxo(ctr, P["4'"])

    seven(0, False)
    f.raw('<line class="rx" x1="118" y1="2" x2="162" y2="2" '
          'marker-start="url(#rh)" marker-end="url(#rh)"/>')
    f.box((140, 2), 26, 12)
    seven(280, True)
    f.cap((0, -R7 - 32), "Keto-Form", cls="cp sm", size=12)
    f.cap((280, -R7 - 32), "Tropylium-Kation + Oxyanion", cls="cp em", size=12)
    FIGS["chromophore"] = f.svg()


for fn in (fig_substrate, fig_step0, fig_step1, fig_step2, fig_step3, fig_biaryl,
           fig_step4, fig_step5, fig_bicycle, fig_step6, fig_product, fig_chromophore):
    fn()

Path(__file__).with_name("figures.py").write_text(
    "# generiert von generate.py – nicht von Hand aendern\nFIGS = " + repr(FIGS) + "\n",
    encoding="utf-8")
print("ok", len(FIGS), "Figuren")
