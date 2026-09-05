#!/usr/bin/env python3
"""Freeze the measured contact structures at `n = 11` and `n = 29`.

`n = 11` is the calibration and `n = 29` is the target, and they are not alternatives.
Trump's packing is exact, so its contacts are *certified* by field arithmetic and the
extraction has a known answer to be caught being wrong against.  The `n = 29` pose is a
hundred-digit reconstruction, so its contacts are *measured* against a declared floor;
what makes that trustworthy is not the tolerance but the gap around it, which this file
records as `separation_decades`.

The extraction is the same code in both cases.  Only the injected `sign` differs, which
is the point: an extractor with one arithmetic hard-coded could not be calibrated
against an exact answer at all.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

import mpmath as mp
from jsonschema import Draft202012Validator

from cases.kingbird29.verify_svg import materialise_svg
from cases.kingbird29.verify_svg import sign as kingbird_sign
from cases.trump11.packing import build as build_trump11
from sqpack.promote.contacts import (
    ContactExtractionError,
    extract_contacts,
    require_decided,
)
from sqpack.verify import exact_sign, verify_packing
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "atlas/known-best/contact-structures.json"
SCHEMA = ROOT / "atlas/known-best/contact-structure.schema.yaml"
PROVENANCE = ROOT / "resources/papers/kingbird-square-29-provenance.svg"

KINGBIRD_DIGITS = 160
KINGBIRD_FLOOR = "1e-80"
AMBIGUITY_RATIO = "1e10"

#: Just inside the ambiguous band: above the floor, below the ceiling.  A displacement
#: this size is what a real near-contact looks like, and the extractor must refuse it
#: rather than round it to whichever side is convenient.
PERTURBATION = "1e-75"

EVIDENCE_ROLE = (
    "contact structures measured from retained poses; no feasibility, optimality, or "
    "exactness claim beyond the arithmetic each entry declares"
)


def _entry(structure, *, source: str, arithmetic: str, known_answer: dict) -> dict:
    record = structure.as_record()
    return {
        "n": record["n"],
        "source": source,
        "arithmetic": arithmetic,
        "side": record["side"],
        "floor": record["floor"],
        "ambiguity_ceiling": record["ambiguity_ceiling"],
        "pairs_tested": record["pairs_tested"],
        "wall_relations_tested": record["wall_relations_tested"],
        "pair_contact_count": len(record["pair_contacts"]),
        "wall_contact_count": len(record["wall_contacts"]),
        "incidence_count": record["incidence_count"],
        "ambiguous_count": len(record["ambiguous"]),
        "angle_class_count": len(record["angle_classes"]),
        "angle_classes": [
            {
                "label": item["label"],
                "members": list(item["members"]),
                "degrees": item["degrees"],
            }
            for item in record["angle_classes"]
        ],
        "chirality": [int(sign) for sign in record["chirality"]],
        "worst_contact_margin": record["worst_contact_margin"],
        "smallest_strict_separation": record["smallest_strict_separation"],
        "separation_decades": record["separation_decades"],
        "pair_contacts": [dict(item) for item in record["pair_contacts"]],
        "wall_contacts": [dict(item) for item in record["wall_contacts"]],
        "known_answer": known_answer,
    }


def trump11_entry() -> dict:
    squares, side, _field = build_trump11()
    report = verify_packing(squares, side, sign=exact_sign)
    structure = require_decided(extract_contacts(squares, side, sign=exact_sign))
    axis_like = [item for item in structure.angle_classes if len(item.members) == 6]
    agrees = (
        len(structure.pair_contacts) == report.touching_pairs
        and len(structure.wall_contacts) == report.container_contacts
        and len(structure.angle_classes) == 2
        and len(axis_like) == 1
    )
    return _entry(
        structure,
        source="cases.trump11.packing (exact, over Q(u) with u = tan(a/2))",
        arithmetic="exact-algebraic",
        known_answer={
            "checked_against": (
                "sqpack.verify.verify_packing under exact_sign, and Trump's published layout"
            ),
            "agrees": agrees,
            "detail": (
                f"the extractor found {len(structure.pair_contacts)} touching pairs and "
                f"{len(structure.wall_contacts)} corner-on-wall incidences against the "
                f"verifier's {report.touching_pairs} and {report.container_contacts}, and "
                f"{len(structure.angle_classes)} orientation classes splitting "
                f"{'6 axis-aligned + 5 tilted' if axis_like else 'unexpectedly'}, which is "
                "the published construction"
            ),
        },
    )


def kingbird29_entry() -> dict:
    mp.mp.dps = KINGBIRD_DIGITS
    _raw, _entities, side, squares = materialise_svg(PROVENANCE)
    report = verify_packing(squares, side, sign=kingbird_sign)
    structure = require_decided(
        extract_contacts(
            squares,
            side,
            sign=kingbird_sign,
            floor=KINGBIRD_FLOOR,
            ambiguity_ratio=AMBIGUITY_RATIO,
        )
    )
    agrees = (
        len(structure.pair_contacts) == report.touching_pairs
        and len(structure.wall_contacts) == report.container_contacts
    )
    return _entry(
        structure,
        source=f"{PROVENANCE.relative_to(ROOT).as_posix()} at {KINGBIRD_DIGITS} decimal digits",
        arithmetic="numerical-multiprecision",
        known_answer={
            "checked_against": "sqpack.verify.verify_packing over the same reconstruction",
            "agrees": agrees,
            "detail": (
                f"{len(structure.pair_contacts)} touching pairs and "
                f"{len(structure.wall_contacts)} corner-on-wall incidences against the "
                f"verifier's {report.touching_pairs} and {report.container_contacts}; the "
                f"worst contact margin is {structure.worst_contact_margin} and the smallest "
                f"strict separation {structure.smallest_strict_separation}, "
                f"{structure.separation_decades} decades apart"
            ),
        },
    )


def perturbation_control() -> dict:
    """Displace one square into the ambiguous band and require a typed refusal."""
    mp.mp.dps = KINGBIRD_DIGITS
    _raw, _entities, side, squares = materialise_svg(PROVENANCE)
    nudge = mp.mpf(PERTURBATION)
    moved = [list(square) for square in squares]
    moved[0] = [(x + nudge, y) for x, y in moved[0]]
    try:
        require_decided(
            extract_contacts(
                moved,
                side,
                sign=kingbird_sign,
                floor=KINGBIRD_FLOOR,
                ambiguity_ratio=AMBIGUITY_RATIO,
            )
        )
    except ContactExtractionError as error:
        return {
            "fired": True,
            "kind": error.kind,
            "detail": str(error)[:400],
            "displacement": PERTURBATION,
        }
    return {
        "fired": False,
        "kind": None,
        "detail": (
            "a square displaced into the ambiguous band produced a structure the "
            "extractor was willing to accept"
        ),
        "displacement": PERTURBATION,
    }


def expected_document() -> dict:
    return {
        "softschema": {
            "contract": "packing.squares:ContactStructureAtlas/v1",
            "schema": "contact-structure.schema.yaml",
            "status": "enforced",
        },
        "generated_by": "python -m devtools.generate_contact_structures",
        "evidence_role": EVIDENCE_ROLE,
        "structures": [trump11_entry(), kingbird29_entry()],
        "controls": {"perturbed_margin_refused": perturbation_control()},
    }


def validate_document(document: dict) -> None:
    schema = safe_load(SCHEMA.read_text(encoding="utf-8"))
    payload = {key: value for key, value in document.items() if key != "softschema"}
    Draft202012Validator(schema).validate(payload)
    for entry in document["structures"]:
        if not entry["known_answer"]["agrees"]:
            raise ValueError(f"n = {entry['n']}: extraction disagrees with its known answer")
    if not document["controls"]["perturbed_margin_refused"]["fired"]:
        raise ValueError("the perturbation control did not fire")


def _text(document: dict) -> str:
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


def update() -> None:
    document = expected_document()
    validate_document(document)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
    temporary.write_text(_text(document), encoding="utf-8")
    temporary.replace(OUTPUT)
    print("contact structures updated")


def check() -> None:
    document = expected_document()
    validate_document(document)
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != _text(document):
        raise ValueError(f"{OUTPUT.relative_to(ROOT)} is stale")
    print("contact structures check passed")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.update:
        update()
    else:
        check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
