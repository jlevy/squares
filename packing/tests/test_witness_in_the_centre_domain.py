"""A least-mass witness must be a placement that exists: in the cell and in the domain.

Finding 9c of the 2026-09-05 adversarial review: a direct-summation cross-check taken at
a cell's midpoint confirms the cell's constant mass -- mass is constant on an open cell
whether or not the cell lies in the centre domain -- but it does not exhibit a feasible
placement, because a cell can meet the domain while its midpoint lies outside it.

Of the standard-library verifiers in `cases/n11_fractional_certificate/`, the finding
is confirmed for `minimal_verify.py`, whose `sweep` sums at the midpoint of the least
cell (its ``centre = ((u_events[i] + u_events[i + 1]) / 2, ...)`` line) and asserts
nothing about the domain, and refuted for `thirdparty/verify.py`, whose `witness`
averages the vertices of the domain clipped to the cell's closure -- a strictly
positive combination of every vertex of a convex polygon with interior, hence a point
of its interior, which is the open cell's intersection with the domain's interior --
and asserts both halves of that. The instance below is one on which the difference
is visible: the least cell meets the domain, its midpoint does not, and both verifiers
still report the same minimum, which is why the review, and this file, call it a
weaker witness and not an acceptance bug.
"""

from __future__ import annotations

import importlib.util
import random
from fractions import Fraction
from pathlib import Path
from types import ModuleType

from cases.n11_fractional_certificate import minimal_verify

THIRDPARTY_VERIFY = (
    Path(__file__).resolve().parents[1]
    / "cases"
    / "n11_fractional_certificate"
    / "thirdparty"
    / "verify.py"
)


def load_script(name: str, path: Path) -> ModuleType:
    """By path, not as a package: that is how a reader runs the thirdparty verifier."""

    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


thirdparty = load_script("n11_thirdparty_verify_witness", THIRDPARTY_VERIFY)

#: Container side 4, shrunken side 2, at the 3-4-5 direction t = 1/3 (cosine 4/5,
#: sine 3/5). The admissible centres are [7/5, 13/5]^2, a rotated square in the sweep's
#: (u, v) frame spanning u in [49/25, 91/25] and v in [-11/25, 31/25].
SIDE = Fraction(4)
SQUARE_SIDE = Fraction(2)
TANGENT = Fraction(1, 3)
COSINE, SINE = Fraction(4, 5), Fraction(3, 5)
REACH = SQUARE_SIDE * (COSINE + SINE) / 2

#: Three atoms, placed in the (u, v) frame and carried back to the container. Atom A's
#: coverage box is u in [1/2, 5/2], v in [-3/5, 7/5]; atom B's is u in [5/2, 9/2] at the
#: same v; atom C's is u in [1, 3], v in [0, 2]. Every reached cell with u above 5/2 is
#: covered by B (weight 2) and the one reached cell with u below 5/2 and v above 0 by A
#: and C together, so the least cell is unique: u in (49/25, 5/2), v in (-11/25, 0),
#: covered by A alone, weight 1.
ATOMS = (
    (Fraction(24, 25), Fraction(61, 50), Fraction(1)),
    (Fraction(64, 25), Fraction(121, 50), Fraction(2)),
    (Fraction(1), Fraction(2), Fraction(1)),
)
LEAST_MASS = Fraction(1)
#: The least cell, as the verifiers whose events include the domain's extremes cut it.
LEAST_CELL_U = (Fraction(49, 25), Fraction(5, 2))
LEAST_CELL_V = (Fraction(-11, 25), Fraction(0))


def to_container(u: Fraction, v: Fraction) -> tuple[Fraction, Fraction]:
    return COSINE * u - SINE * v, SINE * u + COSINE * v


def to_frame(x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    return COSINE * x + SINE * y, -SINE * x + COSINE * y


def in_domain(x: Fraction, y: Fraction) -> bool:
    return REACH <= x <= SIDE - REACH and REACH <= y <= SIDE - REACH


def in_least_cell(u: Fraction, v: Fraction) -> bool:
    return LEAST_CELL_U[0] < u < LEAST_CELL_U[1] and LEAST_CELL_V[0] < v < LEAST_CELL_V[1]


def test_the_atoms_sit_where_the_instance_says() -> None:
    """The (u, v) placements the coverage boxes were designed from, exactly."""

    assert [to_frame(x, y) for x, y, _ in ATOMS] == [
        (Fraction(3, 2), Fraction(2, 5)),
        (Fraction(7, 2), Fraction(2, 5)),
        (Fraction(2), Fraction(1)),
    ]
    assert 5 * REACH == 7
    assert 2 * REACH < SIDE


def test_the_least_cell_meets_the_domain_but_its_midpoint_lies_outside() -> None:
    """The premise of Finding 9c, on this instance and independent of any verifier."""

    inside_both = (Fraction(49, 20), Fraction(-1, 20))
    assert in_least_cell(*inside_both)
    assert in_domain(*to_container(*inside_both))

    midpoint = (
        (LEAST_CELL_U[0] + LEAST_CELL_U[1]) / 2,
        (LEAST_CELL_V[0] + LEAST_CELL_V[1]) / 2,
    )
    assert midpoint == (Fraction(223, 100), Fraction(-11, 50))
    assert in_least_cell(*midpoint)
    assert not in_domain(*to_container(*midpoint))


def test_the_thirdparty_witness_is_in_the_least_cell_and_in_the_domain() -> None:
    """Refuting the finding for `thirdparty/verify.py`: the witness is a real placement.

    Its own cells are cut by the atoms' events alone, so its least cell is the wider
    (1, 5/2) x (-3/5, 0); the witness lands in the part of it the domain reaches, which
    is the least cell above. The audit walks random reached cells through the same
    construction, so it is asked for too.
    """

    certificate = {"L": SIDE, "B": SQUARE_SIDE, "atoms": list(ATOMS)}
    weights = [int(weight) for _, _, weight in ATOMS]

    minimum, witness, cells = thirdparty.least_covered_weight(
        certificate, COSINE, SINE, weights, 1, audit=4, rng=random.Random(0)
    )

    assert minimum == LEAST_MASS
    assert cells == 6
    assert witness is not None
    assert in_domain(*witness)
    assert in_least_cell(*to_frame(*witness))
    assert thirdparty.covered_weight_at(certificate, COSINE, SINE, *witness) == LEAST_MASS


def test_the_minimal_verifier_agrees_on_the_minimum_and_the_cell_count() -> None:
    """The finding held for `minimal_verify.py` too, and is fixed the same way.

    Its witness was the least cell's midpoint, which the test above shows lies outside
    the domain; the direct sum there still equalled the swept minimum, because mass is
    constant on the open cell, so the check passed without exhibiting a placement. It
    now averages the vertices of the domain clipped to the cell, as the thirdparty
    verifier does, and refuses a least cell that meets the domain in no area. That
    refusal is what exposed a second defect: the two strips just outside the domain's
    u-extent clipped to a single repeated corner, which a vertex count could not tell
    from a strip with area, so each scored one cell outside the domain -- eight cells
    here rather than six, and 1,194 across the retained certificate's 181 directions,
    the exact gap between its printed count and the 2026-09-05 review's independent
    replay. Strips are now skipped by area, and the two verifiers count alike.
    """

    weights = [int(weight) for _, _, weight in ATOMS]

    least, cells = minimal_verify.sweep(list(ATOMS), weights, SQUARE_SIDE / 2, SIDE, TANGENT)

    assert least == LEAST_MASS
    assert cells == 6
