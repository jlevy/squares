#!/usr/bin/env python3
"""Contract for contact-feature identification and system assembly.

The check that decides whether assembly is right is not a count.
It is whether the packing the structure was extracted from *satisfies the equations
assembly wrote down*: at Trump's `n = 11` the residual is at the double-precision noise
floor, and a mistyped contact or a wrong feature moves it by orders of magnitude.

Three findings are asserted here rather than described, because each contradicts what
the promotion spec expected and a future reader should meet them as measurements:

- **counting rows is the wrong instrument.**  At `n = 11` there are 35 contact equations
  against 34 unknowns, which reads as overdetermined, while the Jacobian has rank 30 --
  redundant and four conditions short at the same time.  Closure is sized by the rank
  shortfall, and a closure sized by the count would have added none.
- **an angle class does not license an angle identity.**  Classes are decided modulo
  ninety degrees, so `t_i = t_j` is false for a class member a quarter or half turn from
  another.  Emitting those identities left `n = 11` at the noise floor -- its classes
  happen to have equal angles -- and drove `n = 29` to a residual of exactly `pi`.
- **the `n = 29` layout contains reflected squares.**  Seven of twenty-nine are built
  inside `scale(-1 1)` mirror groups, and a centre-plus-rotation pose cannot represent a
  clockwise winding, so assembly refuses them by name rather than describing their
  mirror images.
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


def counting_rows_disagrees_with_the_rank() -> None:
    """The finding that decides how closure is sized.

    `plan-2026-08-28-promotion-pipeline-implementation` phase 2 proposes withholding
    `close()` and requiring the unclosed system to be reported *underdetermined*, which
    presumes the count answers the question.  It does not: `n = 11` is overdetermined by
    the count and four conditions short by the rank, at the same time.
    """
    previous = mp.mp.dps
    mp.mp.dps = PRECISION
    try:
        squares, side, field = trump11.build()
        field.refine_to(PRECISION)
        structure = extract_contacts(squares, side, sign=field.sign)
        system = assemble(structure)

        assert system.unknown_count == 3 * 11 + 1 == 34
        assert len(system.equations) == 35, (
            "the n = 11 equation count moved; a corner-corner contact contributes two "
            "scalar equations and the others one, so this count is the typing's arithmetic"
        )
        assert system.state() == "overdetermined", system.summary()
        assert system.angle_identities == 0, (
            "an angle identity was emitted; classes hold modulo ninety degrees and do "
            "not license one"
        )

        numbers, side_value = as_floats(field, squares, side)
        values = pose_values(system, numbers, side_value)
        info = jacobian_rank(system, values)
        assert info["rank"] == 30, info
        assert info["shortfall"] == 4, (
            f"the n = 11 contact Jacobian rank moved to {info['rank']}; the shortfall is "
            "how many stationarity conditions closure has to supply"
        )

        closed = close(system, values)
        assert len(closed.closure) == 4, closed.summary()
        assert closed.equation_count == len(system.equations) + 4
    finally:
        mp.mp.dps = previous


def closure_is_sized_by_the_measured_shortfall() -> None:
    """Two sizes, two answers -- so the closure count is measured, not assumed.

    Göbel's `n = 5` is one condition short and Trump's `n = 11` is four.  A `close` that
    returned a fixed number, or one derived from the row count, would get at least one of
    them wrong.

    Recorded rather than faked: `close`'s `already-determined` refusal has **no case
    yet**. Both packings here are rank-deficient, and no tolerance makes either look
    determined -- the discarded singular values are around `1e-42` against counted ones
    near `0.5`, so the rank gap is wide rather than marginal.  That branch stays
    unexercised until a determined contact system turns up, and saying so is better than
    a control contrived to reach it.
    """
    previous = mp.mp.dps
    mp.mp.dps = PRECISION
    try:
        for build, expected in ((gobel5.build, 1), (trump11.build, 4)):
            squares, side, field = build()
            field.refine_to(PRECISION)
            structure = extract_contacts(squares, side, sign=field.sign)
            system = assemble(structure)
            numbers, side_value = as_floats(field, squares, side)
            values = pose_values(system, numbers, side_value)
            info = jacobian_rank(system, values)
            assert info["shortfall"] == expected, (
                f"n = {structure.n} shortfall moved to {info['shortfall']}: {info}"
            )
            assert len(close(system, values).closure) == expected

            # The rank verdict rests on a gap, so the gap is asserted rather than the
            # verdict alone: a marginal one would make the rank a judgement call.
            assert info["largest_discarded"] < info["smallest_counted"] * 1e-20, info
    finally:
        mp.mp.dps = previous


def reflected_squares_are_refused_by_name() -> None:
    """A clockwise winding is not a pose this model can describe."""
    squares, side, field = trump11.build()
    structure = extract_contacts(squares, side, sign=field.sign)
    system = assemble(structure)
    numbers, side_value = as_floats(field, squares, side)
    mirrored = [list(reversed(square)) for square in numbers]
    try:
        pose_values(system, mirrored, side_value)
    except SystemAssemblyError as error:
        assert error.kind == "reflected-squares"
        return
    raise AssertionError(
        "a clockwise-wound square was posed as a rotation, which describes its mirror "
        "image rather than the square"
    )


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
    counting_rows_disagrees_with_the_rank()
    closure_is_sized_by_the_measured_shortfall()
    reflected_squares_are_refused_by_name()
    assembly_refuses_an_unidentified_structure()
    extraction_still_agrees_with_a_second_case()
    print("contact feature and system assembly contract selftest passed")
    return 0


def test_promote_system() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
