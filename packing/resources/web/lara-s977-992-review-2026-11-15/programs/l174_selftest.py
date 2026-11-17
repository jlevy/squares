"""Lane L174 self-test: both methods and the reader against hand-derived cases.

Usage: ``python -I -B l174_selftest.py SCRATCH_DIR RECEIPT.json``

* Signs: method A's ``zsign`` and method B's ``qsign`` on every a + b sqrt 2 with
  |a|, |b| <= 60, and on the Pell near-misses p - q sqrt 2 and their negatives, against
  a 120-digit decimal evaluation.
* Pairs: unit squares at hand-placed centres whose class (apart, touching, overlapping)
  is derived by hand in the comments, including the corner-on-edge contact the
  construction relies on, each also moved 10^-9 either way.
* Walls and unit sides: hand-placed squares in a box.
* A miniature of the construction's shape, Goebel's (a, b) = (2, 3): side 3 + 3/sqrt 2,
  a 3 x 3 diamond and triangles of 3 cells, 21 squares; by hand 40 touching pairs
  (20 in the diamond, 3 in each triangle, 2 corner-on-edge contacts per corner),
  16 square-wall contacts, no overlap.
* The reader refuses three broken files.
"""

from __future__ import annotations

import decimal
import json
import sys
from fractions import Fraction
from pathlib import Path

# Run with -I, which leaves the script's own directory off sys.path: put it back, alone.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import l174_method_a as method_a
import l174_method_b as method_b
from gmpy2 import mpq
from l174_construct import Spec, build
from l174_reader import Construction, Square, read

F = Fraction
E = F(1, 10**9)
R2 = (F(0), F(1))  # sqrt 2
IR2 = (F(0), F(1, 2))  # 1/sqrt 2


def q(a: Fraction | int, b: Fraction | int = 0) -> tuple[Fraction, Fraction]:
    return (F(a), F(b))


def qa(x: tuple[Fraction, Fraction], y: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (x[0] + y[0], x[1] + y[1])


def con_of(squares: list[tuple[tuple, tuple, int, Fraction]], width: tuple) -> Construction:
    return Construction(
        name="selftest",
        container=width,
        squares=tuple(
            Square(sid=k, label=f"s{k}", family="t", cx=cx, cy=cy, angle=ang, size=size)
            for k, (cx, cy, ang, size) in enumerate(squares)
        ),
    )


def sign_cases() -> list[tuple[int, int]]:
    cases = [(a, b) for a in range(-60, 61) for b in range(-60, 61)]
    p, qq = 1, 1
    for _ in range(40):
        cases.extend([(p, -qq), (-p, qq), (2 * qq, -p), (-2 * qq, p)])
        p, qq = p + 2 * qq, p + qq
    return cases


def check_signs() -> dict[str, object]:
    decimal.getcontext().prec = 120
    root2 = decimal.Decimal(2).sqrt()
    bad = 0
    cases = sign_cases()
    for a, b in cases:
        ref_val = decimal.Decimal(a) + decimal.Decimal(b) * root2
        ref = (ref_val > 0) - (ref_val < 0)
        sa = method_a.zsign(a, b)
        sb = method_b.qsign((mpq(a), mpq(b)))
        if not (sa == sb == ref):
            bad += 1
    return {"cases": len(cases), "mismatches": bad}


def pair_cases() -> list[tuple[str, tuple, tuple, int]]:
    """(name, square i, square j, expected class); squares as (cx, cy, angle)."""
    o = (q(0), q(0), 0)
    od = (q(0), q(0), 45)
    out: list[tuple[str, tuple, tuple, int]] = []

    def trio(name: str, a: tuple, bx: tuple, by: tuple, ang: int, dx: tuple, dy: tuple) -> None:
        # exact placement touches; moving b by +e*(dx,dy) separates; by -e*(dx,dy) overlaps
        out.append((name, a, (bx, by, ang), 0))
        out.append((name + "+", a, (qa(bx, (dx[0] * E, dx[1] * E)), qa(by, (dy[0] * E, dy[1] * E)), ang), 1))
        out.append((name + "-", a, (qa(bx, (-dx[0] * E, -dx[1] * E)), qa(by, (-dy[0] * E, -dy[1] * E)), ang), -1))

    # upright squares sharing the edge x = 1/2
    trio("up-edge", o, q(1), q(0), 0, q(1), q(0))
    # upright squares meeting at the corner (1/2, 1/2); moving along the diagonal
    trio("up-corner", o, q(1), q(1), 0, q(1), q(1))
    # 45-degree squares meeting vertex to vertex at (1/sqrt 2, 0)
    trio("diag-vertex", od, R2, q(0), 45, q(1), q(0))
    # 45-degree squares sharing an edge on x + y = 1/sqrt 2
    trio("diag-edge", od, IR2, IR2, 45, q(1), q(1))
    # 45-degree square's left vertex on the middle of the upright square's right edge
    trio("mixed-vertex-edge", o, qa(q(F(1, 2)), IR2), q(0), 45, q(1), q(0))
    # 45-degree square's left vertex on the upright square's corner (1/2, 1/2)
    trio("mixed-vertex-corner", o, qa(q(F(1, 2)), IR2), q(F(1, 2)), 45, q(1), q(0))
    # upright square's corner (1/2, 1/2) on the 45-degree square's lower-left edge x + y = 1:
    # centre (c, c), c = 1/2 + sqrt 2/4 (the construction's contact)
    c = q(F(1, 2), F(1, 4))
    trio("corner-on-diag-edge", o, c, c, 45, q(1), q(1))
    out.append(("identical", o, o, -1))
    out.append(("identical-diag", od, od, -1))
    out.append(("far", o, (q(5), q(-7), 45), 1))
    # a 45-degree square inside the upright one's bounding projections on e1 and e2 but
    # cut off on e3: centre (1/2 + 1/sqrt 2 - 0, ...) handled above; here a pair that only
    # e3 separates: upright at 0, diagonal at (1/2 + 1/(2 sqrt2) + e, same)
    out.append(("e3-only", o, (qa(c, q(E)), qa(c, q(E)), 45), 1))
    return out


def check_pairs() -> dict[str, object]:
    width = q(100)
    failures: list[str] = []
    cases = pair_cases()
    for name, si, sj, expected in cases:
        con = con_of([(si[0], si[1], si[2], F(1)), (sj[0], sj[1], sj[2], F(1))], width)
        pa = method_a.Prepared(con)
        pb = method_b.Prepared(con)
        ca = method_a.pair_class(pa, 0, 1)
        cb, _ = method_b.pair_class(pb, 0, 1)
        ca2 = method_a.pair_class(pa, 1, 0)
        cb2, _ = method_b.pair_class(pb, 1, 0)
        if not (ca == cb == ca2 == cb2 == expected):
            failures.append(f"{name}: A={ca}/{ca2} B={cb}/{cb2} expected {expected}")
    return {"cases": len(cases), "failures": failures}


def check_walls() -> dict[str, object]:
    w = q(3)
    cases = [
        # (cx, cy, angle, size, expected (left, bottom, right, top), expected unit)
        (q(F(1, 2)), q(F(1, 2)), 0, F(1), (0, 0, 1, 1), True),
        (q(F(1, 2) - E), q(F(1, 2)), 0, F(1), (-1, 0, 1, 1), True),
        (q(F(5, 2)), q(F(5, 2)), 0, F(1), (1, 1, 0, 0), True),
        (q(F(5, 2) + E), q(F(3, 2)), 0, F(1), (1, 1, -1, 1), True),
        (IR2, q(F(3, 2)), 45, F(1), (0, 1, 1, 1), True),
        (qa(IR2, q(-E)), q(F(3, 2)), 45, F(1), (-1, 1, 1, 1), True),
        (q(F(3, 2)), qa(q(3), (F(0), F(-1, 2))), 45, F(1), (1, 1, 1, 0), True),
        (q(F(3, 2)), q(F(3, 2)), 0, 1 + E, (1, 1, 1, 1), False),
        (q(F(3, 2)), q(F(3, 2)), 45, 1 - E, (1, 1, 1, 1), False),
    ]
    con = con_of([(cx, cy, ang, size) for cx, cy, ang, size, _, _ in cases], w)
    pa = method_a.Prepared(con)
    pb = method_b.Prepared(con)
    failures: list[str] = []
    for k, (_, _, _, _, expected, unit) in enumerate(cases):
        wa = method_a.wall_classes(pa, k)
        wb, kept = method_b.wall_classes(pb, k)
        ua = pa.unit[k]
        ub = method_b.unit_square(pb.polys[k])
        inside_expected = min(expected) >= 0
        if not (wa == wb == expected and ua == ub == unit and kept == inside_expected):
            failures.append(f"case {k}: A={wa} B={wb} kept={kept} unit A={ua} B={ub}")
    return {"cases": len(cases), "failures": failures}


def check_miniature() -> dict[str, object]:
    spec = Spec("mini", "Goebel (2, 3)", side=(F(3), F(3, 2)), diamond_k=3, widths=(2, 1))
    data = build(spec)
    path_text = json.dumps(data)
    con_json = json.loads(path_text)
    squares = [
        Square(
            sid=r["id"],
            label=r["label"],
            family=r["family"],
            cx=(F(r["cx"][0]), F(r["cx"][1])),
            cy=(F(r["cy"][0]), F(r["cy"][1])),
            angle=r["angle"],
            size=F(r["size"]),
        )
        for r in con_json["squares"]
    ]
    con = Construction("mini", (F(3), F(3, 2)), tuple(squares))
    ra = method_a.decide(con)
    rb = method_b.decide(con)
    got = {
        "n": ra["n"],
        "A": [ra["touching"], ra["overlapping"]],
        "B": [rb["touching"], rb["overlapping"]],
        "walls_touching": sum(1 for w in ra["walls"] for c in w if c == 0),  # pyright: ignore[reportGeneralTypeIssues]
        "agree": ra["pair_class_sha256"] == rb["pair_class_sha256"] and ra["walls"] == rb["walls"],
    }
    ok = (
        got["n"] == 21
        and got["A"] == [40, 0]
        and got["B"] == [40, 0]
        and got["walls_touching"] == 16
        and got["agree"]
    )
    return {"got": got, "as_derived": ok}


def check_reader(scratch: Path) -> dict[str, object]:
    scratch.mkdir(parents=True, exist_ok=True)
    good = {
        "name": "r",
        "container": ["3", "0"],
        "n": 1,
        "squares": [
            {"id": 0, "label": "a", "family": "t", "cx": ["1/2", "0"], "cy": ["1/2", "0"], "angle": 0, "size": "1"}
        ],
    }
    broken = {
        "angle-30": {**good, "squares": [{**good["squares"][0], "angle": 30}]},
        "non-canonical": {**good, "squares": [{**good["squares"][0], "cx": ["2/4", "0"]}]},
        "count": {**good, "n": 2},
    }
    results: dict[str, str] = {}
    path = scratch / "reader-good.json"
    path.write_text(json.dumps(good), encoding="utf-8")
    read(path)
    results["good"] = "accepted"
    for name, data in broken.items():
        path = scratch / f"reader-{name}.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        try:
            read(path)
            results[name] = "accepted"
        except (ValueError, TypeError):
            results[name] = "refused"
    ok = results == {"good": "accepted", "angle-30": "refused", "non-canonical": "refused", "count": "refused"}
    return {"results": results, "as_expected": ok}


def main(argv: list[str]) -> int:
    receipt = {
        "signs": check_signs(),
        "pairs": check_pairs(),
        "walls": check_walls(),
        "miniature": check_miniature(),
        "reader": check_reader(Path(argv[1])),
    }
    passed = (
        receipt["signs"]["mismatches"] == 0
        and not receipt["pairs"]["failures"]
        and not receipt["walls"]["failures"]
        and receipt["miniature"]["as_derived"]
        and receipt["reader"]["as_expected"]
    )
    receipt["passed"] = passed
    Path(argv[2]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=1))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
