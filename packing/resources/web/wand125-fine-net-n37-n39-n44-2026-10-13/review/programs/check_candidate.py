"""Every exact premise of one check2 candidate, recomputed apart from the crate and the tools.

Usage: ``python3 -I check_candidate.py CANDIDATE.json EXPECTED_SHA256``

Reads the candidate as data and prints, as JSON: its digest, the claim's count and side,
the declared net's keys, lemma N0's premises (a) to (e) and the last-bin premise (f), the
rows and their exact mass sum against ``total_mass`` and ``n - 1/100000``, containment and
nondegeneracy, the semantic digest by the source's rule, the densest row and image against
lemma F3's cap, the per-bin domain's least width over every node, and the least distance
of any rectangle from a wall. It decides no coverage.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fine_net_exact as exact


def main(argv: list[str]) -> int:
    path, expected = Path(argv[1]), argv[2]
    data = path.read_bytes()
    digest = exact.sha256(data)
    if digest != expected:
        msg = f"{path} hashes to {digest}, not {expected}"
        raise SystemExit(msg)
    candidate = exact.load_json(data)
    measure = exact.read_measure(candidate)
    facts = exact.net_facts(measure.core, measure.step, measure.count)
    premises = exact.premises_n0(facts, measure.count)
    positive = [(rect, mass) for rect, mass in measure.rows if mass > 0]
    densest_row = max(mass / ((x2 - x1) * (y2 - y1)) for (x1, y1, x2, y2), mass in positive)
    densest_image = max(density for _, density in measure.images)
    wall = min(
        min(x1, y1, measure.side - x2, measure.side - y2) for (x1, y1, x2, y2), _ in positive
    )
    least_side = min(min(x2 - x1, y2 - y1) for (x1, y1, x2, y2), _ in positive)
    widths = [
        exact.domain(measure.side, measure.step, r)[1]
        - exact.domain(measure.side, measure.step, r)[0]
        for r in range(measure.count)
    ]
    report = {
        "candidate_sha256": digest,
        "n": measure.n,
        "L": str(measure.side),
        "B": str(measure.core),
        "keys": sorted(candidate),
        "proof_net": candidate["proof_net"],
        "points_empty": candidate["points"] == [],
        "scaling_factor": candidate.get("scaling_factor"),
        "scaling_source_digest_is_own": candidate.get("scaling_source_digest", "absent"),
        "rows": len(measure.rows),
        "positive_rows": len(positive),
        "expanded_images": len(measure.images),
        "mass": str(measure.total),
        "mass_equals_total_mass": measure.total == Fraction(candidate["total_mass"]),
        "mass_equals_n_minus_gap": measure.total == measure.n - exact.GAP,
        "semantic_digest": exact.semantic_digest(candidate),
        "net": {name: str(value) for name, value in facts.items()},
        "premises": premises,
        "all_premises_hold": all(premises.values()),
        "side_squared_at_least_twice_core_squared": measure.side**2 >= 2 * measure.core**2,
        "densest_row_density": float(densest_row),
        "densest_image_density": float(densest_image),
        "eight_times_densest_image_at_most_2_32": 8 * densest_image <= 1 << 32,
        "densest_image_at_most_2_96": densest_image <= 1 << 96,
        "least_rectangle_side": float(least_side),
        "least_distance_to_a_wall": float(wall),
        "per_bin_domain_least_width": float(min(widths)),
        "per_bin_domain_least_width_at": widths.index(min(widths)),
        "per_bin_domain_nonempty_everywhere": all(width > 0 for width in widths),
    }
    sys.stdout.write(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
