#!/usr/bin/env python3
"""Contract for contact-feature identification and system assembly.

The check that decides whether assembly is right is not a count.
It is whether the packing the structure was extracted from *satisfies the equations
assembly wrote down*: at Trump's `n = 11` the residual is at the double-precision noise
floor, and a mistyped contact or a wrong feature moves it by orders of magnitude.

Three findings are asserted here rather than described, because each contradicts what
the promotion spec expected and a future reader should meet them as measurements:

- **counting rows is the wrong instrument.**  At `n = 11` there are 42 contact equations
  against 34 unknowns, and the surplus of eight says nothing about whether they determine
  the pose.  The rank does, and closure is sized by it.
- **`edge-edge` pins collinearity, which is two conditions, and reading it as one was a
  bug that looked like mathematics.**  A single endpoint on the other edge's line leaves
  the second square free to pivot about that point, satisfying the equation while the
  edge digs in linearly -- measured at `n = 11` as overlaps of `-5.1e-6`, `-4.2e-6` and
  `-3.2e-6` at a step of `1e-5`, on three declared edge-edge pairs, growing linearly in
  the step.  With the second equation the contact Jacobian reaches **full rank at both
  retained sizes**, `34` of `34` at `n = 11` and `88` of `88` at `n = 29`.  The four and
  seven "stationarity conditions" an earlier version reported were missing collinearity
  equations, not missing theory.
- **an angle class does not license an angle identity.**  Classes are decided modulo
  ninety degrees, so `t_i = t_j` is false for a class member a quarter or half turn from
  another.  Emitting those identities left `n = 11` at the noise floor -- its classes
  happen to have equal angles -- and drove `n = 29` to a residual of exactly `pi`.
- **a pose is a centre, an angle, *and* a chirality.**  Seven of the `n = 29` layout's
  twenty-nine squares are built inside `scale(-1 1)` mirror groups, and a
  centre-plus-rotation cannot produce a clockwise winding.  Read as rotations they left
  the `n = 29` residual at `2.0`; with the reflection carried in the corner model it
  falls to `1.3e-15`.  That number is why chirality is data on the structure rather than
  something assembly infers.

The order of the checks in `main` is load-bearing in one place: the `side_leak` check
runs before the equation count, so restoring the single-endpoint `edge-edge` equation
trips the *geometric* assertion rather than an arithmetic one.  A control that proves
"the count moved" is much weaker than one that proves "a contact-preserving motion can
now shrink the container".

The reflected case is exercised on a *mirrored copy of `n = 11`* rather than on `n = 29`
itself.  Mirroring an exact packing gives an all-`-1` chirality whose right answer is
already known -- same contacts, same side -- so the reflected path is checked against
something rather than only against itself, and without the hundred-digit walk.
"""

from __future__ import annotations

import dataclasses
from collections import Counter

import mpmath as mp

from cases.gobel5 import packing as gobel5
from cases.trump11 import packing as trump11
from sqpack.promote.contacts import Incidence, extract_contacts
from sqpack.promote.system import (
    SystemAssemblyError,
    assemble,
    close,
    jacobian_rank,
    pose_values,
    residual_at,
)
from sqpack.verify import float_sign

PRECISION = 40


def as_floats(field, squares, side):
    numbers = [
        [(float(field.decimal(x, 30)), float(field.decimal(y, 30))) for x, y in square]
        for square in squares
    ]
    return numbers, float(field.decimal(side, 30))


def features_are_identified_and_typed() -> None:
    """Every contact says which features meet, and the counts are the known ones."""
    squares, side, field = trump11.build()
    structure = extract_contacts(squares, side, sign=field.sign)

    assert len(structure.pair_contacts) == 14, "the 14 zero-gap pairs moved"
    assert len(structure.wall_contacts) == 20, "the 20 boundary coordinates moved"
    assert not structure.ambiguous, "exact arithmetic reported an ambiguous band"

    for incidence in structure.pair_contacts:
        assert incidence.contact in {"corner-edge", "edge-edge", "corner-corner"}
        assert incidence.left_feature and incidence.right_feature

    kinds = Counter(incidence.contact for incidence in structure.pair_contacts)
    assert kinds == Counter({"edge-edge": 7, "corner-edge": 6, "corner-corner": 1}), (
        f"the n = 11 contact typing changed: {dict(kinds)}"
    )

    # The corner-corner one is the pair whose supports disagree across axes; it is the
    # reason features are intersected rather than read off a single axis.
    corner_corner = [
        incidence
        for incidence in structure.pair_contacts
        if incidence.contact == "corner-corner"
    ]
    assert (corner_corner[0].left, corner_corner[0].right) == (4, "5"), (
        "the diagonally-touching pair moved; if squares 4 and 5 no longer meet at a "
        "point, the per-axis-support trap this guards against has moved with them"
    )

    for incidence in structure.wall_contacts:
        assert incidence.contact == "corner-wall"


def the_packing_satisfies_its_own_equations() -> None:
    """The decisive check: assembled equations vanish at the pose they came from."""
    previous = mp.mp.dps
    mp.mp.dps = PRECISION
    try:
        squares, side, field = trump11.build()
        field.refine_to(PRECISION)
        structure = extract_contacts(squares, side, sign=field.sign)
        system = assemble(structure)
        numbers, side_value = as_floats(field, squares, side)
        residuals = residual_at(system, pose_values(system, numbers, side_value))
        worst = max(abs(value) for value in residuals)
        assert worst < 1e-12, (
            f"the assembled equations do not vanish at the packing they describe "
            f"(worst {worst:.3e}); assembly has written down a different system"
        )

        # And they are discriminating: retyping one contact breaks them.
        broken = list(structure.pair_contacts)
        first = broken[0]
        broken[0] = Incidence(
            kind=first.kind,
            left=first.left,
            right=first.right,
            margin=first.margin,
            contact="corner-corner" if first.contact != "corner-corner" else "edge-edge",
            left_feature="corner:0",
            right_feature="corner:2",
        )
        mistyped = assemble(dataclasses.replace(structure, pair_contacts=tuple(broken)))
        mistyped_residuals = residual_at(mistyped, pose_values(mistyped, numbers, side_value))
        assert max(abs(value) for value in mistyped_residuals) > 1e-6, (
            "retyping a contact left the residuals at the noise floor, so this check "
            "cannot tell a right structure from a wrong one"
        )
    finally:
        mp.mp.dps = previous


def the_contact_equations_determine_the_pose() -> None:
    """The measurement that says `close` has nothing to add at `n = 11`.

    `plan-2026-08-28-promotion-pipeline-implementation` phase 2 proposes withholding
    `close()` and requiring the unclosed system to be reported *underdetermined*, which
    presumes the count answers the question.  It does not, and neither does it here in
    the direction first recorded: the contacts, written down correctly, isolate the pose
    outright.
    """
    previous = mp.mp.dps
    mp.mp.dps = PRECISION
    try:
        squares, side, field = trump11.build()
        field.refine_to(PRECISION)
        structure = extract_contacts(squares, side, sign=field.sign)
        system = assemble(structure)

        assert system.unknown_count == 3 * 11 + 1 == 34
        assert len(system.equations) == 42, (
            "the n = 11 equation count moved; corner-corner and edge-edge each contribute "
            "two scalar equations and the others one, so this count is the typing's "
            "arithmetic"
        )
        assert system.state() == "overdetermined", system.summary()
        assert system.angle_identities == 0, (
            "an angle identity was emitted; classes hold modulo ninety degrees and do "
            "not license one"
        )

        numbers, side_value = as_floats(field, squares, side)
        values = pose_values(system, numbers, side_value)
        info = jacobian_rank(system, values)
        assert info["rank"] == 34 and info["shortfall"] == 0, (
            f"the n = 11 contact Jacobian no longer determines the pose: {info}. Full "
            "rank here is what says no stationarity condition is missing at this size"
        )

        try:
            close(system, values)
        except SystemAssemblyError as error:
            assert error.kind == "already-determined", error.kind
        else:
            raise AssertionError(
                "close() added conditions to a system that already isolates its pose, "
                "which is an invented constraint"
            )
    finally:
        mp.mp.dps = previous


def an_edge_edge_contact_pins_collinearity_not_incidence() -> None:
    """Why `edge-edge` is two equations, checked by the motion the missing one allowed.

    One endpoint of the right edge on the left edge's *line* says the lines meet.  It
    leaves the right square free to pivot about that point, and the pivot satisfies the
    equation while driving the squares into each other at first order.  `side_leak` is
    exactly that: the norm of the projection of the side's unit vector onto the null
    space, so a non-zero reading means a contact-preserving motion can shrink the
    container.  It was `1.86e-1` here with the equation missing.
    """
    previous = mp.mp.dps
    mp.mp.dps = PRECISION
    try:
        squares, side, field = trump11.build()
        field.refine_to(PRECISION)
        structure = extract_contacts(squares, side, sign=field.sign)
        assert any(item.contact == "edge-edge" for item in structure.pair_contacts), (
            "n = 11 reports no edge-edge contact, so this check exercises nothing"
        )
        system = assemble(structure)
        numbers, side_value = as_floats(field, squares, side)
        info = jacobian_rank(system, pose_values(system, numbers, side_value))
        assert info["side_leak"] < 1e-12, (
            f"the null space of the n = 11 contact Jacobian contains directions that "
            f"change the side (side_leak {info['side_leak']:.3e}); those are "
            "contact-preserving first-order motions that shrink the container, and the "
            "packing would not be a local optimum of its own system"
        )
    finally:
        mp.mp.dps = previous


def closure_is_supplied_only_where_the_rank_says_it_is_missing() -> None:
    """Two sizes, two answers -- and after the edge-edge repair they are 1 and none.

    Göbel's `n = 5` has no edge-edge contact at all and keeps a genuine shortfall of one.
    Trump's `n = 11` has seven, and with them written down correctly its contacts isolate
    the pose, so `close` refuses.  A `close` that returned a fixed number, or one derived
    from the row count, would get both wrong.

    The `already-determined` refusal had **no case** when it was written, and this file
    said so.  It has two now, which is the branch's first exercise and the clearest sign
    the shortfall it used to report was an artefact.
    """
    previous = mp.mp.dps
    mp.mp.dps = PRECISION
    try:
        squares, side, field = gobel5.build()
        field.refine_to(PRECISION)
        structure = extract_contacts(squares, side, sign=field.sign)
        assert not any(item.contact == "edge-edge" for item in structure.pair_contacts), (
            "n = 5 grew an edge-edge contact; its shortfall is only meaningful as the "
            "case the collinearity repair does not touch"
        )
        system = assemble(structure)
        numbers, side_value = as_floats(field, squares, side)
        values = pose_values(system, numbers, side_value)
        info = jacobian_rank(system, values)
        assert info["shortfall"] == 1, f"n = 5 shortfall moved to {info['shortfall']}: {info}"
        assert len(close(system, values).closure) == 1

        # The rank verdict rests on a gap, so the gap is asserted rather than the verdict
        # alone: a marginal one would make the rank a judgement call.
        assert info["largest_discarded"] < info["smallest_counted"] * 1e-20, info
    finally:
        mp.mp.dps = previous


def a_mirrored_packing_assembles_and_vanishes() -> None:
    """The reflected path, against a known answer: mirror `n = 11` and re-derive.

    Reflecting `x -> side - x` flips every winding without moving a single contact, so
    the mirrored packing must extract to an all-`-1` chirality, assemble, and satisfy its
    own equations exactly as the original does.  Before chirality it could not: the same
    corners read as rotations describe eleven different squares.
    """
    previous = mp.mp.dps
    mp.mp.dps = PRECISION
    try:
        squares, side, field = trump11.build()
        field.refine_to(PRECISION)
        numbers, side_value = as_floats(field, squares, side)
        mirrored = [[(side_value - x, y) for x, y in square] for square in numbers]

        structure = extract_contacts(mirrored, side_value, sign=float_sign(1e-9))
        assert structure.chirality == (-1,) * 11, (
            f"mirroring flipped no windings: {structure.chirality}"
        )
        upright = extract_contacts(squares, side, sign=field.sign)
        assert structure.chirality != upright.chirality
        assert len(structure.pair_contacts) == len(upright.pair_contacts), (
            "mirroring changed the contact count, so this is not the same packing "
            "reflected and the comparison below proves nothing"
        )

        system = assemble(structure)
        assert system.chirality == (-1,) * 11
        residuals = residual_at(system, pose_values(system, mirrored, side_value))
        worst = max(abs(value) for value in residuals)
        assert worst < 1e-9, (
            f"the mirrored packing does not satisfy the equations assembled for it "
            f"(worst {worst:.3e}); the reflection is not in the corner model"
        )
    finally:
        mp.mp.dps = previous


def a_pose_of_the_wrong_chirality_is_refused() -> None:
    """Substituting a mirrored pose into an unmirrored system is a typed refusal.

    This is the failure the old `reflected-squares` refusal was standing in for.  It is
    no longer that a reflection cannot be posed -- it can -- but that *these* corners
    are not poses of *this* system, whose equations were written with the other signs
    baked in.  Left unchecked it would surface as residuals that read like a bad
    structure rather than a mismatched caller.
    """
    squares, side, field = trump11.build()
    system = assemble(extract_contacts(squares, side, sign=field.sign))
    numbers, side_value = as_floats(field, squares, side)
    mirrored = [[(side_value - x, y) for x, y in square] for square in numbers]
    try:
        pose_values(system, mirrored, side_value)
    except SystemAssemblyError as error:
        assert error.kind == "chirality-mismatch", error.kind
        return
    raise AssertionError(
        "a mirrored pose was accepted by a system assembled for the upright packing"
    )


def a_structure_without_chirality_is_refused() -> None:
    """An extraction from before the field existed is refused, not defaulted to `+1`.

    Defaulting would be right for most packings and wrong for exactly the one that
    motivated the field, which is the worst available behaviour.
    """
    squares, side, field = trump11.build()
    structure = extract_contacts(squares, side, sign=field.sign)
    try:
        assemble(dataclasses.replace(structure, chirality=()))
    except SystemAssemblyError as error:
        assert error.kind == "chirality-missing", error.kind
        return
    raise AssertionError("a structure carrying no chirality was assembled anyway")


def assembly_refuses_an_unidentified_structure() -> None:
    """A structure from before features existed is refused, never guessed at."""
    squares, side, field = trump11.build()
    structure = extract_contacts(squares, side, sign=field.sign)
    stripped = [
        Incidence(
            kind=incidence.kind,
            left=incidence.left,
            right=incidence.right,
            margin=incidence.margin,
        )
        for incidence in structure.pair_contacts
    ]
    naked = dataclasses.replace(structure, pair_contacts=tuple(stripped))
    try:
        assemble(naked)
    except SystemAssemblyError as error:
        assert error.kind == "features-not-identified"
        return
    raise AssertionError("assembly proceeded without knowing which features meet")


def extraction_still_agrees_with_a_second_case() -> None:
    """Göbel's `n = 5`, so the typing is not tuned to one packing."""
    squares, side, field = gobel5.build()
    structure = extract_contacts(squares, side, sign=field.sign)
    assert structure.pair_contacts, "n = 5 reported no contacts at all"
    for incidence in structure.pair_contacts:
        assert incidence.contact is not None
    system = assemble(structure)
    numbers, side_value = as_floats(field, squares, side)
    residuals = residual_at(system, pose_values(system, numbers, side_value))
    assert max(abs(value) for value in residuals) < 1e-12


def main() -> int:
    features_are_identified_and_typed()
    the_packing_satisfies_its_own_equations()
    an_edge_edge_contact_pins_collinearity_not_incidence()
    the_contact_equations_determine_the_pose()
    closure_is_supplied_only_where_the_rank_says_it_is_missing()
    a_mirrored_packing_assembles_and_vanishes()
    a_pose_of_the_wrong_chirality_is_refused()
    a_structure_without_chirality_is_refused()
    assembly_refuses_an_unidentified_structure()
    extraction_still_agrees_with_a_second_case()
    print("contact feature and system assembly contract selftest passed")
    return 0


def test_promote_system() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
