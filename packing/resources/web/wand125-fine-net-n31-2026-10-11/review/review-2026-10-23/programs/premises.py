"""Exact premises of mixed_n31_L59775: the file, the measure and the declared net.

Usage: python3 -I premises.py CANDIDATE.json[.gz] EXPECTED_SHA256 OUTPUT.json

Decides, in exact rationals and from the candidate alone:

- the candidate's identity (SHA-256 of the decompressed JSON) against the pin;
- n, L, B, the declared net and the empty point list, against the claim;
- every listed rectangle: 0 <= x0 < x1 <= L, 0 <= y0 < y1 <= L, mass > 0;
- the listed masses sum exactly to total_mass, and total_mass < n (threshold one);
- the merged D4 expansion: its row count, positive densities, its exact integral (equal
  to total_mass), and its invariance under all eight symmetries of the container;
- the declared net: D > 0, B(1 + D) < 1, the last tangent past tan(pi/8)
  (t^2 + 2t - 1 > 0), the last bin's lower end below tan(pi/8), t_last <= 1/2;
- the per-bin centre domain [r(a_j), L - r(a_j)] is nonempty at every node;
- the denominators of every coordinate (for the integer grid of capture.py) and the
  densest image (for the record).

Prints a one-line verdict and writes every value to OUTPUT.json.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from math import lcm
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import n31_exact as nx  # noqa: E402


def fr(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def main() -> int:
    start = time.process_time()
    path, expected_sha, out_path = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    cand = nx.read_candidate(path)
    checks: dict[str, bool] = {}
    facts: dict[str, object] = {}

    checks["sha256_matches_pin"] = cand["sha256"] == expected_sha
    facts["sha256"] = cand["sha256"]
    facts["bytes"] = cand["bytes"]

    n, side, core, step, last = cand["n"], cand["L"], cand["B"], cand["step"], cand["last"]
    checks["n_is_31"] = n == 31
    checks["L_is_2391_400"] = side == Fraction(2391, 400)
    checks["B_is_4999_5000"] = core == Fraction(4999, 5000)
    checks["step_is_1_5002"] = step == Fraction(1, 5002)
    checks["last_is_2072"] = last == 2072
    checks["points_empty"] = cand["points"] == []

    rects = cand["rectangles"]
    facts["rows"] = len(rects)
    checks["rows_are_536"] = len(rects) == 536
    bad_rows = []
    zero_mass = 0
    for k, (x0, y0, x1, y1, m) in enumerate(rects):
        if not (0 <= x0 < x1 <= side and 0 <= y0 < y1 <= side):
            bad_rows.append(k)
        if m < 0:
            bad_rows.append(k)
        if m == 0:
            zero_mass += 1
    checks["rows_inside_container_nondegenerate_nonnegative"] = not bad_rows
    facts["zero_mass_rows"] = zero_mass
    checks["every_mass_positive"] = zero_mass == 0 and not bad_rows

    mass = sum((r[4] for r in rects), Fraction(0))
    facts["mass_sum"] = fr(mass)
    checks["mass_sum_equals_total_mass"] = mass == cand["total_mass"]
    checks["total_mass_is_3099999_100000"] = cand["total_mass"] == Fraction(3099999, 100000)
    checks["mass_below_n"] = mass < n
    facts["n_minus_mass"] = fr(n - mass)

    merged = nx.expand(rects, side)
    facts["expanded_rows"] = len(merged)
    facts["image_count_before_merging"] = 8 * len(rects)
    checks["expanded_densities_positive"] = all(d > 0 for d in merged.values())
    integral = sum(((x1 - x0) * (y1 - y0) * d for (x0, y0, x1, y1), d in merged.items()),
                   Fraction(0))
    checks["expanded_integral_equals_mass"] = integral == mass
    invariant = True
    for (x0, y0, x1, y1), d in merged.items():
        for image in nx.d4_images(x0, y0, x1, y1, side):
            if merged.get(image) != d:
                invariant = False
                break
        if not invariant:
            break
    checks["expanded_measure_d4_invariant"] = invariant
    dens = max(merged.values())
    facts["densest_image_density"] = fr(dens)
    facts["densest_image_density_float"] = float(dens)
    listed_density = max(m / ((x1 - x0) * (y1 - y0)) for x0, y0, x1, y1, m in rects)
    facts["densest_listed_row_mass_over_area_float"] = float(listed_density)
    # The maintained route's admission cap (8 x the densest image density, which is the
    # densest row's mass over its area) is recorded, not used: it is no premise here.
    facts["densest_row_mass_over_area_at_most_2_pow_32"] = bool(listed_density <= 2**32)
    den = 1
    for x0, y0, x1, y1, _m in rects:
        for c in (x0, y0, x1, y1):
            den = lcm(den, c.denominator)
    facts["coordinate_denominator_lcm"] = den
    checks["coordinate_denominators_divide_10_pow_17"] = (10**17) % den == 0
    facts["thinnest_side"] = fr(min(min(x1 - x0, y1 - y0) for x0, y0, x1, y1, _ in rects))

    # The declared net.
    d = step
    checks["net_step_positive"] = d > 0
    shrink = core * (1 + d)
    facts["B_times_1_plus_D"] = fr(shrink)
    facts["B_times_1_plus_D_margin"] = fr(1 - shrink)
    checks["net_B_times_1_plus_D_below_1"] = shrink < 1
    t_last = last * d
    facts["t_last"] = fr(t_last)
    reach = t_last * t_last + 2 * t_last - 1
    facts["t_last_reach_polynomial"] = fr(reach)
    checks["net_t_last_past_tan_pi_8"] = reach > 0
    low = t_last - d / 2
    low_poly = low * low + 2 * low - 1
    facts["last_bin_lower_end_polynomial"] = fr(low_poly)
    checks["net_last_bin_lower_end_below_tan_pi_8"] = low_poly < 0
    checks["net_t_last_at_most_half"] = t_last <= Fraction(1, 2)
    tangent_form = core * (1 + d / (1 - d * d / 4))
    facts["tangent_form_B_1_plus_D_over_1_minus_D2_4"] = fr(tangent_form)
    checks["net_tangent_form_below_1"] = tangent_form < 1

    # Per-bin centre domain at every node.
    least_width = None
    for j in range(last + 1):
        a = max(Fraction(0), j * d - d / 2)
        width = side - 2 * nx.r_of(a)
        if least_width is None or width < least_width:
            least_width = width
    facts["least_per_bin_domain_width"] = fr(least_width)
    facts["least_per_bin_domain_width_float"] = float(least_width)
    checks["per_bin_domain_nonempty_at_every_node"] = least_width > 0

    status = "PREMISES_HOLD" if all(checks.values()) else "PREMISES_FAIL"
    out = {
        "kind": "review-2026-10-23-n31-premises/v1",
        "program": "premises.py",
        "program_sha256": nx.sha256_file(Path(__file__)),
        "module_sha256": nx.sha256_file(Path(nx.__file__)),
        "candidate": str(path.name),
        "status": status,
        "checks": checks,
        "facts": facts,
        "cpu_seconds": round(time.process_time() - start, 3),
    }
    out_path.write_text(json.dumps(out, indent=1, sort_keys=False) + "\n")
    print(status, {k: v for k, v in checks.items() if not v} or "all checks true",
          f"cpu {out['cpu_seconds']} s")
    return 0 if status == "PREMISES_HOLD" else 1


if __name__ == "__main__":
    raise SystemExit(main())
