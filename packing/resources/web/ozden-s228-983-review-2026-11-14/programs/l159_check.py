"""Lane L159's checker: decide a Witness/v2 corners certificate by two methods.

Clean-room code written for the stage 4 review of issue #983. It imports nothing from
this repository or from the source, and reuses no code of any earlier review.

Every square, every wall and every pair is decided, with no distance filter, by method A
(separating axes in Python integers, l159_sat) and method B (exact convex clipping in
gmpy2 rationals, l159_clip). The two share only the reader (l159_reader), which hands
them integers. The verdict is ACCEPT only when both methods accept every square, wall
and pair, their classes agree everywhere, and their listing senses agree.

Usage: l159_check.py CERT.yaml TWIN.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l159_clip as clip  # noqa: E402
import l159_sat as sat  # noqa: E402
from l159_geom import floor_places, sci  # noqa: E402
from l159_reader import read_paths  # noqa: E402

WALLS = ("left", "bottom", "right", "top")
PAIR_THRESHOLDS = ("1e-13", "1e-12", "1e-9", "1e-6", "1e-3")
WALL_THRESHOLDS = ("1e-15", "1e-13", "1e-6", "1e-3")


@dataclass
class Decision:
    """Everything both methods decided about one file."""

    n: int
    side: tuple[int, int]
    not_unit_a: list[int] = field(default_factory=list)
    not_unit_b: list[int] = field(default_factory=list)
    sense_a: list[int] = field(default_factory=list)
    sense_b: list[int] = field(default_factory=list)
    clearance: list[list[Fraction]] = field(default_factory=list)
    wall_a: list[list[str]] = field(default_factory=list)
    wall_b: list[list[str]] = field(default_factory=list)
    contained_b: list[bool] = field(default_factory=list)
    margins: dict[tuple[int, int], Fraction] = field(default_factory=dict)
    class_a: dict[tuple[int, int], str] = field(default_factory=dict)
    class_b: dict[tuple[int, int], str] = field(default_factory=dict)
    area_b: dict[tuple[int, int], Fraction] = field(default_factory=dict)
    disagreements: list[str] = field(default_factory=list)
    verdict: str = "REFUSE"
    stopped: str | None = None


def decide(side: tuple[int, int], squares: list, pairs: list[tuple[int, int]] | None = None) -> Decision:
    """Decide every square, wall and pair (or only the listed pairs) by both methods."""
    n = len(squares)
    d = Decision(n=n, side=side)
    prepared = [sat.prepare(c) for c in squares]
    points = [clip.to_points(c) for c in squares]
    unit_b = [clip.is_unit_square(p) for p in points]
    d.not_unit_a = [i + 1 for i, s in enumerate(prepared) if s is None]
    d.not_unit_b = [i + 1 for i, ok in enumerate(unit_b) if not ok]
    if d.not_unit_a or d.not_unit_b:
        d.stopped = "not a unit square"
        return d
    d.sense_a = [s.sense for s in prepared]  # type: ignore[union-attr]
    d.sense_b = [clip.sense(p) for p in points]
    if d.sense_a != d.sense_b:
        d.disagreements.append("listing senses differ")
    planes = [clip.edge_half_planes(p) for p in points]
    for i in range(n):
        values = sat.clearances(prepared[i], side)  # type: ignore[arg-type]
        d.clearance.append(values)
        d.wall_a.append([sat.clearance_class(v) for v in values])
        d.wall_b.append(clip.walls(points[i], side))
        d.contained_b.append(clip.contained(points[i], side))
        if d.wall_a[i] != d.wall_b[i]:
            d.disagreements.append(f"square {i + 1} wall classes {d.wall_a[i]} vs {d.wall_b[i]}")
        if d.contained_b[i] != ("cross" not in d.wall_b[i]):
            d.disagreements.append(f"square {i + 1} containment against wall classes")
    todo = pairs if pairs is not None else [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    for i, j in todo:
        m = sat.margin(prepared[i - 1], prepared[j - 1])  # type: ignore[arg-type]
        ca = sat.margin_class(m[0])
        cb, area = clip.pair(points[j - 1], planes[i - 1])
        key = (i, j)
        d.margins[key] = sat.margin_fraction(m)
        d.class_a[key] = ca
        d.class_b[key] = cb
        if cb != "apart":
            d.area_b[key] = Fraction(int(area.numerator), int(area.denominator))
        if ca != cb:
            d.disagreements.append(f"pair {key} classes {ca} vs {cb}")
    walls_ok = all(
        cls in ("apart", "contact") for row in d.wall_a for cls in row
    ) and all(d.contained_b)
    pairs_ok = all(c in ("apart", "contact") for c in d.class_a.values())
    if not d.disagreements and walls_ok and pairs_ok:
        d.verdict = "ACCEPT"
    return d


def margin_digest(d: Decision) -> str:
    """SHA-256 of the exact margin list, one line 'i j p/q' per pair in order."""
    h = hashlib.sha256()
    for (i, j), m in sorted(d.margins.items()):
        h.update(f"{i} {j} {m.numerator}/{m.denominator}\n".encode())
    return h.hexdigest()


def _threshold(text: str) -> Fraction:
    return Fraction(1, 10 ** int(text.split("e-")[1]))


def summarize(d: Decision) -> dict[str, object]:
    """The receipt's view of a decision: counts, extremes, contacts and digests."""
    out: dict[str, object] = {
        "verdict": d.verdict,
        "n": d.n,
        "side": f"{d.side[0]}/{d.side[1]}",
        "side_floor_30": floor_places(Fraction(*d.side), 30),
        "not_unit_a": d.not_unit_a,
        "not_unit_b": d.not_unit_b,
        "stopped": d.stopped,
    }
    if d.stopped:
        return out
    out["listed_counterclockwise"] = sum(1 for s in d.sense_a if s == 1)
    out["listed_clockwise"] = sum(1 for s in d.sense_a if s == -1)
    out["senses_agree"] = d.sense_a == d.sense_b
    out["disagreements"] = d.disagreements[:50]
    out["disagreement_count"] = len(d.disagreements)
    out["pairs_decided"] = len(d.margins)
    for name, classes in (("a", d.class_a), ("b", d.class_b)):
        out[f"pair_classes_{name}"] = {
            c: sum(1 for v in classes.values() if v == c) for c in ("apart", "contact", "overlap")
        }
    overlaps = sorted(k for k, v in d.class_a.items() if v == "overlap")
    contacts = sorted(k for k, v in d.class_a.items() if v == "contact")
    out["overlapping_pairs"] = [
        [i, j, sci(d.margins[(i, j)], 6), sci(d.area_b.get((i, j), Fraction(0)), 6)]
        for i, j in overlaps[:200]
    ]
    out["touching_pairs"] = [[i, j] for i, j in contacts[:200]]
    out["overlap_area_sum_b"] = str(sum(d.area_b.values(), Fraction(0)))
    if d.margins:
        least_key = min(d.margins, key=lambda k: (d.margins[k], k))
        least = d.margins[least_key]
        out["least_margin"] = {
            "pair": list(least_key),
            "sci": sci(least, 15),
            "exact": f"{least.numerator}/{least.denominator}",
        }
        out["pairs_below"] = {
            t: sum(1 for m in d.margins.values() if m < _threshold(t)) for t in PAIR_THRESHOLDS
        }
        out["near_pairs"] = [
            [i, j, sci(m, 6)]
            for (i, j), m in sorted(d.margins.items(), key=lambda kv: (kv[1], kv[0]))
            if m < Fraction(1, 1000)
        ]
        out["margin_list_sha256"] = margin_digest(d)
    contacts_w = []
    crosses_w = []
    positive = []
    for i, row in enumerate(d.clearance, start=1):
        for k, v in enumerate(row):
            if v == 0:
                contacts_w.append([i, WALLS[k]])
            elif v < 0:
                crosses_w.append([i, WALLS[k], sci(v, 6)])
            else:
                positive.append((v, i, k))
    out["wall_contacts"] = contacts_w
    out["wall_crossings"] = crosses_w[:200]
    out["not_contained_b"] = [i + 1 for i, ok in enumerate(d.contained_b) if not ok]
    if positive:
        v, i, k = min(positive)
        out["least_positive_clearance"] = {
            "square": i,
            "wall": WALLS[k],
            "sci": sci(v, 15),
            "exact": f"{v.numerator}/{v.denominator}",
        }
        out["positive_clearances_below"] = {
            t: sum(1 for v, _, _ in positive if v < _threshold(t)) for t in WALL_THRESHOLDS
        }
        out["near_walls"] = [
            [i, WALLS[k], sci(v, 6)] for v, i, k in sorted(positive) if v < Fraction(1, 1000)
        ]
    side = Fraction(*d.side)
    out["extent_x_short_of_side"] = sci(min(row[2] for row in d.clearance), 6)
    out["extent_y_short_of_side"] = sci(min(row[3] for row in d.clearance), 6)
    out["side_sci_20"] = sci(side, 20)
    return out


def main(argv: list[str]) -> int:
    cert, twin, out_path = (Path(a) for a in argv[1:4])
    started = time.process_time()
    w = read_paths(cert, twin)
    d = decide(w.side, w.squares)
    receipt: dict[str, object] = {
        "program": "l159_check.py",
        "certificate": str(cert.name),
        "certificate_sha256": hashlib.sha256(cert.read_bytes()).hexdigest(),
        "twin": str(twin.name),
        "twin_sha256": hashlib.sha256(twin.read_bytes()).hexdigest(),
        "reading": {
            "witness_id": w.witness_id,
            "n": w.n,
            "scalars": w.scalars,
            "zero_scalars": w.zero_scalars,
            "side_digits": [len(str(w.side[0])), len(str(w.side[1]))],
            "twin_same_tree": True,
            "claim": w.claim,
            "source": w.source,
            "certificate": w.certificate,
        },
    }
    receipt.update(summarize(d))
    receipt["cpu_seconds"] = round(time.process_time() - started, 1)
    out_path.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(
        receipt["verdict"],
        receipt.get("pairs_decided"),
        "pairs; least margin",
        receipt.get("least_margin", {}).get("sci"),
        receipt.get("least_margin", {}).get("pair"),
        "; wall contacts",
        receipt.get("wall_contacts"),
        f"; {receipt['cpu_seconds']} s",
    )
    return 0 if d.verdict == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
