"""Admit threshold-atom orbit rows against a retained ceiling family exactly.

The reader accepts a ``CeilingCertificate`` record and ordinary or weighted threshold
orbit records. It reconstructs every distinct D4 image, evaluates exact placement
memberships, and counts each contained site's tokens. For token total A it checks

    sum_g sum_{P: tokens(P intersect gS) >= k} y_P
        <= |D4.(S,a)| floor(A / k).

This is only the threshold-row admission.  It deliberately does not decide the ceiling
family's K0--K3 geometry and depth proof; run ``devtools.independent_ceiling_reader``
for that separate obligation.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack.fractional.ceiling import CeilingCertificate
from sqpack.fractional.threshold import ThresholdAtom

KIND = "threshold-atom-orbit-admission/v1"


class AdmissionError(ValueError):
    """An input record cannot support an exact admission decision."""


@dataclass(frozen=True, slots=True)
class Orbit:
    """One declared atom orbit and the D4 images reconstructed from its seed."""

    index: int
    atom: ThresholdAtom
    images: tuple[ThresholdAtom, ...]

    @property
    def per_image_budget(self) -> int:
        # Tokens, not sites: a weighted atom's budget is `floor(A / k)`, and reading `size`
        # here would understate it for every atom carrying a count above one.
        return self.atom.token_count // self.atom.threshold

    @property
    def budget(self) -> int:
        return len(self.images) * self.per_image_budget


def _mapping(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AdmissionError(f"{context} must be a JSON object")
    return value


def _fraction(value: Any, context: str) -> Fraction:
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise AdmissionError(f"{context} is not a rational number: {value!r}") from error


def _load(path: Path, context: str) -> Mapping[str, Any]:
    try:
        # JSON decimal tokens become their exact base-ten rationals instead of binary64.
        value = json.loads(path.read_text(), parse_float=Fraction)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise AdmissionError(f"cannot read {context} {path}: {error}") from error
    return _mapping(value, context)


#: Input receipts that declare a kind must declare one of these. The tool stamped `KIND` on
#: its output from the start but read no declared kind at all, so a record of another shape
#: whose field names happened to line up was admitted without complaint. Its sibling
#: `devtools.admit_fixed_support_dual` has always checked.
ACCEPTED_INPUT_KINDS = frozenset({"threshold-atom-orbits/v1"})


def _check_kind(record: Mapping[str, Any], context: str) -> None:
    kind = record.get("kind")
    if kind is not None and kind not in ACCEPTED_INPUT_KINDS:
        raise AdmissionError(
            f"{context} declares kind {kind!r}, which this reader does not accept"
        )


def _family(record: Mapping[str, Any]) -> CeilingCertificate:
    if "total_weight" not in record:
        raise AdmissionError("family field 'total_weight' is required")
    declared_total = _fraction(record["total_weight"], "family field 'total_weight'")
    try:
        certificate = CeilingCertificate.from_record(dict(record))
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise AdmissionError(f"invalid ceiling family: {error}") from error
    if declared_total < 0:
        raise AdmissionError(f"family field 'total_weight' is negative: {declared_total}")
    if certificate.total_weight != declared_total:
        raise AdmissionError(
            "family total_weight does not match its placements: "
            f"declared {declared_total}, recomputed {certificate.total_weight}"
        )
    return certificate


def _orbits(record: Mapping[str, Any], family: CeilingCertificate) -> tuple[Orbit, ...]:
    if "outer_side" not in record:
        raise AdmissionError("atom input field 'outer_side' is required")
    outer_side = _fraction(record["outer_side"], "atom input field 'outer_side'")
    if outer_side != family.outer_side:
        raise AdmissionError(
            f"atom outer_side {outer_side} does not match family outer_side {family.outer_side}"
        )
    if "square_side" in record:
        square_side = _fraction(record["square_side"], "atom input field 'square_side'")
        if square_side != family.square_side:
            raise AdmissionError(
                "atom square_side does not match family square_side: "
                f"{square_side} != {family.square_side}"
            )
    _check_kind(record, "threshold-atom input")
    entries = record.get("atoms")
    if not isinstance(entries, list) or not entries:
        raise AdmissionError("atom input field 'atoms' must be a nonempty JSON array")
    parsed: list[Orbit] = []
    for index, raw_entry in enumerate(entries):
        entry = _mapping(raw_entry, f"atom {index}")
        try:
            # Orbit admission prices the unit inequality; an LP multiplier is not an
            # input to that row. The model owns both strict serialized site formats.
            atom = ThresholdAtom.from_record(dict(entry) | {"weight": "1"})
        except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
            raise AdmissionError(f"invalid atom {index}: {error}") from error
        for point_index, (x, y) in enumerate(atom.points):
            if not (0 <= x <= outer_side and 0 <= y <= outer_side):
                raise AdmissionError(
                    f"atom {index} point {point_index} ({x}, {y}) lies outside "
                    f"[0, {outer_side}]^2"
                )
        images = atom.orbit(outer_side)
        declared_size = entry.get("orbit_size")
        if not isinstance(declared_size, int) or isinstance(declared_size, bool):
            raise AdmissionError(f"atom {index} field 'orbit_size' must be a JSON integer")
        if declared_size != len(images):
            raise AdmissionError(
                f"atom {index} orbit_size is {declared_size}, but exact D4 reconstruction "
                f"has {len(images)} images"
            )
        parsed.append(Orbit(index, atom, images))
    return tuple(parsed)


def _orbit_report(
    orbit: Orbit,
    family: CeilingCertificate,
    memberships: Mapping[tuple[Fraction, Fraction], tuple[bool, ...]],
) -> dict[str, Any]:
    image_charges: list[Fraction] = []
    for image in orbit.images:
        charge = Fraction(0)
        for placement_index, placement in enumerate(family.placements):
            trace = sum(
                count * memberships[point][placement_index]
                for point, count in zip(image.points, image.multiplicities, strict=True)
            )
            if trace >= image.threshold:
                charge += placement.weight
        image_charges.append(charge)
    total_charge = sum(image_charges, start=Fraction(0))
    budget = Fraction(orbit.budget)
    ratio = total_charge / budget
    return {
        "index": orbit.index,
        "support_size": orbit.atom.size,
        "token_count": orbit.atom.token_count,
        "threshold": orbit.atom.threshold,
        "orbit_size": len(orbit.images),
        "per_image_budget": str(orbit.per_image_budget),
        "budget": str(budget),
        "image_charges": [str(charge) for charge in image_charges],
        "charge": str(total_charge),
        "slack": str(budget - total_charge),
        "charge_to_budget": str(ratio),
        "violated": total_charge > budget,
    }


def admit_records(
    family_record: Mapping[str, Any], atom_record: Mapping[str, Any]
) -> dict[str, Any]:
    """Return a complete exact admission receipt for two already-decoded records."""
    family = _family(family_record)
    orbits = _orbits(atom_record, family)
    distinct_sites = sorted(
        {point for orbit in orbits for image in orbit.images for point in image.points}
    )
    memberships = {
        point: tuple(placement.contains(*point) for placement in family.placements)
        for point in distinct_sites
    }
    rows = [_orbit_report(orbit, family, memberships) for orbit in orbits]
    worst = max(rows, key=lambda row: Fraction(row["charge_to_budget"]))
    violations = [
        {
            "index": row["index"],
            "charge": row["charge"],
            "budget": row["budget"],
            "slack": row["slack"],
            "charge_to_budget": row["charge_to_budget"],
        }
        for row in rows
        if row["violated"]
    ]
    return {
        "kind": KIND,
        "atom_admission": {
            "admitted": not violations,
            "arithmetic": "exact rational",
            "outer_side": str(family.outer_side),
            "square_side": str(family.square_side),
            "placements": len(family.placements),
            "declared_total_weight": str(_fraction(family_record["total_weight"], "total")),
            "recomputed_total_weight": str(family.total_weight),
            "orbit_count": len(orbits),
            "orbit_images": sum(len(orbit.images) for orbit in orbits),
            "distinct_sites": len(distinct_sites),
            "orbits": rows,
            "worst": {
                "index": worst["index"],
                "charge": worst["charge"],
                "budget": worst["budget"],
                "charge_to_budget": worst["charge_to_budget"],
            },
            "violations": violations,
        },
        "ceiling_proof": {
            "checked": False,
            "obligation": (
                "K0--K3 geometry, containment, maximum depth, total, and D4 symmetry "
                "must be decided separately by devtools.independent_ceiling_reader"
            ),
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("family", type=Path)
    parser.add_argument("atoms", type=Path)
    arguments = parser.parse_args(argv)
    try:
        receipt = admit_records(
            _load(arguments.family, "ceiling family"),
            _load(arguments.atoms, "threshold-atom input"),
        )
    except AdmissionError as error:
        print(
            json.dumps(
                {
                    "kind": KIND,
                    "atom_admission": {"admitted": False},
                    "error": str(error),
                }
            )
        )
        return 2
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["atom_admission"]["admitted"] else 1


if __name__ == "__main__":
    sys.exit(main())
