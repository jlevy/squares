"""Decide one Witness/v2 corner certificate in full by methods A and B (lane L64).

Usage: python -I -B l64_check.py CERT.yaml TWIN.json N OUT.json

Written clean room on 2026-11-09. Every square, every wall and every pair is decided by
both methods: separating axes in Fraction (`l64_sat.py`) and exact clipped areas in mpq
(`l64_clip.py`). There is no distance filter. The verdict is ACCEPT only when the file
reads strictly, its JSON twin holds exactly the same witness, every square is a unit
square by both methods, every square lies in [0, S]^2 by both, no pair overlaps by
either, and the two methods agree on every square, wall and pair.

`decide()` is also what the controls call, on squares they build themselves.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

# Run with `python -I`, which leaves the script's own directory off sys.path: put this
# directory, and only it, in front, so the sibling modules load from here.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from gmpy2 import mpq  # noqa: E402

import l64_clip as B
import l64_sat as A
from l64_reader import ReadError, read_twin_json, read_witness
from l64_util import Clock, environment, fixed, frac_str, program_digests, sci, write_receipt

HERE = Path(__file__).resolve().parent
CHECKER = ["l64_util.py", "l64_reader.py", "l64_sat.py", "l64_clip.py", "l64_check.py"]
NEAR = F(1, 10**3)
THRESHOLDS = [(f"1e-{k}", F(1, 10**k)) for k in (15, 13, 12, 9, 6, 3)]
NEAREST = 40
WALLS = ("left", "bottom", "right", "top")


def _build(squares: list[dict]) -> tuple[list, list, list[dict], list[dict]]:
    sa: list[A.SquareA | None] = []
    sb: list[B.SquareB | None] = []
    shape_refusals: list[dict] = []
    disagreements: list[dict] = []
    for sq in squares:
        a = b = None
        ea = eb = None
        try:
            a = A.SquareA(sq["id"], sq["corners"])
        except A.ShapeError as exc:
            ea = str(exc)
        try:
            b = B.SquareB(sq["id"], sq["corners"])
        except B.ShapeErrorB as exc:
            eb = str(exc)
        if (ea is None) != (eb is None):
            disagreements.append({"square": sq["id"], "what": "unit shape", "A": ea, "B": eb})
        if ea is not None or eb is not None:
            shape_refusals.append({"square": sq["id"], "A": ea, "B": eb})
            try:
                a = A.SquareA(sq["id"], sq["corners"], unit=False)
            except A.ShapeError:
                a = None
            try:
                b = B.SquareB(sq["id"], sq["corners"], unit=False)
            except B.ShapeErrorB:
                b = None
            if (a is None) != (b is None):
                disagreements.append({"square": sq["id"], "what": "square shape"})
            if a is None or b is None:
                a = b = None
        if a is not None and b is not None and a.orient != b.sense:
            disagreements.append({"square": sq["id"], "what": "sense"})
        sa.append(a)
        sb.append(b)
    return sa, sb, shape_refusals, disagreements


def decide(squares: list[dict], side: F, nearest: int = NEAREST) -> dict:
    """Decide squares [{'id', 'corners': four (xn, xd, yn, yd)}] at side, by A and B."""
    n = len(squares)
    side_q = mpq(side.numerator, side.denominator)
    ids = [sq["id"] for sq in squares]
    sa, sb, shape_refusals, disagreements = _build(squares)
    not_squares = [squares[k]["id"] for k in range(n) if sa[k] is None]

    # Walls.
    contacts = dict.fromkeys(WALLS, 0)
    outside: list[dict] = []
    least_wall: tuple[F, int, str] | None = None
    least_positive: tuple[F, int, str] | None = None
    corners_on_walls_b = 0
    for k in range(n):
        a, b = sa[k], sb[k]
        if a is None or b is None:
            continue
        cl = A.wall_clearances(a, side)
        m = min(cl.values())
        inside_b, kept = B.contained(b, side_q)
        if (m >= 0) != inside_b:
            disagreements.append({"square": ids[k], "what": "wall", "A": str(m), "B": str(kept)})
        for wall in WALLS:
            v = cl[wall]
            if v == 0:
                contacts[wall] += 1
            if least_wall is None or v < least_wall[0]:
                least_wall = (v, ids[k], wall)
            if v > 0 and (least_positive is None or v < least_positive[0]):
                least_positive = (v, ids[k], wall)
        if m < 0 or not inside_b:
            outside.append({"square": ids[k], "clearance": frac_str(m), "kept_area_B": str(kept)})
        corners_on_walls_b += B.corners_on_walls(b, side_q)

    # Pairs: every one, by both methods.
    classes = {"separated": 0, "touching": 0, "overlapping": 0}
    near: list[tuple[F, int, int, int]] = []
    overlapping: list[dict] = []
    least: tuple[F, int, int, int] | None = None
    pairs = 0
    for i in range(n):
        ai, bi = sa[i], sb[i]
        if ai is None or bi is None:
            continue
        for j in range(i + 1, n):
            aj, bj = sa[j], sb[j]
            if aj is None or bj is None:
                continue
            pairs += 1
            m, axis = A.pair_margin(ai, aj)
            ca = A.classify(m)
            cb, area = B.pair_class(bi, bj)
            if ca != cb:
                disagreements.append(
                    {"pair": [ids[i], ids[j]], "A": ca, "margin": frac_str(m), "B": cb}
                )
            classes[ca] += 1
            if least is None or m < least[0]:
                least = (m, i, j, axis)
            if m < NEAR:
                near.append((m, i, j, axis))
            if ca == "overlapping" or cb == "overlapping":
                overlapping.append(
                    {
                        "pair": [ids[i], ids[j]],
                        "margin_A": frac_str(m),
                        "margin_A_sci": sci(m, 6),
                        "area_B": str(area),
                        "area_B_sci": sci(F(int(area.numerator), int(area.denominator)), 6),
                    }
                )
    near.sort(key=lambda t: t[0])
    axis_names = ("first.u", "first.w", "second.u", "second.w")
    nearest_rows = []
    for m, i, j, axis in near[:nearest]:
        row = {
            "pair": [ids[i], ids[j]],
            "margin": frac_str(m),
            "margin_sci": sci(m, 12),
            "axis": axis_names[axis],
        }
        unit_pair = all(s.u[0] ** 2 + s.u[1] ** 2 == 1 for s in (sa[i], sa[j]))
        if m >= 0 and unit_pair:
            d2 = A.distance2(sa[i], sa[j])
            row["distance_equals_margin"] = d2 == m * m
            if d2 != m * m:
                row["distance2"] = frac_str(d2)
        nearest_rows.append(row)
    below = {name: sum(1 for t in near if t[0] < thr) for name, thr in THRESHOLDS}
    off_axis = sum(1 for a in sa if a is not None and a.u[0] != 0 and a.u[1] != 0)
    senses = {
        "counterclockwise": sum(1 for a in sa if a is not None and a.orient == 1),
        "clockwise": sum(1 for a in sa if a is not None and a.orient == -1),
    }
    accept = (
        len(set(ids)) == n
        and not shape_refusals
        and not not_squares
        and not outside
        and not overlapping
        and not disagreements
    )
    return {
        "verdict": "ACCEPT" if accept else "REFUSE",
        "n": n,
        "distinct_ids": len(set(ids)) == n,
        "side": frac_str(side),
        "unit_squares_both_methods": n - len(shape_refusals),
        "shape_refusals": shape_refusals,
        "not_squares": not_squares,
        "senses_A": senses,
        "off_axis_squares": off_axis,
        "walls": {
            "squares_inside_both_methods": n - len(outside) - len(not_squares),
            "outside": outside,
            "contacts_by_wall": contacts,
            "least_clearance": frac_str(least_wall[0]) if least_wall else None,
            "least_clearance_sci": sci(least_wall[0]) if least_wall else None,
            "least_clearance_at": [least_wall[1], least_wall[2]] if least_wall else None,
            "least_positive_clearance": frac_str(least_positive[0]) if least_positive else None,
            "least_positive_clearance_sci": sci(least_positive[0]) if least_positive else None,
            "least_positive_clearance_at": (
                [least_positive[1], least_positive[2]] if least_positive else None
            ),
            "corners_on_wall_lines_B": corners_on_walls_b,
        },
        "pairs": {
            "decided_by_both": pairs,
            "classes": classes,
            "overlapping": overlapping,
            "least_margin": frac_str(least[0]) if least else None,
            "least_margin_sci": sci(least[0]) if least else None,
            "least_margin_pair": [ids[least[1]], ids[least[2]]] if least else None,
            "pairs_below": below,
            "nearest": nearest_rows,
        },
        "disagreements_A_B": disagreements,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__)
        return 2
    cert, twin, n_text, out = argv[1], argv[2], argv[3], argv[4]
    clock = Clock()
    receipt: dict = {
        "program": "l64_check.py",
        "programs_sha256": program_digests([HERE / f for f in CHECKER]),
        "environment": environment(),
        "certificate": cert,
        "twin": twin,
        "expected_n": int(n_text),
    }
    try:
        w = read_witness(cert, expected_n=int(n_text))
        t = read_twin_json(twin, w)
    except ReadError as exc:
        receipt.update({"verdict": "REFUSE", "read_error": str(exc), "clock": clock.report()})
        write_receipt(out, receipt)
        print(f"{cert}: REFUSE (read: {exc})")
        return 1
    side = F(*w["side"])
    receipt["read"] = {
        "sha256": w["sha256"],
        "bytes": w["bytes"],
        "lines": w["lines"],
        "final_newline": w["final_newline"],
        "witness_id": w["id"],
        "n": w["n"],
        "ids_one_to_n_in_order": w["ids_in_order"],
        "scalars": w["scalars"],
        "scalars_in_lowest_terms": w["scalars_in_lowest_terms"],
        "side_as_written": w["side_text"],
        "side_lowest_terms": frac_str(side),
        "side_floor_40": fixed(side, 40, "floor"),
        "twin": t,
        "claim_block": w["claim"],
        "certificate_block": w["certificate"],
    }
    result = decide(w["squares"], side)
    receipt["decision"] = result
    receipt["verdict"] = result["verdict"]
    receipt["clock"] = clock.report()
    write_receipt(out, receipt)
    p = result["pairs"]
    print(
        f"{cert}: {result['verdict']}; pairs {p['decided_by_both']} {p['classes']}; "
        f"least margin {p['least_margin_sci']}; walls {result['walls']['contacts_by_wall']}; "
        f"cpu {receipt['clock']['cpu_seconds']} s"
    )
    return 0 if result["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
