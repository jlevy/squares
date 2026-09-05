#!/usr/bin/env python3
"""Per-record coverage certificates for the contact-assembly grammar, at `n <= 30`.

`BC-019` asks whether standing records at `n <= 30` are already chunk-structured and, if
not, which grammar move is missing. The contract in `atlas/known-best/contact-assembly-
grammar.yaml` already carries sliding degrees of freedom, a complexity cost, and
canonicalization rules. What it has never carried is the last clause of that exit:
**per-record certificates or typed limitations**.

This supplies them, and the split is clean. Seventeen of the thirty records have every
component expressible as a `rigid-lattice` primitive and get a certificate with the
complexity tuple filled in. Thirteen do not and get a typed limitation naming exactly which
components, with what `X-008` measured about them.

Two things are deliberately *not* computed, because computing them would mean inventing
them.

**`internal_slide_dof` is zero here by the primitive's own semantics, not by a rank.** The
contract's formula `D = 2m - rank(A_normal) - 2` is for a `contact-scaffold`, whose
tangential offsets stay LP variables. A `rigid-lattice` is defined as fixed integer offsets
in one fitted orientation, so it has no internal slide at all, and the detector finds only
rigid lattices in this corpus. Reporting a rank here would be answering a question about a
primitive the corpus does not contain.

**The normal axis and sign of each contact are not recorded and are not reconstructed.**
The contract's `label_fields` require them; the census stores internal edges as square
pairs with a residual. That gap is stated as a typed limitation rather than filled by
inference, because a normal axis inferred from lattice deltas would be an assumption about
the fit dressed as a measurement.

**No `H-044` verdict is emitted.** A record without a certificate here is one the *current
detector* did not express, which the census's own `known_gap` says is not a refutation of
chunk expressibility until the minimal-partition solver exists.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.certify_assembly_coverage
    ... same, with --check, to compare against the retained record
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

from strif import atomic_output_file

from devtools.census_chunk_taxonomy import band, is_tilted, manifest, wall_seating

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATLAS = ROOT / "atlas" / "known-best"
CENSUS = ATLAS / "chunk-components.json"
GRAMMAR = ATLAS / "contact-assembly-grammar.yaml"
RECORD = (
    ROOT
    / "campaign"
    / "series"
    / "series-000-smoke-and-calibration"
    / "results"
    / "bc-019-assembly-coverage.json"
)

HORIZON = 30
"""`BC-019`'s own scope. The corpus runs to 100 and the question does not."""

RIGID_LATTICE = ("bar", "L", "rectangle")
"""The shapes the `rigid-lattice` primitive covers. A singleton is a free square, not an
assembly, and is counted separately in the complexity tuple."""


def serialized(record: dict[str, Any]) -> str:
    return json.dumps(record, indent=2, sort_keys=True) + "\n"


def complexity(entry: dict[str, Any]) -> dict[str, Any]:
    """The contract's ordered tuple, for a record whose components are all expressible."""
    assemblies = [c for c in entry["components"] if c["shape"] in RIGID_LATTICE]
    return {
        "free_square_count": int(entry["free_square_count"]),
        "assembly_count": len(assemblies),
        "internal_slide_dof": 0,
        "internal_slide_dof_basis": (
            "zero by the rigid-lattice primitive's semantics -- fixed integer offsets in "
            "one fitted orientation -- and not by evaluating D = 2m - rank(A_normal) - 2, "
            "which prices a contact-scaffold. The detector finds no contact scaffolds here."
        ),
        "fitted_angle_class_count": int(entry["angle_class_count"]),
        "mandatory_contact_count": sum(
            len(component["internal_edges"]) for component in entry["components"]
        ),
        "largest_assembly_size": max((int(c["size"]) for c in assemblies), default=0),
    }


def limitation(entry: dict[str, Any], seated: dict[str, set[str]]) -> dict[str, Any]:
    """What the grammar could not express here, in the terms `X-008` measured."""
    unexpressed = [
        {
            "id": str(component["id"]),
            "shape": str(component["shape"]),
            "size": int(component["size"]),
            "tilted": is_tilted(str(component["angle_degrees"])),
            "walls_touched": len(
                set().union(*(seated.get(str(m), set()) for m in component["members"]))
            ),
            "is_the_whole_record": int(component["size"]) == int(entry["n"]),
        }
        for component in entry["components"]
        if component["shape"] not in RIGID_LATTICE and component["shape"] != "singleton"
    ]
    return {
        "kind": "unexpressed-components",
        "components": unexpressed,
        "missing_move": (
            "a primitive for axis-aligned polyominoes that are not a bar, rectangle or "
            "corner L. Every component listed here is untilted, which X-008 measures across "
            "the whole corpus: the grammar's gap is not about tilted assemblies."
        ),
        "not_a_verdict": (
            "the current detector did not express these; the census's known_gap says that "
            "is not a refutation of chunk expressibility until the minimal partition solver "
            "exists"
        ),
    }


def coverage() -> dict[str, Any]:
    entries = manifest()
    certified: list[dict[str, Any]] = []
    limited: list[dict[str, Any]] = []

    for entry in band():
        n = int(entry["n"])
        if n > HORIZON:
            continue
        common = {
            "n": n,
            "source": str(entries[n]["source"]["kind"]),
            "component_count": int(entry["component_count"]),
        }
        if int(entry["unsupported_component_count"]) == 0:
            certified.append({**common, "complexity": complexity(entry)})
        else:
            limited.append(
                {**common, "limitation": limitation(entry, wall_seating(entries[n]))}
            )

    return {
        "schema_version": 1,
        "subject": {
            "commitment": "BC-019",
            "contract": "atlas/known-best/contact-assembly-grammar.yaml",
            "horizon": HORIZON,
            "band": "exact",
            "emits_no_verdict": (
                "descriptive; H-044 is untouched and a record without a certificate is one "
                "the current detector did not express, not one shown inexpressible"
            ),
        },
        "totals": {
            "records": len(certified) + len(limited),
            "certified": len(certified),
            "limited": len(limited),
        },
        "unfilled_contract_fields": [
            {
                "field": "mandatory contact graph with normal axis and sign",
                "why": (
                    "the census stores internal edges as square pairs with a residual and "
                    "records no normal axis or sign. Inferring one from lattice deltas "
                    "would be an assumption about the fit presented as a measurement."
                ),
            },
            {
                "field": "full-cell square-by-wall Boolean decision inventory",
                "why": (
                    "wall seating is retained per component here, which is coarser: it "
                    "counts distinct walls touched rather than deciding each square "
                    "against each wall. The full inventory is the full-cell control's."
                ),
            },
        ],
        "certified": certified,
        "limited": limited,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare against the record")
    args = parser.parse_args()

    built = coverage()
    if args.check:
        if not RECORD.exists():
            print(f"  {RECORD.name} is missing", file=sys.stderr)
            return 1
        if RECORD.read_text(encoding="utf-8") != serialized(built):
            print(f"  {RECORD.name} has drifted from a fresh pass", file=sys.stderr)
            return 1
        totals = built["totals"]
        print(
            f"  assembly coverage reproduces: {totals['certified']} certificates and "
            f"{totals['limited']} typed limitations over n <= {HORIZON}"
        )
        return 0

    with atomic_output_file(RECORD) as temporary:
        temporary.write_text(serialized(built), encoding="utf-8")
    print(f"wrote {RECORD.relative_to(ROOT.parent)}")
    totals = built["totals"]
    print(
        f"  {totals['certified']} certificates, {totals['limited']} typed limitations, "
        f"{len(built['unfilled_contract_fields'])} contract fields the corpus cannot fill"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
