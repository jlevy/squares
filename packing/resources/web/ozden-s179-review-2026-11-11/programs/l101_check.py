"""Decide a corners / rational Witness/v2 file by two methods, every square, wall and pair.

Usage: python -I -B l101_check.py WITNESS.yaml TWIN.json N OUT.json

The verdict is ACCEPT only when the reader reads the file and its twin, every square is
a unit square by both methods, every square lies in [0, S]^2 by both, every pair has
disjoint interiors by both, and the two methods' three-way classes agree on every wall
and every pair. No distance filter: all n(n-1)/2 pairs are decided.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gmpy2  # noqa: E402
import yaml  # noqa: E402
from gmpy2 import mpq  # noqa: E402

import l101_clip as clip  # noqa: E402
import l101_reader as reader  # noqa: E402
import l101_sat as sat  # noqa: E402

HERE = Path(__file__).resolve().parent
CHECKER_FILES = ("l101_reader.py", "l101_sat.py", "l101_clip.py", "l101_check.py")
WALLS = ("left", "bottom", "right", "top")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def program_digests() -> dict[str, str]:
    return {name: sha256_file(HERE / name) for name in CHECKER_FILES}


def frac_str(x: Fraction | mpq) -> str:
    x = Fraction(int(x.numerator), int(x.denominator))
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def sci(x: Fraction | mpq, digits: int = 12) -> str:
    """|x| truncated to `digits` significant digits, with its sign, exactly."""
    x = Fraction(int(x.numerator), int(x.denominator))
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    x = abs(x)
    e = len(str(x.numerator)) - len(str(x.denominator))
    while Fraction(10) ** e > x:
        e -= 1
    while Fraction(10) ** (e + 1) <= x:
        e += 1
    m = int(x / Fraction(10) ** (e - digits + 1))
    s = str(m)
    return f"{sign}{s[0]}.{s[1:]}e{e:+d}"


def decide(
    side: tuple[int, int],
    squares: list,
    pair_list: list[tuple[int, int]] | None = None,
    wall_squares: list[int] | None = None,
    keep_margins: bool = False,
) -> dict:
    """Decide the given pairs and walls (0-based indices) by both methods."""
    n = len(squares)
    side_a = Fraction(*side)
    side_b = mpq(*side)
    sq_a = [sat.make_square(p) for p in squares]
    sq_b = [clip.make_square(p) for p in squares]
    bad_a = [i for i, s in enumerate(sq_a) if isinstance(s, str)]
    bad_b = [i for i, s in enumerate(sq_b) if isinstance(s, str)]
    senses_agree = all(
        isinstance(a, str) or isinstance(b, str) or a.sense == b.sense
        for a, b in zip(sq_a, sq_b, strict=True)
    )
    result: dict = {
        "not_unit_A": [[i + 1, sq_a[i]] for i in bad_a],
        "not_unit_B": [[i + 1, sq_b[i]] for i in bad_b],
        "senses_agree": senses_agree,
        "counterclockwise_A": sum(1 for s in sq_a if not isinstance(s, str) and s.sense == 1),
    }
    bad = set(bad_a) | set(bad_b)
    walls_list = list(range(n)) if wall_squares is None else wall_squares
    planes = clip.outer_planes(side_b)
    wall_rows = []
    wall_disagree = []
    for i in walls_list:
        if i in bad:
            continue
        clear_a = sat.wall_clearances(sq_a[i], side_a)
        row = {"square": i + 1, "clearance": clear_a, "A": {}, "B": {}}
        for w in WALLS:
            ca = sat.wall_class(clear_a[w])
            cb, area = clip.wall(sq_b[i], planes[w])
            row["A"][w] = ca
            row["B"][w] = cb
            if ca != cb:
                wall_disagree.append([i + 1, w, ca, cb])
            if cb == "outside":
                row.setdefault("outside_area", {})[w] = frac_str(area)
        row["inside_area_B"] = clip.inside_area(sq_b[i], side_b)
        wall_rows.append(row)
    result["walls_decided"] = len(wall_rows)
    result["wall_disagreements"] = wall_disagree
    result["wall_contacts"] = [
        [r["square"], w] for r in wall_rows for w in WALLS if r["A"][w] == "contact"
    ]
    result["wall_outside"] = [
        [r["square"], w] for r in wall_rows for w in WALLS
        if r["A"][w] == "outside" or r["B"][w] == "outside"
    ]
    result["inside_area_not_1"] = [r["square"] for r in wall_rows if r["inside_area_B"] != 1]
    positives = [
        (r["clearance"][w], r["square"], w) for r in wall_rows for w in WALLS
        if r["clearance"][w] > 0
    ]
    if positives:
        least = min(positives)
        result["least_positive_wall_clearance"] = {
            "value": frac_str(least[0]), "approx": sci(least[0]),
            "square": least[1], "wall": least[2],
        }
    result["wall_clearances_below"] = {
        label: sum(1 for v, _, _ in positives if v < Fraction(bound))
        for label, bound in (("1e-15", Fraction(1, 10**15)), ("1e-12", Fraction(1, 10**12)),
                             ("1e-9", Fraction(1, 10**9)), ("1e-3", Fraction(1, 10**3)))
    }
    result["wall_clearance_rows"] = wall_rows  # dropped from receipts by the caller

    if pair_list is None:
        pair_list = [(i, j) for i in range(n) for j in range(i + 1, n)]
    classes_a = {"clear": 0, "contact": 0, "overlap": 0}
    classes_b = {"clear": 0, "contact": 0, "overlap": 0}
    disagree = []
    overlaps = []
    contacts = []
    area_sum = mpq(0)
    margins: list[tuple[Fraction, int, int]] = []
    for i, j in pair_list:
        if i in bad or j in bad:
            continue
        m = sat.pair_margin(sq_a[i], sq_a[j])
        ca = sat.classify(m)
        cb, area = clip.pair(sq_b[i], sq_b[j])
        classes_a[ca] += 1
        classes_b[cb] += 1
        area_sum += area
        if ca != cb:
            disagree.append([i + 1, j + 1, ca, cb])
        if ca == "overlap" or cb == "overlap":
            overlaps.append({"pair": [i + 1, j + 1], "margin": frac_str(m), "area": frac_str(area)})
        if ca == "contact" or cb == "contact":
            contacts.append([i + 1, j + 1])
        margins.append((m, i + 1, j + 1))
    result["pairs_decided"] = len(margins)
    result["pair_classes_A"] = classes_a
    result["pair_classes_B"] = classes_b
    result["pair_disagreements"] = disagree
    result["overlapping_pairs"] = overlaps
    result["touching_pairs"] = contacts
    result["clipped_area_sum"] = frac_str(area_sum)
    if margins:
        least_m = min(margins)
        result["least_pair_margin"] = {
            "pair": [least_m[1], least_m[2]], "value": frac_str(least_m[0]),
            "approx": sci(least_m[0]),
        }
        lines = "".join(f"{i} {j} {frac_str(m)}\n" for m, i, j in sorted(margins, key=lambda t: (t[1], t[2])))
        result["margins_sha256"] = hashlib.sha256(lines.encode()).hexdigest()
    if keep_margins:
        result["margins"] = margins
    ok = (
        not bad_a and not bad_b and senses_agree
        and not wall_disagree and not result["wall_outside"] and not result["inside_area_not_1"]
        and not disagree and classes_a["overlap"] == 0 and classes_b["overlap"] == 0
    )
    result["verdict"] = "ACCEPT" if ok else "REFUSE"
    return result


def summarize(result: dict, near: Fraction = Fraction(1, 10**12)) -> dict:
    """The receipt form: exact near pairs, approximate clearances, no Fraction objects."""
    out = {k: v for k, v in result.items() if k not in {"wall_clearance_rows", "margins"}}
    rows = result["wall_clearance_rows"]
    out["wall_clearances"] = [
        {"square": r["square"], **{w: sci(r["clearance"][w], 6) for w in WALLS}}
        for r in rows
    ]
    out["near_wall_exact"] = [
        {"square": r["square"], "wall": w, "value": frac_str(r["clearance"][w]),
         "approx": sci(r["clearance"][w])}
        for r in rows for w in WALLS if 0 <= r["clearance"][w] < near
    ]
    if "margins" in result:
        ms = result["margins"]
        out["pairs_below"] = {
            label: sum(1 for m, _, _ in ms if m < bound)
            for label, bound in (("1e-13", Fraction(1, 10**13)), ("1e-12", near),
                                 ("1e-9", Fraction(1, 10**9)), ("1e-6", Fraction(1, 10**6)),
                                 ("1e-3", Fraction(1, 10**3)))
        }
        out["near_pairs_exact"] = [
            {"pair": [i, j], "value": frac_str(m), "approx": sci(m)}
            for m, i, j in sorted(ms) if m < near
        ]
    return out


def main() -> int:
    yaml_path, json_path, n_text, out_path = sys.argv[1:5]
    start = time.process_time()
    w = reader.read_files(Path(yaml_path), Path(json_path), int(n_text))
    read_seconds = time.process_time() - start
    result = decide(w.side, w.squares, keep_margins=True)
    receipt = {
        "program": "l101_check.py",
        "programs_sha256": program_digests(),
        "python": sys.version.split()[0],
        "gmpy2": gmpy2.version(),
        "pyyaml": yaml.__version__,
        "input": {
            "yaml": Path(yaml_path).name,
            "yaml_sha256": sha256_file(Path(yaml_path)),
            "json": Path(json_path).name,
            "json_sha256": sha256_file(Path(json_path)),
        },
        "reading": {
            "n": w.n,
            "ids": "1..n in order",
            "scalars_in_lowest_terms": w.scalar_count,
            "json_twin": "same tree",
            "side": frac_str(Fraction(*w.side)),
            "side_numerator_digits": len(str(w.side[0])),
            "side_denominator_digits": len(str(w.side[1])),
            "meta": w.meta,
        },
        **summarize(result),
        "cpu_seconds": {"read": round(read_seconds, 2),
                        "total": round(time.process_time() - start, 2)},
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + "\n",
                              encoding="utf-8")
    print(receipt["verdict"], "pairs", receipt["pairs_decided"],
          "A", receipt["pair_classes_A"], "B", receipt["pair_classes_B"],
          "walls", receipt["wall_contacts"], "cpu", receipt["cpu_seconds"])
    return 0 if receipt["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
