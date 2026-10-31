"""POV: YOU'RE 1 CLICK - the life of one data point, from a tap on a phone to a business decision.
Original concept for Data in 60. python3 ep.py START END OUT.mp4 | python3 ep.py still DIR t...
"""
import math, sys, subprocess
import numpy as np, cairo
sys.path.insert(0, "/home/claude/engine/anim")
from example_story_mean_median import (text, text_w, line, glow, seg, sm, eo, ei, back, elastic, win, clamp, lerp, arc, noise,
                                       dot, logo, wrap, W, H, FPS, UI, MATH, TEAL, CORAL, AMBER, WHITE, MUTED)
MONO = "DejaVu Sans Mono"
MAG = (1.0, 0.35, 0.75); VIO = (0.62, 0.48, 1.0); YEL = (1.0, 0.84, 0.25); GREEN = (0.35, 0.95, 0.55); BLUE = (0.35, 0.72, 1.0)
BG0, BG1 = (0.010, 0.012, 0.035), (0.035, 0.03, 0.09)

S = dict(hook=0, cable=5.5, db=15, clean=25, group=39, meet=53, pipe=64, end=76)
DURATION = 84.0
COVER_T = 45.6
INTENSITY = [(0, 0.35), (5.5, 0.75), (15, 0.5), (25, 0.55), (39, 0.8), (46, 0.95), (53, 0.6), (64, 0.75), (76, 0.5), (84, 0)]
SFX = []
def cue(t, kind, **kw): SFX.append((t, kind, kw))

def rrect(c, x, y, w, h, r, rgb, a, stroke=None, lw=3):
    r = max(0.1, min(r, h / 2, w / 2))
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()
    c.set_source_rgba(*rgb, a)
    if stroke: c.fill_preserve(); c.set_source_rgba(*stroke[0], stroke[1]); c.set_line_width(lw); c.stroke()
    else: c.fill()

def burst(c, x, y, dt, seed, n=26, col=WHITE, spd=600, life=0.9, size=6):
    if dt < 0 or dt > life: return
    r = np.random.default_rng(seed); a = 1 - dt / life
    for k in range(n):
        ang = r.uniform(0, 2 * math.pi); v = spd * r.uniform(0.3, 1.0)
        c.set_source_rgba(*col, a); c.arc(x + math.cos(ang) * v * dt, y + math.sin(ang) * v * dt + 400 * dt * dt, size * (0.4 + 0.6 * a), 0, 6.3); c.fill()

def bokeh(c, t, a=1.0, seed=3, n=40, drift=20):
    r = np.random.default_rng(seed)
    for k in range(n):
        x = r.uniform(0, W); y = (r.uniform(0, H) - t * drift * r.uniform(0.5, 1.5)) % H; rad = r.uniform(4, 22)
        col = [TEAL, MAG, VIO, BLUE][k % 4]
        glow(c, x, y, rad * 3, col, 0.10 * a)

def caption(c, s, a, y=1700):
    if a <= 0.01: return
    size = 44; ls = wrap(c, s, size, 900); lh = size * 1.3
    wmax = max(text_w(c, l, size, UI, True) for l in ls); bw, bh = wmax + 60, lh * len(ls) + 30
    x0, y0 = 540 - bw / 2, y - bh / 2 + 12 * (1 - a)
    rrect(c, x0, y0, bw, bh, 24, (0, 0, 0), 0.72 * a)
    for i, l in enumerate(ls): text(c, l, 540, y0 + 15 + lh * (i + 0.5), size, WHITE, a, face=UI, bold=True)

CAPS = [(1.4, 5.3, "Tap. You just became data."),
        (5.8, 10.0, "You're now a row: who, what, price, when"),
        (10.2, 14.7, "Racing through fibre at about 200,000 km per second"),
        (15.3, 19.6, "You land in a table. One row among millions"),
        (19.8, 24.7, "Almost all business data lives in tables like this"),
        (25.3, 29.8, "Cleaning time. First: duplicates get deleted"),
        (30.0, 34.6, "Missing price? Fill it with the median: 42.00"),
        (34.8, 38.8, "Weird value? Check it. It was a typo"),
        (39.3, 43.5, "GROUP BY drops every row into its group"),
        (43.7, 48.0, "...and SUM adds each group up"),
        (48.2, 52.8, "Millions of rows. Now just 3 bars"),
        (53.3, 57.6, "Your bar ends up on a screen in a meeting"),
        (57.8, 63.6, "And someone makes a decision because of it"),
        (64.3, 69.8, "Click. Store. Clean. Group. Chart. Decide."),
        (70.0, 75.8, "That's data analysis. And it started with one tap"),
        ]

# ================================================================= scenes
def sc_hook(c, u, T):
    z = 1 + 5 * ei(seg(u, 4.2, 5.5)); bx, by = 540, 1190
    c.save(); c.translate(bx, by); c.scale(z, z); c.translate(-bx, -by)
    bokeh(c, T, 0.8)
    # phone
    px, py, pw, ph = 300, 560, 480, 900
    glow(c, 540, 1000, 520, BLUE, 0.10)
    rrect(c, px, py, pw, ph, 60, (0.06, 0.07, 0.12), 1, stroke=((0.6, 0.65, 0.8), 0.9), lw=6)
    rrect(c, px + 18, py + 18, pw - 36, ph - 36, 46, (0.10, 0.11, 0.18), 1)
    rrect(c, 490, py + 34, 100, 18, 9, (0.02, 0.02, 0.04), 1)
    # product card
    rrect(c, 350, 660, 380, 330, 30, (0.16, 0.18, 0.28), 1)
    # simple shoe icon
    c.set_source_rgba(*MAG, 1); c.move_to(410, 900); c.curve_to(420, 800, 500, 790, 520, 830); c.curve_to(560, 860, 650, 860, 680, 900); c.close_path(); c.fill()
    c.set_source_rgba(1, 1, 1, 0.9); c.rectangle(405, 900, 280, 16); c.fill()
    text(c, "Running Shoes", 540, 1040, 40, WHITE, 1, face=UI, bold=True)
    text(c, "£59.99", 540, 1095, 44, YEL, 1, face=UI, bold=True)
    press = math.exp(-((u - 1.2) * 10) ** 2)
    bw = 300 * (1 - 0.06 * press)
    rrect(c, 540 - bw / 2, by - 50, bw, 100, 50, TEAL, 1)
    text(c, "BUY NOW", 540, by, 40, (0.02, 0.08, 0.08), 1, face=UI, bold=True)
    for k in range(3):
        dt = u - 1.2 - k * 0.12
        if 0 < dt < 0.8: c.set_source_rgba(1, 1, 1, 0.8 * (1 - dt / 0.8)); c.set_line_width(5); c.arc(540, by, 60 + 380 * eo(dt / 0.8), 0, 6.3); c.stroke()
    burst(c, 540, by - 40, u - 1.2, 1, n=30, col=TEAL, spd=700)
    if u > 1.2:
        s = 1.25 * elastic(seg(u, 1.2, 1.9))
        yy = by - 60 - 150 * eo(seg(u, 1.2, 1.7))
        dot(c, 540, yy, s=max(s, .01), look=(0, 0.2) if u < 3 else (0, 1), happy=2.0 < u < 3.0, wide=u > 3.6)
        ta = seg(u, 2.0, 2.4)
        rrect(c, 380, yy - 250, 320, 56, 28, (0, 0, 0), 0.7 * ta, stroke=(TEAL, ta), lw=2)
        text(c, "ROW #4,817,203", 540, yy - 222, 30, TEAL, ta, face=MONO, bold=True)
    c.restore()
    # title (frame 0)
    ta = 1 - seg(u, 4.0, 4.6)
    text(c, "POV:", 540, 230, 90, MAG, ta, face=UI, bold=True, glw=0.8)
    text(c, "You're 1 click", 540, 340, 100, WHITE, ta, face=UI, bold=True, glw=0.5)
    text(c, "Watch where you end up...", 540, 440, 40, MUTED, ta, face=UI)
    fl = math.exp(-(u - 5.3) * 8) * (u > 5.3) + seg(u, 5.0, 5.5)
    return dict(flash=min(1, fl * 0.9))
cue(0.1, "pop", f=500); cue(1.2, "pop", f=900); cue(1.2, "burst"); cue(1.25, "boing", g=0.6); cue(2.0, "tink", p=3)
cue(4.0, "swell", d=1.4); cue(5.4, "whoosh", d=1.0)

def sc_cable(c, u, T):
    cx, cy = 540, 860
    spd = 1.6 if u < 9 else 1.6 + (u - 9) * 0.6
    # tunnel rings
    for k in range(26):
        d = ((k / 26.0) - (T * spd * 0.25)) % 1.0
        d = 0.04 + d * 0.96
        r = 70 / d; a = clamp((1 - d) * 1.2) * 0.9
        col = [TEAL, MAG, BLUE][k % 3]
        if r < 1600:
            c.set_source_rgba(*col, a * 0.5); c.set_line_width(max(1, 8 * (1 - d))); c.arc(cx, cy, r, 0, 6.3); c.stroke()
    for k in range(24):
        ang = k * math.pi / 12 + T * 0.4
        line(c, cx + math.cos(ang) * 60, cy + math.sin(ang) * 60, cx + math.cos(ang) * 1500, cy + math.sin(ang) * 1500, 2, BLUE, 0.18)
    rng = np.random.default_rng(int(T * 30) % 7)
    for k in range(40):
        ang = rng.uniform(0, 6.3); r0 = rng.uniform(150, 900); L = rng.uniform(60, 260)
        line(c, cx + math.cos(ang) * r0, cy + math.sin(ang) * r0, cx + math.cos(ang) * (r0 + L), cy + math.sin(ang) * (r0 + L), 3, WHITE, 0.35)
    glow(c, cx, cy, 300, TEAL, 0.25)
    bob = 12 * math.sin(T * 5)
    dot(c, cx + 8 * noise(T, 0.3), cy + 80 + bob, s=1.5, look=(0, -0.3), wide=u < 2, happy=u > 6.5)
    # data packet card
    fields = [("user_id", "4817"), ("item", "\"shoes\""), ("price", "59.99"), ("time", "\"14:03\"")]
    ca = seg(u, 0.4, 0.9)
    rrect(c, 230, 1080, 620, 360, 30, (0.02, 0.03, 0.08), 0.85 * ca, stroke=(TEAL, 0.9 * ca), lw=3)
    text(c, "{", 270, 1130, 44, MUTED, ca, face=MONO, anchor="l")
    for k, (kk, vv) in enumerate(fields):
        fa = seg(u, 0.8 + 0.7 * k, 1.1 + 0.7 * k)
        y = 1185 + k * 56
        text(c, f"  {kk}: ", 270, y, 38, BLUE, fa, face=MONO, anchor="l")
        text(c, vv, 270 + text_w(c, f"  {kk}: ", 38, MONO), y, 38, YEL if k == 2 else WHITE, fa, face=MONO, bold=True, anchor="l")
    text(c, "}", 270, 1405, 44, MUTED, ca, face=MONO, anchor="l")
    # speed readout
    sa = seg(u, 4.6, 5.0)
    text(c, "SPEED", 540, 250, 26, MUTED, sa, face=UI, bold=True)
    v = int(200000 * eo(seg(u, 4.6, 6.0)))
    text(c, f"≈ {v:,} km/s", 540, 320, 74, TEAL, sa, face=UI, bold=True, glw=0.6)
    text(c, "light inside a fibre-optic cable", 540, 395, 30, MUTED, sa, face=UI)
    fl = math.exp(-u * 6) * 0.9 + seg(u, 9.1, 9.5) * 0 + (math.exp(-(u - 9.2) * 6) * 0.35 if u > 9.2 else 0)
    return dict(flash=fl, shake=4 + 6 * seg(u, 7, 9.5))
for k in range(4): cue(S["cable"] + 0.8 + 0.7 * k, "tick", p=k * 2)
cue(S["cable"] + 0.2, "rumble", d=9.0); cue(S["cable"] + 4.6, "shimmer"); cue(S["cable"] + 9.2, "whoosh", d=0.8); cue(S["cable"] + 8.0, "swell", d=1.5)

ROWS = [("4790", "\"bags\"", "35.00"), ("4801", "\"hats\"", "18.50"), ("4817", "\"shoes\"", "59.99"), ("4823", "\"bags\"", "42.00"), ("4831", "\"shoes\"", "74.00")]
def table(c, x0, y0, rw, rh, rows, a, hl=None, dot_row=None, T=0, cols=("user", "item", "price"), cw=None):
    cw = cw or [rw * 0.3, rw * 0.38, rw * 0.32]
    rrect(c, x0, y0 - rh, rw, rh, 12, (0.12, 0.14, 0.24), a)
    xx = x0
    for k, h in enumerate(cols):
        text(c, h, xx + 26, y0 - rh / 2, rh * 0.42, MUTED, a, face=UI, bold=True, anchor="l"); xx += cw[k]
    for i, r in enumerate(rows):
        y = y0 + i * rh
        if r is None: continue
        bg = (0.06, 0.07, 0.13) if i % 2 == 0 else (0.08, 0.09, 0.16)
        rrect(c, x0, y + 2, rw, rh - 4, 8, bg, a)
        if hl and i in hl: rrect(c, x0, y + 2, rw, rh - 4, 8, hl[i][0], hl[i][1] * a)
        xx = x0
        for k, v in enumerate(r):
            text(c, v, xx + 26, y + rh / 2, rh * 0.42, WHITE, a, face=MONO, anchor="l"); xx += cw[k]

def sc_db(c, u, T):
    bokeh(c, T, 0.5, seed=5)
    zoom = lerp(1.0, 0.16, ei(seg(u, 4.4, 9.0)))
    c.save(); c.translate(540, 900); c.scale(zoom, zoom); c.translate(-540, -900)
    # huge field of tables (only visible when zoomed out)
    fa = seg(u, 4.6, 6.5)
    if fa > 0:
        for gx in range(-6, 7):
            for gy in range(-7, 8):
                if gx == 0 and gy == 0: continue
                x0 = 140 + gx * 900; y0 = 700 + gy * 560
                c.set_source_rgba(0.10, 0.12, 0.22, 0.9 * fa); c.rectangle(x0, y0 - 60, 800, 60); c.fill()
                for i in range(7):
                    c.set_source_rgba(0.06 + 0.02 * (i % 2), 0.07, 0.14, 0.9 * fa); c.rectangle(x0, y0 + i * 60, 800, 56); c.fill()
                    c.set_source_rgba(*[TEAL, MAG, VIO, BLUE][(gx + gy + i) % 4], 0.8 * fa); c.arc(x0 + 30, y0 + i * 60 + 28, 12, 0, 6.3); c.fill()
    rows = [r for r in ROWS]; dock = seg(u, 0.4, 2.0)
    disp = list(rows); disp[2] = None if dock < 1 else rows[2]
    table(c, 140, 700, 800, 90, disp, 1, hl={2: (TEAL, 0.25 * dock)})
    # Dot flying in to its slot
    sx, sy = lerp(540, 110, eo(dock)), lerp(-300, 700 + 2 * 90 + 45 + 40, eo(dock))
    dot(c, sx, sy, s=0.9 if dock >= 1 else 1.2, look=(1, 0.3), happy=u > 2.2 and u < 4.4, wide=u > 4.6)
    c.restore()
    na = seg(u, 5.0, 5.6)
    cnt = int(lerp(5, 4817203, ei(seg(u, 5.0, 9.0))))
    text(c, f"{cnt:,} rows", 540, 290, 92, WHITE, na, face=UI, bold=True, glw=0.5)
    text(c, "and you're one of them", 540, 390, 40, TEAL, na, face=UI, bold=True)
    if u > 6:
        # pulsing locator ring on our row
        r = 40 + 10 * math.sin(T * 6); c.set_source_rgba(*TEAL, 0.9 * seg(u, 6, 6.5)); c.set_line_width(4); c.arc(540 + (110 - 540) * zoom, 900 + (700 + 225 + 40 - 900) * zoom, r, 0, 6.3); c.stroke()
    return dict(flash=math.exp(-u * 6) * 0.8)
cue(S["db"] + 0.3, "fallwhistle", d=1.4); cue(S["db"] + 2.0, "thud", g=0.6); cue(S["db"] + 4.4, "whoosh", d=2.0); cue(S["db"] + 5.0, "swell", d=4.0)
for k in range(12): cue(S["db"] + 5.2 + k * 0.32, "tick", p=k % 6, g=0.5)

def sc_clean(c, u, T):
    bokeh(c, T, 0.4, seed=8)
    text(c, "DATA CLEANING", 540, 260, 70, WHITE, 1, face=UI, bold=True, glw=0.4)
    base = [("4790", "\"bags\"", "35.00"), ("4801", "\"hats\"", "18.50"), ("4817", "\"shoes\"", "59.99"), ("4817", "\"shoes\"", "59.99"),
            ("4823", "\"bags\"", "?"), ("4831", "\"shoes\"", "74.00"), ("4840", "\"hats\"", "9,999.00")]
    rh = 96; x0, y0 = 120, 520
    gone = sm(seg(u, 4.8, 5.4))      # duplicate dissolves, rows slide up
    fill = seg(u, 8.8, 9.3)
    fixd = seg(u, 12.6, 13.1)
    c.save()
    c.rectangle(0, 0, W, H); c.clip()
    # header
    rrect(c, x0, y0 - rh, 840, rh, 12, (0.12, 0.14, 0.24), 1)
    for k, h in enumerate(("user", "item", "price")): text(c, h, x0 + 26 + [0, 210, 430][k], y0 - rh / 2, 40, MUTED, 1, face=UI, bold=True, anchor="l")
    for i, r in enumerate(base):
        y = y0 + i * rh - (rh * gone if i > 3 else 0)
        a = 1.0
        if i == 3: a = 1 - gone
        if a <= 0.01: continue
        bg = (0.06, 0.07, 0.13) if i % 2 == 0 else (0.08, 0.09, 0.16)
        rrect(c, x0, y + 2, 840, rh - 4, 8, bg, a)
        if i == 2: rrect(c, x0, y + 2, 840, rh - 4, 8, TEAL, 0.18)
        if i == 3 and u > 1.8: rrect(c, x0, y + 2, 840, rh - 4, 8, CORAL, 0.25 * a * (0.6 + 0.4 * math.sin(T * 12)))
        if i == 4 and u > 6.0: rrect(c, x0, y + 2, 840, rh - 4, 8, AMBER, 0.22 * (1 - fill * 0.5))
        if i == 6 and u > 10.0: rrect(c, x0, y + 2, 840, rh - 4, 8, MAG, 0.22 * (1 - fixd * 0.6))
        vals = list(r)
        if i == 4: vals[2] = "?" if fill <= 0 else "42.00"
        if i == 6 and fixd > 0: vals[2] = "99.99"
        for k, v in enumerate(vals):
            col = WHITE
            if i == 4 and k == 2: col = AMBER if fill > 0 else CORAL
            if i == 6 and k == 2: col = GREEN if fixd > 0 else MAG
            text(c, v, x0 + 26 + [0, 210, 430][k], y + rh / 2, 40, col, a, face=MONO, bold=(k == 2), anchor="l",
                 scale=1 + 0.4 * math.exp(-((u - 8.9) * 6) ** 2) * (i == 4 and k == 2))
        if i in (2, 3):
            dot(c, x0 - 50 + (0 if i == 2 else 0), y + rh - 4, s=0.75, look=(0, 1) if i == 2 and 2 < u < 4.6 else (1, 0), a=a, wide=(i == 2 and 3 < u < 4.8))
        # tags
        tag = None
        if i == 3 and 1.8 < u: tag = ("DUPLICATE", CORAL, a)
        if i == 4 and 6.0 < u < 9.0: tag = ("MISSING", AMBER, 1)
        if i == 4 and u >= 9.0: tag = ("FILLED", AMBER, 1 - seg(u, 13.6, 14))
        if i == 6 and 10.0 < u < 12.6: tag = ("OUTLIER?", MAG, 1)
        if i == 6 and u >= 12.6: tag = ("TYPO FIXED", GREEN, 1)
        if tag:
            tw = text_w(c, tag[0], 24, UI, True) + 30
            rrect(c, 960 - tw - 6, y + 22, tw, 46, 23, tag[1], 0.95 * tag[2])
            text(c, tag[0], 960 - tw / 2 - 6, y + 45, 24, (0.03, 0.03, 0.06), tag[2], face=UI, bold=True)
    c.restore()
    # scanner beam
    sb = seg(u, 0.2, 1.8)
    if 0 < sb < 1:
        y = lerp(y0 - 20, y0 + 7 * rh, sb)
        g = cairo.LinearGradient(0, y - 60, 0, y + 6); g.add_color_stop_rgba(0, *TEAL, 0); g.add_color_stop_rgba(1, *TEAL, 0.35)
        c.set_source(g); c.rectangle(x0 - 20, y - 60, 880, 66); c.fill(); line(c, x0 - 20, y, x0 + 860, y, 4, TEAL, 1, glw=1)
    burst(c, 540, y0 + 3 * rh + 48, u - 4.8, 31, n=40, col=CORAL, spd=600)
    # median helper
    ma = win(u, 7.0, 10.6, 0.3)
    if ma > 0:
        vals = [18.50, 35.00, 42.00, 59.99, 74.00]
        rrect(c, 120, 1270, 840, 210, 26, (0.03, 0.04, 0.09), 0.92 * ma, stroke=(AMBER, 0.8 * ma))
        text(c, "known prices, sorted:", 540, 1310, 30, MUTED, ma, face=UI, bold=True)
        for k, v in enumerate(vals):
            x = 220 + k * 160; on = k == 2 and u > 8.2
            if on: rrect(c, x - 70, 1345, 140, 60, 14, AMBER, 0.3 * ma)
            text(c, f"{v:.2f}", x, 1375, 36, AMBER if on else WHITE, ma, face=MONO, bold=on)
        text(c, "middle value = median = 42.00", 540, 1445, 32, AMBER, ma * seg(u, 8.2, 8.6), face=UI, bold=True)
    oa = win(u, 10.2, 13.8, 0.3)
    if oa > 0:
        rrect(c, 120, 1290, 840, 170, 26, (0.03, 0.04, 0.09), 0.92 * oa, stroke=(MAG, 0.8 * oa))
        text(c, "a £9,999 hat? Check the source...", 540, 1345, 36, WHITE, oa, face=UI, bold=True)
        text(c, "real price: £99.99", 540, 1410, 38, GREEN, oa * seg(u, 12.0, 12.4), face=UI, bold=True)
    return dict(flash=math.exp(-u * 6) * 0.6)
cue(S["clean"] + 0.2, "slide", d=1.6); cue(S["clean"] + 1.8, "clank"); cue(S["clean"] + 4.8, "burst"); cue(S["clean"] + 5.0, "suck")
cue(S["clean"] + 6.0, "tick", p=0); cue(S["clean"] + 8.2, "tink", p=2); cue(S["clean"] + 8.9, "pop", f=800)
cue(S["clean"] + 10.0, "clank"); cue(S["clean"] + 12.6, "ding")

CATS = [("Shoes", TEAL, 1.0), ("Bags", AMBER, 0.62), ("Hats", VIO, 0.38)]
def sc_group(c, u, T):
    bokeh(c, T, 0.4, seed=11)
    # SQL
    code = ["SELECT item, SUM(price)", "FROM sales", "GROUP BY item;"]
    rrect(c, 110, 190, 860, 230, 26, (0.02, 0.03, 0.07), 0.9, stroke=((1, 1, 1), 0.12), lw=2)
    for k, ln in enumerate(code):
        n = int(len(ln) * clamp((u - 0.2 - k * 0.8) / 0.7))
        hl = (k == 2 and 0.6 < u < 6) or (k == 0 and 4.6 < u < 9)
        if hl: rrect(c, 125, 222 + k * 62, 830, 54, 10, YEL, 0.15)
        text(c, ln[:n], 150, 250 + k * 62, 40, WHITE if hl else (0.75, 0.8, 0.9), 1, face=MONO, anchor="l")
    # bins and bars
    base = 1500; bw = 220; xs = [230, 540, 850]
    rng = np.random.default_rng(7)
    N = 150
    starts = rng.uniform(1.0, 8.0, N); cats = rng.choice(3, N, p=[0.5, 0.3, 0.2]); xr = rng.uniform(-90, 90, N)
    for k, (nm, col, hfrac) in enumerate(CATS):
        grow = sm(seg(u, 1.4, 9.0)) * hfrac
        h = 700 * grow
        x = xs[k]
        c.set_source_rgba(*col, 0.85); c.rectangle(x - bw / 2, base - h, bw, h); c.fill()
        glow(c, x, base - h, 120, col, 0.25)
        text(c, nm, x, base + 50, 40, col, 1, face=UI, bold=True)
        line(c, x - bw / 2 - 10, base - 6, x - bw / 2 - 10, base - 760, 3, (1, 1, 1), 0.08); line(c, x + bw / 2 + 10, base - 6, x + bw / 2 + 10, base - 760, 3, (1, 1, 1), 0.08)
    line(c, 80, base, 1000, base, 4, WHITE, 0.6)
    for i in range(N):
        p = seg(u, starts[i], starts[i] + 0.9)
        if 0 < p < 1:
            k = cats[i]; col = CATS[k][1]
            x = lerp(540 + xr[i] * 4, xs[k] + xr[i] * 0.8, eo(p)); y = lerp(470, base - 700 * sm(seg(u, 1.4, 9.0)) * CATS[k][2], p * p)
            c.set_source_rgba(*col, 0.9); c.arc(x, y, 11, 0, 6.3); c.fill()
    # our Dot: slow-mo fall into Shoes
    p = seg(u, 4.6, 7.4); slow = 0.5 - 0.5 * math.cos(math.pi * p)
    topy = base - 700 * sm(seg(u, 1.4, 9.0)) * 1.0
    if u < 7.4:
        x = lerp(540, xs[0], eo(p)); y = lerp(500, topy - 10, slow)
        dot(c, x, y, s=1.15, look=(-0.5, 1), wide=True, rot=p * 1.5)
        if 4.6 < u < 7.4:
            text(c, "SLOW-MO", 540 + 260, 520, 30, MAG, 0.8 + 0.2 * math.sin(T * 10), face=UI, bold=True)
            for j in range(4): c.set_source_rgba(*TEAL, 0.15 - j * 0.03); c.arc(lerp(540, xs[0], eo(max(0, p - 0.05 * (j + 1)))), lerp(500, topy, max(0, slow - 0.06 * (j + 1))) - 40, 30, 0, 6.3); c.fill()
    else:
        dot(c, xs[0], topy, s=0.7, happy=True, look=(0, -1))
    burst(c, xs[0], topy, u - 7.4, 41, n=30, col=TEAL, spd=500)
    sa = seg(u, 9.4, 9.9)
    for k, (nm, col, hf) in enumerate(CATS):
        text(c, ["£284k", "£176k", "£108k"][k], xs[k], base - 700 * hf - 80, 46, WHITE, sa, face=UI, bold=True)
    fl = math.exp(-u * 6) * 0.6 + (0.4 * math.exp(-(u - 7.4) * 6) if u > 7.4 else 0)
    return dict(flash=fl)
for k in range(30): cue(S["group"] + 1.0 + k * 0.23, "tick", p=k % 6, g=0.4)
cue(S["group"] + 4.6, "swell", d=2.8); cue(S["group"] + 7.4, "thud", g=0.8); cue(S["group"] + 7.45, "ding"); cue(S["group"] + 9.4, "shimmer")

def sc_meet(c, u, T):
    bokeh(c, T, 0.3, seed=13)
    z = lerp(2.2, 1.0, eo(seg(u, 0, 2.2)))
    c.save(); c.translate(540, 760); c.scale(z, z); c.translate(-540, -760)
    # room: screen on wall
    g = cairo.LinearGradient(0, 300, 0, 1300); g.add_color_stop_rgba(0, *BLUE, 0.10); g.add_color_stop_rgba(1, *BLUE, 0.0)
    c.set_source(g); c.rectangle(0, 300, W, 1000); c.fill()
    rrect(c, 120, 420, 840, 620, 20, (0.05, 0.06, 0.12), 1, stroke=((0.7, 0.75, 0.9), 0.8), lw=6)
    text(c, "Sales by item", 540, 480, 40, WHITE, 1, face=UI, bold=True)
    base = 960; xs = [330, 540, 750]
    for k, (nm, col, hf) in enumerate(CATS):
        h = 380 * hf; c.set_source_rgba(*col, 0.9); c.rectangle(xs[k] - 70, base - h, 140, h); c.fill()
        text(c, nm, xs[k], base + 40, 30, col, 1, face=UI, bold=True)
    line(c, 200, base, 880, base, 3, WHITE, 0.6)
    dot(c, xs[0], base - 380, s=0.45, happy=True, look=(0, -1))
    # laser pointer circling shoes bar
    if u > 2.5:
        ang = T * 4; lx, ly = xs[0] + 90 * math.cos(ang), base - 250 + 60 * math.sin(ang)
        glow(c, lx, ly, 40, (1, 0.2, 0.25), 0.8); c.set_source_rgba(1, 0.4, 0.4, 1); c.arc(lx, ly, 7, 0, 6.3); c.fill()
    # table + heads silhouettes
    c.set_source_rgba(0.08, 0.09, 0.15, 1); c.move_to(160, 1420); c.line_to(920, 1420); c.line_to(1040, 1700); c.line_to(40, 1700); c.close_path(); c.fill()
    for k, hx in enumerate((200, 400, 680, 880)):
        c.set_source_rgba(0.13, 0.14, 0.22, 1); c.arc(hx, 1300, 52, 0, 6.3); c.fill(); c.rectangle(hx - 80, 1340, 160, 90); c.fill()
    c.restore()
    da = seg(u, 4.6, 5.0)
    if da > 0:
        s = back(seg(u, 4.6, 5.1))
        c.save(); c.translate(540, 1150); c.scale(max(s, .01), max(s, .01))
        rrect(c, -330, -80, 660, 160, 34, GREEN, 0.95 * da)
        text(c, "DECISION: order more shoes", 0, 0, 44, (0.02, 0.08, 0.05), da, face=UI, bold=True)
        c.restore()
    return dict(flash=math.exp(-u * 6) * 0.5)
cue(S["meet"] + 0.1, "whoosh", d=1.6); cue(S["meet"] + 2.5, "tink", p=1); cue(S["meet"] + 4.6, "boom", g=0.6); cue(S["meet"] + 4.7, "ding")

NODES = [("CLICK", MAG), ("STORE", BLUE), ("CLEAN", AMBER), ("GROUP", TEAL), ("CHART", VIO), ("DECIDE", GREEN)]
def node_xy(k): return (270 if k % 2 == 0 else 810), 430 + k * 190
def sc_pipe(c, u, T):
    bokeh(c, T, 0.5, seed=17)
    text(c, "THE JOURNEY OF 1 CLICK", 540, 270, 62, WHITE, seg(u, 0, 0.4), face=UI, bold=True, glw=0.4)
    prog = clamp((u - 0.6) / 6.0) * 5
    for k in range(5):
        x0, y0 = node_xy(k); x1, y1 = node_xy(k + 1)
        f = clamp(prog - k)
        line(c, x0, y0, x1, y1, 6, (1, 1, 1), 0.12)
        if f > 0: line(c, x0, y0, lerp(x0, x1, f), lerp(y0, y1, f), 8, NODES[k + 1][1], 0.95, glw=0.8)
    for k, (nm, col) in enumerate(NODES):
        x, y = node_xy(k); on = prog >= k - 0.02
        s = back(seg(prog, k, k + 0.3)) if on else 0.85
        rrect(c, x - 170 * s, y - 60 * s, 340 * s, 120 * s, 60 * s, col if on else (0.15, 0.16, 0.25), 0.95)
        text(c, nm, x, y, 46 * s, (0.02, 0.03, 0.06) if on else MUTED, 1, face=UI, bold=True)
    k = min(4, int(prog)); f = sm(prog - k) if prog < 5 else 1
    x0, y0 = node_xy(k); x1, y1 = node_xy(min(5, k + 1))
    dx, dy = lerp(x0, x1, f), lerp(y0, y1, f) - 70
    dot(c, dx, dy - 20 * abs(math.sin(T * 8)) * (prog < 5), s=0.9, happy=prog >= 5, look=(1 if x1 > x0 else -1, 0.3))
    ea = seg(u, 7.0, 7.5)
    text(c, "= DATA ANALYSIS", 540, 1580, 70, YEL, ea, face=UI, bold=True, glw=0.7, scale=max(back(seg(u, 7.0, 7.5)), .01))
    return dict(flash=math.exp(-u * 6) * 0.5 + (0.3 * math.exp(-(u - 7.0) * 6) if u > 7 else 0))
for k in range(6): cue(S["pipe"] + 0.6 + 1.2 * k, "pop", f=500 + 120 * k)
cue(S["pipe"] + 7.0, "boom", g=0.6); cue(S["pipe"] + 7.1, "shimmer")

def sc_end(c, u, T):
    # galaxy of dots forming a big bar chart
    rng = np.random.default_rng(99); N = 1800
    gx = rng.uniform(150, 930, N); col = np.where(gx < 410, 0, np.where(gx < 670, 1, 2))
    hmax = np.array([1.0, 0.62, 0.38])[col] * 900
    gy = 1500 - rng.uniform(0, 1, N) * hmax
    ox, oy = rng.uniform(-600, 1700, N), rng.uniform(-400, 2300, N)
    p = eo(seg(u, 0.2, 3.0))
    for i in range(0, N):
        x, y = lerp(ox[i], gx[i], p), lerp(oy[i], gy[i], p)
        cc = CATS[col[i]][1]; c.set_source_rgba(*cc, 0.85); c.rectangle(x - 3, y - 3, 6, 6); c.fill()
    ta = seg(u, 2.6, 3.2) * (1 - seg(u, 4.6, 5.0))
    rrect(c, 70, 300, 940, 300, 30, (0, 0, 0), 0.6 * ta)
    text(c, "Every chart is made of", 540, 390, 62, WHITE, ta, face=UI, bold=True)
    text(c, "millions of you.", 540, 500, 84, TEAL, ta, face=UI, bold=True, glw=0.7)
    ea = seg(u, 4.8, 5.4)
    if ea > 0:
        c.set_source_rgba(*BG0, 0.9 * ea); c.paint()
        tw = text_w(c, "DATA in 60s", 84, UI, True)
        logo(c, 540 - (tw + 100) / 2, 815, 1.6, ea)
        text(c, "DATA in 60s", 540 + 50, 785, 84, WHITE, ea, face=UI, bold=True)
        text(c, "Learn to read the story in data", 540, 905, 40, MUTED, ea, face=UI)
        dot(c, 540, 1230, s=1.4, happy=True, a=ea)
        text(c, "Follow for more", 540, 1400, 54, TEAL, ea * seg(u, 5.6, 6.2), face=UI, bold=True)
    return dict(fade=seg(u, 7.5, 8.0))
cue(S["end"] + 0.2, "swell", d=2.8); cue(S["end"] + 3.0, "ding"); cue(S["end"] + 4.8, "boom", g=0.5)

ORDER = [("hook", sc_hook), ("cable", sc_cable), ("db", sc_db), ("clean", sc_clean), ("group", sc_group), ("meet", sc_meet), ("pipe", sc_pipe), ("end", sc_end)]

def frame(c, T):
    name, fn = ORDER[0]
    for n, f in ORDER:
        if T >= S[n]: name, fn = n, f
    u = T - S[name]
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *BG0); g.add_color_stop_rgb(0.55, *BG1); g.add_color_stop_rgb(1, *BG0)
    c.set_source(g); c.paint()
    c.save()
    res = {}
    sh = 0
    c.save()
    res = fn(c, u, T) or {}
    c.restore()
    c.restore()
    vg = cairo.RadialGradient(540, 900, 380, 540, 960, 1250); vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0, 0, 0, 0.6)
    c.set_source(vg); c.paint()
    for (a0, b0, s) in CAPS:
        if a0 - 0.1 <= T <= b0 + 0.1: caption(c, s, win(T, a0, b0, 0.25))
    if T > 5.5 and T < S["end"] + 4.8:
        logo(c, 412, 95, 0.7, 0.5); text(c, "DATA in 60s", 560, 83, 32, WHITE, 0.5, face=UI, bold=True)
    fl = res.get("flash", 0)
    if fl > 0: c.set_source_rgba(1, 1, 1, min(0.85, fl)); c.paint()
    fd = res.get("fade", 0)
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
