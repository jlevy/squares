"""Read a frozen Git snapshot and audit low-n frontier transfer arithmetic.

This is a source-record audit, not a certificate replay or a search. Run with the
project Python 3.14 interpreter (PyYAML is a locked project dependency). Decimal
gaps are display arithmetic on retained decimal fields; exact expressions remain
attached. Certificate reach is conditional on the already recorded coverage.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

from sqpack.yamlio import safe_load


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True)


def decimal(value: Fraction) -> str:
    with localcontext() as context:
        context.prec = 40
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=float, default=10)
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 14):
        raise SystemExit("use project Python 3.14")
    if args.output.exists():
        raise SystemExit("refusing to overwrite a retained audit")
    started = time.monotonic()
    commit = git(args.repo, "rev-parse", args.commit).strip()
    cases = []
    for n in range(11, 26):
        source = f"packing/frontier/n-{n:03d}.md"
        text = git(args.repo, "show", f"{commit}:{source}")
        record = safe_load(text.split("---", 2)[1])["packing"]
        lower = record["verified_lower_bound"]
        upper = record["verified_upper_bound"]
        reported = record["reported_upper_bound"]
        with localcontext() as context:
            context.prec = 45
            verified_gap = Decimal(upper["value"]) - Decimal(lower["value"])
            reported_gap = Decimal(reported["value"]) - Decimal(lower["value"])
        cases.append(
            {
                "n": n,
                "source": source,
                "status": record["status"],
                "verified_lower": lower,
                "verified_upper": upper,
                "reported_upper": {k: reported[k] for k in ("value", "exact_form", "found_by")},
                "verified_gap_display": str(verified_gap),
                "reported_gap_display": str(reported_gap),
            }
        )
        if time.monotonic() - started > args.seconds:
            raise TimeoutError("source audit ceiling reached")
    paths = [
        "packing/cases/n12_fractional_certificate/certificate.json",
        "packing/cases/n18_fractional_certificate/certificate-4679-1000.json",
        "packing/cases/n20_fractional_certificate/certificate-24-5.json",
        "packing/cases/n20_fractional_certificate/certificate.json",
    ]
    certificates = []
    for source in paths:
        record = json.loads(git(args.repo, "show", f"{commit}:{source}"))
        side = Fraction(record["outer_side"])
        core = Fraction(record["square_side"])
        mass = Fraction(record["total_mass"])
        gamma = Fraction(record["least_cell_mass"])
        if gamma <= 0 or core <= 0:
            raise ValueError("positive coverage/core required")
        ratio = mass / gamma
        first_n = ratio.numerator // ratio.denominator + 1
        ceiling = side / core
        matched_counts = [
            c["n"]
            for c in cases
            if c["status"] == "open" and c["verified_lower"]["exact_form"] == str(side)
        ]
        count_slack = []
        for n in matched_counts:
            required_gamma = mass / n
            loss_fraction = 1 - mass / (n * gamma)
            count_slack.append(
                {
                    "n": n,
                    "strict_required_gamma_above": str(required_gamma),
                    "strict_required_gamma_above_decimal": decimal(required_gamma),
                    "allowed_relative_loss_from_recorded_gamma": str(loss_fraction),
                    "allowed_relative_loss_percent_display": decimal(100 * loss_fraction),
                    "scope": (
                        "charge loss only, not an allowed side increase; equality in "
                        "the budget does not exclude"
                    ),
                }
            )
        certificates.append(
            {
                "source": source,
                "id": record["id"],
                "n_field": record["n"],
                "side": str(side),
                "core": str(core),
                "mass": str(mass),
                "least_cell_mass": str(gamma),
                "normalized_budget": str(ratio),
                "normalized_budget_decimal": decimal(ratio),
                "first_count_from_charge_arithmetic": first_n,
                "fixed_L_B_single_square_selector_ceiling": str(ceiling),
                "fixed_L_B_single_square_selector_ceiling_decimal": decimal(ceiling),
                "ideal_headroom": str(ceiling - side),
                "ideal_headroom_decimal": decimal(ceiling - side),
                "count_slack": count_slack,
                "scope": (
                    "No coverage replay; budget uses retained gamma. L/B is only the "
                    "ideal side ceiling for unchanged L and B with one selected "
                    "B-square per parent, not a proved achievable rung or a ceiling "
                    "for new supports/cores/charges."
                ),
            }
        )
    by_n = {c["n"]: c for c in cases}
    transfer_caps = []
    for origin, receiver in ((11, 12), (17, 18), (18, 19), (18, 20), (19, 20)):
        origin_upper = by_n[origin]["verified_upper"]
        receiver_lower = by_n[receiver]["verified_lower"]
        with localcontext() as context:
            context.prec = 45
            gap = Decimal(origin_upper["value"]) - Decimal(receiver_lower["value"])
        transfer_caps.append(
            {
                "from_n": origin,
                "to_n": receiver,
                "verified_origin_upper": origin_upper,
                "receiver_current_lower": receiver_lower,
                "upper_minus_receiver_lower_display": str(gap),
                "scope": (
                    "Decimal display comparison only; report must justify exact signs "
                    "from attached expressions. The n17 verified upper is 5, not the "
                    "tighter reported packing."
                ),
            }
        )
    result = {
        "status": "COMPLETE_SOURCE_ARITHMETIC_AUDIT",
        "workflow": "W3",
        "exploration": "X-044",
        "commit": commit,
        "source_mode": "git show immutable commit paths; working tree ignored",
        "cases": cases,
        "certificates": certificates,
        "transfer_caps": transfer_caps,
        "python": sys.version,
        "command": sys.argv,
        "seconds": time.monotonic() - started,
        "limits": (
            "No new geometric measurements, numerical optimization, new bound, proof "
            "replay, frontier promotion, or inference of strictness from decimal fields."
        ),
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(
        json.dumps(
            {
                "commit": commit,
                "seconds": result["seconds"],
                "open_cases": [
                    {
                        "n": c["n"],
                        "lower": c["verified_lower"]["exact_form"],
                        "upper": c["verified_upper"]["exact_form"],
                        "gap": c["verified_gap_display"],
                    }
                    for c in cases
                    if c["status"] == "open"
                ],
                "certificates": [
                    {
                        k: c[k]
                        for k in (
                            "id",
                            "first_count_from_charge_arithmetic",
                            "normalized_budget_decimal",
                            "fixed_L_B_single_square_selector_ceiling_decimal",
                        )
                    }
                    for c in certificates
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
