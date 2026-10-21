"""Scratch: #678's n204.cert against main's house witness at 204 (T-186), under the box's
eight symmetries, in binary64, as the review's identity_260.py measures 260."""
import math, sys
from fractions import Fraction
from pathlib import Path
from sqpack.yamlio import safe_load

def read_cert(text):
    rows = [ln.split() for ln in text.splitlines() if ln.strip()]
    side = Fraction(rows[0][1]); sq = []
    for x, y, t in rows[1:]:
        t = Fraction(t); d = 1 + t * t
        sq.append((Fraction(x), Fraction(y), (1 - t * t) / d, 2 * t / d))
    return side, sq

def read_witness(text):
    w = safe_load(text)["witness"]
    return Fraction(w["side"]), [(Fraction(s["center"][0]), Fraction(s["center"][1]), Fraction(s["basis"][0]), Fraction(s["basis"][1])) for s in w["squares"]]

def syms(S):
    return {"id": lambda x, y: (x, y), "rot90": lambda x, y: (S - y, x), "rot180": lambda x, y: (S - x, S - y),
            "rot270": lambda x, y: (y, S - x), "flipx": lambda x, y: (S - x, y), "flipy": lambda x, y: (x, S - y),
            "diag": lambda x, y: (y, x), "anti": lambda x, y: (S - y, S - x)}

def ang(c, s): return math.degrees(math.atan2(float(s), float(c))) % 90.0

new = read_cert(Path(sys.argv[1]).read_text()); old = read_witness(Path(sys.argv[2]).read_text())
pts = [(float(x), float(y), ang(c, s)) for x, y, c, s in old[1]]
best = None
for name, f in syms(new[0]).items():
    ds = []
    for x, y, c, s in new[1]:
        fx, fy = (float(v) for v in f(x, y)); fa = ang(c, s)
        ds.append(min((math.hypot(fx - bx, fy - by), abs(((fa - ba) + 45) % 90 - 45)) for bx, by, ba in pts))
    within = sum(1 for d, a in ds if d <= 1e-4 and a <= 1e-6)
    if best is None or within > best[1]: best = (name, within, ds)
name, within, ds = best
print(f"side diff {float(new[0]-old[0]):+.3e}; best symmetry {name}: {within}/204 within 1e-4 (centre, same axes)")
print("buckets <1e-8:", sum(d <= 1e-8 for d, _ in ds), " 1e-8..1e-4:", sum(1e-8 < d <= 1e-4 for d, _ in ds),
      " 1e-4..1e-2:", sum(1e-4 < d <= 1e-2 for d, _ in ds), " >1e-2:", sum(d > 1e-2 for d, _ in ds), " max:", f"{max(d for d, _ in ds):.3e}")
print("beyond 0.1:", sum(d > 0.1 for d, _ in ds)); print("axis-aligned: #678", sum(1 for *_, c, s in new[1] if s == 0 or c == 0), "T-186", sum(1 for *_, c, s in old[1] if s == 0 or c == 0))
