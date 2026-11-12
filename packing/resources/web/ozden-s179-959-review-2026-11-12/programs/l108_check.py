"""Decide a rational-corner certificate by both methods: every square, wall and pair.

Lane L108, blind stage 4 review of jlevy/squares#959. Imports nothing from the
repository or the source. No distance filter: every pair goes through both methods.

Usage (from packing/, the project interpreter, isolated mode):
    python -I -B l108_check.py CERT.yaml CERT.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_clip as clipm  # noqa: E402
import l108_reader as reader  # noqa: E402
import l108_sat as satm  # noqa: E402

CHECKER_FILES = ("l108_reader.py", "l108_sat.py", "l108_clip.py", "l108_check.py")
WALLS = ("left", "bottom", "right", "top")
THRESHOLDS = (Fraction(1, 10**15), Fraction(1, 10**13), Fraction(1, 10**12), Fraction(1, 10**9), Fraction(1, 10**6), Fraction(1, 10**3))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def program_digests() -> dict[str, str]:
    return {name: sha256_file(HERE / name) for name in CHECKER_FILES}


def as_fraction(value: Any) -> Fraction:
    """Report helper: an mpq or Fraction as a Fraction (by its integer parts)."""
    return Fraction(int(value.numerator), int(value.denominator))


def dec(value: Fraction, digits: int = 20) -> str:
    """The value in scientific notation, `digits` significant digits, truncated toward 0."""
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    v = abs(value)
    p, q = v.numerator, v.denominator
    e = len(str(p)) - len(str(q))

    def at_least(k: int) -> bool:  # p/q >= 10**k, in integers
        return p * 10 ** max(-k, 0) >= q * 10 ** max(k, 0)

    while not at_least(e):
        e -= 1
    while at_least(e + 1):
        e += 1
    # now 10**e <= v < 10**(e+1)
    shift = digits - 1 - e
    scaled = p * 10**shift // q if shift >= 0 else p // (q * 10 ** (-shift))
    s = str(scaled)
    body = s[0] if len(s) == 1 else f"{s[0]}.{s[1:]}"
    return f"{sign}{body}e{e:+d}"


def exact(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def decide(cert: reader.Certificate, only: set[int] | None = None) -> dict[str, Any]:
    """Both methods over every square and wall, and every pair (or every pair touching `only`)."""
    n = cert.n
    side_a = satm.side_q(cert.side)
    side_b = clipm.side_f(cert.side)
    sq_a = [satm.build(raw) for raw in cert.squares]
    sq_b = [clipm.build(raw) for raw in cert.squares]
    not_unit_a = [i + 1 for i, s in enumerate(sq_a) if s is None]
    not_unit_b = [i + 1 for i, s in enumerate(sq_b) if s is None]
    result: dict[str, Any] = {
        "n": n,
        "not_unit_a": not_unit_a,
        "not_unit_b": not_unit_b,
    }
    if not_unit_a or not_unit_b:
        result["verdict"] = "REFUSE"
        result["reason"] = "not every square is a unit square"
        return result
    assert all(s is not None for s in sq_a) and all(s is not None for s in sq_b)
    a_sq: list[satm.SquareA] = [s for s in sq_a if s is not None]
    b_sq: list[clipm.SquareB] = [s for s in sq_b if s is not None]
    turns = [s.turn for s in a_sq]
    orient = [s.orientation for s in b_sq]
    result["counterclockwise"] = sum(1 for t in turns if t == 1)
    result["clockwise"] = sum(1 for t in turns if t == -1)
    result["orientation_methods_agree"] = turns == orient

    # Walls.
    planes = clipm.wall_planes(side_b)
    wall_rows: list[dict[str, Any]] = []
    wall_disagree: list[tuple[int, str]] = []
    wall_out: list[tuple[int, str]] = []
    contacts: list[tuple[int, str]] = []
    not_in_box_b: list[int] = []
    for i in range(n):
        clear_a = satm.walls(a_sq[i], side_a)
        for name in WALLS:
            va = as_fraction(clear_a[name])
            ca = {"clear": "clear", "contact": "contact", "overlap": "outside"}[satm.classify(clear_a[name])]
            cb_raw, _area = clipm.wall(b_sq[i], planes[name])
            cb = {"clear": "clear", "contact": "contact", "overlap": "outside"}[cb_raw]
            if ca != cb:
                wall_disagree.append((i + 1, name))
            if ca == "outside" or cb == "outside":
                wall_out.append((i + 1, name))
            if ca == "contact":
                contacts.append((i + 1, name))
            wall_rows.append({"square": i + 1, "wall": name, "clearance": va, "a": ca, "b": cb})
        if clipm.area_in_box(b_sq[i], side_b) != 1:
            not_in_box_b.append(i + 1)
    result["walls_decided"] = len(wall_rows)
    result["wall_disagreements"] = wall_disagree
    result["walls_outside"] = wall_out
    result["not_in_box_by_area_b"] = not_in_box_b
    result["wall_contacts"] = [f"{i} {w}" for i, w in contacts]
    positive = sorted((r for r in wall_rows if r["clearance"] > 0), key=lambda r: r["clearance"])
    if positive:
        r0 = positive[0]
        result["least_positive_wall_clearance"] = {"square": r0["square"], "wall": r0["wall"], "value": dec(r0["clearance"]), "exact": exact(r0["clearance"])}
    result["positive_wall_clearances_below"] = {dec(t, 1): sum(1 for r in positive if r["clearance"] < t) for t in THRESHOLDS}
    result["wall_clearances_below_1e-3"] = [
        {"square": r["square"], "wall": r["wall"], "value": dec(r["clearance"])} for r in sorted(wall_rows, key=lambda r: (r["clearance"], r["square"])) if r["clearance"] < Fraction(1, 1000)
    ]

    # Pairs.
    b_planes = [clipm.inner_half_planes(s) for s in b_sq]
    pairs_decided = 0
    pair_disagree: list[tuple[int, int]] = []
    overlaps: list[dict[str, Any]] = []
    touching: list[tuple[int, int]] = []
    area_sum = Fraction(0)
    margin_lines: list[str] = []
    near: list[tuple[Fraction, int, int]] = []
    least: tuple[Fraction, int, int] | None = None
    for i in range(n):
        for j in range(i + 1, n):
            if only is not None and (i + 1) not in only and (j + 1) not in only:
                continue
            pairs_decided += 1
            m = satm.margin(a_sq[i], a_sq[j])
            ca = satm.classify(m)
            cb, area = clipm.pair(b_sq[i], b_planes[j])
            mf = as_fraction(m)
            area_sum += area
            if ca != cb:
                pair_disagree.append((i + 1, j + 1))
            if ca == "overlap" or cb == "overlap":
                overlaps.append({"pair": [i + 1, j + 1], "margin": dec(mf), "area": dec(area), "a": ca, "b": cb})
            if ca == "contact" or cb == "contact":
                touching.append((i + 1, j + 1))
            margin_lines.append(f"{i + 1} {j + 1} {exact(mf)}")
            if mf < Fraction(1, 1000):
                near.append((mf, i + 1, j + 1))
            if least is None or mf < least[0]:
                least = (mf, i + 1, j + 1)
    result["pairs_decided"] = pairs_decided
    result["pair_disagreements"] = [list(p) for p in pair_disagree]
    result["overlapping_pairs"] = overlaps
    result["overlapping_pair_count"] = len(overlaps)
    result["touching_pairs"] = [list(p) for p in touching]
    result["clipped_area_sum"] = exact(area_sum) if area_sum.denominator < 10**200 else dec(area_sum, 30)
    result["margin_list_sha256"] = hashlib.sha256("\n".join(margin_lines).encode()).hexdigest()
    if least is not None:
        result["least_margin"] = {"pair": [least[1], least[2]], "value": dec(least[0], 15), "exact": exact(least[0])}
    result["pairs_below"] = {dec(t, 1): sum(1 for v, _i, _j in near if v < t) for t in THRESHOLDS}
    result["pairs_below_1e-3"] = [{"pair": [i, j], "margin": dec(v, 15)} for v, i, j in sorted(near)]
    ok = (
        not wall_disagree
        and not wall_out
        and not not_in_box_b
        and not pair_disagree
        and not overlaps
        and result["orientation_methods_agree"]
    )
    result["verdict"] = "ACCEPT" if ok else "REFUSE"
    return result


def main(argv: list[str]) -> int:
    yaml_path, json_path, out_path = Path(argv[1]), Path(argv[2]), Path(argv[3])
    t0 = time.process_time()
    try:
        cert = reader.read_paths(yaml_path, json_path)
    except reader.Refused as exc:
        print(f"REFUSED by the reader: {exc}")
        return 1
    res = decide(cert)
    side = Fraction(*cert.side)
    receipt = {
        "program": "l108_check.py",
        "lane": "L108",
        "programs_sha256": program_digests(),
        "python": sys.version.split()[0],
        "source": {
            "yaml": yaml_path.name,
            "yaml_sha256": sha256_file(yaml_path),
            "json": json_path.name,
            "json_sha256": sha256_file(json_path),
        },
        "reading": {
            "scalars_in_lowest_terms": reader.scalar_count(cert),
            "side_digits": [len(str(cert.side[0])), len(str(cert.side[1]))],
            "side_decimal_floor_30": dec(side, 31),
            "twin_equal": True,
        },
        "result": res,
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    out_path.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(res["verdict"], "pairs", res.get("pairs_decided"), "contacts", res.get("wall_contacts"), "least", res.get("least_margin", {}).get("value"))
    return 0 if res["verdict"] == "ACCEPT" else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
