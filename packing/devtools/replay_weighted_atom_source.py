"""Replay a retained weighted-atom charge against its family, through the production model.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.replay_weighted_atom_source \
        READER.json FAMILY.json

A `devtools.plateau_reader` receipt declares a weighted atom's token total, budget, both
charges, and the exact list of placements it charges.  This reader rebuilds that atom as a
production `ThresholdAtom` -- the object under admission -- and recomputes every one of those
figures from the family's own exact placement geometry, refusing on any disagreement.  It is
the independent half of a pair: the declared figures come from `plateau_reader`'s separate
`WeightedPoint` path, and nothing here reads them except to compare.

Two things it deliberately does not do.  It does not decide the family's K0--K3 geometry,
containment, depth or symmetry; run `devtools.independent_ceiling_reader` for that separate
obligation.  And it does not admit a scientific target: a reproduced charge says the
representation carries the retained evidence, not that any bound has moved.

The retained receipts name their source as a scratch path that no longer exists, and nothing
in them binds a receipt to a family by content. This tool hashes the exact byte snapshots
it parses and reports the pair, which is what a later record can pin. The paths may change
after those snapshots were read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack.fractional.ceiling import CeilingCertificate
from sqpack.fractional.threshold import ThresholdAtom

KIND = "weighted-atom-source-replay/v1"

#: Archived v1 receipts call the token total `size`; current v2 receipts name both counts.
LEGACY_READER_KIND = "plateau-reader/v1"
READER_KIND = "plateau-reader/v2"


class ReplayError(ValueError):
    """An input record cannot support an exact replay."""


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    record: dict[str, Any] = {}
    for key, value in pairs:
        if key in record:
            raise ReplayError(f"duplicate JSON object key {key!r}")
        record[key] = value
    return record


def _load(path: Path, context: str) -> tuple[dict[str, Any], str]:
    try:
        # `parse_float=Fraction` keeps a decimal token exact; no float ever enters a charge.
        raw = path.read_bytes()
        value = json.loads(raw, parse_float=Fraction, object_pairs_hook=_no_duplicates)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise ReplayError(f"cannot read {context} {path}: {error}") from error
    if not isinstance(value, dict):
        raise ReplayError(f"{context} must be a JSON object")
    return value, hashlib.sha256(raw).hexdigest()


def _fraction(value: object, context: str) -> Fraction:
    if isinstance(value, bool):
        raise ReplayError(f"{context} is a bool, not a rational number")
    try:
        return Fraction(value)  # type: ignore[arg-type]
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise ReplayError(f"{context} is not a rational number: {value!r}") from error


def _integer(value: object, context: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ReplayError(f"{context} must be a nonnegative JSON integer")
    return value


def declared_atom(reader: dict[str, Any]) -> dict[str, Any]:
    """The weighted atom a `plateau_reader` receipt declares, unvalidated and uncomputed."""

    kind = reader.get("kind")
    if kind not in (LEGACY_READER_KIND, READER_KIND):
        raise ReplayError(
            f"receipt kind is {kind!r}; expected {LEGACY_READER_KIND!r} or {READER_KIND!r}"
        )
    cliques = reader.get("k5_cliques")
    if not isinstance(cliques, dict):
        raise ReplayError("receipt has no 'k5_cliques' object")
    atom = cliques.get("atom")
    if not isinstance(atom, dict):
        raise ReplayError("receipt has no 'k5_cliques.atom' object")
    return atom


def rebuilt_atom(atom: dict[str, Any]) -> ThresholdAtom:
    """The declared sites and token counts, as the production model would hold them."""

    points = atom.get("points")
    if not isinstance(points, list) or not points:
        raise ReplayError("atom field 'points' must be a nonempty JSON array")
    coordinates: list[tuple[Fraction, Fraction]] = []
    multiplicities: list[int] = []
    for index, site in enumerate(points):
        if not isinstance(site, dict):
            raise ReplayError(f"atom point {index} must be a JSON object")
        coordinates.append(
            (
                _fraction(site.get("x"), f"atom point {index} field 'x'"),
                _fraction(site.get("y"), f"atom point {index} field 'y'"),
            )
        )
        multiplicities.append(
            _integer(site.get("multiplicity"), f"atom point {index} field 'multiplicity'")
        )
    threshold = _integer(atom.get("threshold"), "atom field 'threshold'")
    try:
        # Weight one: this replay compares charges against a budget, and the LP multiplier
        # is not part of the retained receipt.
        return ThresholdAtom(tuple(coordinates), threshold, Fraction(1), tuple(multiplicities))
    except (TypeError, ValueError) as error:
        raise ReplayError(
            f"the declared atom is not a valid threshold atom: {error}"
        ) from error


def loaded_family(record: dict[str, Any]) -> CeilingCertificate:
    try:
        return CeilingCertificate.from_record(record)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise ReplayError(f"invalid ceiling family: {error}") from error


def recomputed(atom: ThresholdAtom, family: CeilingCertificate) -> dict[str, Any]:
    """Every figure the receipt declares, derived again from exact placement geometry."""

    threshold_charge = Fraction(0)
    floor_charge = Fraction(0)
    charged: list[int] = []
    for index, placement in enumerate(family.placements):
        held = atom.trace_count(placement.contains)
        if held >= atom.threshold:
            threshold_charge += placement.weight
            floor_charge += placement.weight * (held // atom.threshold)
            charged.append(index)
    budget = atom.token_count // atom.threshold
    return {
        "token_count": atom.token_count,
        "site_count": atom.size,
        "threshold": atom.threshold,
        "budget": budget,
        "threshold_charge": threshold_charge,
        "floor_charge": floor_charge,
        "threshold_violation": threshold_charge - budget,
        "floor_violation": floor_charge - budget,
        "charged_placements": charged,
    }


def _disagreements(
    atom: dict[str, Any], exact: dict[str, Any], *, reader_kind: str
) -> list[str]:
    """Each declared figure against its recomputation, named one at a time."""

    problems: list[str] = []
    counts = [
        ("site_count", "site_count", "site count"),
        ("token_count", "token_count", "token total"),
    ]
    if reader_kind == LEGACY_READER_KIND:
        # Retained v1 bytes require `size` as token count. Any explicit counts supplied
        # alongside it must also agree; none is silently ignored.
        counts = [("size", "token_count", "token total"), *(c for c in counts if c[0] in atom)]
    elif "size" in atom:
        raise ReplayError(
            "v2 atom uses 'site_count' and 'token_count'; legacy 'size' is invalid"
        )
    for field, exact_field, label in counts:
        declared = _integer(atom.get(field), f"atom field '{field}'")
        if declared != exact[exact_field]:
            problems.append(f"declared {label} {declared}, exact {label} {exact[exact_field]}")
    # The threshold is an input, not an independently reconstructed quantity. Changing
    # four to three for the seven-token motif changes the budget from one to two; other
    # threshold changes can preserve every checked figure.
    declared_budget = _integer(atom.get("budget"), "atom field 'budget'")
    if declared_budget != exact["budget"]:
        problems.append(f"declared budget {declared_budget}, exact budget {exact['budget']}")
    for field in ("threshold_charge", "floor_charge", "threshold_violation", "floor_violation"):
        declared = _fraction(atom.get(field), f"atom field '{field}'")
        if declared != exact[field]:
            label = field.replace("_", " ")
            problems.append(f"declared {label} {declared}, exact {label} {exact[field]}")
    declared_charged = atom.get("charged_placements")
    if not isinstance(declared_charged, list):
        raise ReplayError("atom field 'charged_placements' must be a JSON array")
    for index, value in enumerate(declared_charged):
        _integer(value, f"atom field 'charged_placements[{index}]'")
    if list(declared_charged) != exact["charged_placements"]:
        problems.append(
            f"declared charged placements {list(declared_charged)}, "
            f"exact charged placements {exact['charged_placements']}"
        )
    return problems


def replay(reader_path: Path, family_path: Path) -> dict[str, Any]:
    """The full receipt: the rebuilt atom, every recomputation, and every disagreement."""

    reader, reader_digest = _load(reader_path, "reader receipt")
    family_record, family_digest = _load(family_path, "ceiling family")
    atom_record = declared_atom(reader)
    atom = rebuilt_atom(atom_record)
    family = loaded_family(family_record)
    declared_total = _fraction(family_record.get("total_weight"), "family field 'total_weight'")
    exact = recomputed(atom, family)
    problems = _disagreements(atom_record, exact, reader_kind=reader["kind"])
    if declared_total != family.total_weight:
        problems.append(
            f"family declares total_weight {declared_total}, "
            f"its placements sum to {family.total_weight}"
        )
    if "family" in reader:
        summary = reader["family"]
        if not isinstance(summary, dict):
            raise ReplayError("receipt field 'family' must be a JSON object")
        # The receipt's own summary of the family it read is the only content-level binding
        # the retained records carry; the `source` field names a scratch path that is gone.
        declared_placements = _integer(summary.get("placements"), "family field 'placements'")
        written_against = len(family.placements)
        if declared_placements != written_against:
            problems.append(
                f"receipt was written against {declared_placements} placements, "
                f"this family has {len(family.placements)}"
            )
        if "total_weight" in summary:
            summary_total = _fraction(
                summary["total_weight"], "receipt family field 'total_weight'"
            )
            if summary_total != family.total_weight:
                problems.append(
                    f"receipt family total_weight is {summary_total}, "
                    f"this family has {family.total_weight}"
                )
    return {
        "kind": KIND,
        "replay": {
            "reproduced": not problems,
            "arithmetic": "exact rational",
            "reader": {
                "path": reader_path.name,
                "sha256": reader_digest,
                "kind": reader["kind"],
            },
            "family": {
                "path": family_path.name,
                "sha256": family_digest,
                "placements": len(family.placements),
                "outer_side": str(family.outer_side),
                "square_side": str(family.square_side),
                "total_weight": str(family.total_weight),
            },
            "atom": {
                "site_count": exact["site_count"],
                "token_count": exact["token_count"],
                "multiplicities": list(atom.multiplicities),
                "threshold": exact["threshold"],
                "budget": exact["budget"],
                "threshold_charge": str(exact["threshold_charge"]),
                "floor_charge": str(exact["floor_charge"]),
                "threshold_violation": str(exact["threshold_violation"]),
                "floor_violation": str(exact["floor_violation"]),
                "charged_placements": exact["charged_placements"],
                "variant": atom.to_record().get("variant"),
            },
            "disagreements": problems,
        },
        "ceiling_proof": {
            "checked": False,
            "obligation": (
                "K0--K3 geometry, containment, maximum depth, total, and D4 symmetry must "
                "be decided separately by devtools.independent_ceiling_reader"
            ),
        },
        "scientific_target": {
            "run": False,
            "obligation": (
                "a reproduced charge admits the representation only; registering or running "
                "a BC327 comparison needs the remaining admission stages"
            ),
        },
    }


def main(argv: list[str] | None = None) -> int:
    """Replay one retained weighted-atom receipt against its family."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reader", type=Path, help="a plateau-reader/v1 or v2 receipt")
    parser.add_argument("family", type=Path, help="the ceiling family it was written against")
    options = parser.parse_args(argv)
    try:
        receipt = replay(options.reader, options.family)
    except ReplayError as error:
        print(
            json.dumps({"kind": KIND, "replay": {"reproduced": False}, "error": str(error)}),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["replay"]["reproduced"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
