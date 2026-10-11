"""Read the pinned #419/#420 catalogue as reports, without deciding its proofs.

The complete roster and polynomial metadata are checked for internal consistency.
Source checker flags stay labelled as source claims; neither geometry, polynomial
minimality nor a Lean theorem is independently verified by this command.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.retained_data import read_retained_text

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "resources/web/evand-exact-and-local-reports-2026-10-07"
REVISION = "f58a01774a733b232a88576470332185d8d11641"
MAX_N = 324
EXPECTED_EXACT = 269
EXPECTED_LEAN_PACKS = 258
EXPECTED_BAND = 176
NEW_DEGREES = {102: 8, 106: 32, 152: 40, 177: 32}
LOCAL_SPECIAL = {11: "grade A (N11L)", 28: "grade A (N28L)"}


def catalogue(rows: object) -> dict[str, Any]:
    """Refuse malformed or incomplete metadata before deriving report rosters."""
    if not isinstance(rows, list) or len(rows) != MAX_N:
        raise ValueError("catalogue must contain exactly one row for every n=1..324")
    indexed: dict[int, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError("catalogue row is not an object")
        n = row.get("n")
        if type(n) is not int or not 1 <= n <= MAX_N or n in indexed:
            raise ValueError("catalogue count is invalid or duplicated")
        if row.get("status") not in {"exact", "open"}:
            raise ValueError(f"n={n}: unknown source status")
        indexed[n] = row
    exact = [n for n, row in sorted(indexed.items()) if row["status"] == "exact"]
    lean: list[int] = []
    band: list[int] = []
    special: dict[int, str] = {}
    new: dict[int, dict[str, Any]] = {}
    for n in exact:
        row = indexed[n]
        polynomial = row.get("S_poly_ascending")
        degree = row.get("S_degree")
        if (
            type(degree) is not int
            or degree < 1
            or not isinstance(polynomial, list)
            or len(polynomial) != degree + 1
            or any(type(value) is not int for value in polynomial)
            or polynomial[-1] == 0
        ):
            raise ValueError(f"n={n}: polynomial degree/coefficients disagree")
        interval = row.get("S_interval")
        if not isinstance(interval, list) or len(interval) != 2:
            raise ValueError(f"n={n}: missing rational root interval")
        if not all(isinstance(value, str) for value in interval):
            raise ValueError(f"n={n}: interval endpoints must be strings")
        left, right = (Fraction(value) for value in interval)
        if not 0 < left < right:
            raise ValueError(f"n={n}: invalid positive root interval")
        if type(row.get("verify_exact")) is not bool or type(row.get("lean_packs")) is not bool:
            raise ValueError(f"n={n}: source checker flags must be booleans")
        if row["lean_packs"]:
            lean.append(n)
        local = row.get("lean_local_min")
        if local == "band lemma":
            if Decimal(row["S"]) != Decimal(row["S"]).to_integral_value():
                raise ValueError(f"n={n}: band claim has a noninteger side")
            band.append(n)
        elif local:
            if local != LOCAL_SPECIAL.get(n):
                raise ValueError(f"n={n}: unknown local-minimum claim")
            special[n] = local
        if type(row.get("new")) is not bool:
            raise ValueError(f"n={n}: new-form marker must be boolean")
        if row.get("data") != f"minpoly/data/n-{n}.minpoly.json.gz":
            raise ValueError(f"n={n}: source geometry reference does not match its count")
        if row["new"]:
            new[n] = {
                "degree": degree,
                "polynomial_ascending": polynomial,
                "reported_root_interval": interval,
                "reported_side": row["S"],
                "upstream_geometry_data": row["data"],
            }
    if len(exact) != EXPECTED_EXACT or len(lean) != EXPECTED_LEAN_PACKS:
        raise ValueError("source exact/Lean claim roster differs from the pinned report")
    if len(band) != EXPECTED_BAND or special != LOCAL_SPECIAL:
        raise ValueError("source local-minimum roster differs from the pinned report")
    if {n: value["degree"] for n, value in new.items()} != NEW_DEGREES:
        raise ValueError("source new-form roster differs from the pinned report")
    return {
        "source_revision": REVISION,
        "assurance": "reported",
        "independent_geometry_replay": "not-attempted",
        "independent_lean_replay": "not-attempted",
        "polynomial_minimality": "source-claimed, not independently established",
        "exact_configuration_claims": exact,
        "open_counts": sorted(set(indexed) - set(exact)),
        "lean_packs_claims": lean,
        "band_local_minimum_claims": band,
        "special_local_minimum_claims": special,
        "new_form_claims": new,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="compare the retained report rosters"
    )
    arguments = parser.parse_args()
    raw = read_retained_text(PACKET / "source/s12/search/exact/exact_forms.json.gz")
    result = catalogue(json.loads(raw))
    target = PACKET / "reported-catalogue.json"
    if arguments.check:
        if json.loads(target.read_text()) != json.loads(json.dumps(result)):
            raise ValueError("retained reported catalogue is stale")
        print("reported catalogue: 269 exact claims, 258 Lean claims, 178 local-minimum claims")
    else:
        with atomic_output_file(target) as temporary:
            temporary.write_text(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
