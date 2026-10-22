"""Sharp controls for T-225: mutants of each certificate at the scale of its margins.

The packet's receipt holds two gross controls per count (a duplicated square, gap -1; a
square moved S + 2 outside). Every margin of these certificates is about 1e-20, so this
program builds mutants on that edge, as certificate text, and decides each one with:

* this review's checker (`review_t225_check.decide`, both of its routes), and
* the repository's two maintained routes, reached as the packet's replay reaches them:
  the text through `upper_bound_reports.parse_certificate(..., "evand-cert")`, then
  `evand_exact_certificates.exact_verify(evand_arrangement_reports.to_witness(cert))`
  (sqpack's exact witness verifier) and
  `check_rational_witness_independent.check_squares(corner_squares(cert), side)`.

The mutants (contact must be accepted, since the contract is the closed box with disjoint
interiors; 1e-30 past contact must be refused, at exactly -1e-30):

  F0 / F1  side lowered by the least top-or-right clearance / and by 1e-30 more
  N0 / N1  every square translated toward the least-clearance near wall (x >= 0 or
           y >= 0) by that clearance / and by 1e-30 more: the wall moved inward
  P0 / P1  the least-gap pair closed along its best separating axis by exactly its gap /
           by its gap + 1e-30, moving one square of the pair (one whose move closes no
           other pair, where there is one; otherwise the second, and every pair it closes
           is listed)
  R1       one row dropped (n - 1 rows under header n): both readers must refuse
  R2       a coordinate written as a 25-place decimal: this review's reader refuses it;
           the maintained reader admits decimal literals by design and reads them
           exactly, so its verdict is the geometry's and is reported, not expected

It also runs the kernel's own `run_sharp` (side-lowered-past-wall-contact and
tightest-pair-closed-past-contact, at contact and past it), whose construction is the
repository's, for comparison.

Run with the worktree's interpreter from any directory, PYTHONDONTWRITEBYTECODE=1:
  python sharp_controls_t225.py CERT_DIR OUT_DIR N [N ...]
"""

from __future__ import annotations

import gzip
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_t225_check as mine  # noqa: E402

from devtools import evand_arrangement_reports as kernel  # noqa: E402
from devtools import evand_exact_certificates as legacy  # noqa: E402
from devtools import upper_bound_reports as reports  # noqa: E402

EPS = Fraction(1, 10**30)


def lit(v: Fraction) -> str:
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)


def maintained(text: str, n: int) -> dict:
    """Both maintained routes on the mutant text, through the packet's adapter."""
    try:
        cert = reports.parse_certificate(text.encode("ascii"), n, "evand-cert")
    except Exception as error:  # noqa: BLE001
        return {"adapter": f"refused: {type(error).__name__}: {error}"[:300]}
    out = {"adapter": "read"}
    started = time.process_time()
    first, _ = legacy.exact_verify(kernel.to_witness(cert))
    t1 = time.process_time() - started
    started = time.process_time()
    second = legacy.independent.check_squares(legacy.corner_squares(cert), cert.side)
    t2 = time.process_time() - started
    for name, verdict, cpu in (("exact_verify", first, t1), ("independent", second, t2)):
        out[name] = {
            "passed": verdict["verification_passed"],
            "wall": str(verdict["minimum_containment_clearance"]),
            "gap": str(verdict["minimum_best_pair_gap"]),
            "failures": [str(f)[:160] for f in verdict["failures"][:3]],
            "cpu_s": round(cpu, 1),
        }
    return out


def review(text: str, n: int) -> dict:
    try:
        r = mine.decide(text, n, clip=True)
    except mine.Refused as error:
        return {"reader": f"refused: {error}"}
    return {
        "passed": r["passed"],
        "integers": [r["route_integers"]["passed"], r["route_integers"]["least_wall_clearance"]["exact"], r["route_integers"]["least_wall_at"], r["route_integers"]["least_pair_gap"]["exact"], r["route_integers"]["least_pair"], r["route_integers"]["overlapping_count"], r["route_integers"]["contacts"]],
        "fraction": [r["route_fraction"]["passed"], r["route_fraction"]["least_wall_clearance"]["exact"], r["route_fraction"]["least_pair_gap"]["exact"], r["route_fraction"]["overlapping_pairs"], r["route_fraction"]["clip_positive_pairs"]],
        "routes_agree": r["routes_agree"],
    }


def rows_of(text: str) -> tuple[list[str], int, list[list[str]]]:
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    k = 0
    while lines[k].startswith("#"):
        k += 1
    return lines[:k], k, [row.split(" ") for row in lines[k + 1 :]]


def assemble(comments: list[str], n: int, side: str, rows: list[list[str]]) -> str:
    return "\n".join([*comments, f"{n} {side}", *(" ".join(r) for r in rows)]) + "\n"


def geometry(rows: list[list[str]]) -> list[tuple]:
    out = []
    for x, y, t in rows:
        x, y, t = Fraction(x), Fraction(y), Fraction(t)
        c = (1 - t * t) / (1 + t * t)
        s = 2 * t / (1 + t * t)
        out.append((x, y, c, s, (abs(c) + abs(s)) / 2))
    return out


def best_axis(p: tuple, q: tuple) -> tuple[Fraction, tuple, Fraction]:
    x, y, c, s, _ = p
    X, Y, C, T, _ = q
    dx, dy = X - x, Y - y
    best = None
    for u, v in ((c, s), (-s, c), (C, T), (-T, C)):
        hp = (abs(u * c + v * s) + abs(-u * s + v * c)) / 2
        hq = (abs(u * C + v * T) + abs(-u * T + v * C)) / 2
        proj = u * dx + v * dy
        gap = abs(proj) - hp - hq
        if best is None or gap > best[0]:
            best = (gap, (u, v), proj)
    return best


def outcome_ok(expect: str, rv: dict, mt: dict, margin: str, value: Fraction | None) -> bool:
    """Every decider agrees with the expectation; margins exact where stated."""
    if expect == "refuse-read":
        return rv.get("reader", "").startswith("refused") and mt["adapter"].startswith("refused")
    if expect == "reader-difference":
        # this review's reader refuses a decimal; the maintained reader admits decimals by
        # design and reads them exactly, so its geometry verdict is reported, not expected
        return rv.get("reader", "").startswith("refused") and mt["adapter"] == "read"
    want = expect == "accept"
    ok = rv.get("passed") is want and mt.get("adapter") == "read"
    ok = ok and mt["exact_verify"]["passed"] is want and mt["independent"]["passed"] is want
    if value is not None:
        key = "wall" if margin == "wall" else "gap"
        mine_value = Fraction(rv["integers"][1] if margin == "wall" else rv["integers"][3])
        ok = ok and mine_value == value
        ok = ok and Fraction(mt["exact_verify"][key]) == value and Fraction(mt["independent"][key]) == value
    return ok


def main(argv: list[str]) -> int:
    folder, out_dir = Path(argv[1]), Path(argv[2])
    all_ok = True
    for n in map(int, argv[3:]):
        text = gzip.decompress((folder / f"n-{n:03d}.cert.gz").read_bytes()).decode("ascii")
        comments, _, rows = rows_of(text)
        header = text.split("\n")[len(comments)].split(" ")
        side = Fraction(header[1])
        squares = geometry(rows)
        # least clearance per wall
        walls = {"x>=0": None, "y>=0": None, "x<=S": None, "y<=S": None}
        for index, (x, y, _c, _s, h) in enumerate(squares):
            for wall, value in (("x>=0", x - h), ("y>=0", y - h), ("x<=S", side - h - x), ("y<=S", side - h - y)):
                if walls[wall] is None or value < walls[wall][0]:
                    walls[wall] = (value, index)
        far = min((walls["x<=S"], "x<=S"), (walls["y<=S"], "y<=S"), key=lambda w: w[0][0])
        near = min((walls["x>=0"], "x>=0"), (walls["y>=0"], "y>=0"), key=lambda w: w[0][0])
        base = mine.decide(text, n)
        i, j = base["route_integers"]["least_pair"]
        gap, (u, v), proj = best_axis(squares[i], squares[j])
        assert gap == Fraction(base["route_integers"]["least_pair_gap"]["exact"])
        record = {
            "n": n,
            "side": lit(side),
            "wall_clearances": {w: [lit(val[0]), f"{float(val[0]):.6e}", val[1]] for w, val in walls.items()},
            "far_wall": [far[1], lit(far[0][0]), far[0][1]],
            "near_wall": [near[1], lit(near[0][0]), near[0][1]],
            "least_pair": [i, j],
            "least_gap": [lit(gap), f"{float(gap):.15e}"],
            "best_axis": [lit(u), lit(v)],
            "mutants": {},
        }

        def run(label: str, mutant: str, expect: str, margin: str, value: Fraction | None) -> None:
            nonlocal all_ok
            rv = review(mutant, n)
            mt = maintained(mutant, n)
            ok = outcome_ok(expect, rv, mt, margin, value)
            all_ok &= ok
            record["mutants"][label] = {"expect": expect, "margin_expected": None if value is None else lit(value), "review": rv, "maintained": mt, "as_expected": ok}
            print(n, label, "OK" if ok else "UNEXPECTED", json.dumps({"review": rv, "maintained": mt})[:600], flush=True)

        # F0 / F1: the far wall
        drop = far[0][0]
        run("F0_side_lowered_by_far_clearance", assemble(comments, n, lit(side - drop), rows), "accept", "wall", Fraction(0))
        run("F1_side_lowered_by_far_clearance_plus_1e-30", assemble(comments, n, lit(side - drop - EPS), rows), "refuse", "wall", -EPS)
        # N0 / N1: the near wall moved inward, i.e. every square translated toward it
        axis = 0 if near[1] == "x>=0" else 1
        for label, step, expect, value in (
            ("N0_near_wall_moved_in_by_clearance", near[0][0], "accept", Fraction(0)),
            ("N1_near_wall_moved_in_by_clearance_plus_1e-30", near[0][0] + EPS, "refuse", -EPS),
        ):
            moved = [list(r) for r in rows]
            for r in moved:
                r[axis] = lit(Fraction(r[axis]) - step)
            run(label, assemble(comments, n, header[1], moved), expect, "wall", value)
        # P0 / P1: the least-gap pair closed along its best axis
        mover_choice = None
        for mover, other in ((j, i), (i, j)):
            # moving `mover` toward `other`: against the sign of axis . (mover - other)
            direction = (-1 if proj > 0 else 1) if mover == j else (1 if proj > 0 else -1)
            trial = [list(r) for r in rows]
            step = gap + EPS
            trial[mover][0] = lit(Fraction(rows[mover][0]) + direction * step * u)
            trial[mover][1] = lit(Fraction(rows[mover][1]) + direction * step * v)
            probe = mine.decide(assemble(comments, n, header[1], trial), n, clip=False)
            overl = probe["route_integers"]["overlapping_pairs"]
            if [tuple(p) for p in overl] == [(min(i, j), max(i, j))]:
                mover_choice = (mover, direction)
                break
        if mover_choice is None:
            # each square of the pair has a second neighbour at the same exact gap along the
            # same axis (an evenly spaced chain), so either move closes two pairs, each by
            # exactly the same amount; move the second square and record both overlaps
            mover_choice = (j, -1 if proj > 0 else 1)
            record["pair_mover_note"] = "no single move isolates the pair: the mover closes a second pair at the same exact gap"
        record["pair_mover"] = mover_choice[0]
        mover, direction = mover_choice
        for label, step, expect, value in (
            ("P0_pair_closed_by_gap", gap, "accept", Fraction(0)),
            ("P1_pair_closed_by_gap_plus_1e-30", gap + EPS, "refuse", -EPS),
        ):
            moved = [list(r) for r in rows]
            moved[mover][0] = lit(Fraction(rows[mover][0]) + direction * step * u)
            moved[mover][1] = lit(Fraction(rows[mover][1]) + direction * step * v)
            run(label, assemble(comments, n, header[1], moved), expect, "gap", value)
        # R1 / R2: the readers
        run("R1_one_row_dropped", assemble(comments, n, header[1], rows[:-1]), "refuse-read", "", None)
        decimal_rows = [list(r) for r in rows]
        decimal_rows[0][0] = f"{float(Fraction(rows[0][0])):.25f}"
        run("R2_decimal_literal", assemble(comments, n, header[1], decimal_rows), "reader-difference", "", None)
        # the kernel's own sharp controls, for comparison
        cert = reports.parse_certificate(text.encode("ascii"), n, "evand-cert")
        kernel_sharp = {}
        for control in kernel.SHARP_CONTROLS:
            for past in (False, True):
                try:
                    verdicts = kernel.run_sharp(cert, control, past=past)
                    kernel_sharp[f"{control}{'' if past else ' (contact)'}"] = {
                        route: {"passed": r["passed"], "wall": lit(r["wall"]), "gap": lit(r["gap"])} for route, r in verdicts.items()
                    }
                except Exception as error:  # noqa: BLE001
                    kernel_sharp[f"{control}{'' if past else ' (contact)'}"] = f"error: {type(error).__name__}: {error}"[:300]
        record["kernel_run_sharp"] = kernel_sharp
        print(n, "kernel run_sharp", json.dumps(kernel_sharp)[:800], flush=True)
        (out_dir / f"out-controls-n{n}.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print("controls", "all as expected" if all_ok else "SOME UNEXPECTED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
