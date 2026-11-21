"""Lane rR1-lower's shared module: strict reader, D4 expansion, exact geometry.

Written for the blind stage 4 review R1 of jlevy/squares issues 1041 and 1042 from the
mathematics in ../frozen/review-plan.md, without reading any program of the source.
Imports nothing from this repository or the source.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import os
import re
import subprocess
from fractions import Fraction as F
from functools import reduce
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAT = re.compile(r"^-?[0-9]+(/[0-9]+)?$")
TSTAR = F(41421357, 10**8)  # >= sqrt(2) - 1, checked in tstar_ok()
W_BITS = 64  # mass units are 2^-64
G_DEFAULT = 110  # densities are floor(rho * 2^G / (2 Q^2))


def tstar_ok() -> bool:
    return (TSTAR + 1) ** 2 >= 2 and (TSTAR - F(1, 10**8) + 1) ** 2 < 2


def rat(v: object) -> F:
    """A rational from a JSON string 'a/b', 'a', or an int; nothing else."""
    if isinstance(v, bool):
        raise ValueError("boolean where a rational was expected")
    if isinstance(v, int):
        return F(v)
    if isinstance(v, str) and RAT.match(v):
        return F(v)
    raise ValueError(f"not an exact rational: {v!r}")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------- certificate reading


def read_measure(path: Path) -> dict:
    raw = gzip.decompress(path.read_bytes())
    d = json.loads(raw)
    keys = set(d)
    allowed = {"n", "L", "total_mass", "points", "rectangles", "proof_net", "B", "fixed_mass"}
    if not keys <= allowed or not {"n", "L", "rectangles"} <= keys:
        raise ValueError(f"unexpected measure keys {sorted(keys)}")
    # Amendment after the checker freeze: 1042/n161 and n162 carry `fixed_mass`, which the
    # source's documents do not describe; it is accepted only when it equals `total_mass`.
    if "fixed_mass" in d and ("total_mass" not in d or rat(d["fixed_mass"]) != rat(d["total_mass"])):
        raise ValueError("fixed_mass present and not equal to total_mass")
    rows = []
    for r in d["rectangles"]:
        if set(r) != {"rectangle", "mass"} or len(r["rectangle"]) != 4:
            raise ValueError("bad rectangle row")
        x0, y0, x1, y1 = (rat(v) for v in r["rectangle"])
        rows.append((x0, y0, x1, y1, rat(r["mass"])))
    net = d.get("proof_net") or {}
    return {
        "n": int(d["n"]),
        "L": rat(d["L"]),
        "total_mass": rat(d["total_mass"]) if "total_mass" in d else None,
        "points": d.get("points", []),
        "rows": rows,
        "step": rat(net["step"]) if "step" in net else None,
        "last": int(net["last"]) if "last" in net else None,
        "net_keys": sorted(net),
        "fixed_mass_equals_total": "fixed_mass" in d,
        "sha256_raw": hashlib.sha256(raw).hexdigest(),
    }


def read_receipt_rs(path: Path) -> list[int]:
    rs = []
    for line in gzip.decompress(path.read_bytes()).decode().splitlines():
        if line.strip():
            rs.append(int(json.loads(line)["r"]))
    return rs


def load_certificate(folder: Path) -> dict:
    """The certificate of one folder: its levels, its measure, its listed bins."""
    man = json.loads((folder / "manifest.json").read_text())
    levels = []
    base = None
    for lv in man["levels"]:
        m = read_measure(folder / lv["measure"])
        rs = read_receipt_rs(folder / lv["receipts"])
        if base is None:
            base = m
        levels.append({"K": int(lv["K"]), "measure": m, "rs": rs, "file": lv["measure"]})
    return {"folder": folder, "manifest": man, "levels": levels, "base": base}


def bins_of(cert: dict) -> list[tuple[int, int, F, F]]:
    """(K, r, l, h): the listed bins, read as centred at r*step with half-width step/2."""
    out = []
    for lv in cert["levels"]:
        D = lv["measure"]["step"]
        for r in lv["rs"]:
            out.append((lv["K"], r, (r - F(1, 2)) * D, (r + F(1, 2)) * D))
    return out


def coverage_gaps(bins: list[tuple[int, int, F, F]]) -> list[tuple[F, F]]:
    """Gaps of the union of [l, h] over [0, TSTAR] (TSTAR > sqrt 2 - 1), exactly."""
    iv = sorted((max(l, F(0)), h) for _, _, l, h in bins if h > 0)
    gaps = []
    cur = F(0)
    for l, h in iv:
        if l > cur:
            gaps.append((cur, l))
        cur = max(cur, h)
    # the union must reach sqrt(2) - 1: cur >= sqrt 2 - 1  <=>  (cur + 1)^2 >= 2
    if (cur + 1) ** 2 < 2:
        gaps.append((cur, TSTAR))
    return gaps


# ---------------------------------------------------------------- the measure


def images(r: tuple[F, F, F, F], L: F) -> list[tuple[F, F, F, F]]:
    x0, y0, x1, y1 = r
    out = []
    for tr in (False, True):
        a0, b0, a1, b1 = (y0, x0, y1, x1) if tr else (x0, y0, x1, y1)
        for fx in (False, True):
            for fy in (False, True):
                u0, u1 = (L - a1, L - a0) if fx else (a0, a1)
                v0, v1 = (L - b1, L - b0) if fy else (b0, b1)
                out.append((u0, v0, u1, v1))
    return out


def expand(rows: list[tuple[F, F, F, F, F]], L: F, factor: F = F(1)) -> dict:
    """Merged eight-image expansion: rectangle -> mass.  Each image gets mass/8."""
    merged: dict[tuple[F, F, F, F], F] = {}
    for x0, y0, x1, y1, m in rows:
        for im in images((x0, y0, x1, y1), L):
            merged[im] = merged.get(im, F(0)) + m * factor / 8
    return merged


def lcm_den(vals) -> int:
    return reduce(lambda a, b: a * b // math.gcd(a, b), (v.denominator for v in vals), 1)


# ---------------------------------------------------------------- exact angle geometry


def ecs(t: F) -> tuple[F, F]:
    d = 1 + t * t
    return ((1 - t * t) / d, 2 * t / d)


def w_of(t: F) -> F:
    c, s = ecs(t)
    return (abs(c) + abs(s)) / 2


def in_I(q: tuple[F, F], el: tuple[F, F], eh: tuple[F, F]) -> bool:
    """q in the intersection over theta in [theta_l, theta_h] of the centred unit squares.

    For each of the four rotations p = R^{-k} q the support function p.e(theta) must be at
    most 1/2 on the interval; its maximum is |p| when the direction of p lies in the
    sector [theta_l, theta_h], else the larger end value.
    """
    x, y = q
    for p in ((x, y), (y, -x), (-x, -y), (-y, x)):
        if p[0] * el[0] + p[1] * el[1] > F(1, 2):
            return False
        if p[0] * eh[0] + p[1] * eh[1] > F(1, 2):
            return False
        if p != (0, 0):
            c1 = el[0] * p[1] - el[1] * p[0]
            c2 = p[0] * eh[1] - p[1] * eh[0]
            if c1 >= 0 and c2 >= 0 and p[0] ** 2 + p[1] ** 2 > F(1, 4):
                return False
    return True


def hull_int(pts: list[tuple[int, int]]) -> list[tuple[int, int]]:
    pts = sorted(set(pts))

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo: list[tuple[int, int]] = []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up: list[tuple[int, int]] = []
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def bin_polygon(l: F, h: F, Q: int, mutant_center_square: bool = False) -> dict:
    """A lattice polygon P (vertices in units 1/Q) inside every centred unit square of the
    bin t in [max(l, 0), min(h, TSTAR)], each vertex verified exactly."""
    lo = max(l, F(0))
    hi = min(h, TSTAR)
    if not lo < hi:
        raise ValueError("empty bin")
    el, eh = ecs(lo), ecs(hi)
    if mutant_center_square:  # deliberately broken variant T1: the square at the middle angle
        c, s = ecs((lo + hi) / 2)
        ideal = [((c - s) / 2, (s + c) / 2), ((-c - s) / 2, (-s + c) / 2), ((-c + s) / 2, (-s - c) / 2),
                 ((c + s) / 2, (s - c) / 2)]
        verts = [(math.trunc(vx * Q), math.trunc(vy * Q)) for vx, vy in ideal]
        return {"verts": hull_int(verts), "lo": lo, "hi": hi, "el": el, "eh": eh, "mutant": True}
    ch, sh = eh
    cl, sl = el
    det = ch * cl + sh * sl
    v0 = ((cl - sh) / (2 * det), (ch + sl) / (2 * det))
    em = ecs((lo + hi) / 2)  # a point of the arc between the two tangent points
    base = [(el[0] / 2, el[1] / 2), (em[0] / 2, em[1] / 2), (eh[0] / 2, eh[1] / 2), v0]
    ideal = []
    for k in range(4):
        for x, y in base:
            for _ in range(k):
                x, y = -y, x
            ideal.append((x, y))
    verts = []
    for vx, vy in ideal:
        if not in_I((vx, vy), el, eh):
            raise AssertionError("ideal vertex outside the intersection")
        for j in range(4000):
            f = 1 - F(j, 2**36)
            q = (math.trunc(vx * f * Q), math.trunc(vy * f * Q))
            if in_I((F(q[0], Q), F(q[1], Q)), el, eh):
                verts.append(q)
                break
        else:
            raise AssertionError("could not round a vertex inward")
    hull = hull_int(verts)
    for q in hull:  # every hull vertex is one of the verified points
        assert q in verts
    return {"verts": hull, "lo": lo, "hi": hi, "el": el, "eh": eh, "mutant": False}


def poly_area(verts: list[tuple[int, int]]) -> int:
    return sum(verts[i][0] * verts[(i + 1) % len(verts)][1] - verts[(i + 1) % len(verts)][0] * verts[i][1]
               for i in range(len(verts)))


# ---------------------------------------------------------------- exact captures


def clip_convex(poly: list[tuple[F, F]], x0: F, y0: F, x1: F, y1: F) -> list[tuple[F, F]]:
    def clip(pts, inside, inter):
        out = []
        n = len(pts)
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            ip, iq = inside(p), inside(q)
            if ip:
                out.append(p)
            if ip != iq:
                out.append(inter(p, q))
        return out

    def ix(X):
        return lambda p, q: (X, p[1] + (q[1] - p[1]) * (X - p[0]) / (q[0] - p[0]))

    def iy(Y):
        return lambda p, q: (p[0] + (q[0] - p[0]) * (Y - p[1]) / (q[1] - p[1]), Y)

    pts = poly
    for inside, inter in (
        (lambda p: p[0] >= x0, ix(x0)),
        (lambda p: p[0] <= x1, ix(x1)),
        (lambda p: p[1] >= y0, iy(y0)),
        (lambda p: p[1] <= y1, iy(y1)),
    ):
        if not pts:
            return []
        pts = clip(pts, inside, inter)
    return pts


def area_poly(pts: list[tuple[F, F]]) -> F:
    n = len(pts)
    if n < 3:
        return F(0)
    return abs(sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))) / 2


def square_vertices(c: tuple[F, F], t: F) -> list[tuple[F, F]]:
    co, si = ecs(t)
    hx, hy = co / 2, si / 2
    gx, gy = -si / 2, co / 2
    cx, cy = c
    return [(cx + hx + gx, cy + hy + gy), (cx - hx + gx, cy - hy + gy), (cx - hx - gx, cy - hy - gy),
            (cx + hx - gx, cy + hy - gy)]


def exact_capture(merged: dict, poly: list[tuple[F, F]]) -> F:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    tot = F(0)
    for (x0, y0, x1, y1), m in merged.items():
        if x1 <= bx0 or x0 >= bx1 or y1 <= by0 or y0 >= by1:
            continue
        a = area_poly(clip_convex(poly, x0, y0, x1, y1))
        if a:
            tot += m * a / ((x1 - x0) * (y1 - y0))
    return tot


def admissible(c: tuple[F, F], t: F, L: F) -> bool:
    w = w_of(t)
    return w <= c[0] <= L - w and w <= c[1] <= L - w


# ---------------------------------------------------------------- the lattice data


def lattice(merged: dict, L: F) -> dict:
    """Choose Q and convert rectangles to integers; round inward only if Q must be capped."""
    coords = [v for r in merged for v in r] + [L / 2]
    q0 = lcm_den(coords)
    rounded = False
    if q0 <= 2**37:
        Q = q0
        while Q < 2**33:
            Q *= 2
    else:
        Q = 2**35
        rounded = True
    rects = []
    rho_max = F(0)
    for (x0, y0, x1, y1), m in merged.items():
        rho = m / ((x1 - x0) * (y1 - y0))
        rho_max = max(rho_max, rho)
        X0, Y0 = math.ceil(x0 * Q), math.ceil(y0 * Q)
        X1, Y1 = math.floor(x1 * Q), math.floor(y1 * Q)
        if X1 > X0 and Y1 > Y0 and m > 0:
            rects.append((X0, Y0, X1, Y1, rho))
    G = G_DEFAULT
    while rho_max * 2**G >= 2**125 and G > W_BITS:
        G -= 1
    if G <= W_BITS:
        raise ValueError("density too large for the integer bounds")
    two_q2 = 2 * Q * Q
    ints = [(X0, Y0, X1, Y1, (rho * 2**G) // two_q2, rho) for X0, Y0, X1, Y1, rho in rects]
    for X0, Y0, X1, Y1, d, _ in ints:
        assert abs(X0) < 2**42 and abs(X1) < 2**42 and abs(Y0) < 2**42 and abs(Y1) < 2**42
        assert 0 <= d < 2**63
    return {"Q": Q, "q0": q0, "rounded": rounded, "G": G, "rects": ints, "rho_max": rho_max}


def write_rects(lat: dict, path: Path) -> None:
    with open(path, "w") as f:
        f.write(f"G {lat['G']}\nN {len(lat['rects'])}\n")
        for X0, Y0, X1, Y1, d, rho in lat["rects"]:
            f.write(f"{X0} {Y0} {X1} {Y1} {d} {float(rho)!r}\n")


def build_c(scratch: Path) -> Path:
    exe = scratch / "rr1_decide"
    subprocess.run(["gcc", "-O2", "-std=gnu11", "-o", str(exe), str(HERE / "rr1_decide.c"), "-lm"], check=True)
    return exe


def run_c(exe: Path, args: list[str], env_extra: dict | None = None) -> str:
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([str(exe), *args], capture_output=True, text=True, env=env)
    if p.returncode != 0:
        raise RuntimeError(f"rr1_decide {args[0]} failed: {p.stderr.strip()}")
    return p.stdout


def domain(L: F, lo: F, Q: int) -> tuple[int, int]:
    """The quadrant [L/2, L - w(lo)], rounded outward to the lattice."""
    return math.floor(L / 2 * Q), math.ceil((L - w_of(lo)) * Q)
