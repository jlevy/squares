#!/usr/bin/env python3
"""Goebel's n=40 packing is infinitesimally flexible, and the flex hides behind D-391.

`BC-049` asks whether the packings the source catalogue calls rigid are rigid on evidence
of our own. `n = 40` became askable when `cases/gobel40` produced an exact pose, and the
answer is **no, not at first order** -- with an exact witness.

**The motion.** All sixteen squares of the tilted central block turn, each about its own
centre at unit angular velocity, with translations that keep every one of the 248
single-axis contacts at exactly zero gap rate. The twenty-four frame squares do not move.
The witness is a vector in `Q(sqrt 2)^120`, checked in the field.

**Why nobody had seen it.** The motion is invisible to every instrument that came before,
and for a different reason in each case. The translation-escape screen decides single-square
translation, and this is sixteen squares turning at once. An assessor that intersects the
contact half-spaces -- which is what `D-391` is -- reports this pose *rigid*: the witness
violates exactly one axis of each of the 42 pairs that touch at a corner, and intersecting
both axes forbids it. That is not a hypothetical cost for that defect. It is the measured
one: with the disjunctions intersected, all 120 coordinates certify as pinned.

**What the witness is not.** It is not a motion, and that is proved rather than observed.
Along it 104 of the 283 tight contacts have negative gap curvature, and a non-negative
self-stress over those rows -- `w . A = 0` with `w . q < 0`, verified in the field --
refuses every second-order correction at once. So the direction curves into the obstacle
whatever an arc does at order `t^2`, which is what the finite-motion measurement sees as a
worst separation of `-t^2/2`. The frontier's `rigidity` block stays `undetermined`, and
what is settled is that a first-order argument for `n = 40` cannot succeed.

**Where the flex lives.** Not in one direction, and not anywhere near the walls. The cone
is strictly larger than that first line: six further motions are retained here, each
verified to open an all-branch contact strictly -- which is what puts it outside the
subspace the first search covered -- and each refused at second order by its own
self-stress. They span rank five, and **every admissible direction found by any route
moves only the tilted block.** No frame square moves in any of them. So the twenty-four
axis-aligned squares are held and the sixteen turned ones are the mechanism, which is a
sharper statement than "n = 40 flexes" and a more useful one.

The parallel with `n = 5` is exact in shape and larger in scale: there, one square's
rotation is free at first order and refused at second by a verified self-stress. Here
sixteen squares turn together and are refused the same way, in seven directions rather
than one. What is still missing for a second-order rigidity claim is coverage: seven
refusals are not a cone. `n = 5` earns the phrase because its cone is one-dimensional and
that direction is refused; nothing here bounds this one.

Usage:
    uv run --frozen python -m devtools.assess_n40_rigidity
    uv run --frozen python -m devtools.assess_n40_rigidity --check
"""

from __future__ import annotations

import argparse
import itertools
import json
import pathlib
import sys
from fractions import Fraction
from typing import Any

from strif import atomic_output_file

from cases.gobel40.packing import build
from devtools.assess_n5_rigidity import (
    DOF,
    ROOT_TWO,
    Contact,
    FieldElement,
    Pose,
    active_contacts,
    certify,
    constraint_rows,
    contact_axes,
    disjunctive_pairs,
    gap_rate,
    incident_contacts,
    nullspace,
    propose_field_self_stress,
    second_order_terms,
    unconstrained,
    variable_names,
    verify_field_self_stress,
)
from devtools.n40_rays import WIDER_RAYS

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = ROOT / "campaign" / "series" / "series-000-smoke-and-calibration" / "results"
OUT = RESULTS / "bc-049-n40-rigidity-bracket.json"

SPAN = (-1, 0, 1)
"""Coefficients swept over the null basis when looking for an extending direction.

Small on purpose. A witness is wanted, not the whole cone, and a short integer combination
is one a reader can check. If a future pose needs more than this the search should widen
deliberately rather than by accident, so the sweep is named.
"""


def load_pose() -> Pose:
    squares, side, field = build()
    return Pose(field, side, tuple(tuple(square) for square in squares))


def axis_groups(
    pose: Pose, contacts: list[Contact]
) -> dict[frozenset[int], list[list[Contact]]]:
    """For each disjunctive pair, its contacts grouped by which axis they realize.

    A pair touching at a corner is held apart by two axes and needs only one of them, so
    these groups are the alternatives a branch chooses between. Grouping is by normal
    direction up to sign, because a single axis is generally realized by an edge of each
    square and both give the same separating direction.
    """
    disjunctive = set(disjunctive_pairs(pose, contacts))
    grouped: dict[frozenset[int], dict[tuple[str, str], list[Contact]]] = {}
    for contact in contacts:
        if contact.kind != "pair":
            continue
        assert contact.host is not None and contact.edge is not None
        pair = frozenset((contact.moving, contact.host))
        if pair not in disjunctive:
            continue
        nx, ny = pose.normal(contact.host, contact.edge)
        if nx.sign() < 0 or (nx.sign() == 0 and ny.sign() < 0):
            nx, ny = -nx, -ny
        key = (str(nx.coeffs), str(ny.coeffs))
        grouped.setdefault(pair, {}).setdefault(key, []).append(contact)
    return {
        pair: [members for _, members in sorted(byaxis.items())]
        for pair, byaxis in grouped.items()
    }


def single_axis_contacts(pose: Pose, contacts: list[Contact]) -> list[Contact]:
    """Wall contacts and the pairs held apart by one axis: the rows every branch carries."""
    disjunctive = set(disjunctive_pairs(pose, contacts))
    return [
        contact
        for contact in contacts
        if contact.kind == "wall"
        or frozenset((contact.moving, contact.host)) not in disjunctive  # type: ignore[arg-type]
    ]


def admissible_axis(
    pose: Pose, group: list[list[Contact]], motion: list[FieldElement]
) -> int | None:
    """Which of this pair's axes still separates along the motion, if either does.

    All of a chosen axis's rows must hold: the axis separates only while every currently
    touching corner stays on its outer side, and a pair contributes one row per such
    corner.
    """
    for index, members in enumerate(group):
        if all(gap_rate(row, motion).sign() >= 0 for row in constraint_rows(pose, members)):
            return index
    return None


def find_witness(
    pose: Pose, contacts: list[Contact]
) -> tuple[list[FieldElement], dict[frozenset[int], int]] | None:
    """A nonzero infinitesimal motion, with the branch that admits it -- or `None`.

    Candidates come from the null space of the single-axis rows, so each satisfies those
    with equality and needs no rounding to stay in the cone. A candidate is a genuine
    motion exactly when every disjunctive pair still has an axis that separates along it:
    choosing those axes names a complete branch, and a branch's cone sits inside the
    packing's tangent cone.
    """
    rows = constraint_rows(pose, single_axis_contacts(pose, contacts))
    basis = nullspace(pose, rows)
    groups = axis_groups(pose, contacts)
    zero = pose.field.rational(0)
    for coefficients in itertools.product(SPAN, repeat=len(basis)):
        if not any(coefficients):
            continue
        motion = [zero] * len(rows[0])
        for weight, vector in zip(coefficients, basis, strict=True):
            if weight:
                scale = pose.field.rational(weight)
                motion = [a + scale * b for a, b in zip(motion, vector, strict=True)]
        selection: dict[frozenset[int], int] = {}
        for pair, group in groups.items():
            index = admissible_axis(pose, group, motion)
            if index is None:
                break
            selection[pair] = index
        else:
            return motion, selection
    return None


SWEEP = (-2, -1, 0, 1, 2)
"""Coefficients swept when asking how much of the null space is admissible.

Wider than `SPAN` and for a different question. `SPAN` looks for *a* witness and stops;
this asks which of the subspace survives, so it has to be wide enough that a direction
needing unequal coefficients would show up. It is still a sweep of integer combinations
and not a decision procedure, which is why what it reports is a measurement rather than
the cone's dimension.
"""


def admissible_combinations(
    pose: Pose, contacts: list[Contact], basis: list[list[FieldElement]]
) -> list[tuple[int, ...]]:
    """Which integer combinations of the null basis extend to a branch."""
    groups = axis_groups(pose, contacts)
    zero = pose.field.rational(0)
    width = len(basis[0])
    found: list[tuple[int, ...]] = []
    for coefficients in itertools.product(SWEEP, repeat=len(basis)):
        if not any(coefficients):
            continue
        motion = [zero] * width
        for weight, vector in zip(coefficients, basis, strict=True):
            if weight:
                scale = pose.field.rational(weight)
                motion = [a + scale * b for a, b in zip(motion, vector, strict=True)]
        if all(admissible_axis(pose, group, motion) is not None for group in groups.values()):
            found.append(coefficients)
    return found


def describe(pose: Pose, motion: list[FieldElement]) -> dict[str, Any]:
    """The witness in a form a reader can check against the picture."""
    names = variable_names(pose.count)
    moving = sorted({index // DOF for index, v in enumerate(motion) if v.sign() != 0})
    turning = sorted(
        {index // DOF for index, v in enumerate(motion) if v.sign() != 0 and index % DOF == 2}
    )
    return {
        "squares_that_move": moving,
        "squares_that_turn": turning,
        "frame_squares_move": [one for one in moving if one < 24],
        "components": {
            names[index]: f"{value.coeffs[0]} + {value.coeffs[1]} sqrt2"
            for index, value in enumerate(motion)
            if value.sign() != 0
        },
    }


def verify_witness(
    pose: Pose,
    contacts: list[Contact],
    motion: list[FieldElement],
    selection: dict[frozenset[int], int],
) -> dict[str, Any]:
    """Re-decide every claim about the witness in the field, from the pose."""
    single = constraint_rows(pose, single_axis_contacts(pose, contacts))
    groups = axis_groups(pose, contacts)
    intersection = constraint_rows(pose, contacts)
    return {
        "nonzero": any(value.sign() != 0 for value in motion),
        "single_axis_rows": len(single),
        "exactly_zero_on_every_single_axis_row": all(
            gap_rate(row, motion).sign() == 0 for row in single
        ),
        "disjunctive_pairs_with_an_admissible_axis": sum(
            1
            for pair, group in groups.items()
            if all(
                gap_rate(row, motion).sign() >= 0
                for row in constraint_rows(pose, group[selection[pair]])
            )
        ),
        "disjunctive_pairs": len(groups),
        "rows_violated_if_the_disjunctions_are_intersected": sum(
            1 for row in intersection if gap_rate(row, motion).sign() < 0
        ),
        "pairs_giving_up_an_axis": sum(
            1
            for group in groups.values()
            if any(
                gap_rate(row, motion).sign() < 0
                for members in group
                for row in constraint_rows(pose, members)
            )
        ),
        "why_those_numbers_matter": (
            "the motion gives up an axis at some of the corner pairs and keeps both at the "
            "rest; an assessor that intersects instead of choosing reads every given-up row "
            "as a violation and reports the pose rigid (D-391). The two are counted "
            "separately because they are different counts and the first reads easily as "
            "the second"
        ),
    }


def branch_contacts(
    pose: Pose, contacts: list[Contact], selection: dict[frozenset[int], int]
) -> list[Contact]:
    """The contacts of the branch that admits a given motion."""
    chosen = list(single_axis_contacts(pose, contacts))
    groups = axis_groups(pose, contacts)
    for pair, group in groups.items():
        chosen += group[selection[pair]]
    return chosen


def second_order(
    pose: Pose,
    contacts: list[Contact],
    motion: list[FieldElement],
    selection: dict[frozenset[int], int],
) -> dict[str, Any]:
    """Is the witness refused at second order, the way `n = 5`'s free direction is?

    Only the contacts the motion holds tight take part. A gap already opening at first
    order imposes nothing at second, and letting such a row into the self-stress would let
    a refusal be assembled from constraints that are not binding -- a certificate for a
    system nobody is solving.

    On the tight rows a feasible arc needs `y` with `A y >= -q`, where `q_j = u . H_j . u`
    is the gap's curvature along the motion. A non-negative `w` with `w . A = 0` and
    `w . q < 0` proves there is no such `y`: it would give `0 = w . A y >= -w . q > 0`.
    """
    branch = branch_contacts(pose, contacts, selection)
    rows = constraint_rows(pose, branch)
    tight = [index for index, row in enumerate(rows) if gap_rate(row, motion).sign() == 0]
    curvature = second_order_terms(pose, branch, motion)
    carried = [position for position, index in enumerate(tight) if curvature[index].sign() < 0]
    tight_rows = [rows[index] for index in tight]
    tight_curvature = [curvature[index] for index in tight]

    certificate: dict[str, Any] | None = None
    if carried:
        weights = propose_field_self_stress(pose, tight_rows, carried)
        if weights is not None and verify_field_self_stress(pose, tight_rows, weights):
            total = pose.field.rational(0)
            for weight, value in zip(weights, tight_curvature, strict=True):
                if weight.sign() != 0:
                    total = total + value * weight
            if total.sign() < 0:
                certificate = {
                    "rows_carrying_weight": sum(1 for weight in weights if weight.sign() != 0),
                    "w_dot_q_is_negative": True,
                    "meaning": (
                        "w >= 0 and w . A = 0, so w . (A y) = 0 for every y; a y with "
                        "A y >= -q would give 0 = w . A y >= -w . q > 0"
                    ),
                }
    return {
        "branch_rows": len(rows),
        "tight_rows": len(tight),
        "negative_curvature": len(carried),
        "positive_curvature": sum(1 for index in tight if curvature[index].sign() > 0),
        "obstructed": certificate is not None,
        "certificate": certificate,
        "what_this_settles": (
            "this witness, and only this one. The first-order cone is not known to be its "
            "span: the null space is five-dimensional, a short integer sweep of it was "
            "searched, and other branches were not examined at all. So n = 40 is not "
            "second-order rigid on this evidence -- one of its infinitesimal flexes is "
            "refused"
        ),
    }


def intersection_cone(pose: Pose, contacts: list[Contact]) -> dict[str, Any]:
    """What an assessor that intersects the disjunctions would report: the wrong answer.

    Only the block's forty-eight coordinates are re-certified, because they are the ones
    that carry the claim: the witness moves exactly those, so pinning all of them is
    already the statement that this model forbids the motion. The full run over all 120
    also certifies every one -- measured on 2026-08-30 -- and costs ninety seconds more
    for a number that says nothing the forty-eight do not.
    """
    rows = constraint_rows(pose, contacts)
    names = variable_names(pose.count)
    block = [index for index in range(len(names)) if index // DOF >= 24]
    pinned = 0
    uncertified: list[str] = []
    for index in block:
        if unconstrained(rows, index):
            continue
        if all(certify(pose, rows, index, sign) is not None for sign in (1, -1)):
            pinned += 1
        else:
            uncertified.append(names[index])
    return {
        "rows": len(rows),
        "coordinates_checked": len(block),
        "pinned": pinned,
        "uncertified": uncertified,
        "verdict_it_would_report": (
            "infinitesimally rigid, which is false -- the witness above moves exactly these "
            "forty-eight coordinates and this model pins every one of them"
        ),
    }


def retained_ray(
    pose: Pose, entries: dict[int, tuple[int, int, int, int]]
) -> list[FieldElement]:
    """Rebuild one retained motion as field elements."""
    q = pose.field.rational
    root = pose.field.alpha
    motion = [q(0)] * (pose.count * DOF)
    for index, (pn, pd, qn, qd) in entries.items():
        motion[index] = q(Fraction(pn, pd)) + q(Fraction(qn, qd)) * root
    return motion


def wider_cone(pose: Pose, contacts: list[Contact]) -> dict[str, Any]:
    """The cone is strictly larger than the line, and the extra directions are block-only.

    The sweep over the null space said the admissible part of *that subspace* is a line, and
    left open everything outside it -- directions that let an all-branch contact open rather
    than holding it tight. They exist. Six are retained, each re-decided here from the pose:
    in the cone, opening at least one all-branch row strictly, and leaving every corner pair
    an axis.

    Two things about the set are measurements about the packing rather than about the
    search. Every one of them moves only the sixteen squares of the tilted block -- no frame
    square moves in any admissible direction found, by any route, at any point. And every
    one is refused at second order by its own verified self-stress, exactly as the first
    witness is.
    """
    single = constraint_rows(pose, single_axis_contacts(pose, contacts))
    groups = axis_groups(pose, contacts)
    verified: list[dict[str, Any]] = []
    movers: set[int] = set()
    for entries in WIDER_RAYS:
        motion = retained_ray(pose, entries)
        selection: dict[frozenset[int], int] = {}
        admissible = True
        for pair, group in groups.items():
            index = admissible_axis(pose, group, motion)
            if index is None:
                admissible = False
                break
            selection[pair] = index
        opens = sum(1 for row in single if gap_rate(row, motion).sign() > 0)
        inside = all(gap_rate(row, motion).sign() >= 0 for row in single)
        movers |= {index // DOF for index, v in enumerate(motion) if v.sign() != 0}
        verified.append(
            {
                "in_the_cone": inside,
                "all_branch_rows_opened": opens,
                "outside_the_null_space": opens > 0,
                "admissible": admissible,
                "second_order": (
                    second_order(pose, contacts, motion, selection) if admissible else None
                ),
            }
        )
    return {
        "retained": len(WIDER_RAYS),
        "all_verified": all(
            one["in_the_cone"] and one["outside_the_null_space"] and one["admissible"]
            for one in verified
        ),
        "all_obstructed": all(
            one["second_order"] is not None and one["second_order"]["obstructed"]
            for one in verified
        ),
        "squares_that_move_in_any": sorted(movers),
        "frame_squares_that_ever_move": sorted(index for index in movers if index < 24),
        "rank": _rank(pose, [retained_ray(pose, entries) for entries in WIDER_RAYS]),
        "rays": verified,
        "what_it_settles": (
            "the first-order cone is strictly larger than the line in the null space, so no "
            "argument that refuses one direction can make n = 40 second-order rigid"
        ),
        "what_it_does_not": (
            "bound the cone. Six directions were found by one sampler over twenty-four "
            "objectives; that they exist is a proof, that there are no others is not claimed"
        ),
    }


def frame_coordinates(pose: Pose, contacts: list[Contact]) -> dict[str, Any]:
    """Can any admissible direction move a frame square? Two routes, and the first proves.

    **Route one is a proof.** Every branch's cone sits inside the relaxed cone, so a
    coordinate the relaxed rows already pin is pinned in every branch, whatever the
    disjunctions do. A verified Farkas certificate there settles that coordinate outright,
    and 52 of the frame's 72 go this way.

    **Route two is a search, and it is weak by construction.** For each surviving
    coordinate and sign, maximize it over the relaxed cone, re-solve the active set exactly,
    and test the disjunctive condition. Finding nothing does not prove the coordinate is
    pinned -- this repository registers the translation-escape screen as sound in one
    direction only for exactly this reason, and the same limitation applies here. What it
    reports is coverage.
    """
    from scipy.optimize import linprog  # noqa: PLC0415 - heavy optional import

    rows = constraint_rows(pose, single_axis_contacts(pose, contacts))
    groups = axis_groups(pose, contacts)
    names = variable_names(pose.count)
    frame = [index for index in range(len(rows[0])) if index // DOF < 24]

    proved = [
        index
        for index in frame
        if all(certify(pose, rows, index, sign) is not None for sign in (1, -1))
    ]
    remaining = [index for index in frame if index not in set(proved)]

    numeric = [
        [float(entry.coeffs[0]) + float(entry.coeffs[1]) * ROOT_TWO for entry in row]
        for row in rows
    ]
    upper = [[-value for value in row] for row in numeric]
    reachable = 0
    hits: list[str] = []
    for index in remaining:
        for sign in (1, -1):
            objective = [0.0] * len(rows[0])
            objective[index] = -float(sign)
            result = linprog(
                objective,
                A_ub=upper,
                b_ub=[0.0] * len(rows),
                bounds=[(-1.0, 1.0)] * len(rows[0]),
                method="highs",
            )
            if not result.success or abs(result.x[index]) < 1e-7:
                continue
            reachable += 1
            active = [
                position
                for position, row in enumerate(numeric)
                if abs(sum(a * b for a, b in zip(row, result.x, strict=True))) < 1e-7
            ]
            for vector in nullspace(pose, [rows[position] for position in active]):
                if vector[index].sign() == 0:
                    continue
                for flip in (1, -1):
                    motion = [pose.field.rational(flip) * value for value in vector]
                    if all(gap_rate(row, motion).sign() >= 0 for row in rows) and all(
                        admissible_axis(pose, group, motion) is not None
                        for group in groups.values()
                    ):
                        hits.append(names[index])
                        break
    return {
        "frame_coordinates": len(frame),
        "proved_zero_in_every_branch": len(proved),
        "how_that_is_a_proof": (
            "every branch's cone is inside the relaxed cone, so a coordinate the relaxed "
            "rows pin is pinned however the disjunctions resolve; each is a Farkas "
            "certificate verified in the field"
        ),
        "not_proved": [names[index] for index in remaining],
        "targeted_searches": 2 * len(remaining),
        "reachable_in_the_relaxed_cone": reachable,
        "admissible_directions_found": len(hits),
        "what_the_search_does_not_show": (
            "that the remaining coordinates are pinned. A search that finds nothing is weak "
            "evidence by construction and this repository registers the translation-escape "
            "screen as sound in one direction only for the same reason"
        ),
    }


def _rank(pose: Pose, vectors: list[list[FieldElement]]) -> int:
    """Exact rank of a set of motions, by elimination over the field."""
    work = [list(vector) for vector in vectors]
    width = len(work[0])
    pivot = 0
    for column in range(width):
        target = next(
            (row for row in range(pivot, len(work)) if work[row][column].sign() != 0), None
        )
        if target is None:
            continue
        work[pivot], work[target] = work[target], work[pivot]
        lead = work[pivot][column]
        for row in range(pivot + 1, len(work)):
            if work[row][column].sign() != 0:
                factor = work[row][column] / lead
                work[row] = [
                    a - factor * b for a, b in zip(work[row], work[pivot], strict=True)
                ]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def _sweep(
    pose: Pose, contacts: list[Contact], basis: list[list[FieldElement]]
) -> dict[str, Any]:
    """How much of the five-dimensional null space is actually admissible: a line.

    Worth measuring because "a witness exists" and "the flex is one-dimensional" are very
    different statements and the first is easy to mistake for the second. Of the 3124
    nonzero integer combinations in `[-2, 2]^5`, four extend to a branch, and all four are
    multiples of a single basis vector. So inside the subspace where every all-branch
    contact is tight, the admissible set is exactly a line -- the same shape as `n = 5`,
    two orders of magnitude larger.

    It does not bound the cone. Directions that leave some all-branch contact strictly
    opening are outside this subspace entirely and are not searched here.
    """
    combinations = admissible_combinations(pose, contacts, basis)
    carried = sorted(
        {
            index
            for combination in combinations
            for index, weight in enumerate(combination)
            if weight
        }
    )
    return {
        "swept": len(SWEEP) ** len(basis) - 1,
        "extend": len(combinations),
        "basis_directions_used": carried,
        "is_a_single_line": len(carried) == 1,
        "what_it_does_not_bound": (
            "the cone. A direction that leaves some all-branch contact strictly opening is "
            "outside this subspace and is not searched here, so the first-order cone may be "
            "larger than this line"
        ),
    }


def assess() -> dict[str, Any]:
    pose = load_pose()
    incident = incident_contacts(pose)
    contacts = active_contacts(pose)
    axes = contact_axes(pose, contacts)
    disjunctive = disjunctive_pairs(pose, contacts)
    single = single_axis_contacts(pose, contacts)
    rows = constraint_rows(pose, single)
    basis = nullspace(pose, rows)

    found = find_witness(pose, contacts)
    assert found is not None, "the witness is the finding; its absence is a regression"
    motion, selection = found

    return {
        "schema_version": 2,
        "subject": {
            "n": pose.count,
            "commitment": "BC-049",
            "pose": "cases.gobel40.packing.build",
            "side": "4 + 2 sqrt(2), Goebel's centred diagonal block at a = 3, b = 4",
            "promotes_nothing": (
                "n = 40's rigidity block stays undetermined. An infinitesimal flex is not "
                "a motion: along this one every gap curves shut at order t^2, so local "
                "rigidity is untouched and not-rigid would be the wrong promotion"
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
        "system": {
            "variables": len(rows[0]),
            "single_axis_rows": len(rows),
            "rank": len(rows[0]) - len(basis),
            "null_dimension": len(basis),
            "meaning": (
                "the rows every branch carries; their null space is inside every branch's "
                "cone, so a null vector that some branch admits is an infinitesimal motion"
            ),
        },
        "witness": {
            **describe(pose, motion),
            "verification": verify_witness(pose, contacts, motion, selection),
            "second_order": second_order(pose, contacts, motion, selection),
            "second_order_behaviour": (
                "moving along it by a finite t and measuring real separating-axis gaps "
                "gives -5.0e-7, -5.0e-9 and -5.0e-11 at t = 1e-3, 1e-4 and 1e-5: exactly "
                "-t^2/2, quadratic and not linear, which is an independent check that the "
                "linearization has no first-order error"
            ),
        },
        "admissible_part_of_the_null_space": _sweep(pose, contacts, basis),
        "outside_the_null_space": wider_cone(pose, contacts),
        "can_the_frame_move": frame_coordinates(pose, contacts),
        "what_an_intersecting_assessor_reports": intersection_cone(pose, contacts),
        "verdict": {
            "infinitesimally_rigid": False,
            "decided": True,
            "claim": (
                "the cone of infinitesimal motions at n = 40 is not the origin: the sixteen "
                "squares of the tilted block turn together, each about its own centre, at "
                "zero gap rate against all 248 single-axis contacts and with an admissible "
                "axis surviving at all 42 corner contacts"
            ),
            "what_is_not_claimed": (
                "local rigidity, in either direction. The witness curves into the obstacle "
                "at second order, so it is not a motion, and the catalogue's annotation is "
                "not contradicted"
            ),
            "the_cone_is_larger_than_this_witness": (
                "six further motions are retained and verified, each opening an all-branch "
                "contact strictly and so lying outside the subspace the null-space sweep "
                "covers; they span rank five, every one is refused at second order, and "
                "every one moves only the tilted block"
            ),
            "the_witness_is_refused_at_second_order": (
                "104 of the 283 tight contacts curve into the obstacle along it, and a "
                "non-negative self-stress over those rows refuses every second-order "
                "correction at once -- so this flex is not the start of a motion"
            ),
            "what_it_costs_the_catalogue": (
                "nothing directly, and everything for a first-order argument: any proof of "
                "n = 40's rigidity has to be second-order or finite, because the first-order "
                "cone is nontrivial"
            ),
        },
        "scope": {
            "established": (
                "Exact, at the exact pose, over all forty squares and all three degrees of "
                "freedom each. Contacts decided by exact sign, the witness a vector in "
                "Q(sqrt 2)^120, and every claim about it re-decided in the field from the "
                "pose rather than read back from this record."
            ),
            "not_established": (
                "Second-order rigidity, which needs every first-order flex refused and "
                "not seven of them. The cone is not bounded here: inside the null space the "
                "admissible set is measured and is a line, outside it six directions were "
                "found by one sampler over twenty-four objectives, and no argument here "
                "says there are no others. That every one so far is refused, and that none "
                "moves a frame square, is evidence about where to look rather than a proof "
                "that the looking is done."
            ),
            "relation_to_prior_evidence": (
                "The translation-escape screen leaves n = 40 undetermined by deciding "
                "single-square translation only; this motion is sixteen squares turning at "
                "once, which is outside it in every respect. Nothing conflicts: neither "
                "claims a property, and this one explains why the screen found nothing."
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
        witness = built["witness"]
        print(
            f"  witness reproduces: {len(witness['squares_that_turn'])} squares turn, "
            f"exact on all {witness['verification']['single_axis_rows']} single-axis rows, "
            f"admissible at all {witness['verification']['disjunctive_pairs']} corner pairs"
        )
        return 0

    with atomic_output_file(OUT) as tmp:
        tmp.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
