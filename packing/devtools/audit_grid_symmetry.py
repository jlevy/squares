"""Audit the fixed five-by-five mixed-capacity D4 census by binomial formulas.

No producer or cycle dynamic program is imported. Geometry and the reviewed D4
action on closed existential cell assignments remain mathematical premises.
The CLI takes the identity count from the H259 receipt only after auditing that
receipt's whole census by closed binomial sums and checking it counts this grid.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

from devtools.audit_cell_occupancies import MAX_BYTES, coefficient, decode, plain_integer
from devtools.audit_cell_occupancies import audit_payload as audit_census

SCHEMA = "grid-symmetry-audit/v1"
SOURCE_SCHEMA = "grid-symmetry-count/v1"
COUNTED_OBJECTS = "D4 orbits of integer occupancies of indexed cells; square identities ignored"
CAPACITIES = [1 if i in (0, 4) or j in (0, 4) else 2 for i in range(5) for j in range(5)]
NAMES = ["r0", "r1", "r2", "r3", "f0", "f1", "f2", "f3"]


def fixed_counts(target: int) -> list[int]:
    """Use independent hand-derived fixed-polynomial coefficient formulas.

    A quarter/half-turn has a central singleton of capacity two. Its possible
    occupancies select the appropriate residue before reducing the degree.
    A reflection has singleton polynomial (1+x)^2(1+x+x^2)^3 and paired
    polynomial (1+y)^7(1+y+y^2)^3, where y=x^2.
    """
    plain_integer(target, "target", 128)
    identity = coefficient(16, 9, target)
    quarter = sum(
        coefficient(4, 2, (target - centre) // 4)
        for centre in range(3)
        if target >= centre and (target - centre) % 4 == 0
    )
    half = sum(
        coefficient(8, 4, (target - centre) // 2)
        for centre in range(3)
        if target >= centre and (target - centre) % 2 == 0
    )
    reflection = sum(
        coefficient(2, 3, singleton) * coefficient(7, 3, (target - singleton) // 2)
        for singleton in range(9)
        if target >= singleton and (target - singleton) % 2 == 0
    )
    return [identity, quarter, half, quarter, *([reflection] * 4)]


def profiles() -> list[list[list[int]]]:
    """Return reviewed cycle inventories, sorted as the producer contract requires."""
    identity = [[1, 1]] * 16 + [[1, 2]] * 9
    quarter = [[1, 2]] + [[4, 1]] * 4 + [[4, 2]] * 2
    half = [[1, 2]] + [[2, 1]] * 8 + [[2, 2]] * 4
    reflection = [[1, 1]] * 2 + [[1, 2]] * 3 + [[2, 1]] * 7 + [[2, 2]] * 3
    return [identity, quarter, half, quarter, *([reflection] * 4)]


def audit_payload(
    payload: object, identity_count: int, *, target: int = 17
) -> dict[str, object]:
    """Validate a full receipt; non-17 targets support separate synthetic controls."""
    if not isinstance(payload, dict):
        raise TypeError("receipt must be an object")
    receipt = cast(dict[str, object], payload)
    if set(receipt) != {
        "schema",
        "grid_size",
        "capacities",
        "target",
        "actions",
        "fixed_sum",
        "orbit_assignments",
        "counted_objects",
    }:
        raise ValueError("receipt fields differ from schema")
    if receipt["schema"] != SOURCE_SCHEMA or receipt["counted_objects"] != COUNTED_OBJECTS:
        raise ValueError("schema or counted objects mismatch")
    if plain_integer(receipt["grid_size"], "grid_size", 8) != 5:
        raise ValueError("auditor supports only the five-by-five mixed grid")
    if plain_integer(receipt["target"], "target", 128) != target:
        raise ValueError("target mismatch")
    if not isinstance(receipt["capacities"], list):
        raise TypeError("capacities must be a list")
    capacities = cast(list[object], receipt["capacities"])
    if [plain_integer(v, "capacity", 2) for v in capacities] != CAPACITIES:
        raise ValueError("row-major capacities mismatch")
    expected = fixed_counts(target)
    if plain_integer(identity_count, "identity count", 3**25) != expected[0]:
        raise ValueError("identity differs from independently recomputed H259 count")
    if not isinstance(receipt["actions"], list):
        raise TypeError("actions must be a list")
    actions = cast(list[object], receipt["actions"])
    if len(actions) != 8:
        raise ValueError("exactly eight actions required")
    for action, name, profile, count in zip(actions, NAMES, profiles(), expected, strict=True):
        if not isinstance(action, dict):
            raise TypeError("action must be an object")
        row = cast(dict[str, object], action)
        if set(row) != {"name", "cycle_profile", "fixed_assignments"} or row["name"] != name:
            raise ValueError("action roster mismatch")
        if not isinstance(row["cycle_profile"], list):
            raise TypeError("cycle profile must be a list")
        raw_profile = cast(list[object], row["cycle_profile"])
        actual: list[list[int]] = []
        for cycle in raw_profile:
            if not isinstance(cycle, list) or len(cycle) != 2:
                raise ValueError("cycle must contain length and capacity")
            pair = cast(list[object], cycle)
            actual.append(
                [
                    plain_integer(pair[0], "cycle length", 25),
                    plain_integer(pair[1], "cycle capacity", 2),
                ]
            )
        if actual != profile:
            raise ValueError(f"cycle profile mismatch for {name}")
        if plain_integer(row["fixed_assignments"], "fixed assignments", 3**25) != count:
            raise ValueError(f"fixed count mismatch for {name}")
    total = sum(expected)
    if total % 8:
        raise ValueError("Burnside sum is not divisible by eight")
    if plain_integer(receipt["fixed_sum"], "fixed_sum", 8 * 3**25) != total:
        raise ValueError("fixed sum mismatch")
    if plain_integer(receipt["orbit_assignments"], "orbit_assignments", 3**25) != total // 8:
        raise ValueError("orbit count mismatch")
    return {
        "schema": SCHEMA,
        "audit_passed": True,
        "target": target,
        "method": "closed-binomial-fixed-polynomials",
        "producer_imported": False,
        "fixed_counts": dict(zip(NAMES, expected, strict=True)),
        "fixed_sum": total,
        "orbit_assignments": total // 8,
        "identity_count": identity_count,
        "strict_reduction": total // 8 < identity_count,
        "scope": "D4 occupancy orbits; reviewed geometry and closed-assignment premises",
    }


def read_bounded(path: Path) -> bytes:
    with path.open("rb") as handle:
        raw = handle.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("receipt exceeds byte budget")
    return raw


def identity_count_of(identity: object, *, target: int = 17) -> int:
    """Audit the H259 census by its content and return its raw identity count.

    The census is recomputed whole by closed binomial sums, and it must count this
    grid: the same target, and the same capacities as a multiset (H259 lists them
    grouped, this audit row-major). Its bytes are not compared with a pinned digest
    (OR-16); a census that passes these checks is the H259 count whatever its layout.
    """
    census = audit_census(identity)
    if census["target"] != target:
        raise ValueError("identity census counts a different target")
    if sorted(cast(list[int], census["capacities"])) != sorted(CAPACITIES):
        raise ValueError("identity census counts a different grid")
    return cast(int, census["target_assignments"])


def audit(receipt_path: Path, identity_path: Path) -> dict[str, object]:
    raw = read_bounded(receipt_path)
    identity_raw = read_bounded(identity_path)
    identity_count = identity_count_of(decode(identity_raw))
    result = audit_payload(decode(raw), identity_count)
    if result["strict_reduction"] is not True:
        raise ValueError("orbit count does not strictly improve the raw identity count")
    result.update(
        {
            "receipt_bytes": len(raw),
            "receipt_sha256": hashlib.sha256(raw).hexdigest(),
            "identity_receipt_sha256": hashlib.sha256(identity_raw).hexdigest(),
        }
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("identity_receipt", type=Path)
    args = parser.parse_args(argv)
    try:
        result = audit(args.receipt, args.identity_receipt)
    except (ValueError, OSError, TypeError, RecursionError, KeyError) as error:
        print(json.dumps({"schema": SCHEMA, "audit_passed": False, "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
