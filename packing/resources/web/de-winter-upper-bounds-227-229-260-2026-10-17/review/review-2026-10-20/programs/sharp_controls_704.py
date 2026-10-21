"""Sharp controls for T-196's replay (PR #704): mutants at the scale of the margins.

The packet's two controls are gross (a duplicated square, gap -1; a square moved S + 2
outside). These probe the same two routes at the scale where the certificates' least
margins live: a wall lowered by exactly the clearance (contact, must pass) and by a
further 1e-30 (must fail); the least-gap pair closed by exactly its gap (contact, must
pass) and by a further 1e-30 (must fail); and two bases the adapter must refuse.

Run from a worktree's packing/ with its venv:
  python -I sharp_controls_704.py REVIEW_DIR N [N ...]
It writes REVIEW_DIR/out-controls-nN.json per count.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports

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
            "wall": first["minimum_containment_clearance"],
            "gap": first["minimum_best_pair_gap"],
            "failures": [str(f) for f in first["failures"][:3]],
            "cpu": round(t1, 1),
        },
        "independent": {
            "passed": second["verification_passed"],
            "wall": second["minimum_containment_clearance"],
            "gap": second["minimum_best_pair_gap"],
            "failures": [str(f)[:120] for f in second["failures"][:3]],
            "cpu": round(t2, 1),
        },
    }


def lit(v: Fraction) -> str:
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)


def sat_best(p, q):
    """Best axis (unit) and gap for a pair, as the review checker defines them."""
    x, y, c, s = p
    X, Y, C, T = q
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


def main(argv: list[str]) -> int:
    review = Path(argv[1])
    packet = reports.packet_path("de-winter-upper-bounds-227-229-260-2026-10-17")
    for n in map(int, argv[2:]):
        raw = (review / "data" / f"n{n}_exact.json").read_bytes()
        value = json.loads(raw)
        cert = reports.parse_certificate(raw, n, "center-basis-json")
        S = cert.side
        squares = [
            (Fraction(sq["center"][0]), Fraction(sq["center"][1]), Fraction(sq["basis"][0]), Fraction(sq["basis"][1]))
            for sq in value["squares"]
        ]
        # least wall clearance and least-gap pair, from the review checker's receipt
        checked = json.loads((review / "out-check.json").read_text())[str(n)]
        wall = Fraction(checked["min_wall_clearance_half_extent"])
        i, j = checked["least_pair"]
        gap, (u, v), proj = sat_best(squares[i], squares[j])
        assert gap == Fraction(checked["least_pair_gap"])
        out = {"n": n, "wall_clearance": str(wall), "least_pair": [i, j], "least_gap": str(gap)}

        def mutate(side=None, move=None):
            data = json.loads(raw)
            if side is not None:
                data["side"] = lit(side)
            if move is not None:
                k, (mx, my) = move
                sq = data["squares"][k]
                sq["center"] = [lit(Fraction(sq["center"][0]) + mx), lit(Fraction(sq["center"][1]) + my)]
            return json.dumps(data).encode()

        # W1: side lowered by exactly the clearance -> contact with the far wall, must pass
        out["W1_side_minus_clearance"] = routes(reports.parse_certificate(mutate(side=S - wall), n, "center-basis-json"))
        # W2: and 1e-30 further -> must fail on a wall
        out["W2_side_minus_clearance_minus_1e-30"] = routes(reports.parse_certificate(mutate(side=S - wall - EPS), n, "center-basis-json"))
        # P1/P2: move square j toward square i along the best axis by gap (contact) and gap + 1e-30
        sign = -1 if proj > 0 else 1  # proj = axis . (c_j - c_i); move j against it
        for label, delta in (("P1_pair_closed_by_gap", gap), ("P2_pair_closed_by_gap_plus_1e-30", gap + EPS)):
            mv = (j, (sign * delta * u, sign * delta * v))
            mutant = mutate(move=mv)
            mcert = reports.parse_certificate(mutant, n, "center-basis-json")
            out[label] = routes(mcert)
            # the review checker's clipping area on the moved pair
            sys.path.insert(0, str(review))
            import review_704_check as rc  # noqa: E402

            mdata = json.loads(mutant)
            mp = tuple(Fraction(t) for t in (*mdata["squares"][i]["center"], *mdata["squares"][i]["basis"]))
            mq = tuple(Fraction(t) for t in (*mdata["squares"][j]["center"], *mdata["squares"][j]["basis"]))
            out[label]["review_sat_gap"] = str(rc.sat_gap(mp, mq))
            out[label]["review_clip_area"] = str(rc.intersection_area(mp, mq))
        # B1: basis off the unit circle by 1e-30 -> the adapter must refuse
        data = json.loads(raw)
        sq = data["squares"][0]
        sq["basis"] = [lit(Fraction(sq["basis"][0]) + EPS), sq["basis"][1]]
        try:
            reports.parse_certificate(json.dumps(data).encode(), n, "center-basis-json")
            out["B1_basis_off_circle"] = "ACCEPTED (wrong)"
        except Exception as error:  # noqa: BLE001
            out["B1_basis_off_circle"] = f"refused: {error}"
        # B2: a JSON number for a coordinate -> the adapter must refuse
        data = json.loads(raw)
        data["squares"][0]["center"][0] = float(Fraction(data["squares"][0]["center"][0]))
        try:
            reports.parse_certificate(json.dumps(data).encode(), n, "center-basis-json")
            out["B2_float_coordinate"] = "ACCEPTED (wrong)"
        except Exception as error:  # noqa: BLE001
            out["B2_float_coordinate"] = f"refused: {error}"
        (review / f"out-controls-n{n}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
        print(json.dumps(out, indent=1), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
