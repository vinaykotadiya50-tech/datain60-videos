"""Our ORIGINAL stick-figure hero for "Dot vs Math": a white stick body whose head is Dot (the teal data point with eyes).
Not a copy of any existing character: teal glowing Dot head with eyes, white limbs, teal hands.
hero(c, x, y, pose_name or dict, s=1.0, flip=False, rot=0.0, look=(1,0), happy=False, wide=False, a=1.0)
(x, y) = point on the ground between the feet (grounded) or the feet level (air).
"""
import math, sys, cairo
sys.path.insert(0, "/home/claude/engine/anim")
from example_story_mean_median import glow, TEAL, WHITE, seg, sm

# angles in degrees: 0 = straight down, positive = towards the facing direction (forward), 180 = straight up
POSES = {
    "stand":   dict(lean=0,   sh_f=14,  el_f=12,  sh_b=-14,  el_b=12,  hip_f=8,   kn_f=-4,   hip_b=-8,  kn_b=-4),
    "ready":   dict(lean=10,  sh_f=70,  el_f=95,  sh_b=40,   el_b=110, hip_f=28,  kn_f=-26,  hip_b=-22, kn_b=-18),
    "crouch":  dict(lean=28,  sh_f=50,  el_f=50,  sh_b=-35,  el_b=30,  hip_f=85,  kn_f=-115, hip_b=35,  kn_b=-115),
    "air":     dict(lean=8,   sh_f=150, el_f=25,  sh_b=135,  el_b=25,  hip_f=70,  kn_f=-95,  hip_b=15,  kn_b=-75),
    "punch":   dict(lean=18,  sh_f=92,  el_f=0,   sh_b=-25,  el_b=115, hip_f=32,  kn_f=-12,  hip_b=-32, kn_b=0),
    "wind":    dict(lean=-12, sh_f=40,  el_f=70,  sh_b=-150, el_b=-45, hip_f=22,  kn_f=-12,  hip_b=-24, kn_b=-6),
    "throw":   dict(lean=22,  sh_f=20,  el_f=30,  sh_b=115,  el_b=5,   hip_f=34,  kn_f=-10,  hip_b=-36, kn_b=-4),
    "kick":    dict(lean=-18, sh_f=55,  el_f=70,  sh_b=-55,  el_b=40,  hip_f=100, kn_f=0,    hip_b=-6,  kn_b=0),
    "hurt":    dict(lean=-32, sh_f=-45, el_f=-30, sh_b=-85,  el_b=-25, hip_f=35,  kn_f=-25,  hip_b=-12, kn_b=-25),
    "scared":  dict(lean=-14, sh_f=120, el_f=110, sh_b=100,  el_b=120, hip_f=12,  kn_f=-18,  hip_b=-14, kn_b=-12),
    "cast":    dict(lean=6,   sh_f=105, el_f=10,  sh_b=150,  el_b=20,  hip_f=26,  kn_f=-14,  hip_b=-26, kn_b=-6),
    "victory": dict(lean=0,   sh_f=160, el_f=8,   sh_b=-160, el_b=-8,  hip_f=12,  kn_f=-4,   hip_b=-12, kn_b=-4),
    "point":   dict(lean=6,   sh_f=95,  el_f=0,   sh_b=-20,  el_b=20,  hip_f=14,  kn_f=-6,   hip_b=-14, kn_b=-6),
}
KEYS = list(POSES["stand"].keys())

def run_pose(ph):
    s, c2 = math.sin(ph), math.sin(ph + 1.6)
    return dict(lean=16, sh_f=-55 * s, el_f=80, sh_b=55 * s, el_b=80,
                hip_f=45 * s, kn_f=-20 - 55 * max(0, c2), hip_b=-45 * s, kn_b=-20 - 55 * max(0, -c2))

def blend(p, q, t):
    return {k: p[k] + (q[k] - p[k]) * t for k in KEYS}

def pose_at(u, base, acts, ramp=0.12):
    """base: pose dict; acts: list of (t0, t1, name_or_dict). Blends in/out with a short ramp."""
    p = base
    for t0, t1, nm in acts:
        if t0 - ramp <= u <= t1 + ramp:
            q = POSES[nm] if isinstance(nm, str) else nm
            w = min(sm(seg(u, t0 - ramp, t0)), 1 - sm(seg(u, t1, t1 + ramp)))
            p = blend(p, q, w)
    return p

def _pt(x, y, ang, L, fwd):
    r = math.radians(ang)
    return x + fwd * math.sin(r) * L, y + math.cos(r) * L

def joints(p, s=1.0, fwd=1):
    T, UA, FA, TH, SH = 82 * s, 46 * s, 44 * s, 54 * s, 54 * s
    hip = (0.0, 0.0)
    lean = p["lean"]
    neck = (fwd * math.sin(math.radians(lean)) * T, -math.cos(math.radians(lean)) * T)
    J = dict(hip=hip, neck=neck)
    for side in ("f", "b"):
        e = _pt(*neck, p["sh_" + side] + lean * 0.3, UA, fwd); h = _pt(*e, p["sh_" + side] + p["el_" + side] + lean * 0.3, FA, fwd)
        k = _pt(*hip, p["hip_" + side], TH, fwd); f = _pt(*k, p["hip_" + side] + p["kn_" + side], SH, fwd)
        J["el_" + side], J["hand_" + side], J["kn_" + side], J["ft_" + side] = e, h, k, f
    return J

def hero(c, x, y, pose, s=1.0, flip=False, rot=0.0, look=(1, 0), happy=False, wide=False, blink=False, air=False, a=1.0):
    if a <= 0.003: return
    p = POSES[pose] if isinstance(pose, str) else pose
    fwd = -1 if flip else 1
    J = joints(p, s, fwd)
    footy = max(J["ft_f"][1], J["ft_b"][1])
    oy = -footy if not air else -118 * s
    c.save(); c.translate(x, y); c.rotate(rot); c.translate(0, oy)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    def limb(pts, w, col, al):
        c.set_source_rgba(*col, al); c.set_line_width(w); c.move_to(*pts[0]); [c.line_to(*q) for q in pts[1:]]; c.stroke()
    back = [[J["neck"], J["el_b"], J["hand_b"]], [J["hip"], J["kn_b"], J["ft_b"]]]
    front = [[J["hip"], J["neck"]], [J["hip"], J["kn_f"], J["ft_f"]], [J["neck"], J["el_f"], J["hand_f"]]]
    for pts in back: limb(pts, 22 * s, TEAL, 0.10 * a); limb(pts, 10 * s, (0.78, 0.80, 0.84), a)
    for pts in front: limb(pts, 24 * s, TEAL, 0.12 * a); limb(pts, 11 * s, WHITE, a)
    for hk in ("hand_f", "hand_b"):
        c.set_source_rgba(*TEAL, a); c.arc(*J[hk], 8 * s, 0, 6.3); c.fill()
    # head = Dot
    R = 30 * s
    hx, hy = J["neck"][0] + fwd * math.sin(math.radians(p["lean"])) * (R + 4 * s), J["neck"][1] - math.cos(math.radians(p["lean"])) * (R + 4 * s)
    glow(c, hx, hy, R * 2.6, TEAL, 0.22 * a)
    g = cairo.RadialGradient(hx - R * 0.35, hy - R * 0.4, R * 0.1, hx, hy, R)
    g.add_color_stop_rgba(0, 0.55, 1.0, 0.95, a); g.add_color_stop_rgba(1, *TEAL, a)
    c.set_source(g); c.arc(hx, hy, R, 0, 2 * math.pi); c.fill()
    lx, ly = look[0] * fwd, look[1]
    for side in (-1, 1):
        ex, ey = hx + side * 10 * s + lx * 6 * s, hy - 3 * s + ly * 3 * s
        if happy:
            c.set_source_rgba(0.04, 0.08, 0.1, a); c.set_line_width(3.4 * s); c.arc(ex, ey + 3 * s, 5.5 * s, math.pi * 1.1, math.pi * 1.9); c.stroke()
        elif blink:
            c.set_source_rgba(0.04, 0.08, 0.1, a); c.set_line_width(3 * s); c.move_to(ex - 5 * s, ey); c.line_to(ex + 5 * s, ey); c.stroke()
        else:
            rr = 1.25 if wide else 1.0
            c.save(); c.translate(ex, ey); c.scale(6.5 * s * rr, 8.5 * s * rr); c.set_source_rgba(1, 1, 1, a); c.arc(0, 0, 1, 0, 6.3); c.fill(); c.restore()
            c.set_source_rgba(0.04, 0.06, 0.08, a); c.arc(ex + lx * 2.8 * s, ey + ly * 2.8 * s, 3.8 * s, 0, 6.3); c.fill()
    c.restore()
    return (x + J["hand_f"][0], y + oy + J["hand_f"][1])

def hero_track(c, dd, u, acts=(), idle="ready", s=1.0, **kw):
    """drive the hero from a Track state dict (x, y, walk, air, rot) plus timed action poses."""
    if dd.get("air"): base = POSES["air"]
    elif dd.get("walk") is not None: base = run_pose(dd["walk"] * 0.7)
    else: base = POSES[idle] if isinstance(idle, str) else idle
    p = pose_at(u, base, list(acts))
    return hero(c, dd["x"], dd["y"], p, s=s, rot=dd.get("rot", 0.0), air=bool(dd.get("air")), **kw)
