"""Scratch: #678's n260.cert against T-196's retained exact packing, best of the box's eight
symmetries, counting squares beyond 1e-4, 1e-2 and a tenth (binary64)."""
import gzip, json, math, sys
from fractions import Fraction
from pathlib import Path
def cert(text):
    rows = [l.split() for l in text.splitlines() if l.strip()]
    S = Fraction(rows[0][1]); out = []
    for x, y, t in rows[1:]:
        t = Fraction(t); d = 1 + t * t; out.append((Fraction(x), Fraction(y), (1 - t * t) / d, 2 * t / d))
    return S, out
def js(text):
    d = json.loads(text); return Fraction(d["side"]), [(Fraction(s["center"][0]), Fraction(s["center"][1]), Fraction(s["basis"][0]), Fraction(s["basis"][1])) for s in d["squares"]]
ang = lambda c, s: math.degrees(math.atan2(float(s), float(c))) % 90.0
new = cert(Path(sys.argv[1]).read_text()); old = js(gzip.decompress(Path(sys.argv[2]).read_bytes()).decode())
S = new[0]
syms = [lambda x, y: (x, y), lambda x, y: (S - y, x), lambda x, y: (S - x, S - y), lambda x, y: (y, S - x),
        lambda x, y: (S - x, y), lambda x, y: (x, S - y), lambda x, y: (y, x), lambda x, y: (S - y, S - x)]
pts = [(float(x), float(y)) for x, y, *_ in old[1]]
best = None
for f in syms:
    ds = [min(math.hypot(float(a) - bx, float(b) - by) for bx, by in pts) for a, b in (f(x, y) for x, y, *_ in new[1])]
    w = sum(d <= 1e-4 for d in ds)
    if best is None or w > best[0]: best = (w, ds)
w, ds = best
print("260 vs T-196: within 1e-4:", w, " beyond 1e-2:", sum(d > 1e-2 for d in ds), " beyond 0.1:", sum(d > 0.1 for d in ds), " max:", f"{max(ds):.3f}")
