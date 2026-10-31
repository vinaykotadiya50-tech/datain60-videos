"""DOT vs MATH: SURVIVE 5 WAVES - original wave-battle maths animation for Data in 60.
Our original mascot Dot fights maths enemies and wins with real maths: sqrt, limits, Euler's identity, derivatives, a geometric series.
python3 ep.py START END OUT.mp4  |  python3 ep.py still DIR t1 t2 ...
"""
import math, sys, subprocess
import numpy as np, cairo
sys.path.insert(0, "/home/claude/engine/anim")
from example_story_mean_median import (text, text_w, line, glow, seg, sm, eo, ei, back, elastic, win, clamp, lerp, arc, land_sq, noise,
                                       num, dot, Track, draw_world, cam, logo, wrap, W, H, FPS, G, UI, MATH, TEAL, CORAL, AMBER, WHITE, MUTED)

YEL = (1.0, 0.84, 0.22); GREEN = (0.35, 0.95, 0.55); BLUE = (0.35, 0.75, 1.0); RED = (1.0, 0.30, 0.30); VIO = (0.72, 0.55, 1.0)
S = dict(intro=0, w1=6, w2=20, w3=34, w4=48, w5=62, fin=82)
DURATION = 92.0
COVER_T = 71.0
INTENSITY = [(0, 0.35), (6, 0.5), (20, 0.6), (34, 0.7), (48, 0.75), (62, 0.9), (76, 1.0), (82, 0.7), (88, 0.5), (92, 0.0)]
WAVES = [("w1", "WAVE 1", "THE GIANT 9"), ("w2", "WAVE 2", "ENDLESS INFINITY"), ("w3", "WAVE 3", "THE e-i-PI GHOST"),
         ("w4", "WAVE 4", "THE PARABOLA"), ("w5", "WAVE 5 · BOSS", "THE SUM TITAN")]

SFX = []
def sfx(seg_name, u, kind, **kw): SFX.append((S[seg_name] + u, kind, kw))

# ---------------------------------------------------------------- helpers
def burst(c, x, y, dt, seed, n=26, col=WHITE, spd=620, life=0.9, size=7):
    if dt < 0 or dt > life: return
    r = np.random.default_rng(seed); a = 1 - dt / life
    for k in range(n):
        ang = r.uniform(0, 2 * math.pi); v = spd * r.uniform(0.35, 1.0)
        px = x + math.cos(ang) * v * dt; py = y + math.sin(ang) * v * dt + 700 * dt * dt
        c.set_source_rgba(*col, a); c.arc(px, py, size * r.uniform(0.5, 1.2) * (0.4 + 0.6 * a), 0, 6.3); c.fill()

def ring(c, x, y, dt, col=WHITE, life=0.6, rmax=320, w=10):
    if dt < 0 or dt > life: return
    t = dt / life; c.set_source_rgba(*col, (1 - t) * 0.9); c.set_line_width(w * (1 - t) + 1); c.arc(x, y, rmax * eo(t), 0, 6.3); c.stroke()

def mtext(c, parts, x, y, size, col=WHITE, a=1.0, glw=0.0, anchor="c"):
    """parts: list of (string, kind) kind 'n' normal or 's' superscript - Latin Modern Math."""
    ws = [text_w(c, s, size * (0.58 if k == "s" else 1.0), MATH) for s, k in parts]
    tw = sum(ws); x0 = x - tw / 2 if anchor == "c" else x
    for (s, k), w in zip(parts, ws):
        if k == "s": text(c, s, x0 + w / 2, y - size * 0.36, size * 0.58, col, a, glw=glw)
        else: text(c, s, x0 + w / 2, y, size, col, a, glw=glw)
        x0 += w
    return tw

def radical(c, x, y, w, h, col, a, lw=12, prog=1.0):
    """draw a sqrt sign: (x,y) = bottom of the v; spans width w over content of height h."""
    pts = [(x - 70, y - h * 0.42), (x - 40, y - h * 0.5), (x, y), (x + 40, y - h * 1.08), (x + 40 + w, y - h * 1.08)]
    L = [math.dist(pts[i], pts[i + 1]) for i in range(4)]; tot = sum(L) * clamp(prog)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for ww, al in ((lw * 4, 0.12), (lw, 1.0)):
        c.set_source_rgba(*col, a * al); c.set_line_width(ww); c.move_to(*pts[0]); left = tot
        for i in range(4):
            if left <= 0: break
            f = min(1, left / L[i]); c.line_to(lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)); left -= L[i]
        c.stroke()

def bubble(c, x, y, s, a, size=40):
    if a <= 0.01: return
    w = text_w(c, s, size, UI, True) + 60; h = size + 44; x0, y0 = x - w / 2, y - h
    c.set_source_rgba(1, 1, 1, 0.95 * a)
    r = h / 2; c.new_sub_path(); c.arc(x0 + w - r, y0 + r, r, -math.pi / 2, math.pi / 2); c.arc(x0 + r, y0 + r, r, math.pi / 2, 1.5 * math.pi); c.close_path(); c.fill()
    c.move_to(x - 14, y - 2); c.line_to(x + 4, y + 26); c.line_to(x + 16, y - 2); c.close_path(); c.fill()
    text(c, s, x, y0 + h / 2, size, (0.04, 0.12, 0.14), a, face=UI, bold=True)

def spin_glyph(c, s, x, y, size, col, a, rot, glw=0.8, face=MATH):
    text(c, s, x, y, size, col, a, face=face, rot=rot, glw=glw)

def dt_hit(u, t): return u - t

# ================================================================= INTRO
IT = Track(540, G)
def intro(u):
    z = lerp(1.25, 1.0, sm(seg(u, 0, 3)))
    def d(c):
        look = (1, 0) if 3.0 < u < 4.2 else (-1, 0) if 4.2 < u < 5.0 else (0, 0)
        sq = 0.3 * math.sin(u * 3) * seg(u, 0.5, 2.0) * (1 - seg(u, 2.0, 2.4))
        dot(c, 540, G, s=1.7, look=look, sq=sq, blink=1.2 < u < 1.33 or 4.6 < u < 4.73, wide=u > 5.0)
        bubble(c, 610, G - 200, "Bring it on!", win(u, 2.0, 4.4, 0.25))
        return {}
    return cam(540, 1000, z), d, dict(title=1 - seg(u, 4.5, 5.0))
sfx("intro", 0.05, "pop", f=520); sfx("intro", 2.0, "boing", g=0.6); sfx("intro", 4.9, "swell", d=1.2)

# ================================================================= WAVE 1 - the giant 9 vs sqrt
T1 = Track(540, G)
T1.hop(3.0, 3.55, 640, G - 160, 160)
T1.path(3.55, 4.4, lambda t: (lerp(640, 300, eo(t)), lerp(G - 160, G, t * t) - 140 * math.sin(math.pi * t), -6.3 * t), (300, G))
T1.walk(9.4, 10.3, 600)
T1.hop(11.2, 11.6, 600, G, 70); T1.hop(12.2, 12.6, 600, G, 70)
def w1(u):
    nine_x = lerp(1350, 780, sm(seg(u, 0, 2.4)))
    stomp = sum(math.exp(-((u - k) * 9) ** 2) for k in (0.6, 1.2, 1.8, 2.4))
    shake = 22 * sum(math.exp(-(u - k) * 7) * (u > k) for k in (0.6, 1.2, 1.8, 2.4) ) * (u < 3.0) + 30 * math.exp(-(u - 7.0) * 6) * (u > 7.0)
    def d(c):
        dd = T1.at(u)
        res = {}
        # the 9 / 3
        shrink = sm(seg(u, 8.0, 8.8))
        kick = seg(u, 10.6, 11.8)
        if kick <= 0:
            sz = lerp(560, 230, shrink); y = G - 18 * stomp
            if shrink < 1: num(c, "9", nine_x, y, sz, WHITE, 1 - shrink, glw=0.5)
            if shrink > 0: num(c, "3", nine_x, y, sz, YEL, shrink, glw=1.0)
            if 7.0 <= u < 8.9:
                ra = 1 - seg(u, 8.4, 8.9)
                radical(c, nine_x - 150 * (1 - shrink) - 60 * shrink, G - 20, 300 * (1 - shrink) + 130 * shrink, 400 * (1 - shrink) + 170 * shrink, YEL, ra, prog=1.0)
        else:
            x, y = arc(nine_x, G, 1500, 500, 500, eo(kick))
            text(c, "3", x, y - 80, 230, YEL, 1, rot=kick * 9, glw=1.0)
        # thrown sqrt
        if 5.0 <= u < 7.0:
            sp = back(seg(u, 5.0, 5.4)); tt = seg(u, 6.2, 7.0)
            hx, hy = 330, G - 330 + 14 * math.sin(u * 5)
            x, y = arc(hx, hy, nine_x - 60, G - 200, 180, ei(tt) if tt > 0 else 0)
            c.save(); c.translate(x, y); c.rotate(tt * 8); c.scale(max(sp, .01) * 0.6, max(sp, .01) * 0.6)
            glow(c, 0, -60, 170, YEL, 0.35); radical(c, 0, 60, 120, 140, YEL, 1, lw=14); c.restore()
        burst(c, nine_x - 60, G - 200, u - 7.0, 11, n=40, col=YEL, spd=900)
        ring(c, nine_x - 60, G - 200, u - 7.0, YEL, rmax=520)
        burst(c, nine_x, G - 120, u - 8.8, 12, n=24, col=YEL, spd=500)
        burst(c, 680, G - 60, u - 10.6, 13, n=18, col=WHITE, spd=500)
        dot(c, dd["x"], dd["y"], s=1.45, look=(1, 0) if u < 9 else (1, -0.3), sq=dd["sq"], walk=dd["walk"], rot=dd["rot"],
            wide=0.6 < u < 3.0, happy=u > 11.0, blink=False)
        bubble(c, 330, G - 190, "Ouch!", win(u, 4.4, 5.6, 0.2), 36)
        res["flash"] = 0.55 * math.exp(-(u - 7.0) * 5) * (u > 7.0)
        return res
    return cam(560, 1000, 1.0, shake=shake), d, dict(cap=[(0.4, 4.2, "A giant 9 stomps in. Way too big to jump!"),
                                                       (4.5, 8.3, "Dot finds a square root sign..."),
                                                       (8.5, 12.6, "√9 = 3. Giant shrunk, then kicked!")],
                                                  hint=("sqrt", seg(u, 8.4, 8.9) * (1 - seg(u, 13.4, 13.9))))
for k in (0.6, 1.2, 1.8, 2.4): sfx("w1", k, "thud", g=0.9)
sfx("w1", 3.0, "boing"); sfx("w1", 3.55, "boing", g=1.2); sfx("w1", 4.3, "thud", g=0.4); sfx("w1", 5.0, "shimmer")
sfx("w1", 6.2, "whoosh", d=0.8); sfx("w1", 7.0, "boom", g=1.0); sfx("w1", 8.0, "suck"); sfx("w1", 8.8, "ding")
sfx("w1", 10.6, "pop", f=400); sfx("w1", 10.7, "fallwhistle", d=1.0); sfx("w1", 11.2, "tink", p=2); sfx("w1", 12.2, "tink", p=4)

# ================================================================= WAVE 2 - infinity vs 1/x
T2 = Track(540, G)
T2.hop(1.3, 1.9, 340, G, 140); T2.hop(2.2, 2.7, 200, G, 90)
T2.walk(8.8, 9.5, 330); T2.hop(9.6, 10.1, 470, G - 0, 120)
for k in range(3): T2.hop(10.8 + 0.8 * k, 11.3 + 0.8 * k, 470, G, 100)
def inf_x(u): return lerp(1450, 640, sm(seg(u, 0.3, 3.0)))
def w2(u):
    shake = 10 * (seg(u, 0.3, 3.0) > 0) * (u < 3.2) + 26 * math.exp(-(u - 4.4) * 6) * (u > 4.4)
    def d(c):
        dd = T2.at(u)
        x = inf_x(u); grow = lerp(220, 380, seg(u, 0.3, 3.0))
        rot = -(1450 - x) / 120
        sh = sm(seg(u, 4.8, 6.8))
        if u < 6.9:
            sc = lerp(1.0, 0.12, sh)
            cy = G - grow * 0.45 * sc - 10
            if u > 4.4: rot = 0
            text(c, "∞", x, cy, grow * 1.5 * sc, WHITE, 1, rot=rot if u < 4.4 else 0, glw=0.8)
            # fraction falls on top
            if u > 3.4:
                fy = lerp(G - 1000, cy - grow * 0.55 * sc, eo(seg(u, 3.6, 4.4)))
                fa = seg(u, 3.4, 3.7)
                line(c, x - 260 * max(sc, 0.25), fy, x + 260 * max(sc, 0.25), fy, 14 * max(sc, 0.3), YEL, fa, glw=0.8)
                text(c, "1", x, fy - 130 * max(sc, 0.25), 210 * max(sc, 0.25), YEL, fa, glw=0.8)
            if 4.9 < u < 6.9:
                k = min(3, int((u - 4.9) / 0.5))
                lab = ["x = 10:  1/x = 0.1", "x = 1,000:  1/x = 0.001", "x = 1,000,000:  1/x = 0.000001", "x = 10¹²:  1/x = 0.000000000001"][k]
                text(c, lab, 540, G - 760, 46, WHITE, win(u, 4.9, 6.9, 0.2), face=UI, bold=True)
        elif u < 9.9:
            ps = back(seg(u, 6.9, 7.3)); text(c, "0", x, G - 40, 90 * max(ps, .01), YEL, 1, glw=1.0)
        burst(c, x, G - 200, u - 4.4, 21, n=36, col=YEL, spd=800)
        ring(c, x, G - 200, u - 4.4, YEL, rmax=500)
        burst(c, x, G - 40, u - 9.95, 22, n=22, col=YEL, spd=450)
        # dust behind rolling infinity
        if 0.3 < u < 3.2:
            for k in range(6):
                px = x + 140 + k * 40 + (u * 300) % 40; c.set_source_rgba(1, 1, 1, 0.15); c.arc(px, G - 10 - k * 4, 10 - k, 0, 6.3); c.fill()
        dot(c, dd["x"], dd["y"], s=1.45, look=(1, 0), sq=dd["sq"], walk=dd["walk"], rot=dd["rot"], wide=0.3 < u < 3.4, happy=u > 10.2)
        bubble(c, 230, G - 190, "Nope nope nope", win(u, 1.0, 3.2, 0.2), 34)
        return dict(flash=0.45 * math.exp(-(u - 4.4) * 5) * (u > 4.4))
    return cam(560, 1000, 1.0, shake=shake), d, dict(cap=[(0.3, 4.2, "Infinity rolls in. It never stops growing!"),
                                                       (4.4, 8.4, "Put it under 1: the bigger x gets, the smaller 1/x gets"),
                                                       (8.6, 13.4, "It heads to 0. Squash!")],
                                                  hint=("lim", seg(u, 7.0, 7.5) * (1 - seg(u, 13.3, 13.8))))
sfx("w2", 0.3, "rumble", d=2.8); sfx("w2", 1.3, "boing", g=0.6); sfx("w2", 3.4, "fallwhistle", d=1.0); sfx("w2", 4.4, "boom")
for k in range(4): sfx("w2", 4.9 + 0.5 * k, "tick", p=k * 2)
sfx("w2", 6.9, "pop", f=900); sfx("w2", 9.6, "boing"); sfx("w2", 9.95, "burst")
for k in range(3): sfx("w2", 11.3 + 0.8 * k, "tink", p=k + 3)

# ================================================================= WAVE 3 - e^(i pi) ghost vs +1
T3 = Track(380, G)
FIRES = [2.0, 3.1, 4.2]
for f in FIRES: T3.hop(f + 0.22, f + 0.72, 380, G, 190)
def ghost_xy(u):
    return lerp(1300, 740, eo(seg(u, 0, 1.5))), lerp(400, G - 560, eo(seg(u, 0, 1.5))) + 30 * math.sin(u * 2.4)
def w3(u):
    shake = 30 * math.exp(-(u - 7.8) * 6) * (u > 7.8)
    def d(c):
        dd = T3.at(u); gx, gy = ghost_xy(u)
        col = (lerp(1, 1, 0), 0.84, 0.22)
        if u < 7.8:
            imp = sm(seg(u, 6.9, 7.8))
            # ghost body: a soft blob with eyes, wearing its formula
            if imp < 1:
                a = 1 - imp; sc = 1 - 0.9 * imp
                glow(c, gx, gy + 40, 320 * sc, VIO, 0.35 * a)
                c.save(); c.translate(gx, gy + 40); c.scale(sc, sc)
                c.set_source_rgba(*VIO, 0.25 * a); c.move_to(-170, 60)
                c.curve_to(-180, -200, 180, -200, 170, 60)
                for k in range(4): c.line_to(170 - (k + 0.5) * 85, 60 + 40 * (k % 2 == 0));
                c.close_path(); c.fill(); c.restore()
                mtext(c, [("e", "n"), ("iπ", "s")], gx - 40 * (seg(u, 5.6, 6.4)), gy, 200 * sc, YEL, a, glw=0.9)
                for s_ in (-1, 1):
                    c.set_source_rgba(1, 1, 1, a); c.arc(gx + s_ * 45 * sc, gy + 110 * sc, 14 * sc, 0, 6.3); c.fill()
            # +1 flying in and = 0
            if u > 5.0:
                sp = back(seg(u, 5.0, 5.4)); tt = seg(u, 5.6, 6.4)
                x, y = arc(380, G - 300, gx + 160, gy, 120, eo(tt))
                text(c, "+ 1", x, y, 130 * max(sp, .01) * (1 - imp * 0.9), GREEN, 1 - imp, glw=0.9)
            if u > 6.5:
                text(c, "= 0", gx + 400, gy, 130 * (1 - imp * 0.9), WHITE, seg(u, 6.5, 6.8) * (1 - imp), glw=0.7)
            if imp > 0: text(c, "0", gx + 100, gy, 160 * back(imp), WHITE, imp, glw=1.0)
        burst(c, gx + 100, gy, u - 7.8, 31, n=50, col=VIO, spd=1000, life=1.1)
        burst(c, gx + 100, gy, u - 7.8, 32, n=30, col=YEL, spd=700)
        ring(c, gx + 100, gy, u - 7.8, WHITE, rmax=650, life=0.8)
        if u > 8.4:
            fa = seg(u, 8.4, 9.0) * (1 - seg(u, 13.3, 13.8))
            mtext(c, [("e", "n"), ("iπ", "s"), (" + 1 = 0", "n")], 640, G - 560, 150, YEL, fa, glw=0.6)
        # projectiles -1
        for k, f in enumerate(FIRES):
            p = seg(u, f, f + 1.0)
            if 0 < p < 1:
                px = lerp(gx - 140, -150, p); py = G - 50
                text(c, "−1", px, py, 80, CORAL, 1, glw=0.8)
                for j in range(5): c.set_source_rgba(*CORAL, 0.25 - j * 0.05); c.arc(px + 60 + j * 26, py, 10 - j, 0, 6.3); c.fill()
        dot(c, dd["x"], dd["y"], s=1.45, look=(1, -0.6), sq=dd["sq"], walk=dd["walk"], rot=dd["rot"], wide=1.0 < u < 5.0, happy=u > 8.0)
        bubble(c, 420, G - 190, "Missed me!", win(u, 4.9, 5.9, 0.2), 34) if False else None
        return dict(flash=0.6 * math.exp(-(u - 7.8) * 5) * (u > 7.8))
    return cam(580, 980, 1.0, shake=shake), d, dict(cap=[(0.3, 4.4, "A ghost made of e, i and pi throws −1s!"),
                                                       (4.6, 8.4, "Because e^(i pi) = −1... so Dot adds 1"),
                                                       (8.6, 13.4, "Euler's identity: the ghost becomes 0!")])
sfx("w3", 0.0, "whoosh", d=1.4)
for f in FIRES: sfx("w3", f, "pop", f=300); sfx("w3", f + 0.22, "boing", g=0.5)
sfx("w3", 5.0, "shimmer"); sfx("w3", 5.6, "whoosh", d=0.8); sfx("w3", 6.5, "clank"); sfx("w3", 6.9, "suck"); sfx("w3", 7.8, "boom"); sfx("w3", 8.4, "ding")

# ================================================================= WAVE 4 - parabola vs d/dx
T4 = Track(260, G)
T4.hop(1.6, 2.1, 200, G, 120)
HITS4 = [5.2, 8.0, 10.6]
def curve_state(u):
    k = sum(1 for h in HITS4 if u >= h + 0.6)
    m = 0.0
    for i, h in enumerate(HITS4):
        if h <= u < h + 0.6: k = i; m = sm(seg(u, h, h + 0.6))
    return k, m
F = [lambda X: X * X, lambda X: 2 * X, lambda X: 2.0 + 0 * X, lambda X: 0 * X]
LAB = [[("y = x", "n"), ("2", "s")], [("y = 2x", "n")], [("y = 2", "n")], [("y = 0", "n")]]
def w4(u):
    shake = sum(24 * math.exp(-(u - h) * 6) * (u > h) for h in HITS4) + 14 * sum(math.exp(-((u - s_) * 8) ** 2) for s_ in (0.8, 1.6, 2.4, 3.2))
    def d(c):
        dd = T4.at(u)
        vx = lerp(1250, 720, sm(seg(u, 0, 1.4))); k, m = curve_state(u)
        whip = 0.25 * math.sin(u * 7) * (u < 5.0)
        fade = 1 - seg(u, 11.2, 12.0)
        dropy = 600 * ei(seg(u, 10.6 + 0.6, 12.0))
        pts = []
        for i in range(81):
            X = -1.7 + 3.4 * i / 80
            Y0 = F[k](X); Y1 = F[min(k + 1, 3)](X)
            Y = lerp(Y0, Y1, m) if m > 0 else Y0
            if k == 3: Y = 0
            pts.append((vx + X * 230, G - 120 - (Y + whip * X) * 210 + dropy))
        c.save(); c.rectangle(-2000, -3000, 6000, 3000 + G - 4); c.clip()
        for ww, al in ((40, 0.06), (18, 0.12), (8, 1.0)):
            c.set_source_rgba(*WHITE, al * fade); c.set_line_width(ww); c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.stroke()
        c.restore()
        lab = LAB[k] if m < 0.5 else LAB[min(k + 1, 3)]
        mtext(c, lab, vx, G - 860, 110, YEL if k > 0 or m > 0.5 else WHITE, fade, glw=0.6)
        # d/dx projectiles
        for i, h in enumerate(HITS4):
            sp = back(seg(u, h - 1.2, h - 0.9)); tt = seg(u, h - 0.8, h)
            if h - 1.2 <= u < h:
                x, y = arc(240, G - 330, vx - 60, G - 400, 160, ei(tt))
                text(c, "d/dx", x, y, 90 * max(sp, .01), AMBER, 1, face=MATH, rot=tt * 6.3, glw=0.9)
            burst(c, vx - 60, G - 400, u - h, 40 + i, n=34, col=AMBER, spd=800)
            ring(c, vx - 60, G - 400, u - h, AMBER, rmax=420)
        dot(c, dd["x"], dd["y"], s=1.45, look=(1, -0.4), sq=dd["sq"], walk=dd["walk"], rot=dd["rot"], wide=u < 4.0, happy=u > 11.5)
        return dict(flash=sum(0.35 * math.exp(-(u - h) * 6) * (u > h) for h in HITS4))
    return cam(600, 960, 1.0, shake=shake), d, dict(cap=[(0.3, 4.2, "A parabola whips around: y = x squared"),
                                                       (4.4, 7.9, "Differentiate! x squared becomes 2x"),
                                                       (8.1, 10.5, "Again: 2x becomes 2"),
                                                       (10.6, 13.6, "Once more: 2 becomes 0. Flattened!")])
sfx("w4", 0.0, "whoosh", d=1.2)
for s_ in (0.8, 1.6, 2.4, 3.2): sfx("w4", s_, "thud", g=0.5)
for h in HITS4: sfx("w4", h - 1.2, "shimmer"); sfx("w4", h - 0.8, "whoosh", d=0.8); sfx("w4", h, "boom", g=0.8)
sfx("w4", 11.2, "fallwhistle", d=0.8); sfx("w4", 12.0, "thud", g=0.6)

# ================================================================= WAVE 5 - the Sum Titan vs the unit square
TERMS = ["1/2", "1/4", "1/8", "1/16", "1/32", "1/64", "1/128", "1/256"]
NB = len(TERMS)
TX = 800                              # tower centre
BH = [150, 130, 115, 100, 90, 80, 72, 66]   # block heights
def blk_y(k):
    return G - sum(BH[:k]) - BH[k] / 2
TOP_Y = G - sum(BH)
SQ = (110, G - 420, 420)              # x0, y0 top, side
def piece_rect(k):
    """k-th piece: half of the remaining rectangle, alternating vertical/horizontal splits."""
    x0, y0, w, h = SQ[0], SQ[1], SQ[2], SQ[2]
    for i in range(k + 1):
        if i % 2 == 0: r = (x0, y0, w / 2, h); x0 += w / 2; w /= 2
        else: r = (x0, y0, w, h / 2); y0 += h / 2; h /= 2
    return r
T5 = Track(420, G)
T5.walk(2.6, 3.2, 330); T5.hop(4.4, 4.9, 600, G, 90)
T5.hop(14.0, 14.7, 330, SQ[1], 200)
for k in range(3): T5.hop(15.6 + 0.9 * k, 16.1 + 0.9 * k, 330, SQ[1], 110)
PT = [6.4 + 0.62 * k for k in range(NB)]   # piece fly start
def w5(u):
    z = lerp(1.0, 0.72, sm(seg(u, 0.4, 3.5))) if u < 12.8 else lerp(0.72, 0.95, sm(seg(u, 12.8, 14.5)))
    cy = lerp(980, 900, sm(seg(u, 0.4, 3.5))) if u < 12.8 else lerp(900, 960, sm(seg(u, 12.8, 14.5)))
    shake = 8 * (0.4 < u < 3.6) + 34 * math.exp(-(u - 12.0) * 5) * (u > 12.0)
    def d(c):
        dd = T5.at(u)
        # tower drop: blocks below fall as pieces leave
        gone = sum(1 for k in range(NB) if u > PT[k])
        for k in range(NB):
            app = seg(u, 0.4 + 0.32 * k, 0.75 + 0.32 * k)
            if app <= 0: continue
            if u > PT[k]: continue
            drop = sum(BH[j] * sm(seg(u, PT[j], PT[j] + 0.4)) for j in range(k) if u > PT[j])
            y = blk_y(k) + drop - (1 - eo(app)) * 400
            w = 300 - k * 18
            c.set_source_rgba(0.02, 0.02, 0.03, app); c.rectangle(TX - w / 2, y - BH[k] / 2 + 3, w, BH[k] - 6); c.fill()
            c.set_source_rgba(*WHITE, app); c.set_line_width(4); c.rectangle(TX - w / 2, y - BH[k] / 2 + 3, w, BH[k] - 6); c.stroke()
            text(c, ("+ " if k else "") + TERMS[k], TX, y, BH[k] * 0.48, WHITE, app, face=UI, bold=True)
        # Sigma head with eyes
        ha = seg(u, 3.0, 3.5)
        if ha > 0 and u < 12.6:
            drop = sum(BH[j] * sm(seg(u, PT[j], PT[j] + 0.4)) for j in range(NB) if u > PT[j])
            hy = TOP_Y - 170 + drop - (1 - eo(ha)) * 500 + 8 * math.sin(u * 3)
            glow(c, TX, hy, 300, RED, 0.25 * ha)
            text(c, "Σ", TX, hy, 330, WHITE, ha, glw=0.6)
            for s_ in (-1, 1): glow(c, TX + s_ * 40, hy - 20, 40, RED, 0.9 * ha); c.set_source_rgba(1, 0.9, 0.9, ha); c.arc(TX + s_ * 40, hy - 20, 9, 0, 6.3); c.fill()
            text(c, "...", TX, TOP_Y - 20 + drop, 60, WHITE, ha * (1 - seg(u, PT[-1], PT[-1] + 0.3)), face=UI, bold=True)
        if 12.0 <= u < 12.8:
            text(c, "Σ", TX + 200 * seg(u, 12, 12.8), G - 170 + 0, 330, WHITE, 1 - seg(u, 12.0, 12.8), rot=seg(u, 12, 12.8) * 4)
        burst(c, TX, G - 200, u - 12.0, 51, n=60, col=RED, spd=1100, life=1.2)
        # the unit square
        sa = seg(u, 5.0, 5.4)
        if sa > 0:
            x0, y0, s_ = SQ
            prog = seg(u, 5.0, 6.0); per = 4 * s_ * prog
            c.set_line_width(6); c.set_source_rgba(*GREEN, sa); c.move_to(x0, y0 + s_)
            segs = [(x0, y0), (x0 + s_, y0), (x0 + s_, y0 + s_), (x0, y0 + s_)]; px, py = x0, y0 + s_; left = per
            for qx, qy in segs:
                L = math.dist((px, py), (qx, qy)); f = min(1, left / L) if L else 1
                c.line_to(lerp(px, qx, f), lerp(py, qy, f)); left -= L; px, py = qx, qy
                if left <= 0: break
            c.stroke()
            text(c, "1", x0 + s_ / 2, y0 - 34, 46, GREEN, seg(u, 5.8, 6.2), face=UI, bold=True)
            text(c, "1", x0 - 34, y0 + s_ / 2, 46, GREEN, seg(u, 5.8, 6.2), face=UI, bold=True)
        for k in range(NB):
            tt = seg(u, PT[k], PT[k] + 0.5)
            if tt <= 0: continue
            rx, ry, rw, rh = piece_rect(k)
            col = [TEAL, AMBER, BLUE, CORAL, VIO, GREEN, YEL, TEAL][k]
            sx, sy = TX, blk_y(k)
            cx_, cy_ = arc(sx, sy, rx + rw / 2, ry + rh / 2, 220, eo(tt))
            ww, hh = lerp(220, rw, eo(tt)), lerp(BH[k] - 6, rh, eo(tt))
            c.set_source_rgba(*col, 0.85); c.rectangle(cx_ - ww / 2, cy_ - hh / 2, ww, hh); c.fill()
            c.set_source_rgba(0.02, 0.02, 0.03, 1); c.set_line_width(3); c.rectangle(cx_ - ww / 2, cy_ - hh / 2, ww, hh); c.stroke()
            if k < 4: text(c, TERMS[k], cx_, cy_, [64, 52, 38, 28][k], (0.03, 0.05, 0.08), 1, face=UI, bold=True)
            if tt >= 1: burst(c, rx + rw / 2, ry + rh / 2, u - PT[k] - 0.5, 60 + k, n=10, col=col, spd=300, life=0.5, size=5)
        if u > 12.0:
            ea = seg(u, 12.0, 12.4)
            glow(c, SQ[0] + SQ[2] / 2, SQ[1] + SQ[2] / 2, 420, GREEN, 0.45 * ea * (1 - seg(u, 14, 16)))
            c.set_source_rgba(*GREEN, 0.9 * ea); c.rectangle(SQ[0], SQ[1], SQ[2], SQ[2]); c.fill()
            text(c, "= 1", SQ[0] + SQ[2] / 2, SQ[1] + SQ[2] / 2, 150 * max(back(seg(u, 12.0, 12.5)), .01), (0.02, 0.06, 0.05), ea, face=UI, bold=True)
        dot(c, dd["x"], dd["y"], s=1.45, look=(1, -0.8) if u < 12 else (0, -0.3), sq=dd["sq"], walk=dd["walk"], rot=dd["rot"],
            wide=1.0 < u < 5.0, happy=u > 12.4)
        bubble(c, 330, G - 200, "Uh oh...", win(u, 3.4, 4.4, 0.2), 34)
        bubble(c, 330, SQ[1] - 200, "One!", win(u, 15.0, 17.0, 0.2), 38)
        return dict(flash=0.6 * math.exp(-(u - 12.0) * 4) * (u > 12.0))
    return cam(560, cy, z, shake=shake), d, dict(cap=[(0.3, 4.6, "The Sum Titan: 1/2 + 1/4 + 1/8 + ... forever!"),
                                                    (4.8, 8.9, "Dot draws a 1 by 1 square..."),
                                                    (9.1, 12.0, "Each piece fills half of what's left"),
                                                    (12.2, 16.6, "Forever adds up to exactly 1. Titan down!")],
                                                hint=("series", seg(u, 12.6, 13.1) * (1 - seg(u, 19.3, 19.8))))
sfx("w5", 0.4, "rumble", d=3.2)
for k in range(NB): sfx("w5", 0.75 + 0.32 * k, "thud", g=0.35 + 0.05 * k)
sfx("w5", 3.0, "boom", g=0.6); sfx("w5", 5.0, "slide", d=1.0)
for k in range(NB): sfx("w5", PT[k] + 0.5, "tink", p=k)
sfx("w5", 11.0, "swell", d=1.0); sfx("w5", 12.0, "boom", g=1.0); sfx("w5", 12.1, "shimmer"); sfx("w5", 12.4, "ding")
sfx("w5", 14.0, "boing"); [sfx("w5", 16.1 + 0.9 * k, "tink", p=k + 4) for k in range(3)]

# ================================================================= FINALE
def fin(u):
    def d(c):
        dot(c, 540, G, s=1.6, happy=True, sq=0.25 * math.sin(u * 8) * (u < 3))
        return {}
    r = lerp(2200, 330, sm(seg(u, 0.3, 3.0)))
    return cam(540, 1080, lerp(1.0, 0.8, sm(seg(u, 0.3, 3.0)))), d, dict(circle=(r, seg(u, 0.3, 1.0)), win=seg(u, 1.6, 2.2) * (1 - seg(u, 5.2, 5.6)),
                                                                        end=seg(u, 5.4, 6.0), fade=seg(u, 9.5, 10.0),
                                                                        cap=[(1.8, 5.4, "5 waves. 5 real maths tricks. Dot wins!")])
sfx("fin", 0.3, "whoosh", d=1.5); sfx("fin", 1.6, "ding"); sfx("fin", 1.7, "shimmer"); sfx("fin", 5.4, "boom", g=0.5)

ORDER = [("intro", intro), ("w1", w1), ("w2", w2), ("w3", w3), ("w4", w4), ("w5", w5), ("fin", fin)]

# ---------------------------------------------------------------- overlays
def caption(c, s, a, y=1690):
    if a <= 0.01: return
    size = 42; ls = wrap(c, s, size, 900); lh = size * 1.32
    wmax = max(text_w(c, l, size, UI) for l in ls); bw, bh = wmax + 56, lh * len(ls) + 28
    x0, y0 = 540 - bw / 2, y - bh / 2 + 10 * (1 - a); r = min(22, bh / 2)
    c.set_source_rgba(0, 0, 0, 0.7 * a)
    c.new_sub_path(); c.arc(x0 + bw - r, y0 + r, r, -math.pi / 2, 0); c.arc(x0 + bw - r, y0 + bh - r, r, 0, math.pi / 2)
    c.arc(x0 + r, y0 + bh - r, r, math.pi / 2, math.pi); c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi); c.close_path(); c.fill()
    for i, l in enumerate(ls): text(c, l, 540, y0 + 14 + lh * (i + 0.5), size, WHITE, a, face=UI)

def hint(c, kind, a):
    if a <= 0.01: return
    y = 470
    if kind == "sqrt":
        radical(c, 470, y + 50, 80, 110, YEL, a, lw=7); text(c, "9", 555, y, 110, WHITE, a); text(c, "=", 670, y, 110, YEL, a); text(c, "3", 770, y, 110, YEL, a, glw=0.6)
    elif kind == "lim":
        text(c, "lim", 330, y - 10, 100, WHITE, a); text(c, "x→∞", 330, y + 70, 46, WHITE, a)
        line(c, 450, y, 560, y, 6, YEL, a); text(c, "1", 505, y - 60, 90, YEL, a); text(c, "x", 505, y + 60, 90, YEL, a)
        text(c, "=  0", 690, y, 110, YEL, a, glw=0.6)
    elif kind == "series":
        text(c, "1/2 + 1/4 + 1/8 + ...  =  1", 540, y, 66, YEL, a, face=UI, bold=True, glw=0.5)

def banner(c, T):
    for i, (nm, big, sub) in enumerate(WAVES):
        t0 = S[nm]; t1 = S[ORDER[[o[0] for o in ORDER].index(nm) + 1][0]]
        if not (t0 <= T < t1): continue
        u = T - t0
        # big slam then dock at top
        p = sm(seg(u, 1.1, 1.6))
        sc = lerp(back(seg(u, 0, 0.45)) * 1.0, 0.5, p)
        y = lerp(760, 250, p)
        a = 1 - seg(T, t1 - 0.3, t1)
        if u < 1.6:
            c.set_source_rgba(0, 0, 0, 0.45 * (1 - p)); c.paint()
        text(c, big, 540, y, 150 * max(sc, .01), WHITE, a, face=UI, bold=True, glw=0.9)
        text(c, sub, 540, y + 120 * max(sc, .01) + 10, 64 * max(sc, .01), CORAL if i == 4 else YEL, a, face=UI, bold=True)

def frame(c, T):
    name, fn = ORDER[0]
    for n, f in ORDER:
        if T >= S[n]: name, fn = n, f
    u = T - S[name]
    cm, draw, extra = fn(u)
    c.set_source_rgb(0.008, 0.010, 0.016); c.paint()
    circ = extra.get("circle")
    c.save()
    if circ:
        r, ca = circ
        c.arc(540, 1050, r, 0, 2 * math.pi); c.clip()
        c.set_source_rgb(0.02, 0.025, 0.035); c.paint()
    sh = cm.get("shake", 0)
    c.translate(W / 2 + sh * noise(T, 1.0), H / 2 + sh * noise(T + 3.3, 1.1))
    c.scale(cm["z"], cm["z"]); c.rotate(cm["rot"]); c.translate(-cm["x"], -cm["y"])
    draw_world(c, cm)
    res = draw(c) or {}
    c.restore()
    if circ:
        r, ca = circ; c.set_source_rgba(1, 1, 1, 0.85 * ca); c.set_line_width(5); c.arc(540, 1050, r, 0, 2 * math.pi); c.stroke()
    g = cairo.RadialGradient(540, 900, 300, 540, 960, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.7); c.set_source(g); c.paint()
    fl = res.get("flash", 0)
    if fl > 0: c.set_source_rgba(1, 1, 1, min(fl, 0.8)); c.paint()
    # title
    ta = extra.get("title", 0)
    if ta > 0:
        text(c, "DOT", 540, 330, 170, TEAL, ta, face=UI, bold=True, glw=0.9)
        text(c, "vs", 540, 460, 70, MUTED, ta, face=UI)
        text(c, "MATH", 540, 580, 170, WHITE, ta, face=UI, bold=True, glw=0.6)
        text(c, "Can Dot survive 5 waves?", 540, 720, 52, YEL, ta, face=UI, bold=True)
    banner(c, T)
    hk = extra.get("hint")
    if hk: hint(c, hk[0], hk[1])
    wa = extra.get("win", 0)
    if wa > 0:
        s_ = back(seg(u, 1.6, 2.1))
        text(c, "ALL 5 WAVES", 540, 300, 120, GREEN, wa, face=UI, bold=True, glw=0.8, scale=max(s_, .01))
        text(c, "CLEARED!", 540, 430, 120, GREEN, wa, face=UI, bold=True, glw=0.8, scale=max(s_, .01))
        tricks = "√      1/x      +1      d/dx      Σ"
        text(c, tricks, 540, 1580, 70, YEL, wa * seg(u, 2.4, 3.0))
    for (a0, b0, s) in extra.get("cap", []):
        if a0 - 0.1 <= u <= b0 + 0.1: caption(c, s, win(u, a0, b0, 0.25))
    end = extra.get("end", 0)
    if end > 0:
        c.set_source_rgba(0.008, 0.010, 0.016, 0.9 * end); c.paint()
        tw = text_w(c, "DATA in 60s", 84, UI, True)
        logo(c, 540 - (tw + 100) / 2, 815, 1.6, end)
        text(c, "DATA in 60s", 540 + 50, 785, 84, WHITE, end, face=UI, bold=True)
        text(c, "Maths is a superpower", 540, 905, 44, YEL, end, face=UI, bold=True)
        text(c, "Follow for more Dot vs Math", 540, 1500, 50, TEAL, end * seg(u, 6.2, 6.8), face=UI, bold=True)
        dot(c, 540, 1300, s=1.5, happy=True, a=end)
    if T > 1.0 and end <= 0:
        logo(c, 418, 120, 0.7, 0.5); text(c, "DATA in 60s", 560, 108, 34, WHITE, 0.5, face=UI, bold=True)
    fd = extra.get("fade", 0)
    if fd > 0: c.set_source_rgba(0, 0, 0, fd); c.paint()

def render(start, end, out):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(surf); c.set_antialias(cairo.ANTIALIAS_BEST)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr0", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for fi in range(start, end):
        frame(c, fi / FPS); surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    if sys.argv[1] == "still":
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(surf)
        for t in sys.argv[3:]:
            frame(c, float(t)); surf.write_to_png(f"{sys.argv[2]}/f_{float(t):06.2f}.png")
    else:
        render(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
