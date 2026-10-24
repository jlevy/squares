"""Exact premises of the four #446 fine-net certificates, decided apart from every checker.

For each of n = 19, 20, 26, 27 this reads the retained candidate strictly and decides,
in exact rationals (Python's fractions only):

- custody: the stored and decompressed SHA-256 against the retention record and the
  source's receipts;
- the claim: n, the side L against the register's side, B, the declared net, no points;
- the rectangle field order: which of the two readings gives positive-area rectangles
  inside K = [0, L]^2;
- the measure: every mass positive, the listed total equal to total_mass = n - 1/100000,
  the D4 expansion (distinct images, coincidences merged) integrating back to it;
- the net: lemma N0's premises (a) to (e), the sharp extent condition, the last bin's
  reach past tan(pi/8), every per-bin domain nonempty, and the core at each node's angle
  inside K at its domain's far corner;
- the numbers the register and the bundles print, and the gains over the case records.

Usage (from anywhere; the packet path is the retained release packet):

    python3 -I premises.py --packet PACKET --out outputs/premises.json
"""

from __future__ import annotations

import argparse
import json
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from t233lib import (  # noqa: E402
    CERTS,
    as_rect,
    bin_floor,
    cos_sin,
    domain_upper,
    expand,
    half_width,
    loose_json,
    read_candidate,
    strict_json,
)

# The case records' lower bounds at main 31584003e (T-103 to T-106), both lanes.
STANDING = {
    19: Fraction(193, 40),
    20: Fraction(981, 200),
    26: Fraction(1109, 200),
    27: Fraction(11287, 2000),
}
# Upper bounds on main (n-019.md etc.), as exact forms, for a sanity comparison only.
UPPER_FLOAT = {19: 4.88561808316412, 20: 5.0, 26: 5.62132034355964, 27: 5.70710678118654}


def frac(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def order_report(cand, order: str) -> dict:
    ok_area = ok_inside = 0
    for row in cand.rows:
        r = as_rect(row, order)
        if r.x1 < r.x2 and r.y1 < r.y2:
            ok_area += 1
            if 0 <= r.x1 and r.x2 <= cand.L and 0 <= r.y1 and r.y2 <= cand.L:
                ok_inside += 1
    return {"rows": len(cand.rows), "positive_area": ok_area, "inside_K": ok_inside}


def net_report(cand) -> dict:
    B, D, m, L = cand.B, cand.step, cand.last, cand.L
    count = m + 1
    tmax = m * D
    facts: dict[str, object] = {}
    checks: dict[str, bool] = {}
    checks["a_positive_step_and_count_in_range"] = D > 0 and 2 <= count <= 2**16
    shrink = B * (1 + D)
    checks["b_B_times_1_plus_D_below_1"] = shrink < 1
    endpoint_poly = tmax * tmax + 2 * tmax - 1
    checks["c_last_tangent_past_tan_pi_8"] = endpoint_poly > 0
    checks["d_last_tangent_at_most_half"] = tmax <= Fraction(1, 2)
    tangent_form = B * (1 + D / (1 - D * D / 4))
    checks["e_tangent_form_below_1"] = tangent_form < 1
    z = D / 2
    sharp = B * (1 + 2 * z - z * z) / (1 + z * z)
    checks["sharp_extent_at_half_step_below_1"] = sharp < 1
    # last bin needed: its lower end is below tan(pi/8)
    low = tmax - D / 2
    low_poly = low * low + 2 * low - 1
    checks["last_bin_lower_end_below_tan_pi_8"] = low_poly < 0
    high = tmax + D / 2
    checks["bins_reach_tan_pi_8"] = high * high + 2 * high - 1 > 0
    # first node is the axis direction, bins are contiguous by construction (t_r = r D)
    checks["first_node_is_axis"] = True
    # every per-bin domain nonempty; the core at the node angle inside K at (U_r, U_r)
    least_gap = None
    least_fit = None
    worst_fit_r = None
    nonempty = True
    for r in range(count):
        upper = domain_upper(L, D, r)
        gap = upper - L / 2
        if gap <= 0:
            nonempty = False
        if least_gap is None or gap < least_gap:
            least_gap = gap
        a = bin_floor(D, r)
        # bins that meet [0, tan(pi/8)]: a_r^2 + 2 a_r - 1 <= 0
        if a * a + 2 * a - 1 <= 0:
            c, s = cos_sin(D, r)
            fit = half_width(a) - B * (c + s) / 2  # >= 0 iff core inside K at (U_r, U_r)
            if least_fit is None or fit < least_fit:
                least_fit = fit
                worst_fit_r = r
    checks["every_per_bin_domain_nonempty"] = nonempty
    checks["core_inside_K_at_every_domain_corner"] = least_fit is not None and least_fit > 0
    facts.update(
        {
            "step": frac(D),
            "last": m,
            "count": count,
            "last_tangent": frac(tmax),
            "endpoint_polynomial": frac(endpoint_poly),
            "B_times_1_plus_D": frac(shrink),
            "margin_1_minus_B_times_1_plus_D": frac(1 - shrink),
            "per_edge_margin": frac((1 - shrink) / 2),
            "tangent_form": frac(tangent_form),
            "sharp_extent_at_half_step": frac(sharp),
            "last_bin_lower_end": frac(low),
            "last_bin_lower_end_polynomial": frac(low_poly),
            "least_domain_width_U_r_minus_L_over_2": frac(least_gap),
            "least_domain_width_decimal": float(least_gap),
            "least_rho_a_r_minus_half_core_extent": float(least_fit),
            "at_node": worst_fit_r,
        }
    )
    return {"checks": checks, "facts": facts, "all_hold": all(checks.values())}


def measure_report(cand, order: str) -> dict:
    meas = expand(cand, order)
    listed = sum((row.mass for row in cand.rows), Fraction(0))
    checks = {
        "every_mass_positive": all(row.mass > 0 for row in cand.rows),
        "listed_total_equals_total_mass": listed == cand.total_mass,
        "total_mass_is_n_minus_1e-5": cand.total_mass == cand.n - Fraction(1, 100000),
        "total_mass_below_n": cand.total_mass < cand.n,
        "expanded_integrates_to_total_mass": meas.total == cand.total_mass,
        "points_empty": cand.points == [],
        "every_expanded_rectangle_inside_K": all(
            0 <= r.x1 < r.x2 <= cand.L and 0 <= r.y1 < r.y2 <= cand.L for r in meas.rects
        ),
    }
    max_row_density = max(
        row.mass / ((as_rect(row, order).x2 - as_rect(row, order).x1)
                    * (as_rect(row, order).y2 - as_rect(row, order).y1))
        for row in cand.rows
    )
    max_dens = max(meas.density)
    checks["eight_times_densest_row_at_most_2_pow_32"] = 8 * max_row_density <= 2**32
    checks["expanded_density_at_most_2_pow_96"] = max_dens <= 2**96
    checks["side_at_most_1000"] = cand.L <= 1000
    checks["rows_at_most_1e6"] = len(cand.rows) <= 10**6
    return {
        "checks": checks,
        "all_hold": all(checks.values()),
        "facts": {
            "listed_rows": len(cand.rows),
            "expanded_distinct_rectangles": len(meas.rects),
            "coincident_images_merged": 8 * len(cand.rows) - len(meas.rects),
            "listed_total": frac(listed),
            "total_mass": frac(cand.total_mass),
            "mass_gap_n_minus_M": frac(cand.n - cand.total_mass),
            "max_row_density_decimal": float(max_row_density),
            "max_expanded_density_decimal": float(max_dens),
            "min_row_mass_decimal": float(min(row.mass for row in cand.rows)),
        },
    }


def semantic_digest_attempts(raw: bytes) -> dict[str, str]:
    """Try a few canonical serializations against the source's candidate_digest."""
    import hashlib  # noqa: PLC0415

    doc = strict_json(raw)
    forms = {
        "sorted_compact": json.dumps(doc, sort_keys=True, separators=(",", ":")),
        "sorted_compact_ascii_false": json.dumps(
            doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ),
        "unsorted_compact": json.dumps(doc, separators=(",", ":")),
        "sorted_default": json.dumps(doc, sort_keys=True),
    }
    return {k: hashlib.sha256(v.encode()).hexdigest() for k, v in forms.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    t0 = time.perf_counter()
    packet: Path = args.packet
    retention = loose_json((packet / "acquisition" / "release-assets.json").read_bytes())
    stored_by_path = {}
    for asset in retention["assets"]:
        for member in asset["members"]:
            if "stored" in member:
                stored_by_path[member["stored"]] = member
    report: dict[str, object] = {"kind": "t233-review-premises/v1", "cases": {}}
    every = True
    for n, (name, side) in CERTS.items():
        cand = read_candidate(packet, n)
        rel = f"release/certificates/{name}/candidate.json.gz"
        member = stored_by_path.get(rel, {})
        receipt = loose_json(
            (packet / "release" / "certificates" / name / "check2" / "receipt.json").read_bytes()
        )
        prepub = loose_json(
            (packet / "release" / "certificates" / name / "verification"
             / "prepublication-receipt.json").read_bytes()
        )
        custody = {
            "stored_sha256": cand.stored_sha256,
            "stored_bytes": cand.stored_bytes,
            "decompressed_sha256": cand.raw_sha256,
            "decompressed_bytes": cand.raw_bytes,
            "matches_retention_record": member.get("sha256") == cand.raw_sha256
            and member.get("bytes") == cand.raw_bytes,
            "matches_check2_receipt_file_sha256": receipt["file_sha256"] == cand.raw_sha256,
            "matches_check2_receipt_input_sha256": receipt["receipt"]["input_sha256"]
            == cand.raw_sha256,
            "matches_prepublication_input_sha256": prepub["input_sha256"] == cand.raw_sha256,
            "source_candidate_digest": receipt["candidate_digest"],
        }
        _stored, raw = (None, None)
        from t233lib import read_gzip_single  # noqa: PLC0415

        _stored, raw = read_gzip_single(packet / rel)
        attempts = semantic_digest_attempts(raw)
        custody["candidate_digest_reproduced_by"] = sorted(
            k for k, v in attempts.items() if v == receipt["candidate_digest"]
        )
        claim = {
            "n_matches": cand.n == n,
            "side_matches_register": cand.L == side,
            "side": frac(cand.L),
            "side_decimal_text_equivalent": float(cand.L),
            "B": frac(cand.B),
            "B_is_4999_over_5000": cand.B == Fraction(4999, 5000),
            "net_is_step_1_5002_last_2072": cand.step == Fraction(1, 5002) and cand.last == 2072,
            "net_keys": cand.net_keys,
            "file_keys": cand.keys,
            "gain_over_case_record": frac(cand.L - STANDING[n]),
            "below_upper_bound_on_main": float(cand.L) < UPPER_FLOAT[n],
        }
        orders = {o: order_report(cand, o) for o in ("x1y1x2y2", "x1x2y1y2")}
        measure = measure_report(cand, "x1y1x2y2")
        net = net_report(cand)
        summary = receipt["verifier_summary"]["premises"]
        agree = {
            "B": summary["B"] == frac(cand.B),
            "D": summary["D"] == frac(cand.step),
            "L": summary["L"] == frac(cand.L),
            "angle_count": summary["angle_count"] == cand.last + 1,
            "centre_domain_per_bin": summary["centre_domain"] == "per-bin",
            "format_M": summary["format"] == "M",
            "mass_exact": summary["mass_exact"] == frac(cand.total_mass),
            "mass_below_n": summary["mass_below_n"] == frac(cand.n - cand.total_mass),
            "source_rectangles": summary["source_rectangles"] == len(cand.rows),
            "expanded_rectangles": summary["expanded_rectangles"]
            == measure["facts"]["expanded_distinct_rectangles"],
            "expanded_points_zero": summary["expanded_points"] == 0,
            "expanded_segments_zero": summary["expanded_segments"] == 0,
        }
        case_ok = (
            all(v for k, v in custody.items() if k.startswith("matches"))
            and claim["n_matches"]
            and claim["side_matches_register"]
            and claim["B_is_4999_over_5000"]
            and claim["net_is_step_1_5002_last_2072"]
            and claim["below_upper_bound_on_main"]
            and orders["x1y1x2y2"]["inside_K"] == len(cand.rows)
            and measure["all_hold"]
            and net["all_hold"]
            and all(agree.values())
        )
        every = every and case_ok
        report["cases"][str(n)] = {
            "certificate": name,
            "custody": custody,
            "claim": claim,
            "field_orders": orders,
            "measure": measure,
            "net": net,
            "source_summary_premises_agree": agree,
            "verdict": "PREMISES_HOLD" if case_ok else "PREMISES_FAIL",
        }
    usage = resource.getrusage(resource.RUSAGE_SELF)
    report["verdict"] = "ALL_PREMISES_HOLD" if every else "A_PREMISE_FAILS"
    report["cpu_seconds"] = round(usage.ru_utime + usage.ru_stime, 3)
    report["wall_seconds"] = round(time.perf_counter() - t0, 3)
    args.out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    print(report["verdict"], "cpu", report["cpu_seconds"], "s")
    for n, case in report["cases"].items():
        print(n, case["verdict"], case["measure"]["facts"]["expanded_distinct_rectangles"],
              case["net"]["facts"]["B_times_1_plus_D"], case["claim"]["gain_over_case_record"],
              "digest:", case["custody"]["candidate_digest_reproduced_by"])
    return 0 if every else 1


if __name__ == "__main__":
    raise SystemExit(main())
