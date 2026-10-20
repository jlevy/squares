"""The independent corner checker must honor its Witness/v2 geometry contract."""

from __future__ import annotations

import gzip
import itertools
import math
import random
from collections.abc import Callable
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import check_rational_witness_independent as independent
from devtools import regularize_axis_components as axis_tool
from devtools.check_rational_witness_independent import (
    Point,
    Projection,
    Square,
    axes,
    check,
    check_squares,
    interval,
    pair_gap,
    parse,
)
from sqpack.witness import WitnessError, exact_verify, load_witness
from sqpack.yamlio import load_yaml

WITNESSES = Path(__file__).resolve().parent.parent / "witnesses"


def _grid_document() -> dict:
    return yaml.safe_load((WITNESSES / "grid-n004.yaml").read_text(encoding="utf-8"))


def _write(path: Path, document: dict) -> Path:
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return path


def test_centered_corners_do_not_pass_as_lower_left_geometry(tmp_path: Path) -> None:
    document = _grid_document()
    witness = document["witness"]
    witness["id"] = "W-centered-control"
    witness["n"] = 1
    witness["squares"] = [deepcopy(witness["squares"][1])]
    lower_left = _write(tmp_path / "lower-left.yaml", document)
    assert check(lower_left)["verification_passed"]

    witness["coordinates"]["origin"] = "container-center"
    centered = _write(tmp_path / "centered.yaml", document)
    with pytest.raises(ValueError, match="lower-left"):
        parse(centered)
    main_witness = load_witness(centered, fallback_schema=WITNESSES / "witness.schema.yaml")
    assert not exact_verify(main_witness)[1].valid


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("square_size", "2", "unit squares"),
        (
            "coordinates",
            {"origin": "lower-left", "axes": "x-left-y-up", "angle_unit": "not-applicable"},
            "x-right-y-up",
        ),
        (
            "coordinates",
            {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "radians"},
            "x-right-y-up",
        ),
    ],
)
def test_unsupported_geometry_metadata_rejects(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    document = _grid_document()
    document["witness"][field] = value
    path = _write(tmp_path / "bad-metadata.yaml", document)
    with pytest.raises(ValueError, match=message):
        parse(path)
    with pytest.raises(WitnessError):
        load_witness(path, fallback_schema=WITNESSES / "witness.schema.yaml")


def test_complete_positive_integer_count_is_required(tmp_path: Path) -> None:
    document = _grid_document()
    document["witness"]["n"] = 3
    path = _write(tmp_path / "incomplete.yaml", document)
    with pytest.raises(ValueError, match="complete square list"):
        parse(path)

    document["witness"]["squares"] = document["witness"]["squares"][:1]
    document["witness"]["n"] = True
    path = _write(tmp_path / "boolean-count.yaml", document)
    with pytest.raises(ValueError, match="complete square list"):
        parse(path)


def test_non_contract_and_non_rational_corners_reject(tmp_path: Path) -> None:
    document = _grid_document()
    document["softschema"]["contract"] = "other:Witness/v2"
    path = _write(tmp_path / "wrong-contract.yaml", document)
    with pytest.raises(ValueError, match="Witness/v2 contract"):
        parse(path)

    document["softschema"]["contract"] = "packing.squares:Witness/v2"
    document["witness"]["squares"][0]["corners"][0][0] = 0.0
    path = _write(tmp_path / "float-corner.yaml", document)
    with pytest.raises(ValueError, match="rational strings"):
        parse(path)


# think-uomm: `check_squares` takes each square's projections onto its own two axes once
# per square instead of once per pair. What follows holds that route to `pair_gap`'s direct
# definition, exactly over Q, on adversarial squares and on the retained atlas views, and
# pins the count of projections it saves.


def _pair_gap_direct(left: Square, right: Square) -> Fraction:
    """`pair_gap`'s direct definition, verbatim from `ded4727b`: all eight intervals
    projected afresh."""
    gaps: list[Fraction] = []
    for axis in (*axes(left), *axes(right)):
        left_min, left_max = interval(left, axis)
        right_min, right_max = interval(right, axis)
        gaps.extend((right_min - left_max, left_min - right_max))
    return max(gaps)


Separation = Callable[[Square, Square, list[Projection], list[Projection]], Fraction]


def _decide(
    squares: list[Square], side: Fraction, separation: Separation
) -> tuple[dict[str, Any], list[Fraction]]:
    """`check_squares`'s verdict, and every pair gap it decided in order, when each pair is
    separated by `separation` in place of the module's own."""
    gaps: list[Fraction] = []

    def recorded(
        left: Square, right: Square, left_own: list[Projection], right_own: list[Projection]
    ) -> Fraction:
        gap = separation(left, right, left_own, right_own)
        gaps.append(gap)
        return gap

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(independent, "_separation", recorded)
        verdict = check_squares(squares, side)
    assert len(gaps) == math.comb(len(squares), 2), "a pair bypassed `_separation`"
    return verdict, gaps


def _assert_decided_as_the_direct_definition(
    squares: list[Square], side: Fraction
) -> list[Fraction]:
    """Every pair gap `check_squares` decides from its cached projections equals the gap
    with every projection taken afresh, as a `Fraction`, and so does `pair_gap`'s; the
    whole verdict is the one the fresh gaps give. Returns the gaps."""
    shipped = independent._separation  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    cached_verdict, cached = _decide(squares, side, shipped)
    fresh_verdict, fresh = _decide(
        squares, side, lambda left, right, *_own: _pair_gap_direct(left, right)
    )
    assert cached == fresh
    assert all(type(gap) is Fraction for gap in cached)
    assert cached_verdict == fresh_verdict
    assert check_squares(squares, side) == fresh_verdict
    pairs = itertools.combinations(squares, 2)
    assert [pair_gap(left, right) for left, right in pairs] == fresh
    return fresh


def _square(
    corner: Point,
    turn: Point = (Fraction(1), Fraction(0)),
    *,
    size: Fraction = Fraction(1),
    clockwise: bool = False,
) -> Square:
    """A square with its first corner at `corner` and its first edge along `turn`,
    `(cos, sin)` exactly, its corners listed counter-clockwise unless `clockwise`."""
    (x, y), (c, s) = corner, turn
    u, v = (c * size, s * size), (-s * size, c * size)
    square = [(x, y), (x + u[0], y + u[1]), (x + u[0] + v[0], y + u[1] + v[1])]
    square.append((x + v[0], y + v[1]))
    return square[::-1] if clockwise else square


def _pythagorean(m: int, k: int) -> Point:
    """The exact rotation `((m^2 - k^2) / (m^2 + k^2), 2mk / (m^2 + k^2))`."""
    return Fraction(m * m - k * k, m * m + k * k), Fraction(2 * m * k, m * m + k * k)


def _opposite(turn: Point) -> Point:
    return -turn[0], -turn[1]


def _quarter(turn: Point) -> Point:
    return -turn[1], turn[0]


def _adversarial_cases() -> dict[str, tuple[list[Square], Fraction]]:
    """Squares built so the pair decision sits on its edges: contacts of each kind,
    shared corners, overlaps and clearances one part in 10^40, reversed corner order,
    and corners that are not squares at all, which the checker must refuse identically."""
    half, one, two, four = Fraction(1, 2), Fraction(1), Fraction(2), Fraction(4)
    sliver = Fraction(1, 10**40)
    tilt, wide = (Fraction(3, 5), Fraction(4, 5)), _pythagorean(10**30 + 7, 3)
    unit, wide_unit = _square((one, one)), _square((one, one), wide)

    def along_wide(distance: Fraction) -> Square:
        return _square((one + distance * wide[0], one + distance * wide[1]), wide)

    return {
        "edge contact": ([unit, _square((two, one))], four),
        "aligned squares sharing a corner": ([unit, _square((two, two))], four),
        "a tilted square on an aligned one's corner": ([unit, _square((two, two), tilt)], four),
        "a tilted vertex on an aligned edge": ([unit, _square((one + half, two), tilt)], four),
        "tilted squares sharing a corner back to back": (
            [_square((two, two), tilt), _square((two, two), _opposite(tilt))],
            four,
        ),
        "tilted squares sharing a corner and an edge": (
            [_square((two, two), tilt), _square((two, two), _quarter(tilt))],
            four,
        ),
        "differently tilted squares sharing a corner and overlapping": (
            [_square((two, two), tilt), _square((two, two), _pythagorean(12, 5))],
            four,
        ),
        "one square twice": ([unit, list(unit)], four),
        "one square, its corners relabelled": ([unit, unit[2:] + unit[:2]], four),
        "clockwise against counter-clockwise": (
            [
                unit,
                _square((two, one), clockwise=True),
                _square((one + half, one), tilt, clockwise=True),
            ],
            four,
        ),
        "wide rationals overlapping by a sliver": ([wide_unit, along_wide(1 - sliver)], four),
        "wide rationals apart by a sliver": ([wide_unit, along_wide(1 + sliver)], four),
        "wide rationals in contact": ([wide_unit, along_wide(one)], four),
        "a point inside a square": ([unit, [(one + half, one + half)] * 4], four),
        "a point on a square's corner": ([unit, [(two, two)] * 4], four),
        "collinear corners": (
            [unit, [(one, 3 * one), (two, 3 * one), (3 * one, 3 * one), (two, 3 * one)]],
            four,
        ),
        "a square of side two and a parallelogram": (
            [
                _square((one, one), size=two),
                [
                    (3 * one, 3 * one),
                    (four, 3 * one),
                    (four + half, four),
                    (3 * one + half, four),
                ],
            ],
            5 * one,
        ),
        "a square through the wall": ([unit, _square((-half, 3 * one))], four),
        "one square": ([unit], two),
    }


@pytest.mark.parametrize("name", sorted(_adversarial_cases()))
def test_adversarial_pairs_decide_as_the_direct_definition(name: str) -> None:
    squares, side = _adversarial_cases()[name]
    gaps = _assert_decided_as_the_direct_definition(squares, side)
    reversed_gaps = [
        pair_gap(right, left) for left, right in itertools.combinations(squares, 2)
    ]
    assert reversed_gaps == gaps


def test_adversarial_cases_reach_every_edge_of_the_decision() -> None:
    """The catalogue holds what it claims: contact, overlap and clearance, the slivers
    exactly, and verdicts refused for the squares' own failures and for the wall. A
    point's normals are zero, so on either route a point inside a square reads as
    contact; `square_failures` is what refuses it."""
    cases = _adversarial_cases()
    gaps = {
        name: [_pair_gap_direct(*pair) for pair in itertools.combinations(squares, 2)]
        for name, (squares, _side) in cases.items()
    }
    touching = [name for name, found in gaps.items() if found == [0]]
    assert sorted(touching) == [
        "a point inside a square",
        "a point on a square's corner",
        "a square of side two and a parallelogram",
        "a tilted square on an aligned one's corner",
        "a tilted vertex on an aligned edge",
        "aligned squares sharing a corner",
        "edge contact",
        "tilted squares sharing a corner and an edge",
        "tilted squares sharing a corner back to back",
        "wide rationals in contact",
    ]
    assert gaps["differently tilted squares sharing a corner and overlapping"][0] < 0
    assert gaps["one square twice"] == gaps["one square, its corners relabelled"] == [-1]
    assert gaps["clockwise against counter-clockwise"][0] == 0
    assert gaps["wide rationals overlapping by a sliver"] == [-Fraction(1, 10**40)]
    assert gaps["wide rationals apart by a sliver"] == [Fraction(1, 10**40)]
    assert gaps["one square"] == []
    verdicts = {name: check_squares(*case) for name, case in cases.items()}
    refused = sorted(
        name for name, verdict in verdicts.items() if not verdict["verification_passed"]
    )
    assert refused == [
        "a point inside a square",
        "a point on a square's corner",
        "a square of side two and a parallelogram",
        "a square through the wall",
        "clockwise against counter-clockwise",
        "collinear corners",
        "differently tilted squares sharing a corner and overlapping",
        "one square twice",
        "one square, its corners relabelled",
        "wide rationals overlapping by a sliver",
    ]
    assert any(
        "container penetration" in failure
        for failure in verdicts["a square through the wall"]["failures"]
    )
    assert verdicts["one square"]["minimum_best_pair_gap"] == "2"


def test_random_tilted_squares_decide_as_the_direct_definition() -> None:
    """Two dozen unit squares at random rational centres and four exact rotations, so
    tilted pairs overlap, touch and clear one another at once."""
    rng = random.Random(20261020)
    rotations = [(Fraction(1), Fraction(0)), (Fraction(3, 5), Fraction(4, 5))]
    rotations += [(Fraction(5, 13), Fraction(12, 13)), (Fraction(-8, 17), Fraction(15, 17))]
    half = Fraction(1, 2)
    squares: list[Square] = []
    for _ in range(24):
        x, y = (Fraction(rng.randint(10, 50), 10) for _ in range(2))
        c, s = rng.choice(rotations)
        squares.append(
            [
                (x + c * a - s * b, y + s * a + c * b)
                for a, b in ((half, half), (-half, half), (-half, -half), (half, -half))
            ]
        )
    gaps = _assert_decided_as_the_direct_definition(squares, Fraction(6))
    assert any(gap < 0 for gap in gaps), "the sample must hold an overlapping pair"
    assert any(gap == 0 for gap in gaps), "and a touching pair"
    assert any(gap > 0 for gap in gaps), "and a clear one"


@pytest.mark.parametrize("n", [3, 4, 12, 30])
def test_check_squares_projects_each_square_on_its_own_axes_once(n: int) -> None:
    """The saving itself. `check_squares` projects each square onto its own two normals
    once and each pair onto the other square's normals, so it calls `interval`
    `2n + 4 comb(n, 2)` times. Separating every pair with `pair_gap` would call it
    `8 comb(n, 2)` times and decide the same values, so only this count tells them apart."""
    squares = [_square((Fraction(index), Fraction(0))) for index in range(n)]
    calls = 0

    def counted(square: Square, axis: Point) -> tuple[Fraction, Fraction]:
        nonlocal calls
        calls += 1
        return interval(square, axis)

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(independent, "interval", counted)
        verdict = check_squares(squares, Fraction(n))
    assert verdict["verification_passed"]
    assert verdict["pairs_tested"] == math.comb(n, 2)
    assert calls == 2 * n + 4 * math.comb(n, 2)


def _atlas_view(n: int) -> tuple[Fraction, list[Square]]:
    """A retained regularized view's side and exact corners, read as `--verify-atlas`
    reads them (`view_corners`)."""
    text = gzip.decompress(axis_tool.ATLAS.view(n).read_bytes()).decode("utf-8")
    return axis_tool.view_corners(load_yaml(text)["witness"])


@pytest.mark.parametrize("n", [18, 26, 37])
def test_retained_atlas_views_decide_as_the_direct_definition(n: int) -> None:
    """Whole retained views, rotated over Q with denominators of 170 to 490 digits."""
    side, squares = _atlas_view(n)
    gaps = _assert_decided_as_the_direct_definition(squares, side)
    assert check_squares(squares, side)["verification_passed"]
    assert min(gaps) >= 0


def test_widest_retained_rationals_decide_as_the_direct_definition() -> None:
    """n=29's view carries the layer's widest rationals, denominators near 4,000 digits,
    which is where the projections cost what think-uomm saves; its first square and the
    four whose exact centres lie nearest it are decided as the direct definition decides
    them."""
    side, squares = _atlas_view(29)

    def centre(square: Square) -> Point:
        return sum((x for x, _ in square), Fraction(0)) / 4, sum(
            (y for _, y in square), Fraction(0)
        ) / 4

    ox, oy = centre(squares[0])

    def distance(square: Square) -> Fraction:
        x, y = centre(square)
        return (x - ox) ** 2 + (y - oy) ** 2

    nearest = sorted(squares, key=distance)[:5]
    gaps = _assert_decided_as_the_direct_definition(nearest, side)
    assert min(gaps) >= 0
