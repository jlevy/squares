"""Sharp controls: take each candidate to exact contact, then 1e-40 past it, on both routes.

Usage: python3.14 controls.py INPUTS_DIR OUT_DIR

For each subject, every control is decided by route A and route B, and the expectation
is stated beside it ('pass' at contact, 'fail' past it). The controls:

1. box at the exact extent E (largest corner coordinate): pass; at E - 1e-40: fail;
2. the square nearest a near wall moved onto it: pass; 1e-40 past it: fail;
3. the least-slack pair closed along its separating normal by its slack: pass (touching);
   by its slack + 1e-40: fail;
4. one square of that pair turned by t = tan(theta/2) = 1e-15 (an exact rotation): fail;
5. one basis scaled by 1 + 1e-40 (not a unit square): fail;
6. a square duplicated: fail;
7. (293 only) the strip's column moved left onto the 260 block's right extent: pass;
   1e-40 past it: fail.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

import qio
import route_area
import route_sat

EPS = Fraction(1, 10**40)


def decide(side: Fraction, sq: list[qio.Square]) -> tuple[bool, bool]:
    return bool(route_sat.check(side, sq)["accepted"]), bool(route_area.check(side, sq)["accepted"])


def controls(label: str, side: Fraction, sq: list[qio.Square], strip_from: int | None = None) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def run(name: str, s: Fraction, q: list[qio.Square], expect: str) -> None:
        a, b = decide(s, q)
        got_a, got_b = ("pass" if a else "fail"), ("pass" if b else "fail")
        ok = got_a == expect and got_b == expect
        rows.append({"subject": label, "control": name, "expect": expect, "route_A": got_a, "route_B": got_b, "as_expected": ok})
        print(f"{label:22s} {name:58s} expect {expect}: A {got_a}, B {got_b} {'ok' if ok else 'UNEXPECTED'}", flush=True)

    base = route_sat.check(side, sq)
    ext = base["extent_hi"]
    assert isinstance(ext, Fraction)
    run("positive at the declared side", side, sq, "pass")
    run("box at the exact extent E", ext, sq, "pass")
    run("box at E - 1e-40", ext - EPS, sq, "fail")

    # near wall: least left or bottom clearance
    best = None
    for i, s in enumerate(sq):
        h = route_sat.half_extent(s)
        for axis, v in ((0, s[0] - h), (1, s[1] - h)):
            if best is None or v < best[0]:
                best = (v, i, axis)
    assert best is not None
    v, i, axis = best
    for extra, expect in ((Fraction(0), "pass"), (EPS, "fail")):
        q = list(sq)
        cx, cy, a, b = q[i]
        q[i] = (cx - v - extra, cy, a, b) if axis == 0 else (cx, cy - v - extra, a, b)
        run(f"square {i + 1} onto the {'left' if axis == 0 else 'bottom'} wall (+{extra})", side, q, expect)

    # least-slack pair closed along its separating normal
    slack, i, j, k = base["least_pair_slack"]  # type: ignore[misc]
    ux, uy = route_sat.axis_of(sq[i], sq[j], k)
    proj = ux * (sq[j][0] - sq[i][0]) + uy * (sq[j][1] - sq[i][1])
    sign = 1 if proj > 0 else -1
    for extra, expect in ((Fraction(0), "pass"), (EPS, "fail")):
        q = list(sq)
        cx, cy, a, b = q[j]
        step = (slack + extra) * sign
        q[j] = (cx - ux * step, cy - uy * step, a, b)
        run(f"pair {i + 1},{j + 1} closed by slack {float(slack):.1e} (+{extra})", side, q, expect)

    # turn square j by an exact small rotation
    c1, s1 = qio.basis_from_t(Fraction(1, 10**15))
    q = list(sq)
    cx, cy, a, b = q[j]
    q[j] = (cx, cy, a * c1 - b * s1, a * s1 + b * c1)
    run(f"square {j + 1} turned by t = 1e-15", side, q, "fail")

    q = list(sq)
    cx, cy, a, b = q[i]
    q[i] = (cx, cy, a * (1 + EPS), b * (1 + EPS))
    run(f"square {i + 1} basis scaled by 1 + 1e-40", side, q, "fail")

    run("square 1 duplicated", side, list(sq) + [sq[0]], "fail")

    if strip_from is not None:
        # the column is the strip squares whose centre is at x = S + 1/2, S = side - 1
        block, strip = sq[:strip_from], sq[strip_from:]
        col_centre = side - Fraction(1, 2)
        col_x = side - 1
        right = max(x for blk in block for x, _ in route_area.corners(blk))
        ys = [y for blk in block for x, y in route_area.corners(blk) if x == right]
        facing = [y for y in ys if any(c[1] - Fraction(1, 2) < y < c[1] + Fraction(1, 2) for c in strip if c[0] == col_centre)]
        gap = col_x - right
        print(
            f"{label:22s} block right extent {float(right):.18f} at y {[float(y) for y in ys]};"
            f" column at x = S; gap {float(gap):.6e}; corner faces a column square: {bool(facing)}"
        )
        if facing:
            for extra, expect in ((Fraction(0), "pass"), (EPS, "fail")):
                moved = [(c[0] - gap - extra, c[1], c[2], c[3]) if c[0] == col_centre else c for c in strip]
                run(f"strip column moved onto the block's corner (+{extra})", side, block + moved, expect)
    return rows


def main() -> None:
    inp, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    _, s260, sq260, _ = qio.read_tcert(inp / "s260_1028.cert")
    subjects: list[tuple[str, Fraction, list[qio.Square], int | None]] = []
    for n in (130, 307):
        _, side, sq, _ = qio.read_view(inp / f"n{n}-view-solved.yaml")
        subjects.append((f"cand{n} (view)", side, sq, None))
        _, side, sq, _ = qio.read_tcert(inp / f"n{n}-solve-witness.cert")
        subjects.append((f"cand{n} (solve cert)", side, sq, None))
    for variant in ("16+16+1", "17top+16"):
        subjects.append((f"cand293 ({variant})", s260 + 1, sq260 + qio.l_strip(s260, variant), 260))
    rows: list[dict[str, object]] = []
    for label, side, sq, strip_from in subjects:
        rows += controls(label, side, sq, strip_from)
    bad = [r for r in rows if not r["as_expected"]]
    print(f"{len(rows)} controls, {len(rows) - len(bad)} as expected, {len(bad)} not")
    (outdir / "controls.json").write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    main()
