#!/usr/bin/env python3
"""Retain the two n=5 endpoints that `D-034` names, as a control's two constituents.

`D-034` records that two `n = 5` rows share side `2.767766952966`, closed form, contact
certificate, angle signature and contact count while differing geometrically, and that
this makes their identity unresolved. The claim has been quoted since 2026-08-23 without
the two endpoints ever being retained: `golden/basin-maps.yaml` keeps the aggregate rows
and not the poses, so nothing downstream could check the claim or score a relation on it.

They are not lost, only unretained -- the census is a fixed seed stream -- so this
reproduces them through `check_golden_basins`'s own functions rather than a second census,
and writes what a control needs: both poses, both keys, and the measured invariants.

**This does not prove a component count**, and the artifact says so in a field rather than
a comment. What the pair would decide, and the one quantity missing, are in
`check_identity_relation`'s prospective control, which reads this file.

Usage:
    uv run --frozen python -m devtools.build_n5_identity_pair
    uv run --frozen python -m devtools.build_n5_identity_pair --check
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from typing import Any

from strif import atomic_output_file

from devtools.check_golden_basins import SIDE_DECIMALS, census_from, census_starts, census_unit
from sqpack.research.canonical import canonical_key
from sqpack.research.quench import QuenchResult

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "campaign" / "series" / "series-000-smoke-and-calibration" / "results"
RECORD = OUT / "bc-083-n5-identity-pair.json"

N = 5
SEEDS = 6
# The side D-034 names, to the golden map's own precision. Matching on the rounded side
# rather than on a tolerance keeps this tied to the number the defect quotes.
PAIR_SIDE = 2.767766953


@dataclass(frozen=True, slots=True)
class Endpoint:
    """One census endpoint, with everything a relation could be scored on."""

    seed: int
    side: float
    geometric_key: str
    contact_certificate: str
    x: list[float]
    y: list[float]
    theta: list[float]


def _endpoints() -> list[tuple[int, QuenchResult]]:
    """The six n=5 census endpoints, from the fixed seed stream."""
    units = census_starts(N, SEEDS)
    with ProcessPoolExecutor() as pool:
        done = list(pool.map(census_unit, units))
    return [(seed, result) for _n, seed, result in sorted(done, key=lambda r: r[1])]


def build() -> dict[str, Any]:
    endpoints = _endpoints()
    _atlas, configs = census_from(N, endpoints)

    rows: list[Endpoint] = []
    # `census_from` keeps the lowest-side pose per identity but not which seed produced
    # it, and the seed is what makes the pair reproducible by hand, so recover it here
    # through the same key function the census used.
    seed_by_identity: dict[tuple[str, str], int] = {}
    for seed, result in endpoints:
        key = canonical_key(result.x, result.y, result.theta, result.side)
        seed_by_identity.setdefault((key.geometric, key.contact), seed)

    for identity, config in configs.items():
        x, y, theta, side = config
        if round(side, SIDE_DECIMALS) != PAIR_SIDE:
            continue
        seed = seed_by_identity[identity]
        rows.append(
            Endpoint(
                seed=seed,
                side=side,
                geometric_key=identity[0],
                contact_certificate=identity[1],
                x=list(x),
                y=list(y),
                theta=list(theta),
            )
        )

    rows.sort(key=lambda r: r.geometric_key)
    if len(rows) != 2:
        raise SystemExit(
            f"expected exactly 2 endpoints at side {PAIR_SIDE}, found {len(rows)}; "
            "D-034's pair is not reproducing and this artifact must not be written"
        )
    first, second = rows

    return {
        "schema_version": 1,
        "subject": {
            "n": N,
            "defect": "D-034",
            "commitment": "BC-083",
            "side": PAIR_SIDE,
            "source": "the six-seed n=5 census in devtools.check_golden_basins",
        },
        "endpoints": [asdict(row) for row in rows],
        "measured": {
            "share_contact_certificate": first.contact_certificate
            == second.contact_certificate,
            "share_geometric_key": first.geometric_key == second.geometric_key,
            "side_difference": abs(first.side - second.side),
        },
        "component_count": None,
        "why_component_count_is_null": (
            "Not proved, and not provable by the route that proved n = 3 and n = 4. Those "
            "classifications are exhaustive because orientation is forced -- every square "
            "axis-aligned -- so the configuration space is a finite union of separation "
            "cells, 64 raw branches at n = 3 and 4096 at n = 4, each decided by an LP. The "
            "n = 5 optimum has two angle classes, so orientation is not forced and the "
            "space carries continuous angle parameters; the separation-cell method does "
            "not apply, and the obstruction is its kind rather than its count. exp-042 "
            "names the missing claim exactly: A_to_B_stationary_connection is one of its "
            "eleven declared scope refusals."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="compare against the retained record")
    args = ap.parse_args()

    built = build()
    if args.check:
        if not RECORD.exists():
            print(f"  {RECORD.name} is missing", file=sys.stderr)
            return 1
        retained = json.loads(RECORD.read_text(encoding="utf-8"))
        # Compare the identity content, not the float poses: the quench is deterministic
        # but its last bits are not a claim this file makes, and D-021 records a 1e-11
        # floor below which no difference here means anything.
        for field in ("subject", "measured", "component_count"):
            if retained.get(field) != built[field]:
                print(f"  {RECORD.name}: {field} has drifted", file=sys.stderr)
                return 1
        keys = [(e["geometric_key"], e["contact_certificate"]) for e in retained["endpoints"]]
        rebuilt = [(e["geometric_key"], e["contact_certificate"]) for e in built["endpoints"]]
        if keys != rebuilt:
            print(f"  {RECORD.name}: the pair's keys have drifted", file=sys.stderr)
            return 1
        print(f"  D-034's n=5 pair reproduces: {len(keys)} endpoints, keys unchanged")
        return 0

    with atomic_output_file(RECORD) as tmp:
        tmp.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {RECORD.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
