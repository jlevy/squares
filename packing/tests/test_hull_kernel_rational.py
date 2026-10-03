"""The kernel's rational type, gmpy2's `mpq`, against `fractions.Fraction`.

The producer's and checker's outputs are serialised as `str(Q)` and the producer locates
regions with `float(Q)` and snaps them with `round(Q)`, so these three, with hashing and
comparison, are what make the kernel's bytes independent of the arithmetic library.
"""

from __future__ import annotations

import json
import math
import random
from fractions import Fraction
from typing import Any

from gmpy2 import mpq

from sqpack.hull_kernel import rational
from sqpack.hull_kernel.frame import make_frame
from sqpack.hull_kernel.geometry import clip
from sqpack.hull_kernel.induction import hull
from sqpack.hull_kernel.rational import BACKEND, Q


def test_the_backend_is_gmpy2_and_named_for_receipts() -> None:
    assert Q is rational.Q is mpq
    assert isinstance(Q(1, 2), mpq)
    assert BACKEND["library"] == "gmpy2"
    assert BACKEND["version"].startswith("2.3.")
    assert BACKEND["mp"].startswith("GMP")
    assert json.loads(json.dumps(BACKEND)) == BACKEND


def test_mpq_prints_parses_rounds_and_floats_as_fraction_does() -> None:
    rng = random.Random(20261003)
    samples: list[tuple[int, int]] = [(0, 1), (1, 2), (-1, 2), (3, 2), (-3, 2), (7, 1), (-7, 1)]
    for _ in range(5000):
        bits = rng.choice((8, 40, 100, 160))
        samples.append((rng.randrange(-(2**bits), 2**bits), rng.randrange(1, 2**bits)))
    for n, d in samples:
        f, q = Fraction(n, d), Q(n, d)
        assert str(q) == str(f)
        assert Q(str(f)) == f
        assert float(q) == float(f)
        assert hash(q) == hash(f)
        assert q == f
        assert f == q
        assert (q < f) is False
        assert round(q * 2**20) == round(f * 2**20)
        assert (q * 2**20).denominator == 1 or (f * 2**20).denominator != 1
        assert math.lcm(q.denominator, 6) == math.lcm(f.denominator, 6)
    assert Q(0.1) == Fraction(0.1)
    assert Q("-12") == -12
    assert str(Q(6, 4)) == "3/2"
    assert str(Q(-6, 3)) == "-2"


def test_mixed_fraction_and_mpq_geometry_agrees_and_dedupes() -> None:
    square_f = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(1)),
    ]
    square_q = [(Q(x), Q(y)) for x, y in square_f]
    mixed: list[Any] = [*square_f, *square_q]
    assert hull(mixed) == hull(square_q)
    assert len({*square_f, *square_q}) == 4
    line = (Q(1), Q(1), Q(3, 2))
    fractions: list[Any] = list(square_f)
    assert clip(fractions, line) == clip(square_q, line)
    assert all(isinstance(x, mpq) for x, _ in clip(square_q, line))
    assert sorted([Fraction(1, 3), Q(1, 4), Fraction(1, 5)]) == [
        Q(1, 5),
        Q(1, 4),
        Q(1, 3),
    ]


def test_a_frame_carries_its_cells_as_mpq() -> None:
    triangle = [
        (Fraction(1), Fraction(1)),
        (Fraction(19, 10), Fraction(1)),
        (Fraction(29, 20), Fraction(89, 50)),
    ]
    frame = make_frame(
        name="one",
        cap=Fraction(3),
        length=3,
        cells=[triangle],
        cell_names=["only"],
        occupancy=1,
        action_names=("r0",),
    )
    assert all(type(x) is mpq and type(y) is mpq for x, y in frame.cell(0))
    assert type(frame.cap) is mpq
    assert frame.cell(0) == triangle
    assert str(frame.cap) == "3"
