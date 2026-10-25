#!/usr/bin/env python3
"""Pose-by-pose measurement of the T-226, T-227 and T-228 packings against their kin.

A measurement for credit and lineage; it decides nothing. For each (view, reference)
pair it applies the box's eight symmetries to the reference, in the reference's own box
[0, S_ref], and reports:

* under which symmetries nearest centres pair the two one to one (each view square's
  nearest reference centre, all distinct);
* for the symmetry with the least total squared displacement under an optimal
  assignment (its own Hungarian algorithm, floats for the costs), the number of squares
  within 1e-6 and beyond 1e-3, 1e-2 and 1e-1 (compared exactly, centres being
  rational), the largest move, and the turns modulo 90 degrees (a reflection reverses a
  square's angle);
* the same counts with the reference scaled to the view's side about the origin corner.

Readers: rational centre/half-angle certificates (this review's reader), de Winter's
exact JSON (centre and basis), and witness YAML (centre and basis), all as data.

Usage: python -I identity_0nse.py REPO OUT.json
"""

from __future__ import annotations

import gzip
import importlib.util
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("review_0nse_check", HERE / "review_0nse_check.py")
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)

WEB = "packing/resources/web"
THRESHOLDS = {"1e-6": Fraction(1, 10**6), "1e-4": Fraction(1, 10**4), "1e-3": Fraction(1, 10**3), "1e-2": Fraction(1, 10**2), "1e-1": Fraction(1, 10)}


class Packing:
    def __init__(self, name: str, side: Fraction, centres: list[tuple[Fraction, Fraction]], angles: list[float]) -> None:
        self.name, self.side, self.centres, self.angles = name, side, centres, angles


def from_cert(name: str, path: Path) -> Packing:
    data = path.read_bytes()
    if path.suffix == ".gz":
        data = gzip.decompress(data)
    _, side, rows, _ = check.read(data.decode("ascii"))
    centres = [(Fraction(*x), Fraction(*y)) for x, y, _ in rows]
    angles = [math.degrees(2 * math.atan2(t[0], t[1])) for _, _, t in rows]
    return Packing(name, Fraction(*side), centres, angles)


def from_dewinter(name: str, path: Path) -> Packing:
    d = json.loads(gzip.decompress(path.read_bytes()))
    centres = [(Fraction(s["center"][0]), Fraction(s["center"][1])) for s in d["squares"]]
    angles = [math.degrees(math.atan2(float(Fraction(s["basis"][1])), float(Fraction(s["basis"][0])))) for s in d["squares"]]
    return Packing(name, Fraction(d["side"]), centres, angles)


def from_witness(name: str, path: Path) -> Packing:
    text = gzip.decompress(path.read_bytes()).decode("utf-8")
    side = Fraction(re.search(r"^  side: '?([0-9/]+)'?$", text, re.M).group(1))
    blocks = re.findall(
        r"center:\n\s+- '?([0-9/.-]+)'?\n\s+- '?([0-9/.-]+)'?\n\s+basis:\n\s+- '?([0-9/.-]+)'?\n\s+- '?([0-9/.-]+)'?",
        text,
    )
    centres = [(Fraction(x), Fraction(y)) for x, y, _, _ in blocks]
    angles = [math.degrees(math.atan2(float(Fraction(s)), float(Fraction(c)))) for _, _, c, s in blocks]
    return Packing(name, side, centres, angles)


SYMMETRIES = {
    "identity": (lambda x, y, s: (x, y), 1),
    "quarter turn": (lambda x, y, s: (s - y, x), 1),
    "half turn": (lambda x, y, s: (s - x, s - y), 1),
    "three-quarter turn": (lambda x, y, s: (y, s - x), 1),
    "mirror x": (lambda x, y, s: (s - x, y), -1),
    "mirror y": (lambda x, y, s: (x, s - y), -1),
    "transpose": (lambda x, y, s: (y, x), -1),
    "anti-transpose": (lambda x, y, s: (s - y, s - x), -1),
}


def hungarian(cost: list[list[float]]) -> list[int]:
    """Row i -> column assignment[i] minimising the total cost (shortest augmenting paths)."""
    n = len(cost)
    inf = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [inf] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = inf
            j1 = 0
            row = cost[i0 - 1]
            ui0 = u[i0]
            for j in range(1, n + 1):
                if not used[j]:
                    cur = row[j - 1] - ui0 - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    assignment = [0] * n
    for j in range(1, n + 1):
        if p[j]:
            assignment[p[j] - 1] = j - 1
    return assignment


def turn(a: float, b: float) -> float:
    d = (a - b) % 90.0
    return min(d, 90.0 - d)


def measure(view: Packing, ref: Packing) -> dict:
    n = len(view.centres)
    assert n == len(ref.centres)
    vf = [(float(x), float(y)) for x, y in view.centres]
    per_symmetry = {}
    for name, (g, orientation) in SYMMETRIES.items():
        moved = [g(x, y, ref.side) for x, y in ref.centres]
        mf = [(float(x), float(y)) for x, y in moved]
        nearest = []
        total = 0.0
        for vx, vy in vf:
            best, at = None, -1
            for k, (mx, my) in enumerate(mf):
                d = (vx - mx) ** 2 + (vy - my) ** 2
                if best is None or d < best:
                    best, at = d, k
            nearest.append(at)
            total += best
        per_symmetry[name] = {"one_to_one": len(set(nearest)) == n, "nearest_total_sq": total, "moved": moved, "orientation": orientation, "nearest": nearest}
    ranked = sorted(per_symmetry, key=lambda s: per_symmetry[s]["nearest_total_sq"])[:2]
    best_name, best = None, None
    for name in ranked:
        mf = [(float(x), float(y)) for x, y in per_symmetry[name]["moved"]]
        cost = [[(vx - mx) ** 2 + (vy - my) ** 2 for mx, my in mf] for vx, vy in vf]
        assignment = hungarian(cost)
        total = sum(cost[i][assignment[i]] for i in range(n))
        if best is None or total < best[0]:
            best_name, best = name, (total, assignment)
    total, assignment = best
    sym = per_symmetry[best_name]
    moved, orientation = sym["moved"], sym["orientation"]

    def counts(scale: Fraction) -> dict:
        within = 0
        within_4 = 0
        beyond = {k: 0 for k in THRESHOLDS if k not in ("1e-6", "1e-4")}
        largest = (Fraction(-1), -1)
        for i in range(n):
            mx, my = moved[assignment[i]]
            dx = view.centres[i][0] - mx * scale
            dy = view.centres[i][1] - my * scale
            d2 = dx * dx + dy * dy
            if d2 <= THRESHOLDS["1e-6"] ** 2:
                within += 1
            if d2 <= THRESHOLDS["1e-4"] ** 2:
                within_4 += 1
            for k in beyond:
                if d2 > THRESHOLDS[k] ** 2:
                    beyond[k] += 1
            if d2 > largest[0]:
                largest = (d2, i)
        return {"within_1e-6": within, "within_1e-4": within_4, "beyond": beyond, "largest_move": math.sqrt(float(largest[0])), "largest_move_square": largest[1]}

    own = counts(Fraction(1))
    rescaled = counts(view.side / ref.side)
    turns = [turn(view.angles[i], orientation * ref.angles[assignment[i]]) for i in range(n)]
    largest_turn = max(range(n), key=lambda i: turns[i])
    return {
        "view": view.name,
        "reference": ref.name,
        "view_side": float(view.side),
        "reference_side": float(ref.side),
        "one_to_one_under": [s for s, r in per_symmetry.items() if r["one_to_one"]],
        "best_symmetry": best_name,
        "assignment_is_nearest_centre_map": assignment == sym["nearest"],
        "assignment_total_sq": total,
        "own_box": own,
        "reference_scaled_to_view_side": rescaled,
        "turned_beyond_1e-3_deg": sum(1 for t in turns if t > 1e-3),
        "turned_beyond_1_deg": sum(1 for t in turns if t > 1.0),
        "largest_turn_deg": turns[largest_turn],
        "largest_turn_square": largest_turn,
        "largest_turn_angles": [view.angles[largest_turn], ref.angles[assignment[largest_turn]]],
    }


def main(argv: list[str]) -> int:
    repo, out = Path(argv[1]), Path(argv[2])
    web = repo / WEB
    P = {
        "T-226 (#670)": from_cert("T-226 (#670)", web / "couzo-issue670-2026-10-17/source/certificates/n204.cert"),
        "T-228 (#675)": from_cert("T-228 (#675)", web / "couzo-issue675-2026-10-18/source/certificates/best/n204.cert"),
        "T-223 (#678)@204": from_cert("T-223 (#678)@204", web / "couzo-issue678-2026-10-18/source/certificates/best/n204.cert"),
        "T-225@204": from_cert("T-225@204", web / "evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-204.cert.gz"),
        "T-186@204": from_witness("T-186@204", web / "mishapolk-kkt-refinements-2026-10-14/facts/n-204.yaml.gz"),
        "T-227@227 (#672)": from_cert("T-227@227 (#672)", web / "couzo-issue672-2026-10-17/source/certificates/n227.cert"),
        "T-196 (#668)@227": from_dewinter("T-196 (#668)@227", web / "de-winter-upper-bounds-227-229-260-2026-10-17/source/n227/n227_exact.json.gz"),
        "T-225@227": from_cert("T-225@227", web / "evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-227.cert.gz"),
        "T-227@229 (#672)": from_cert("T-227@229 (#672)", web / "couzo-issue672-2026-10-17/source/certificates/n229.cert"),
        "T-196 (#668)@229": from_dewinter("T-196 (#668)@229", web / "de-winter-upper-bounds-227-229-260-2026-10-17/source/n229/n229_exact.json.gz"),
        "T-198 (#674 opening)": from_cert("T-198 (#674 opening)", web / "evand-n229-dilation-2026-10-17/source/search/packer/candidates/s229.cert"),
        "T-199 (#674 update)": from_cert("T-199 (#674 update)", web / "evand-n229-dilation-update-2026-10-18/source/search/packer/candidates/s229_v2.cert"),
        "T-225@229": from_cert("T-225@229", web / "evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-229.cert.gz"),
    }
    for name, p in P.items():
        assert len(p.centres) == int(name.split("@")[-1][:3]) if "@" in name else 204, name
    pairs = [
        ("T-227@227 (#672)", "T-196 (#668)@227"),
        ("T-225@227", "T-227@227 (#672)"),
        ("T-225@227", "T-196 (#668)@227"),
        ("T-227@229 (#672)", "T-196 (#668)@229"),
        ("T-198 (#674 opening)", "T-227@229 (#672)"),
        ("T-199 (#674 update)", "T-227@229 (#672)"),
        ("T-198 (#674 opening)", "T-196 (#668)@229"),
        ("T-199 (#674 update)", "T-198 (#674 opening)"),
        ("T-225@229", "T-227@229 (#672)"),
        ("T-225@229", "T-199 (#674 update)"),
        ("T-226 (#670)", "T-186@204"),
        ("T-228 (#675)", "T-186@204"),
        ("T-223 (#678)@204", "T-186@204"),
        ("T-228 (#675)", "T-226 (#670)"),
        ("T-223 (#678)@204", "T-226 (#670)"),
        ("T-223 (#678)@204", "T-228 (#675)"),
        ("T-225@204", "T-226 (#670)"),
        ("T-225@204", "T-228 (#675)"),
        ("T-225@204", "T-223 (#678)@204"),
    ]
    results = []
    for view, ref in pairs:
        r = measure(P[view], P[ref])
        results.append(r)
        o = r["own_box"]
        print(
            f"{view} vs {ref}: one-to-one under {r['one_to_one_under']}; best {r['best_symmetry']}; "
            f"within 1e-6 {o['within_1e-6']}, 1e-4 {o['within_1e-4']}; beyond {o['beyond']}; largest {o['largest_move']:.4g} (sq {o['largest_move_square']}); "
            f"turned >1e-3deg {r['turned_beyond_1e-3_deg']}, >1deg {r['turned_beyond_1_deg']}; largest turn {r['largest_turn_deg']:.4g} deg; "
            f"rescaled within/beyond {r['reference_scaled_to_view_side']['within_1e-6']}/{r['reference_scaled_to_view_side']['beyond']}",
            flush=True,
        )
    out.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
