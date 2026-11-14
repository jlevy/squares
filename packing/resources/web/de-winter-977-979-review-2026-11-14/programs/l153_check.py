"""Lane L153 checker: decide a center-basis certificate by two methods, in full.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review.

Every square, every square-wall pair and every pair of squares is decided by method A
(`l153_sat`, separating axes in Python integers) and by method B (`l153_clip`, exact
convex clipping in gmpy2 rationals), with no distance filter. The two share only the
reader (`l153_reader`), which hands them integers.

The verdict is ACCEPT only when both methods find every square a unit square, every
square inside [0, S]^2 (A: no negative clearance; B: no wall crossed and the
intersection with the box of area exactly 1), every pair apart or in contact, and their
classes agree on every square, wall and pair.

Usage: l153_check.py LABEL CERT.json [TWIN.yaml] OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l153_clip as B  # noqa: E402
import l153_reader as reader  # noqa: E402
import l153_sat as A  # noqa: E402
from gmpy2 import mpq  # noqa: E402

THRESHOLDS = (60, 30, 20, 15, 14, 13, 12, 9, 6, 3, 2, 1)
NEAR = Fraction(1, 10**9)


def sci(value: Fraction | int, sig: int = 6) -> str:
    """A decimal print of an exact value with `sig` significant digits, truncated."""
    value = Fraction(value)
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    mag = abs(value)
    e = len(str(mag.numerator)) - len(str(mag.denominator))
    while Fraction(10) ** e > mag:
        e -= 1
    while Fraction(10) ** (e + 1) <= mag:
        e += 1
    digits = str(int(mag * Fraction(10) ** (sig - 1 - e)))
    return f"{sign}{digits[0]}.{digits[1:]}e{e:+d}"


def floor_places(value: Fraction, places: int) -> str:
    scaled = value.numerator * 10**places // value.denominator
    text = str(scaled).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def exact(value: Fraction) -> str:
    return str(value)


def sha256_file(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def decide(side_pair: tuple[int, int], squares: list, keep_margins: bool = False) -> dict:
    """Both methods over every square, wall and pair. Returns the full comparison."""
    n = len(squares)
    side = Fraction(*side_pair)
    side_q = mpq(*side_pair)
    t0 = time.process_time()
    prep = [A.prepare(sq) for sq in squares]
    unit_a = [A.is_unit(p) for p in prep]
    polys = [B.corners(sq) for sq in squares]
    unit_b = [B.is_unit(p) for p in polys]
    result: dict = {
        "n": n,
        "unit_a": sum(unit_a),
        "unit_b": sum(unit_b),
        "not_unit": [k + 1 for k in range(n) if not (unit_a[k] and unit_b[k])],
        "unit_disagree": [k + 1 for k in range(n) if unit_a[k] != unit_b[k]],
    }
    if result["not_unit"]:
        result["verdict"] = "REFUSE"
        result["reason"] = "not every square is a unit square"
        return result
    # Walls.
    wall_contacts_a: list[list] = []
    wall_crossing_a: list[list] = []
    wall_disagree: list[list] = []
    wall_crossing_b: list[list] = []
    not_inside_b: list[int] = []
    clear_list: list[str] = []
    least_clear: tuple[Fraction, int, str] | None = None
    clear_counts = dict.fromkeys(THRESHOLDS, 0)
    clearances: list[dict[str, Fraction]] = []
    for k in range(n):
        ca = A.clearances(prep[k], side)
        clearances.append(ca)
        for name in A.WALLS:
            value = ca[name]
            clear_list.append(exact(value))
            cls_a = A.classify(value)
            cls_a = "crossing" if cls_a == "overlap" else cls_a
            cls_b, _ = B.wall(polys[k], name, side_q)
            if cls_a != cls_b:
                wall_disagree.append([k + 1, name, cls_a, cls_b])
            if cls_a == "contact":
                wall_contacts_a.append([k + 1, name])
            if cls_a == "crossing":
                wall_crossing_a.append([k + 1, name, sci(value)])
            if cls_b == "crossing":
                wall_crossing_b.append([k + 1, name])
            if value > 0:
                if least_clear is None or value < least_clear[0]:
                    least_clear = (value, k + 1, name)
                for t in THRESHOLDS:
                    if value < Fraction(1, 10**t):
                        clear_counts[t] += 1
        if B.inside_area(polys[k], side_q) != 1:
            not_inside_b.append(k + 1)
    t_walls = time.process_time() - t0
    # Pairs.
    counts_a = {"apart": 0, "contact": 0, "overlap": 0}
    counts_b = {"apart": 0, "contact": 0, "overlap": 0}
    contacts: list[list[int]] = []
    overlaps: list[list] = []
    disagree: list[list] = []
    near: list[list] = []
    pair_counts = dict.fromkeys(THRESHOLDS, 0)
    least: tuple[Fraction, int, int] | None = None
    area_sum = mpq(0)
    digest = hashlib.sha256()
    margins: dict[tuple[int, int], Fraction] = {}
    t_a = 0.0
    t_b = 0.0
    for i in range(n):
        pi, qi = prep[i], polys[i]
        for j in range(i + 1, n):
            s0 = time.process_time()
            m = A.margin(pi, prep[j])
            s1 = time.process_time()
            cls_b, area = B.pair(qi, polys[j])
            s2 = time.process_time()
            t_a += s1 - s0
            t_b += s2 - s1
            cls_a = A.classify(m)
            counts_a[cls_a] += 1
            counts_b[cls_b] += 1
            digest.update(f"{i + 1} {j + 1} {m}\n".encode())
            if keep_margins:
                margins[(i + 1, j + 1)] = m
            if cls_a != cls_b:
                disagree.append([i + 1, j + 1, cls_a, cls_b])
            if cls_a == "contact":
                contacts.append([i + 1, j + 1])
            elif cls_a == "overlap":
                overlaps.append([i + 1, j + 1, exact(m), str(area)])
            else:
                if least is None or m < least[0]:
                    least = (m, i + 1, j + 1)
                for t in THRESHOLDS:
                    if m < Fraction(1, 10**t):
                        pair_counts[t] += 1
                if m < NEAR:
                    near.append([i + 1, j + 1, sci(m, 8)])
            area_sum += area
    accept = (
        not wall_disagree
        and not wall_crossing_a
        and not wall_crossing_b
        and not not_inside_b
        and not disagree
        and counts_a["overlap"] == 0
        and counts_b["overlap"] == 0
    )
    result.update(
        {
            "walls": {
                "contacts": wall_contacts_a,
                "crossing_a": wall_crossing_a,
                "crossing_b": wall_crossing_b,
                "not_inside_b": not_inside_b,
                "disagree": wall_disagree,
                "least_positive": None
                if least_clear is None
                else {
                    "square": least_clear[1],
                    "wall": least_clear[2],
                    "value": exact(least_clear[0]),
                    "approx": sci(least_clear[0], 8),
                },
                "positive_below_1e-t": {str(t): c for t, c in clear_counts.items()},
                "clearance_list_sha256": hashlib.sha256(
                    "\n".join(clear_list).encode()
                ).hexdigest(),
            },
            "pairs": {
                "decided": counts_a["apart"] + counts_a["contact"] + counts_a["overlap"],
                "classes_a": counts_a,
                "classes_b": counts_b,
                "disagree": disagree,
                "contacts": contacts,
                "overlaps": overlaps,
                "overlap_area_sum_b": str(area_sum),
                "least_positive": None
                if least is None
                else {
                    "pair": [least[1], least[2]],
                    "value": exact(least[0]),
                    "approx": sci(least[0], 15),
                },
                "positive_below_1e-t": {str(t): c for t, c in pair_counts.items()},
                "near_below_1e-9": near,
                "margin_list_sha256": digest.hexdigest(),
            },
            "cpu_seconds": {
                "walls_and_squares": round(t_walls, 1),
                "pairs_a": round(t_a, 1),
                "pairs_b": round(t_b, 1),
            },
            "verdict": "ACCEPT" if accept else "REFUSE",
        }
    )
    result["_clearances"] = clearances
    if keep_margins:
        result["_margins"] = margins
    return result


def public(result: dict) -> dict:
    return {k: v for k, v in result.items() if not k.startswith("_")}


def main(argv: list[str]) -> int:
    label = argv[1]
    cert = argv[2]
    twin = argv[3] if len(argv) == 5 else None
    out_path = argv[-1]
    t0 = time.process_time()
    data = reader.read(cert, twin)
    n = data["n"]
    side_pair = data["side"]
    side = Fraction(*side_pair)
    squares = data["squares"]
    result = decide(side_pair, squares)
    receipt = {
        "program": "l153_check.py",
        "label": label,
        "inputs": {
            Path(cert).name: sha256_file(cert),
            **({Path(twin).name: sha256_file(twin)} if twin else {}),
        },
        "reading": {
            "n": n,
            "format": data["format"],
            "twin": "same n, side and squares" if twin else None,
            "twin_header": data.get("twin_header"),
            "scalars": 1 + 4 * n,
            "side_digits": [len(str(side.numerator)), len(str(side.denominator))],
            "side_floor_40": floor_places(side, 40),
        },
        **public(result),
        "cpu_seconds_total": round(time.process_time() - t0, 1),
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + "\n")
    pairs = receipt.get("pairs", {})
    print(
        label,
        receipt["verdict"],
        f"n={n}",
        f"pairs={pairs.get('decided')}",
        f"contacts={len(pairs.get('contacts', []))}",
        f"walls={receipt.get('walls', {}).get('contacts')}",
        f"least={pairs.get('least_positive', {}) and pairs['least_positive']['approx']}",
        f"at={pairs.get('least_positive', {}) and pairs['least_positive']['pair']}",
    )
    return 0 if receipt["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
