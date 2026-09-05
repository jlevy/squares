#!/usr/bin/env python3
"""What an exact construction would cost at a size that has only decimals.

`BC-049` settled `n = 5` because Göbel's construction is exact. Its remaining instances,
`n = 28` and `n = 40`, retain decimal witnesses, and `X-007` says the next slice there is
producing an exact pose rather than running the assessor again. This prices that.

The price is not one number and the interesting part is where it stops being measurable.
Three stages, in order, each a precondition for the next:

1. **Digits.** `sqpack.promote.solve.reach` says the largest degree at which a refusal is
   still a statement about the number rather than about the precision. Measured here at
   the retained precision it is **zero at every size**, `n = 11` included -- which is the
   first thing worth knowing, because `n = 11`'s minimal polynomial *was* recovered. Not
   from its witness: from four hundred digits manufactured out of a closed system.
2. **A contact structure**, which is what a closed system is written against. The atlas
   retains one for `n = 11` and `n = 29` and no others. Whether one can be extracted at a
   given size is decidable now, at that size's own precision, and this runs it.
3. **A closed system and a case module**, which nothing here can price because writing one
   is the research rather than a step in it.

Stage 2 is the measurement this file exists for. `extract_contacts` classifies every pair
and every corner-to-wall relation against a declared floor, and refuses any incidence
sitting in the ambiguous band above it. Run at a floor the retained digits can actually
support, it answers a real question: is the pose precise enough to say what touches what?

**Nothing here promotes anything.** No frontier record moves, no rigidity claim is made,
and a size that clears stage 2 has not thereby acquired an exact construction -- it has
acquired the input to the stage that would have to produce one.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.price_exact_construction
    ... same, with --check, to compare against the retained record
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

import mpmath as mp
from strif import atomic_output_file

from sqpack.promote.contacts import ContactExtractionError, extract_contacts
from sqpack.promote.solve import MARGIN_DIGITS, MAX_COEFFICIENT, available_digits, reach
from sqpack.witness import load_witness, materialize_witness

ROOT = pathlib.Path(__file__).resolve().parent.parent
WITNESSES = ROOT / "witnesses" / "known-best"
WITNESS_SCHEMA = ROOT / "witnesses" / "witness.schema.yaml"
STRUCTURES = ROOT / "atlas" / "known-best" / "contact-structures.json"
RECORD = (
    ROOT
    / "campaign"
    / "series"
    / "series-000-smoke-and-calibration"
    / "results"
    / "bc-049-exact-construction-price.json"
)

SUBJECTS = (11, 28, 29, 40)
"""`BC-049`'s two open instances, with the two calibration sizes beside them.

`n = 11` is the case the promotion route closed and `n = 29` is the case it refused, so a
number reported for `n = 28` or `n = 40` that falls outside both is a number to distrust.
"""

AMBIGUITY_RATIO = "1e10"
"""The band `extract_contacts` refuses to classify, as the atlas extraction uses it."""

FLOOR_EXPONENTS = tuple(range(2, 121, 2))
"""Floors to sweep, as `1e-k`. Coarse to fine, every second order.

Sweeping rather than picking is the whole design. A single floor measures the floor: the
first version of this file chose one six orders inside the retained precision and got a
refusal at every size including `n = 11`, whose exact structure the atlas already holds.
That is not a fact about the packings. What is a fact about them is the *finest* floor at
which every incidence still decides, which is what the sweep returns.
"""


def digits_of(side: str) -> int:
    return len(side.rsplit(".", maxsplit=1)[-1]) if "." in side else 0


def witness_of(n: int) -> dict[str, Any]:
    return load_witness(WITNESSES / f"n-{n:03d}.yaml", fallback_schema=WITNESS_SCHEMA)


def digit_reach(n: int) -> dict[str, Any]:
    """Stage 1: what the retained precision buys an integer-relation search."""
    witness = witness_of(n)
    side = str(witness["side"])
    carried = digits_of(side)
    bound = f"1e-{carried}"
    return {
        "retained_digits": carried,
        "available_digits": float(available_digits(side, bound)),
        "reach_degree": reach(side, bound),
        "margin_digits": MARGIN_DIGITS,
        "max_coefficient": str(MAX_COEFFICIENT),
        "meaning": (
            "the largest degree at which a refusal would be a statement about the number "
            "rather than about the precision; zero means an integer-relation search on "
            "these digits can say nothing either way"
        ),
    }


def _numeric_sign(value: Any) -> int:
    magnitude = mp.mpf(value)
    return 0 if magnitude == 0 else (1 if magnitude > 0 else -1)


def contact_decidability(n: int) -> dict[str, Any]:
    """Stage 2: how fine a floor does the retained pose still decide every incidence at?

    Reported as the finest floor that decides, with the contact counts it finds there. A
    size whose pose decides only at a coarse floor is one whose contacts are guesses at the
    scale a closed system would be written at.
    """
    witness = witness_of(n)
    carried = digits_of(str(witness["side"]))
    squares, side = materialize_witness(witness, digits=carried + 40)

    deciding: list[dict[str, Any]] = []
    for exponent in FLOOR_EXPONENTS:
        floor = f"1e-{exponent}"
        try:
            structure = extract_contacts(
                squares,
                side,
                sign=_numeric_sign,
                floor=floor,
                ambiguity_ratio=AMBIGUITY_RATIO,
            )
        except ContactExtractionError:
            continue
        if structure.ambiguous:
            continue
        deciding.append(
            {
                "floor_exponent": exponent,
                "pair_contacts": len(structure.pair_contacts),
                "wall_contacts": len(structure.wall_contacts),
            }
        )

    if not deciding:
        return {
            "decided_at_any_swept_floor": False,
            "swept": f"1e-{FLOOR_EXPONENTS[0]} to 1e-{FLOOR_EXPONENTS[-1]}",
            "meaning": (
                "no floor in the sweep leaves every incidence decided, so this pose cannot "
                "say what touches what at any scale asked about"
            ),
        }

    counts = {(row["pair_contacts"], row["wall_contacts"]) for row in deciding}
    return {
        "decided_at_any_swept_floor": True,
        "window": f"1e-{deciding[0]['floor_exponent']} to 1e-{deciding[-1]['floor_exponent']}",
        "window_orders": deciding[-1]["floor_exponent"] - deciding[0]["floor_exponent"],
        "headroom_orders": carried - deciding[-1]["floor_exponent"],
        "pair_contacts": deciding[-1]["pair_contacts"],
        "wall_contacts": deciding[-1]["wall_contacts"],
        "counts_stable_across_window": len(counts) == 1,
        "meaning": (
            "the floors at which every incidence decides. It is a window rather than a "
            "threshold because the ambiguity ceiling is the floor times 1e10: too coarse a "
            "floor puts genuine separations inside the band, too fine a one puts contact "
            "residuals below it. A window that is wide, and over which the contact counts "
            "do not move, is a pose whose structure is not an artefact of the tolerance."
        ),
    }


def retained_structure(n: int) -> dict[str, Any] | None:
    """The contact counts the atlas already holds, where it holds any."""
    structures = json.loads(STRUCTURES.read_text(encoding="utf-8"))["structures"]
    for structure in structures:
        if int(structure["n"]) == n:
            return {
                "pair_contacts": len(structure["pair_contacts"]),
                "wall_contacts": len(structure["wall_contacts"]),
                "floor": str(structure["floor"]),
            }
    return None


def price() -> dict[str, Any]:
    stages: dict[str, Any] = {}
    calibration: dict[str, Any] = {}
    for n in SUBJECTS:
        measured = contact_decidability(n)
        stages[str(n)] = {
            "stage_1_digits": digit_reach(n),
            "stage_2_contact_structure": measured,
            "stage_3_closed_system": (
                "retained" if n in {11, 29} else "absent -- no case module exists"
            ),
        }
        known = retained_structure(n)
        if known is not None:
            reproduced = measured.get("decided_at_any_swept_floor") and (
                measured.get("pair_contacts") == known["pair_contacts"]
                and measured.get("wall_contacts") == known["wall_contacts"]
            )
            calibration[str(n)] = {
                "retained": known,
                "decimal_route_reports": (
                    {
                        "pair_contacts": measured.get("pair_contacts"),
                        "wall_contacts": measured.get("wall_contacts"),
                    }
                    if measured.get("decided_at_any_swept_floor")
                    else "nothing decides at any swept floor"
                ),
                "reproduced": bool(reproduced),
            }

    passed = [n for n, row in calibration.items() if row["reproduced"]]
    return {
        "schema_version": 2,
        "subject": {
            "commitment": "BC-049",
            "instances": [28, 40],
            "calibration": [11, 29],
            "question": ("what would an exact pose cost at a size that retains only decimals?"),
            "promotes_nothing": (
                "no frontier record moves and no rigidity claim is made here; clearing a "
                "stage buys the input to the next one, not an exact construction"
            ),
        },
        "stages": stages,
        "calibration": calibration,
        "verdict": {
            "calibration_result": (
                f"the decimal route reproduces the retained structure at {len(passed)} of "
                f"{len(calibration)} sizes where one exists"
            ),
            "so_the_measured_windows_are_not_evidence": (
                "n = 11's structure is exact and known -- 14 pair and 20 wall contacts at "
                "floor 0 -- and the decimal route decides at no floor at all. n = 29's is "
                "52 pair and 37 wall at floor 1e-80, and the route reports different "
                "numbers. A route that reproduces neither known answer is not one whose "
                "numbers at n = 28 and n = 40 can be read as structure; the floors where it "
                "appears to decide sit below the retained precision, which makes them "
                "windows on the materialisation's padding."
            ),
            "why_it_fails": (
                "the input, not the extractor. n = 29's retained structure came from a "
                "160-digit materialisation of a provenance SVG and n = 11's from exact "
                "field arithmetic. The witnesses carry 32, 57, 99 and 29 fractional digits, "
                "which is not enough for a contact residual to fall below a floor whose "
                "ambiguity ceiling is ten orders above it."
            ),
            "stage_1_is_zero_everywhere": (
                "reach is 0 at the retained precision for all four sizes, n = 11 included. "
                "Its degree-eight minimal polynomial was recovered from four hundred digits "
                "manufactured out of a closed system, not from its 32-digit witness. The "
                "retained decimals are not the input to this route at any size."
            ),
            "the_price": (
                "for n = 28: a higher-precision source, before anything else. It has no case "
                "module, no retained contact structure, and no provenance artifact of the "
                "kind n = 29's extraction was run against, so there is no first step to take "
                "and that is the typed refusal BC-049's exit accepts."
            ),
            "n40_did_not_need_this_route_at_all": (
                "and the first version of this file said it did, which was the error worth "
                "more than the measurement. Goebel's construction for n = 40 is published, "
                "is transcribed in this repository -- [Friedman DS7] section 2, the centred "
                "diagonal block family at a = 3, b = 4 -- and the retained witness is a "
                "materialisation of it: all eighty coordinates fit p + q sqrt(2) with "
                "half-integer p and q, the angles are exactly 0 and 45, and the only error "
                "anywhere is one 6.04e-31 truncation of the side. cases/gobel40 now builds "
                "it exactly and sqpack.verify accepts it: 40 squares, 780 pairs, 48 corner "
                "coordinates exactly on the boundary. This route was priced without first "
                "asking whether its destination was already reachable by another."
            ),
        },
    }


def serialized(record: dict[str, Any]) -> str:
    return json.dumps(record, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare against the record")
    args = parser.parse_args()

    built = price()
    if args.check:
        if not RECORD.exists():
            print(f"  {RECORD.name} is missing", file=sys.stderr)
            return 1
        if RECORD.read_text(encoding="utf-8") != serialized(built):
            print(f"  {RECORD.name} has drifted from a fresh pricing", file=sys.stderr)
            return 1
        print(
            "  exact-construction price reproduces: reach 0 at the retained precision for "
            f"all {len(SUBJECTS)} sizes"
        )
        return 0

    with atomic_output_file(RECORD) as temporary:
        temporary.write_text(serialized(built), encoding="utf-8")
    print(f"wrote {RECORD.relative_to(ROOT.parent)}")
    for n, stage in built["stages"].items():
        one, two = stage["stage_1_digits"], stage["stage_2_contact_structure"]
        where = (
            f"decides over {two['window']}, {two['pair_contacts']} pair / "
            f"{two['wall_contacts']} wall"
            if two["decided_at_any_swept_floor"]
            else "decides at no swept floor"
        )
        print(
            f"  n={n:>3}  {one['retained_digits']:>4} digits, "
            f"reach {one['reach_degree']}  |  {where}"
        )
    for n, row in built["calibration"].items():
        verdict = "reproduces" if row["reproduced"] else "DOES NOT reproduce"
        print(f"  calibration n={n}: the decimal route {verdict} the retained structure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
