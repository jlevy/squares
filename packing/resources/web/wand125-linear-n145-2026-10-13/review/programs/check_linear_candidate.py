"""Every exact premise of the linear candidate, and the arithmetic of its scope.

Usage::

    python3 -I check_linear_candidate.py CANDIDATE.json EXPECTED_SHA256 \\
        COMPLETION_AUDIT.json CASE_RECORDS_DIR

Reads the candidate as data and prints, as JSON: its digest and the claim; the orbit and
image counts by kind; containment, nondegeneracy and nonnegative masses; the exact mass
against ``total_mass`` and ``n - 1/100000``; the invariance of the weighted images under
both generators of D4; the semantic digest by the source's rule; the net's containment
facts; Tokoharu's centre half-width at every net angle; and the arithmetic of the claim's
scope at n = 145 to 150: Green's reported value (DS7 Theorem 9, k = 12) bounded from
80-digit integer square roots and compared with the source's rational upper bound and
stated margin, Nagamochi's and Karakus's closed forms, and the case records' upper and
lower bounds read from ``CASE_RECORDS_DIR/n-NNN.md``. It decides no coverage.
"""

from __future__ import annotations

import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import linear_exact as exact

DIGITS = 100


def record_value(text: str, field: str) -> Fraction:
    """The ``value`` printed under ``field`` in a case record's frontmatter."""
    match = re.search(rf"^  {field}:\n(?:    .*\n)*?    value: '([^']+)'", text, re.MULTILINE)
    if match is None:
        msg = f"no {field} value in the case record"
        raise SystemExit(msg)
    return Fraction(match.group(1))


def main(argv: list[str]) -> int:
    path, expected, audit_path, records = Path(argv[1]), argv[2], Path(argv[3]), Path(argv[4])
    data = path.read_bytes()
    digest = exact.sha256(data)
    if digest != expected:
        msg = f"{path} hashes to {digest}, not {expected}"
        raise SystemExit(msg)
    candidate = exact.load_json(data)
    measure = exact.read_measure(candidate)
    audit = exact.load_json(audit_path.read_bytes())
    side = measure.side
    facts = exact.net_facts(measure.core, measure.step, measure.last + 1)
    widths = [exact.half_width(measure, r) for r in range(measure.last + 1)]
    least_width = min(widths)
    # Green's reported value for k = 12 (DS7 Theorem 9) is
    # 2 sqrt 2 - 1 + 11 (132 + 2 sqrt 6) / 145, which the case records write as
    # 22 sqrt 6 / 145 + 2 sqrt 2 + 1307/145.
    root2, root6 = exact.sqrt_bounds(2, DIGITS), exact.sqrt_bounds(6, DIGITS)
    green_low = 2 * root2[0] - 1 + Fraction(11, 145) * (132 + 2 * root6[0])
    green_high = 2 * root2[1] - 1 + Fraction(11, 145) * (132 + 2 * root6[1])
    green_alt_low = Fraction(22, 145) * root6[0] + 2 * root2[0] + Fraction(1307, 145)
    compared = Fraction(audit["compared_with"])
    improvement = Fraction(audit["improvement_lower"])
    scope = {}
    for count in range(145, 151):
        k = math.isqrt(count)
        text = (records / f"n-{count:03}.md").read_text(encoding="utf-8")
        nagamochi = count - 2 * k + 1
        karakus = count - k + Fraction(1, 4)
        scope[count] = {
            "nagamochi_1_plus_sqrt": nagamochi,
            "side_exceeds_nagamochi": (side - 1) > 0 and (side - 1) ** 2 > nagamochi,
            "karakus_half_plus_sqrt": str(karakus),
            "side_exceeds_karakus": (side - Fraction(1, 2)) ** 2 > karakus,
            "side_exceeds_green_k12": side > green_high,
            "record_reported_upper": str(record_value(text, "reported_upper_bound")),
            "record_verified_upper": str(record_value(text, "verified_upper_bound")),
            "record_reported_lower": str(record_value(text, "reported_lower_bound")),
            "record_verified_lower": str(record_value(text, "verified_lower_bound")),
            "verified_upper_exceeds_side": record_value(text, "verified_upper_bound") > side,
            "reported_upper_exceeds_side": record_value(text, "reported_upper_bound") > side,
            "side_exceeds_reported_lower": side > record_value(text, "reported_lower_bound"),
            "side_exceeds_verified_lower": side > record_value(text, "verified_lower_bound"),
        }
    report = {
        "candidate_sha256": digest,
        "schema": candidate["schema"],
        "n": measure.n,
        "L": str(side),
        "B": str(measure.core),
        "net": candidate["net"],
        "keys": sorted(candidate),
        "orbits": {
            kind: sum(1 for k, _, _ in measure.primitives if k == kind) for kind in exact.KINDS
        },
        "positive_orbits": {
            kind: sum(1 for k, _, m in measure.primitives if k == kind and m > 0)
            for kind in exact.KINDS
        },
        "images": {kind: len(rows) for kind, rows in measure.images.items()},
        "mass": str(measure.total),
        "mass_equals_total_mass": measure.total == Fraction(candidate["total_mass"]),
        "mass_equals_n_minus_gap": measure.total == measure.n - exact.GAP,
        "d4_invariant": exact.invariant_under_d4(measure),
        "semantic_digest": exact.semantic_digest(candidate),
        "net_facts": {name: str(value) for name, value in facts.items()},
        "core_fits": facts["rotated_side_upper"] < 1,
        "net_reaches_past_pi_over_4": facts["endpoint_check"] > 0,
        "last_tangent_at_most_half": facts["endpoint"] <= Fraction(1, 2),
        "centre_half_width_least": str(least_width),
        "centre_half_width_least_at": widths.index(least_width),
        "centre_domain_nonempty_everywhere": least_width > 0,
        "least_distance_to_a_wall": float(
            min(
                min(v, side - v)
                for _, geometry, m in measure.primitives
                if m > 0
                for v in geometry
            )
        ),
        "green_k12_bounds": [float(green_low), float(green_high)],
        "green_k12_two_forms_agree": green_low == green_alt_low,
        "source_compared_with_is_an_upper_bound_on_green": compared >= green_high,
        "source_compared_with_minus_green_upper": float(compared - green_high),
        "side_minus_source_compared_with_equals_improvement_lower": side - compared
        == improvement,
        "improvement_lower": float(improvement),
        "improvement_lower_exceeds_0_0261330": improvement > Fraction("0.0261330"),
        "scope": scope,
    }
    sys.stdout.write(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
