"""Exact clearances (slack) and contact lists of the houses and of the new certificates.

Usage (from packing/, Python 3.14):
  python -I house_slack.py CANDIDATES_DIR HOUSES_DIR OUT.json

A measurement, not a feasibility decision (the houses were decided when they were
adopted; the new certificates are decided by decide_feasibility.py). For each packing:
every wall clearance exactly (method A's corner rule), and the exact separating-axis
gap of every pair whose centres lie within 1.8 of each other (a binary64 prefilter: two
unit squares whose centres are d apart have a separating-axis gap of at least
d cos 45 deg - 1/2 - sqrt(2)/2 > 0.06 when d >= 1.8, so no pair left out can be a
contact or set the least gap). It records the least wall clearance, the least pair gap,
the gaps' decades below 1e-6, and the contact pairs (gap < 1e-9) and wall contacts
(clearance < 1e-9).

House witnesses (Witness/v2, centre and basis (c, s)) are checked to be exact unit
squares: c^2 + s^2 = 1 exactly for every square.
"""

from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exact_geometry as eg  # noqa: E402
from cert_reader import read_cert  # noqa: E402

NAMES = {175: "s175_1105", 204: "s204_trig1", 260: "s260_ks_1105", 268: "s268_1105", 293: "s293_1105", 303: "s303_1105", 304: "s304_1105"}
CONTACT = F(1, 10**9)


def frac(s) -> F:
    s = str(s)
    p, _, q = s.partition("/")
    return F(int(p), int(q or 1))


def square_cs(x: F, y: F, c: F, s: F, h: F = F(1, 2)):
    ux, uy = c * h, s * h
    vx, vy = -s * h, c * h
    corners = (
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
    )
    return corners, ((c, s), (-s, c))


def read_witness(path: Path):
    doc = yaml.load(path.read_text(), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    w = doc["witness"]
    side = frac(w["side"])
    sq = []
    unit = True
    for item in w["squares"]:
        x, y = (frac(v) for v in item["center"])
        c, s = (frac(v) for v in item["basis"])
        if c * c + s * s != 1:
            unit = False
        sq.append((x, y, c, s))
    if str(w.get("square_size")) != "1":
        raise ValueError("square_size")
    return {"n": w["n"], "S": side, "squares": sq, "unit_basis_exact": unit, "id": w["id"]}


def measure(side: F, squares_a: list, centres: list[tuple[float, float]]) -> dict:
    t0 = time.process_time()
    n = len(squares_a)
    clear = [eg.wall_clearance_a(s, side) for s in squares_a]
    kmin = min(range(n), key=lambda i: clear[i])
    wall_contacts = [i + 1 for i, c in enumerate(clear) if c < CONTACT]
    gmin = None
    garg = None
    contacts = []
    decades: dict[str, int] = {}
    near = 0
    for i in range(n):
        xi, yi = centres[i]
        for j in range(i + 1, n):
            xj, yj = centres[j]
            if math.hypot(xi - xj, yi - yj) >= 1.8:
                continue
            near += 1
            g, _ = eg.pair_gap_a(squares_a[i], squares_a[j])
            if gmin is None or g < gmin:
                gmin, garg = g, (i + 1, j + 1)
            if g < CONTACT:
                contacts.append([i + 1, j + 1])
            if g < F(1, 10**6):
                key = "negative" if g < 0 else ("zero" if g == 0 else f"1e{math.floor(math.log10(float(g)))}")
                decades[key] = decades.get(key, 0) + 1
    return {
        "least_wall_clearance": f"{clear[kmin].numerator}/{clear[kmin].denominator}",
        "least_wall_clearance_float": float(clear[kmin]),
        "least_wall_square": kmin + 1,
        "wall_contacts_below_1e-9": len(wall_contacts),
        "near_pairs_measured": near,
        "least_pair_gap": f"{gmin.numerator}/{gmin.denominator}",
        "least_pair_gap_float": float(gmin),
        "least_pair": list(garg),
        "pair_gaps_below_1e-6_by_decade": dict(sorted(decades.items())),
        "contact_pairs_below_1e-9": len(contacts),
        "contacts": contacts,
        "wall_contact_squares": wall_contacts,
        "cpu_seconds": round(time.process_time() - t0, 3),
    }


def main() -> None:
    cand, houses, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    result: dict = {}
    for n, name in NAMES.items():
        w = read_witness(houses / f"W-known-best-n{n}.yaml")
        sq = [square_cs(*q) for q in w["squares"]]
        cen = [(float(q[0]), float(q[1])) for q in w["squares"]]
        r = measure(w["S"], sq, cen)
        r.update({"id": w["id"], "n": w["n"], "unit_basis_exact": w["unit_basis_exact"], "side": f"{w['S'].numerator}/{w['S'].denominator}"})
        result[f"house {n}"] = r
        c = read_cert(cand / f"{name}.cert")
        sqn = [eg.square_a(*q) for q in c["squares"]]
        cenn = [(float(q[0]), float(q[1])) for q in c["squares"]]
        result[f"new {n}"] = measure(c["S"], sqn, cenn)
        print(n, "house", r["id"], "unit", r["unit_basis_exact"], "wall", r["least_wall_clearance_float"], "gap", r["least_pair_gap_float"],
              "contacts", r["contact_pairs_below_1e-9"], "walls", r["wall_contacts_below_1e-9"], r["pair_gaps_below_1e-6_by_decade"],
              "| new contacts", result[f"new {n}"]["contact_pairs_below_1e-9"], "walls", result[f"new {n}"]["wall_contacts_below_1e-9"])
    for label, fn in (("T-257 260", "T-257-s260_1028.cert"),):
        c = read_cert(houses / fn)
        sqn = [eg.square_a(*q) for q in c["squares"]]
        cenn = [(float(q[0]), float(q[1])) for q in c["squares"]]
        result[label] = measure(c["S"], sqn, cenn)
        r = result[label]
        print(label, "wall", r["least_wall_clearance_float"], "gap", r["least_pair_gap_float"], "contacts", r["contact_pairs_below_1e-9"], r["pair_gaps_below_1e-6_by_decade"])
    out.write_text(json.dumps(result, indent=1) + "\n")


if __name__ == "__main__":
    main()
