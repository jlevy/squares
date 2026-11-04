"""Decide a centre-basis Witness/v2 certificate exactly, every wall and every pair, by two methods.

Usage: oz_check.py CERT.yaml EXPORT.json[.gz] N SIDE OUT.json

CERT.yaml is read by ozlib's own fail-closed reader; EXPORT is the lab's JSON export of the
same squares, read with the standard library's json module, and must hold exactly the same
squares. SIDE is the exact side the issue states. The verdict needs every format hypothesis,
every basis exactly unit, every square inside the box by both methods and every pair with
disjoint interiors by both methods, with the methods agreeing everywhere.
"""

from __future__ import annotations

import json
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ozlib as oz  # noqa: E402
from gmpy2 import mpq  # noqa: E402


def main() -> int:
    cert, export, n_s, side_s, out_p = sys.argv[1:6]
    n = int(n_s)
    t0 = time.process_time()
    w0 = time.time()
    doc = oz.read_witness_yaml(cert)
    fmt = oz.check_format(doc, n, side_s)
    gz = export.endswith(".gz")
    exp = oz.read_witness_json(export, gz=gz)

    # The export must hold the same squares, exactly.
    same_text = []
    same_value = []
    by_id_exp = {sq["id"]: sq for sq in exp["squares"]}
    for sq in doc["squares"]:
        e = by_id_exp.get(sq["id"])
        if e is None:
            same_text.append(False)
            same_value.append(False)
            continue
        same_text.append(sq["center"] == e["center"] and sq["basis"] == e["basis"])
        same_value.append(all(
            oz.to_F(a) == oz.to_F(b)
            for a, b in zip(sq["center"] + sq["basis"], e["center"] + e["basis"])))
    export_cmp = {
        "export_sha256": exp["sha256_bytes_read"],
        "export_square_count": len(exp["squares"]),
        "export_n": exp["header"]["n"],
        "export_side": exp["header"]["side"],
        "export_side_equal": exp["header"]["side"] == doc["header"]["side"],
        "export_ids_equal": sorted(by_id_exp) == sorted(sq["id"] for sq in doc["squares"]),
        "squares_textually_equal": sum(same_text),
        "squares_exactly_equal": sum(same_value),
        "export_claim_block": exp["claim"],
        "export_keys": exp["keys"],
    }
    export_cmp["identical_squares"] = (
        export_cmp["export_square_count"] == len(doc["squares"])
        and export_cmp["export_ids_equal"]
        and export_cmp["export_side_equal"]
        and all(same_value)
    )

    squares = oz.witness_squares(doc)
    S_F = oz.to_F(doc["header"]["side"])

    # Unit bases, in both kernels, and each square's own area from its corners.
    norm_bad_F = [sq["id"] for sq in squares if sq["F"][2] ** 2 + sq["F"][3] ** 2 != 1]
    norm_bad_Q = [sq["id"] for sq in squares if sq["Q"][2] ** 2 + sq["Q"][3] ** 2 != 1]
    area_bad = []
    not_convex = []
    for sq in squares:
        cor = oz.corners_Q(sq["Q"])
        if oz.area2(cor) != 2:
            area_bad.append(sq["id"])
        if not oz.is_ccw_convex(cor):
            not_convex.append(sq["id"])
    tilted = [sq["id"] for sq in squares if sq["F"][2] * sq["F"][3] != 0]
    shape = {
        "basis_norm_not_1_fraction": norm_bad_F,
        "basis_norm_not_1_mpq": norm_bad_Q,
        "corner_area_not_1": area_bad,
        "corners_not_ccw_convex": not_convex,
        "tilted_count": len(tilted),
        "axis_parallel_count": len(squares) - len(tilted),
    }
    shape["all_unit"] = not (norm_bad_F or norm_bad_Q or area_bad or not_convex)

    t1 = time.process_time()
    walls = oz.decide_walls(squares, S_F)
    t2 = time.process_time()
    pairs = oz.decide_pairs(squares)
    t3 = time.process_time()

    # Exact squared distances of the nearest pairs (a measurement; decides nothing more).
    byid = {sq["id"]: sq for sq in squares}
    near_rows = []
    for m, i, j, axis in pairs["near"][:40]:
        d2 = oz.dist2_squares_Q(oz.corners_Q(byid[i]["Q"]), oz.corners_Q(byid[j]["Q"]))
        near_rows.append({
            "pair": [i, j], "sat_margin": oz.frac_str(m), "sat_margin_approx": oz.sci(m),
            "axis": ["u_i", "u_i_perp", "u_j", "u_j_perp"][axis],
            "dist2": str(d2), "dist_approx": "0" if d2 == 0 else f"{float(d2) ** 0.5:.13e}",
            "dist_equals_margin": (oz.F_to_Q(m) ** 2 == d2) if m >= 0 else None,
        })
    near_counts = {}
    for k in (30, 25, 22, 21, 20, 18, 15, 12, 9, 6):
        near_counts[f"margin_below_1e-{k}"] = sum(1 for row in pairs["near"] if row[0] < Fraction(1, 10**k))
    t4 = time.process_time()

    verdict = (
        fmt["all_hold"]
        and export_cmp["identical_squares"]
        and shape["all_unit"]
        and walls["method1_all_inside"]
        and walls["method2_all_inside"]
        and not walls["clearance_disagreements"]
        and not walls["corner_vs_area_disagreements"]
        and pairs["method1_all_disjoint"]
        and pairs["method2_all_disjoint"]
        and not pairs["method_disagreements"]
    )
    pairs_out = {k: v for k, v in pairs.items() if k != "near"}
    pairs_out["near_count_below_1e-6"] = len(pairs["near"])
    receipt = {
        "program": "oz_check.py",
        "program_sha256": oz.sha256_file(__file__),
        "ozlib_sha256": oz.sha256_file(HERE / "ozlib.py"),
        "python": platform.python_version(),
        "gmpy2": oz.gmpy2_version(),
        "argv": sys.argv[1:],
        "cert_sha256": doc["sha256"],
        "n": n,
        "side": doc["header"]["side"],
        "side_approx": oz.sci(S_F, 20),
        "format": fmt,
        "export": export_cmp,
        "shape": shape,
        "walls": walls,
        "pairs": pairs_out,
        "nearest_pairs": near_rows,
        "near_pair_counts": near_counts,
        "verdict": "ACCEPT" if verdict else "REFUSE",
        "cpu_seconds": {
            "read_and_shape": round(t1 - t0, 2),
            "walls": round(t2 - t1, 2),
            "pairs_both_methods": round(t3 - t2, 2),
            "distances": round(t4 - t3, 2),
            "total": round(time.process_time() - t0, 2),
        },
        "wall_seconds": round(time.time() - w0, 2),
    }
    Path(out_p).write_text(json.dumps(receipt, indent=1) + "\n")
    print(f"{Path(cert).name}: {receipt['verdict']}; pairs {pairs['pairs_decided']}, least margin "
          f"{pairs['least_margin_approx']} at {pairs['least_margin_pair']}; least wall clearance "
          f"{walls['least_clearance_approx']} (square {walls['least_clearance_square']}); "
          f"cpu {receipt['cpu_seconds']['total']} s")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
