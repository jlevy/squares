"""Independently replay a BC303 literal-parent receipt from raw source atoms.

This audit imports no parent-mass reader. It rebuilds all closed memberships from the
source atoms, checks every number the receipt reports, and reports both frozen budget
comparisons. The source is identified by its proposal revision and repository-relative
path and the run by the receipt's execution revision; the audit records them and
compares no file with a Git blob (OR-16). The replay is the check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import lcm
from pathlib import Path
from typing import cast

SOURCE_REVISION = "39714308ce2081abbd76624387d134fee4be6deb"
SOURCE_PATH = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/"
    "bc-293-measure-free-96-25.json"
)

type Point = tuple[Fraction, Fraction]
type Atom = tuple[Point, Fraction]
type Parent = tuple[Fraction, Fraction, Fraction, Fraction]


class AuditError(ValueError):
    """The source, receipt, or independent arithmetic disagrees."""


# The audit reads as a list of invariant predicates; a positional predicate keeps
# each check beside the value it verifies.
def _require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise AuditError(message)


def _git_blob(data: bytes) -> str:
    """Git's blob id of some bytes, recorded so the source read can be found in history."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data, usedforsecurity=False).hexdigest()


def audit(repository: Path, receipt_path: Path) -> dict[str, object]:
    """Reconstruct the Q0 and four-corner masses without importing the reader."""

    root = repository.resolve()
    receipt = cast(dict[str, object], json.loads(receipt_path.read_bytes()))
    _require(receipt.get("schema") == "bc303-literal-parent-union/v1", "receipt schema")
    _require(receipt.get("source_revision") == SOURCE_REVISION, "source revision")
    revision = str(receipt["implementation_revision"])
    _require(len(revision) == 40, "execution revision")
    source = (root / SOURCE_PATH).read_bytes()

    document = cast(dict[str, object], json.loads(source))
    raw_rows = cast(list[list[str]], document["atoms"])
    atoms: list[Atom] = [
        ((Fraction(x), Fraction(y)), Fraction(weight)) for x, y, weight in raw_rows
    ]
    sites = dict(atoms)
    q = Fraction(96, 25)
    total = sum((weight for _, weight in atoms), Fraction())
    scale = lcm(*(weight.denominator for _, weight in atoms))
    _require(len(atoms) == len(sites) == 377, "distinct source atoms")
    _require(
        all(0 <= x <= q and 0 <= y <= q and weight > 0 for (x, y), weight in atoms),
        "positive in-container source atoms",
    )
    _require(total == Fraction(22524199, 2000000), "source total")
    _require(scale == 4_000_000, "source weight scale")
    _require(Fraction(cast(str, document["outer_side"])) == q, "container side")
    transforms = (
        lambda x, y: (x, y),
        lambda x, y: (q - x, y),
        lambda x, y: (x, q - y),
        lambda x, y: (q - x, q - y),
        lambda x, y: (y, x),
        lambda x, y: (q - y, x),
        lambda x, y: (y, q - x),
        lambda x, y: (q - y, q - x),
    )
    _require(
        all(
            sites.get(transform(x, y)) == weight
            for transform in transforms
            for (x, y), weight in atoms
        ),
        "weighted D4 invariance",
    )

    corners: tuple[Parent, ...] = (
        (Fraction(), Fraction(), Fraction(1), Fraction(1)),
        (q - 1, Fraction(), q, Fraction(1)),
        (Fraction(), q - 1, Fraction(1), q),
        (q - 1, q - 1, q, q),
    )
    groups = [
        [
            index
            for index, ((x, y), _) in enumerate(atoms)
            if left <= x <= right and bottom <= y <= top
        ]
        for left, bottom, right, top in corners
    ]
    _require(
        all(
            set(group).isdisjoint(other)
            for index, group in enumerate(groups)
            for other in groups[index + 1 :]
        ),
        "corner overlap",
    )
    units = [sum(int(scale * atoms[index][1]) for index in group) for group in groups]
    _require(len(set(units)) == 1, "D4 corner mass")
    mass = units[0]
    one_budget = scale * total - 10 * (scale + 15)
    four_budget = scale * total - 7 * (scale + 15)
    _require(mass == receipt.get("integer_mass_N"), "literal parent mass")
    _require(sum(units) == receipt.get("four_corner_union_units"), "four-corner mass")
    _require(one_budget == receipt.get("one_parent_budget_units"), "one-parent budget")
    _require(four_budget == receipt.get("four_parent_budget_units"), "four-parent budget")
    _require(
        mass - one_budget == receipt.get("one_parent_excess_units"),
        "one-parent signed difference",
    )
    _require(
        sum(units) - four_budget == receipt.get("four_corner_excess_units"),
        "four-parent signed difference",
    )
    _require(
        (mass > one_budget) == receipt.get("one_parent_nonextension"),
        "one-parent decision",
    )
    _require(
        (sum(units) > four_budget) == receipt.get("four_corner_nonextension"),
        "four-parent decision",
    )
    low, high = Fraction(23, 20000), Fraction(19977, 20000)
    boundary = [
        index
        for index in groups[0]
        if atoms[index][0][0] in (0, 1) or atoms[index][0][1] in (0, 1)
    ]
    parent_only = [
        index
        for index in groups[0]
        if not (low <= atoms[index][0][0] <= high and low <= atoms[index][0][1] <= high)
    ]
    return {
        "audit_schema": "bc303-literal-parent-union-independent/v1",
        "source_revision": SOURCE_REVISION,
        "source_path": SOURCE_PATH,
        "source_git_blob": _git_blob(source),
        "implementation_revision": revision,
        "source_atom_count": len(atoms),
        "distinct_sites": len(sites),
        "weight_scale": scale,
        "total_mass": str(total),
        "weighted_D4_invariant": True,
        "closed_Q0_member_indices_zero_based": groups[0],
        "corner_member_indices_zero_based": groups,
        "corner_units": units,
        "corner_sets_pairwise_disjoint": True,
        "boundary_member_indices_zero_based": boundary,
        "parent_only_beyond_T1_core_indices_zero_based": parent_only,
        "integer_mass_N": mass,
        "one_budget_units": int(one_budget),
        "four_budget_units": int(four_budget),
        "one_unused_units": int(one_budget - mass),
        "four_unused_units": int(four_budget - sum(units)),
        "four_corners_gap": str(q - 2),
        "one_nonextension": mass > one_budget,
        "four_nonextension": sum(units) > four_budget,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.repository, args.receipt)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
