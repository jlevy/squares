"""Sharp controls for T-224's replay (PR #708): mutants at the scale of the margins.

The packet's two controls are gross (a duplicated square, gap -1; a square moved outside
by about 18). These probe the same two maintained routes, through the `evand-cert`
adapter, at the scale where the certificate's least margins live: the side lowered by
exactly the least wall clearance (contact, must pass) and by a further 1e-30 (must
fail); the least-gap pair closed by exactly its gap along the separating axis (contact,
must pass) and by a further 1e-30 (must fail); and two files the adapter must refuse (a
decimal literal; 269 rows). The review checker's clipping area is computed on each
moved pair as a third opinion.

Run from a worktree's packing/ with its venv:
  python -I sharp_controls_708.py REVIEW_DIR CERT N
It writes REVIEW_DIR/out-controls-nN.json.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from devtools import evand_arrangement_reports as kernel  # noqa: E402
from devtools import evand_exact_certificates as legacy  # noqa: E402
from devtools import upper_bound_reports as reports  # noqa: E402

EPS = Fraction(1, 10**30)


def routes(cert: legacy.Certificate) -> dict:
    started = time.process_time()
    first, _ = legacy.exact_verify(kernel.to_witness(cert))
    t1 = time.process_time() - started
    started = time.process_time()
    second = legacy.independent.check_squares(legacy.corner_squares(cert), cert.side)
    t2 = time.process_time() - started
    return {
        "exact_verify": {
            "passed": first["verification_passed"],
            "wall": str(first["minimum_containment_clearance"]),
            "gap": f"{float(Fraction(first['minimum_best_pair_gap'])):.6e}",
            "failures": [str(f)[:100] for f in first["failures"][:2]],
            "cpu": round(t1, 1),
        },
        "independent": {
            "passed": second["verification_passed"],
            "wall": str(second["minimum_containment_clearance"]),
            "gap": f"{float(Fraction(second['minimum_best_pair_gap'])):.6e}",
            "failures": [str(f)[:100] for f in second["failures"][:2]],
            "cpu": round(t2, 1),
        },
    }


def lit(v: Fraction) -> str:
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)


def main(argv: list[str]) -> int:
    review, cert_path, n = Path(argv[1]), Path(argv[2]), int(argv[3])
    sys.path.insert(0, str(review))
    import review_708_check as rc  # noqa: E402

    raw = cert_path.read_bytes()
    lines = raw.decode("ascii").split("\n")
    header_index = next(i for i, ln in enumerate(lines) if ln.strip() and not ln.startswith("#"))
    side, squares, _tangents = rc.read(cert_path, n)
    checked = json.loads((review / "out-check.json").read_text())
    wall = Fraction(checked["min_wall_clearance"])
    i, j = checked["least_pair"]
    gap, axis = rc.sat_gap(squares[i], squares[j])
    assert gap == Fraction(checked["least_pair_gap"])
    x, y, c, s = squares[i]
    X, Y, C, T = squares[j]
    u, v = ((c, s), (-s, c), (C, T), (-T, C))[axis]
    proj = u * (X - x) + v * (Y - y)
    out = {
        "n": n,
        "wall_clearance": lit(wall),
        "wall_square": checked["min_wall_square"],
        "least_pair": [i, j],
        "least_gap": f"{float(gap):.16e}",
        "axis_index": axis,
        "axis_is_face_normal_of": "first" if axis < 2 else "second",
        "pair_tilts_equal": (c, s) == (C, T) or (c, s) == (-T, C) or (c, s) == (-C, -T) or (c, s) == (T, -C),
    }

    def mutate(new_side=None, move=None, rows=None):
        out_lines = list(lines)
        if new_side is not None:
            out_lines[header_index] = f"{n} {lit(new_side)}"
        if move is not None:
            k, (mx, my) = move
            parts = out_lines[header_index + 1 + k].split()
            parts[0] = lit(Fraction(parts[0]) + mx)
            parts[1] = lit(Fraction(parts[1]) + my)
            out_lines[header_index + 1 + k] = " ".join(parts)
        if rows is not None:
            out_lines = out_lines[: header_index + 1 + rows] + [""]
        return "\n".join(out_lines).encode("ascii")

    def parse(data: bytes):
        return reports.parse_certificate(data, n, "evand-cert")

    out["W1_side_minus_clearance"] = routes(parse(mutate(new_side=side - wall)))
    out["W2_side_minus_clearance_minus_1e-30"] = routes(parse(mutate(new_side=side - wall - EPS)))
    sign = -1 if proj > 0 else 1
    for label, delta in (("P1_pair_closed_by_gap", gap), ("P2_pair_closed_by_gap_plus_1e-30", gap + EPS)):
        data = mutate(move=(j, (sign * delta * u, sign * delta * v)))
        out[label] = routes(parse(data))
        _s, msq, _t = rc.read_bytes(data, n) if hasattr(rc, "read_bytes") else (None, None, None)
        if msq is None:
            tmp = review / "mutant.cert"
            tmp.write_bytes(data)
            _s, msq, _t = rc.read(tmp, n)
            tmp.unlink()
        out[label]["review_sat_gap"] = f"{float(rc.sat_gap(msq[i], msq[j])[0]):.6e}"
        out[label]["review_clip_area"] = f"{float(rc.intersection_area(msq[i], msq[j])):.6e}"
    # F1: a decimal literal for a coordinate -> the adapter must refuse
    out_lines = list(lines)
    parts = out_lines[header_index + 1].split()
    parts[0] = repr(float(Fraction(parts[0])))
    out_lines[header_index + 1] = " ".join(parts)
    try:
        parse("\n".join(out_lines).encode("ascii"))
        out["F1_decimal_literal"] = "ACCEPTED (wrong)"
    except Exception as error:  # noqa: BLE001
        out["F1_decimal_literal"] = f"refused: {str(error)[:120]}"
    # F2: one row short -> the adapter must refuse
    try:
        parse(mutate(rows=n - 1))
        out["F2_one_row_short"] = "ACCEPTED (wrong)"
    except Exception as error:  # noqa: BLE001
        out["F2_one_row_short"] = f"refused: {str(error)[:120]}"
    (review / f"out-controls-n{n}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
