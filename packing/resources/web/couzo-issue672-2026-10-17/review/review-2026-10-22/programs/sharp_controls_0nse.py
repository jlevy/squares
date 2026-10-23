"""Sharp controls for T-226, T-227 and T-228: mutants at the scale of each margin.

The packets' receipts hold two gross controls per count (a duplicated square, gap -1; a
square moved outside). This program builds mutants of each certificate at exact contact
and 1e-30 past it, as certificate text, and decides each one with:

* this review's checker (`review_0nse_check.decide_text`, both of its routes), and
* the repository's two maintained routes, called as the packets' replay calls them
  (`evand_arrangement_reports.run_case`): the text through
  `upper_bound_reports.parse_certificate(..., "evand-cert")`, then
  `evand_exact_certificates.exact_verify(evand_arrangement_reports.to_witness(cert))`
  and `check_rational_witness_independent.check_squares(corner_squares(cert), side)`.

Mutants (the contract is the closed box with disjoint interiors, so contact is accepted;
1e-30 past contact must be refused, at a margin of exactly -1e-30):

  F0 / F1  side lowered by the least top-or-right clearance / and by 1e-30 more
  N0 / N1  every square translated toward the near wall (x >= 0 or y >= 0) with the
           least clearance by that clearance / and by 1e-30 more
  P0 / P1  one square of the least-gap pair moved along the pair's best separating axis
           toward the other by exactly the gap / by the gap + 1e-30 (the mover is the one
           whose move overlaps only the pair, where one does)
  R1       one row dropped under the same header: every reader must refuse
  R2       one coordinate written as a 25-place decimal: this review's reader refuses
           it; the maintained reader's verdict is reported, not expected

It also runs the kernel's `run_sharp` (both `SHARP_CONTROLS`, at contact and past it).
The maintained routes' verdicts are theirs; this program adds the mutants and the
expectations.

Run from packing/ with the project interpreter, PYTHONDONTWRITEBYTECODE=1:
  python PROGRAMS/sharp_controls_0nse.py OUT_DIR LABEL=N=PATH [LABEL=N=PATH ...]
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("review_0nse_check", HERE / "review_0nse_check.py")
mine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mine)

sys.path.insert(0, str(Path.cwd()))
from devtools import evand_arrangement_reports as kernel  # noqa: E402
from devtools import evand_exact_certificates as legacy  # noqa: E402
from devtools import upper_bound_reports as reports  # noqa: E402

EPS = Fraction(1, 10**30)


def lit(v: Fraction) -> str:
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)


def frac(pair: tuple[int, int]) -> Fraction:
    return Fraction(pair[0], pair[1])


def maintained(text: str, n: int) -> dict:
    try:
        cert = reports.parse_certificate(text.encode("ascii"), n, "evand-cert")
    except Exception as error:  # noqa: BLE001
        return {"adapter": f"refused: {type(error).__name__}: {error}"[:300]}
    out: dict = {"adapter": "read"}
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
            "cpu_s": round(cpu, 2),
        }
    return out


def review(text: str) -> dict:
    r = mine.decide_text(text)
    if "format_error" in r:
        return {"reader": f"refused: {r['format_error']}"}
    z, c = r["route_Z"], r["route_C"]
    return {
        "accepted": r["accepted"],
        "routes_agree": r["routes_agree"],
        "Z": {
            "accepted": z["accepted"],
            "wall": z["least_wall_clearance"],
            "gap": z["least_gap"],
            "gap_pair": z["least_gap_pair"],
            "overlaps": z["overlapping_pairs"],
            "touching": z["touching_pairs"],
            "failures": z["failures"][:3],
        },
        "C": {
            "accepted": c["accepted"],
            "wall": c["least_wall_clearance"],
            "positive_area_pairs": c["positive_area_pairs"],
            "touching": c["touching_pairs"],
            "failures": c["failures"][:3],
        },
    }


def outcome_ok(expect: str, rv: dict, mt: dict, margin: str, value: Fraction | None) -> bool:
    if expect == "refuse-read":
        return rv.get("reader", "").startswith("refused") and mt["adapter"].startswith("refused")
    if expect == "reader-difference":
        return rv.get("reader", "").startswith("refused")
    want = expect == "accept"
    ok = rv.get("accepted") is want and rv.get("routes_agree") is True and mt.get("adapter") == "read"
    ok = ok and rv["Z"]["accepted"] is want and rv["C"]["accepted"] is want
    ok = ok and mt["exact_verify"]["passed"] is want and mt["independent"]["passed"] is want
    if value is not None:
        key = "wall" if margin == "wall" else "gap"
        ok = ok and Fraction(rv["Z"][key]) == value
        if margin == "wall":
            ok = ok and Fraction(rv["C"]["wall"]) == value
        ok = ok and Fraction(mt["exact_verify"][key]) == value
        ok = ok and Fraction(mt["independent"][key]) == value
    if margin == "gap" and not want:
        ok = ok and rv["C"]["positive_area_pairs"] >= 1
    return ok


def split(text: str) -> tuple[list[str], list[str], list[list[str]]]:
    lines = text.split("\n")
    if lines[-1] == "":
        lines.pop()
    k = 0
    while lines[k].startswith("#"):
        k += 1
    return lines[:k], lines[k].split(" "), [row.split(" ") for row in lines[k + 1 :]]


def assemble(comments: list[str], header: list[str], rows: list[list[str]]) -> str:
    return "\n".join([*comments, " ".join(header), *(" ".join(r) for r in rows)]) + "\n"


def control_one(label: str, n: int, path: Path) -> tuple[dict, bool]:
    text = path.read_bytes().decode("ascii")
    comments, header, rows = split(text)
    _, side_pair, parsed, _ = mine.read(text)
    route = mine.RouteZ(n, side_pair, parsed)
    names = ("x>=0", "y>=0", "x<=S", "y<=S")
    least: dict[str, tuple[Fraction, int]] = {}
    for index in range(n):
        for wall, value in zip(names, route.wall_clearances(index)):
            value = frac(value)
            if wall not in least or value < least[wall][0]:
                least[wall] = (value, index)
    far = min(("x<=S", "y<=S"), key=lambda w: least[w][0])
    near = min(("x>=0", "y>=0"), key=lambda w: least[w][0])
    base = route.run()
    i, j, _ = base["least_gap_pair"]
    gap_pair, axis, sign = route.pair_gap(i, j)
    gap = frac(gap_pair)
    owner = i if axis < 2 else j
    (ux, uy) = (frac(c) for c in route.axis_vector(owner, axis % 2))
    record = {
        "label": label,
        "n": n,
        "side": header[1],
        "least_wall_clearances": {w: [lit(v), f"{float(v):.6e}", k] for w, (v, k) in least.items()},
        "far_wall": [far, lit(least[far][0]), least[far][1]],
        "near_wall": [near, lit(least[near][0]), least[near][1]],
        "least_pair": [i, j],
        "least_gap": [lit(gap), f"{float(gap):.15e}"],
        "best_axis": {"owner": owner, "axis": "u" if axis % 2 == 0 else "v", "vector": [lit(ux), lit(uy)], "projection_sign": sign},
        "mutants": {},
    }
    all_ok = True

    def run(name: str, mutant: str, expect: str, margin: str, value: Fraction | None) -> None:
        nonlocal all_ok
        rv = review(mutant)
        mt = maintained(mutant, n)
        ok = outcome_ok(expect, rv, mt, margin, value)
        all_ok &= ok
        record["mutants"][name] = {
            "expect": expect,
            "margin_expected": None if value is None else lit(value),
            "review": rv,
            "maintained": mt,
            "as_expected": ok,
        }
        print(label, name, "OK" if ok else "UNEXPECTED", json.dumps({"review": rv, "maintained": mt})[:700], flush=True)

    drop = least[far][0]
    run("F0_side_lowered_by_far_clearance", assemble(comments, [header[0], lit(Fraction(header[1]) - drop)], rows), "accept", "wall", Fraction(0))
    run("F1_side_lowered_by_far_clearance_plus_1e-30", assemble(comments, [header[0], lit(Fraction(header[1]) - drop - EPS)], rows), "refuse", "wall", -EPS)
    coord = 0 if near == "x>=0" else 1
    for name, step, expect, value in (
        ("N0_moved_to_near_wall_by_clearance", least[near][0], "accept", Fraction(0)),
        ("N1_moved_to_near_wall_by_clearance_plus_1e-30", least[near][0] + EPS, "refuse", -EPS),
    ):
        moved = [list(r) for r in rows]
        for r in moved:
            r[coord] = lit(Fraction(r[coord]) - step)
        run(name, assemble(comments, header, moved), expect, "wall", value)

    # choose the mover: j toward i (against the projection sign), or i toward j
    candidates = ((j, -sign), (i, sign))
    chosen = None
    probes = {}
    for mover, direction in candidates:
        trial = [list(r) for r in rows]
        step = gap + EPS
        trial[mover][0] = lit(Fraction(rows[mover][0]) + direction * step * ux)
        trial[mover][1] = lit(Fraction(rows[mover][1]) + direction * step * uy)
        _, s2, p2, _ = mine.read(assemble(comments, header, trial))
        r2 = mine.RouteZ(n, s2, p2)
        overlapping = []
        for other in range(n):
            if other == mover:
                continue
            a, b = min(other, mover), max(other, mover)
            if r2.pair_gap(a, b)[0][0] < 0:
                overlapping.append([a, b])
        probes[str(mover)] = overlapping
        if overlapping == [[min(i, j), max(i, j)]] and chosen is None:
            chosen = (mover, direction)
    if chosen is None:
        chosen = candidates[0]
        record["pair_mover_note"] = "no single move overlaps only the pair; the listed overlaps of each candidate mover are in probes"
    record["pair_mover"] = chosen[0]
    record["pair_mover_probes_at_gap_plus_1e-30"] = probes
    mover, direction = chosen
    for name, step, expect, value in (
        ("P0_pair_closed_by_gap", gap, "accept", Fraction(0)),
        ("P1_pair_closed_by_gap_plus_1e-30", gap + EPS, "refuse", -EPS),
    ):
        moved = [list(r) for r in rows]
        moved[mover][0] = lit(Fraction(rows[mover][0]) + direction * step * ux)
        moved[mover][1] = lit(Fraction(rows[mover][1]) + direction * step * uy)
        run(name, assemble(comments, header, moved), expect, "gap", value)

    run("R1_one_row_dropped", assemble(comments, header, rows[:-1]), "refuse-read", "", None)
    decimal_rows = [list(r) for r in rows]
    decimal_rows[0][0] = f"{float(Fraction(rows[0][0])):.25f}"
    run("R2_decimal_literal", assemble(comments, header, decimal_rows), "reader-difference", "", None)

    cert = reports.parse_certificate(text.encode("ascii"), n, "evand-cert")
    sharp = {}
    for control in kernel.SHARP_CONTROLS:
        for past in (False, True):
            key = f"{control}{'' if past else ' (contact)'}"
            try:
                verdicts = kernel.run_sharp(cert, control, past=past)
                sharp[key] = {route: {"passed": v["passed"], "wall": lit(v["wall"]), "gap": lit(v["gap"])} for route, v in verdicts.items()}
                want = not past
                margin = "wall" if control.startswith("side") else "gap"
                expected = Fraction(0) if not past else -kernel.SHARP_EPSILON
                ok = all(v["passed"] is want and v[margin] == expected for v in verdicts.values())
            except Exception as error:  # noqa: BLE001
                sharp[key] = f"error: {type(error).__name__}: {error}"[:300]
                ok = False
            sharp[key + " as expected"] = ok
            all_ok &= ok
    record["kernel_run_sharp"] = sharp
    record["kernel_sharp_epsilon"] = lit(kernel.SHARP_EPSILON)
    print(label, "kernel run_sharp", json.dumps(sharp)[:900], flush=True)
    return record, all_ok


def main(argv: list[str]) -> int:
    out_dir = Path(argv[1])
    every = True
    for spec in argv[2:]:
        label, n, path = spec.split("=", 2)
        record, ok = control_one(label, int(n), Path(path))
        every &= ok
        name = label.replace("@", "-n").replace("/", "-")
        (out_dir / f"out-controls-{name}.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print("controls", "all as expected" if every else "SOME UNEXPECTED")
    return 0 if every else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
