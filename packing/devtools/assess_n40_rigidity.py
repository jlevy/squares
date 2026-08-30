#!/usr/bin/env python3
"""Bracket the first-order rigidity of Goebel's n=40 packing, and refuse to decide it.

`BC-049` asks whether the packings the source catalogue calls rigid are rigid on evidence
of our own. `n = 40` became askable when `cases/gobel40` produced an exact pose, and the
answer is that this repository cannot yet give one -- for a reason that is measured here
rather than asserted.

**The obstruction is the contact model, not the field.** `D-388` predicted that `n = 40`
would need a Farkas search whose weights live in `Q(sqrt 2)`; that search now exists and
reproduces `n = 5` exactly. It was not enough. Two further defects turned up the first time
it ran, both absent at `n = 5` and both flattering: `D-390`, an incidence read as a contact,
and `D-391`, a tangent cone that is a union of half-spaces being intersected.

**What can be said is a bracket.** With `D-390`'s spurious rows removed, two polyhedral
models sit either side of the truth, and the gap between them is exactly the 42 pairs that
touch at a corner:

- **Intersect** the disjunctions and the cone is contained in every branch, so any nonzero
  direction it admits is a genuine infinitesimal motion. It admits none: all 120
  coordinates are pinned by certificates verified in the field. No flex can be exhibited
  this cheaply.
- **Drop** them and the cone contains every branch, so pinning every coordinate would prove
  rigidity outright. It pins 56 of 120. Rigidity is not proved.

So `n = 40` is first-order **undecided**, with the two sides measured and the distance
between them named. Deciding it is `2^42` linear programs by the route
`cases/trump11/tangent_cones.py` takes at `n = 11`, where the same enumeration is `2^7`.

Nothing here promotes a frontier record. `n = 40`'s `rigidity` block stays `undetermined`
on the translation-escape screen's evidence, which is a different and weaker instrument;
this adds a first-party bracket, not a property.

Usage:
    uv run --frozen python -m devtools.assess_n40_rigidity
    uv run --frozen python -m devtools.assess_n40_rigidity --check
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

from strif import atomic_output_file

from cases.gobel40.packing import build
from devtools.assess_n5_rigidity import (
    Contact,
    Pose,
    active_contacts,
    certify,
    constraint_rows,
    contact_axes,
    disjunctive_pairs,
    incident_contacts,
    unconstrained,
    variable_names,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = ROOT / "campaign" / "series" / "series-000-smoke-and-calibration" / "results"
OUT = RESULTS / "bc-049-n40-rigidity-bracket.json"


def load_pose() -> Pose:
    squares, side, field = build()
    return Pose(field, side, tuple(tuple(square) for square in squares))


def relaxed_contacts(pose: Pose, contacts: list[Contact]) -> list[Contact]:
    """Wall contacts, and only the pairs held apart by a single axis.

    Every branch of the disjunction is a superset of this row set, so its cone contains
    every branch's cone. A coordinate pinned here is pinned however the disjunctions
    resolve -- which is what makes a verdict of rigidity from this model sound, and what
    makes its silence uninformative.
    """
    single = {pair for pair, axes in contact_axes(pose, contacts).items() if len(axes) == 1}
    return [
        contact
        for contact in contacts
        if contact.kind == "wall" or frozenset((contact.moving, contact.host)) in single  # type: ignore[arg-type]
    ]


def cone(pose: Pose, rows: list[list[Any]]) -> dict[str, Any]:
    """Which coordinates this row set pins, with every certificate verified in the field."""
    names = variable_names(pose.count)
    pinned: list[str] = []
    uncertified: list[str] = []
    free: list[str] = []
    for index, name in enumerate(names):
        if unconstrained(rows, index):
            free.append(name)
        elif all(certify(pose, rows, index, sign) is not None for sign in (1, -1)):
            pinned.append(name)
        else:
            uncertified.append(name)
    return {
        "rows": len(rows),
        "pinned": len(pinned),
        "uncertified": uncertified,
        "free": free,
    }


def assess() -> dict[str, Any]:
    pose = load_pose()
    incident = incident_contacts(pose)
    contacts = active_contacts(pose)
    axes = contact_axes(pose, contacts)
    disjunctive = disjunctive_pairs(pose, contacts)
    relaxed = relaxed_contacts(pose, contacts)

    upper = cone(pose, constraint_rows(pose, relaxed))
    lower = cone(pose, constraint_rows(pose, contacts))

    return {
        "schema_version": 1,
        "subject": {
            "n": pose.count,
            "commitment": "BC-049",
            "pose": "cases.gobel40.packing.build",
            "side": "4 + 2 sqrt(2), Goebel's centred diagonal block at a = 3, b = 4",
            "promotes_nothing": (
                "n = 40's rigidity block stays undetermined on the translation-escape "
                "screen's evidence; this is a first-party bracket, not a property"
            ),
        },
        "contact_model": {
            "incidences": len(incident),
            "contacts": len(contacts),
            "merely_incident": len(incident) - len(contacts),
            "why_that_gap_exists": (
                "a corner landing on the endpoint of a host edge is an incidence, and the "
                "edge separates the two squares only if the whole moving square lies on its "
                "outer side; edge-to-edge neighbours fail that on two of four edges (D-390)"
            ),
            "touching_pairs": len(axes),
            "disjunctive_pairs": len(disjunctive),
            "why_those_cannot_be_intersected": (
                "a pair touching at one corner is held apart by two axes and non-overlap "
                "asks that either keep separating, so the tangent cone is a union of "
                "half-spaces rather than their intersection (D-391)"
            ),
        },
        "bracket": {
            "upper_model": {
                "rows": "walls, and the pairs held apart by a single axis",
                "contains": "every branch of the disjunction",
                "so_pinning_everything_would_prove": "infinitesimal rigidity, outright",
                **upper,
            },
            "lower_model": {
                "rows": "walls, and every separating pair row including both axes",
                "contained_in": "every branch of the disjunction",
                "so_any_nonzero_direction_would_prove": "an infinitesimal flex, outright",
                **lower,
            },
        },
        "verdict": {
            "infinitesimally_rigid": None,
            "decided": False,
            "claim": (
                "n = 40's first-order cone is bracketed and not decided: the model "
                "contained in every branch is trivial, so no flex is exhibited, and the "
                "model containing every branch pins 56 of 120 coordinates, so rigidity is "
                "not proved"
            ),
            "what_would_decide_it": (
                "enumerating the 2^42 branchwise cones, which is what "
                "cases/trump11/tangent_cones.py does at n = 11 for 2^7 = 128 of them; a "
                "branch-and-bound that prunes on a fully pinned prefix is the same "
                "instrument and may not need every leaf"
            ),
            "what_is_not_the_obstruction": (
                "the field. D-388 named the mixed rows as what stopped the assessor here, "
                "and the ordered-field search that answers them exists and reproduces n = 5 "
                "exactly. It ran on this pose and the answer it gave was governed by the "
                "contact model instead"
            ),
        },
        "scope": {
            "established": (
                "Exact, at the exact pose, over all forty squares and all three degrees of "
                "freedom each. Both models are built from contacts decided by exact sign "
                "and every certificate is verified in Q(sqrt 2). The bracket itself is the "
                "finding: 120 of 120 pinned below, 56 of 120 above."
            ),
            "not_established": (
                "First-order rigidity, in either direction. The lower model's triviality is "
                "not rigidity -- it is the absence of a cheap flex -- and the upper model's "
                "64 uncertified coordinates are not motions. Second-order questions do not "
                "arise until the first-order cone is known."
            ),
            "relation_to_prior_evidence": (
                "The translation-escape screen leaves n = 40 undetermined by deciding "
                "single-square translation only. This is stronger in covering rotation and "
                "all forty squares at once, and weaker in reaching no verdict; the two do "
                "not conflict because neither claims a property."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="compare against the retained record"
    )
    args = parser.parse_args()

    built = assess()
    if args.check:
        if not OUT.exists():
            print(f"  {OUT.name} is missing", file=sys.stderr)
            return 1
        if json.loads(OUT.read_text(encoding="utf-8")) != built:
            print(f"  {OUT.name} has drifted from a fresh assessment", file=sys.stderr)
            return 1
        model = built["contact_model"]
        print(
            f"  n=40 contact model reproduces: {model['merely_incident']} of "
            f"{model['incidences']} incidences are not contacts, "
            f"{model['disjunctive_pairs']} of {model['touching_pairs']} touching pairs are "
            "disjunctive"
        )
        bracket = built["bracket"]
        print(
            f"  bracket reproduces: {bracket['lower_model']['pinned']}/120 pinned below, "
            f"{bracket['upper_model']['pinned']}/120 above -- undecided"
        )
        return 0

    with atomic_output_file(OUT) as tmp:
        tmp.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
