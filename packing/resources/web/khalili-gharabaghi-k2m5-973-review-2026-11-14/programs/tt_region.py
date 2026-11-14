"""Run the source's Tight-Tile checker (ttbox.run, read before running) on one chart and face region, and check
its certified cells against exact masses computed here (review of #973, L144).

usage: python -I tt_region.py TTDIR COVER OUT_JSON CHART d0 sign yb [p0 p1 q0 q1] [--maxcells N] [--no-oracle]
                                 [--corner ks ss rho]
  TTDIR   the source's tight_tile/ folder (ttbox.py, ttpoly.py, ttarea.py are imported from it)
  CHART   C_u | "W_t t+1" | "W_t t-1" | "W_d d+1" | "W_d d-1" | "W_td t+1 d+1 a" ... | S_u | "S_d d+1" | "S_d d-1"
          (for strips, yb is "s1,s2" as in run_tt.py: "3.9+,4.0-"), or CORNER (with --corner) for the centre zone
          of a C_u corner box
  p0..q1  optional face box (default: the chart's whole face)

The run is the source's: ttbox.charts_line / charts_strip / charts_corner3 build the chart and ttbox.run certifies
it.  The oracle (this review's own code) wraps ttbox.analyse, records for every certified cell its polygon, its
low/high functions and its vertex values T, maps each vertex (p, q, h) with h > 0 to a pose by THIS file's chart
formulas, written from the paper's chart tables, and requires exact mu(P) - 1 >= T (k2m5_exact).
"""
import json
import os
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from k2m5_exact import load_cover, mass  # noqa: E402

args = sys.argv[1:]
ttdir, cover, out, chart_name, d0, sign, yb = args[:7]
rest = args[7:]
maxcells = 400000
oracle = True
corner = None
box = None
k = 0
while k < len(rest):
    if rest[k] == "--maxcells":
        maxcells = int(rest[k + 1]); k += 2
    elif rest[k] == "--no-oracle":
        oracle = False; k += 1
    elif rest[k] == "--corner":
        corner = tuple(F(v) for v in rest[k + 1:k + 4]); k += 4
    else:
        box = tuple(F(v) for v in rest[k:k + 4]); k += 4
sys.path.insert(1, ttdir)
import ttbox as T  # noqa: E402  (the source's checker)
import ttarea  # noqa: E402

d0, sign = F(d0), int(sign)
K, U0 = F(os.environ.get("K", "4")), F(os.environ.get("U0", "1/4000"))
T0 = K * U0


def send(x):
    return F(x[:-1]) + T0 if x.endswith("+") else F(x[:-1]) - T0 if x.endswith("-") else F(x)


strip = "," in yb
if corner is not None:
    ks, ss, rho = corner
    charts = T.charts_corner3(d0, F(yb), sign, ks, ss, rho, F(4), U0)
elif strip:
    s1, s2 = yb.split(",")
    charts = T.charts_strip(d0, send(s1), send(s2), sign, K, U0)
else:
    charts = T.charts_line(d0, F(yb), sign, K, U0)
sel = [c for c in charts if c[0] == chart_name]
if len(sel) != 1:
    raise SystemExit(f"chart {chart_name!r} not among {[c[0] for c in charts]}")
name, ch, poly, h0 = sel[0]
# the area term, as run_tt.py attaches it (the Lebesgue rectangle from the cover file)
lines = open(cover).read().split("\n")
i = 0
while not lines[i].split() or lines[i].startswith("#") or lines[i].startswith("mixed"):
    i += 1
pitch, wden, n = int(lines[i + 1]), int(lines[i + 2]), int(lines[i + 4])
v = [int(t) for t in lines[i + 5 + n + 1].split()]
xs, ys = [F(a, pitch) for a in v[2::2]], [F(a, pitch) for a in v[3::2]]
U = (min(xs), min(ys), max(xs), max(ys), F(v[1], wden) / ((max(xs) - min(xs)) * (max(ys) - min(ys))))
if d0 + 1 > U[0]:
    ch["area_term"] = ttarea.AreaTerm(ch, U)
if box is not None:
    p0, p1, q0, q1 = box
    poly = [(p0, q0), (p1, q0), (p1, q1), (p0, q1)]

# ---- this review's chart formulas (paper, section 6.3 tables), independent of the chart dicts ----
ybF = None if strip else F(yb)


def pose(p, q, h):
    """centre and u of the chart point (p, q, h)"""
    nm = chart_name
    u = sign * h
    if corner is not None:                       # CORNER zone: (p,q) = (a,b), offsets h (ks + a h), h (ss + b h)
        ks, ss, _ = corner
        return d0 + h * (ks + p * h), ybF + h * (ss + q * h), u
    if nm == "C_u":
        return d0 + h * p, ybF + h * q, u
    if nm.startswith("W_t "):
        ts = 1 if "t+1" in nm else -1
        return d0 + h * p, ybF + ts * q, u
    if nm.startswith("W_d "):
        ds = 1 if "d+1" in nm else -1
        return d0 + ds * q, ybF + h * p, u
    if nm.startswith("W_td "):                   # face (tau, eps) = (|t|, |delta|)
        ts = 1 if "t+1" in nm else -1
        ds = 1 if "d+1" in nm else -1
        return d0 + ds * q, ybF + ts * p, u
    if nm == "S_u":
        return d0 + h * p, q, u
    if nm.startswith("S_d "):
        ds = 1 if "d+1" in nm else -1
        return d0 + ds * q, p, u
    raise ValueError(nm)


def aff(pl, p, q):
    return sum((c * p ** e[0] * q ** e[1] * (0 if e[2] else 1) for e, c in pl.items()), F(0))


records = []
orig = T.analyse


def wrapped(segcons, chart, polyg, h0_, need_reach=True, low=None, high=None):
    r = orig(segcons, chart, polyg, h0_, need_reach=need_reach, low=low, high=high)
    if oracle and r[0] == "ok":
        lo = low if low is not None else T.P(0)
        hi = high if high is not None else T.P(h0_)
        records.append((list(polyg), lo, hi, list(r[1]["Tv"])))
    return r


T.analyse = wrapped
t0 = time.time()
st, fails = T.run(T.load(cover), ch, [poly], h0, maxcells=maxcells, minarea=F(1, 2 ** 60))
secs = time.time() - t0
res = dict(chart=name, d0=str(d0), sign=sign, yb=yb, face=[[str(a), str(b)] for a, b in poly], h0=str(h0),
           ok=st["ok"], cells=st["cells"], fails=st["fails"], worst=float(st["worst"][0]) if st["worst"] else None,
           fail_reasons=sorted({f[1] for f in fails}) if fails else [], secs_checker=round(secs, 1))
if fails:
    pts_ = [v for f in fails for v in f[0]]
    res["failed_cells_face_bbox"] = [float(min(a for a, _ in pts_)), float(max(a for a, _ in pts_)),
                                     float(min(b for _, b in pts_)), float(max(b for _, b in pts_))]
if oracle:
    cv = load_cover(cover)
    t1 = time.time()
    nv = 0
    worst = None
    viol = []
    for polyg, lo, hi, Tv in records:
        for t, vtx in enumerate(polyg):
            for hl, fn in ((0, lo), (1, hi)):
                h = aff(fn, vtx[0], vtx[1])
                if h <= 0:
                    continue
                cx, cy, u = pose(vtx[0], vtx[1], h)
                m = mass(cv, cx, cy, u) - 1
                Tval = Tv[2 * t + hl]
                nv += 1
                gap = m - Tval
                if gap < 0:
                    viol.append([str(vtx[0]), str(vtx[1]), str(h), float(m), float(Tval)])
                if worst is None or gap < worst[0]:
                    worst = (gap, [str(vtx[0]), str(vtx[1]), str(h)], float(m), float(Tval))
    res["oracle"] = dict(cells=len(records), vertices_h_pos=nv, violations=len(viol), first=viol[:5],
                         least_gap=float(worst[0]) if worst else None, at=worst[1] if worst else None,
                         mu_minus_1=worst[2] if worst else None, T=worst[3] if worst else None,
                         secs=round(time.time() - t1, 1))
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res))
