"""Decide a corners/rational Witness/v2 certificate by two methods, every square, wall
and pair, with no distance filter.

Lane L127, clean room. Usage (from packing/, project interpreter, -I):

    python -I -B l127_check.py CERT.yaml TWIN.json OUT.json

The verdict is ACCEPT only when the reader accepts the file and its twin, both methods
accept every square as a unit square with the same listing sense, both put every square
inside the box with equal per-wall classes, and both find every pair apart or touching
with equal classes.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from math import gcd
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l127_clip as mb  # noqa: E402
import l127_reader as rd  # noqa: E402
import l127_sat as ma  # noqa: E402

Rat = tuple[int, int]

THRESHOLDS = (13, 12, 9, 6, 3)  # count margins below 10^-k
WALL_THRESHOLDS = (15, 13, 6, 3)


def below(r: Rat, k: int) -> bool:
    """r < 10^-k for r = p/q, q > 0."""
    return r[0] * 10**k < r[1]


def reduce(r: Rat) -> Rat:
    g = gcd(r[0], r[1])
    return (r[0] // g, r[1] // g)


def rat_str(r: Rat) -> str:
    p, q = reduce(r)
    return str(p) if q == 1 else f"{p}/{q}"


def sci(r: Rat, sig: int = 15) -> str:
    """Decimal scientific print of p/q, truncated toward zero to `sig` digits."""
    p, q = r
    if p == 0:
        return "0"
    neg = p < 0
    p = abs(p)
    e = len(str(p)) - len(str(q))
    if p * 10 ** max(0, -e) < q * 10 ** max(0, e):
        e -= 1
    # now 10^e <= p/q < 10^(e+1)
    shift = sig - 1 - e
    digits = p * 10**shift // q if shift >= 0 else p // (q * 10 ** (-shift))
    s = str(digits)
    mant = s[0] + ("." + s[1:] if len(s) > 1 else "")
    return f"{'-' if neg else ''}{mant}e{e:+03d}"


def rat_lt(a: Rat, b: Rat) -> bool:
    return a[0] * b[1] < b[0] * a[1]


def decide(side: Rat, squares: list[Any], *, keep_margins: bool = True) -> dict[str, Any]:
    """Both methods over every square, wall and pair. Never raises on geometry."""
    n = len(squares)
    res: dict[str, Any] = {"n": n, "side": rat_str(side), "problems": []}
    probs: list[str] = res["problems"]
    sa: list[ma.SquareA | None] = []
    sb: list[mb.SquareB | None] = []
    not_unit_a: list[int] = []
    not_unit_b: list[int] = []
    for k, c in enumerate(squares):
        try:
            sa.append(ma.make_square(c))
        except ma.NotUnit:
            sa.append(None)
            not_unit_a.append(k + 1)
        try:
            sb.append(mb.make_square(c))
        except mb.NotUnit:
            sb.append(None)
            not_unit_b.append(k + 1)
    res["not_unit_a"] = not_unit_a
    res["not_unit_b"] = not_unit_b
    if not_unit_a or not_unit_b:
        probs.append("not every square is a unit square")
        res["verdict"] = "REFUSE"
        return res
    senses_a = [s.sense for s in sa if s is not None]
    senses_b = [s.sense for s in sb if s is not None]
    res["senses_agree"] = senses_a == senses_b
    res["ccw_count"] = sum(1 for s in senses_a if s == 1)
    res["cw_count"] = sum(1 for s in senses_a if s == -1)
    if senses_a != senses_b:
        probs.append("listing senses differ between methods")

    # ---------------- walls
    contacts: list[list[Any]] = []
    outside_a: list[list[Any]] = []
    outside_b: list[list[Any]] = []
    wall_disagree: list[list[Any]] = []
    not_inside_b: list[int] = []
    pos_clear: list[tuple[Rat, int, str]] = []
    nearest_wall: list[dict[str, Any]] = []
    for k in range(n):
        a = sa[k]
        b = sb[k]
        assert a is not None and b is not None
        cl = ma.wall_clearances(a, side)
        cb = mb.wall_classes(b, side)
        if not mb.inside_box(b, side):
            not_inside_b.append(k + 1)
        best: tuple[Rat, str] | None = None
        for wall in ma.WALLS:
            ca = ma.wall_class(cl[wall])
            if ca != cb[wall]:
                wall_disagree.append([k + 1, wall, ca, cb[wall]])
            if ca == "touch":
                contacts.append([k + 1, wall])
            elif ca == "outside":
                outside_a.append([k + 1, wall])
            else:
                pos_clear.append((cl[wall], k + 1, wall))
            if cb[wall] == "outside":
                outside_b.append([k + 1, wall])
            if best is None or rat_lt(cl[wall], best[0]):
                best = (cl[wall], wall)
        assert best is not None
        nearest_wall.append({"square": k + 1, "wall": best[1], "clearance": rat_str(best[0])})
    res["wall_contacts"] = contacts
    res["outside_a"] = outside_a
    res["outside_b"] = outside_b
    res["not_inside_b"] = not_inside_b
    res["wall_disagreements"] = wall_disagree
    if outside_a or outside_b or not_inside_b:
        probs.append("a square is not inside the box")
    if wall_disagree:
        probs.append("wall classes differ between methods")
    pos_clear_sorted = sorted(pos_clear, key=lambda t: _key(t[0]))
    if pos_clear_sorted:
        r, sqid, wall = pos_clear_sorted[0]
        res["least_positive_clearance"] = {"square": sqid, "wall": wall, "value": rat_str(r), "sci": sci(r)}
    res["positive_clearances_below"] = {
        f"1e-{k}": sum(1 for t in pos_clear if below(t[0], k)) for k in WALL_THRESHOLDS
    }
    res["clearances_below_1e-12"] = [
        {"square": t[1], "wall": t[2], "sci": sci(t[0])} for t in pos_clear_sorted if below(t[0], 12)
    ]
    res["nearest_wall"] = nearest_wall

    # ---------------- pairs
    margin_hash = hashlib.sha256()
    pair_disagree: list[list[Any]] = []
    overlaps: list[dict[str, Any]] = []
    touches: list[list[int]] = []
    least: tuple[Rat, int, int] | None = None
    counts = dict.fromkeys(THRESHOLDS, 0)
    near: list[tuple[Rat, int, int]] = []
    area_sum = mb.mpq(0)
    npairs = 0
    margins: dict[tuple[int, int], Rat] = {}
    for i in range(n):
        ai = sa[i]
        bi = sb[i]
        assert ai is not None and bi is not None
        for j in range(i + 1, n):
            aj = sa[j]
            bj = sb[j]
            assert aj is not None and bj is not None
            m = ma.pair_margin(ai, aj)
            ca = ma.pair_class(m)
            cbj, area = mb.pair(bi, bj)
            npairs += 1
            mr = reduce(m)
            margin_hash.update(f"{i + 1} {j + 1} {rat_str(mr)}\n".encode())
            if keep_margins:
                margins[(i + 1, j + 1)] = mr
            if ca != cbj:
                pair_disagree.append([i + 1, j + 1, ca, cbj])
            if ca == "overlap" or cbj == "overlap":
                overlaps.append({"pair": [i + 1, j + 1], "margin": sci(mr), "area": str(area)})
                area_sum += area
            elif ca == "touch":
                touches.append([i + 1, j + 1])
            if least is None or rat_lt(mr, least[0]):
                least = (mr, i + 1, j + 1)
            for k in THRESHOLDS:
                if mr[0] * 10**k < mr[1]:
                    counts[k] += 1
            if below(mr, 12):
                near.append((mr, i + 1, j + 1))
    res["pairs_decided"] = npairs
    res["pair_disagreements"] = pair_disagree
    res["overlapping_pairs"] = overlaps
    res["overlap_count"] = len(overlaps)
    res["touching_pairs"] = touches
    res["overlap_area_sum"] = str(area_sum)
    res["margin_list_sha256"] = margin_hash.hexdigest()
    if least is not None:
        res["least_margin"] = {"pair": [least[1], least[2]], "value": rat_str(least[0]), "sci": sci(least[0])}
    res["margins_below"] = {f"1e-{k}": counts[k] for k in THRESHOLDS}
    near.sort(key=lambda t: _key(t[0]))
    res["near_pairs_below_1e-12"] = [{"pair": [t[1], t[2]], "sci": sci(t[0], 6)} for t in near]
    if pair_disagree:
        probs.append("pair classes differ between methods")
    if overlaps:
        probs.append("overlapping pairs")
    res["verdict"] = "ACCEPT" if not probs else "REFUSE"
    if keep_margins:
        res["_margins"] = margins
    return res


def _key(r: Rat) -> Fraction:
    """An exact sort key for a rational (sorting only; nothing is decided by it)."""
    return Fraction(r[0], r[1])


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(argv: list[str]) -> int:
    cert, twin, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
    t0 = time.process_time()
    receipt: dict[str, Any] = {
        "program": "l127_check.py",
        "inputs": {cert.name: sha256_file(cert), twin.name: sha256_file(twin)},
    }
    try:
        doc = rd.read_certificate(cert.read_text(encoding="utf-8"), twin.read_text(encoding="utf-8"))
    except rd.Refused as exc:
        receipt["verdict"] = "REFUSE"
        receipt["reader"] = f"refused: {exc}"
        out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
        print("REFUSE", exc)
        return 1
    receipt["reader"] = {
        "id": doc["id"],
        "n": doc["n"],
        "twin": doc["twin"],
        "side_digits": [len(str(doc["side"][0])), len(str(doc["side"][1]))],
        "scalars_read": 1 + 8 * doc["n"],
        "zero_scalars": sum(1 for s in doc["squares"] for pt in s for c in pt if c[0] == 0),
    }
    res = decide(doc["side"], doc["squares"], keep_margins=False)
    res.pop("_margins", None)
    res.pop("nearest_wall", None)
    receipt.update(res)
    receipt["cpu_seconds"] = round(time.process_time() - t0, 1)
    out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(
        receipt["verdict"],
        f"pairs={res['pairs_decided']}",
        f"contacts={res['wall_contacts']}",
        f"least={res.get('least_margin')}",
        f"problems={res['problems']}",
    )
    return 0 if receipt["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
