"""Complete two-square covers, boundary preservation and proof/domain substitutions."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from fractions import Fraction
from functools import cache
from itertools import product
from typing import Any, cast

from sqpack.exact_lp import ExactLP, ExactLPError, prove_infeasible, rational_sign
from sqpack.uniform_cell import (
    PairChoice,
    PoseBox,
    RationalInterval,
    UniformCellDescriptor,
    build_uniform_cell,
)
from sqpack.uniform_cell_check import check_uniform_cell
from sqpack.uniform_cover import (
    TwoSquareCover,
    TwoSquareRoot,
    UniformCoverLeaf,
    check_two_square_cover,
    prove_two_square_cover,
)


def _root() -> TwoSquareRoot:
    centers = RationalInterval(Fraction(1, 2), Fraction(7, 5))
    pose = PoseBox(centers, centers, RationalInterval(0, Fraction(1, 50000)))
    return TwoSquareRoot((pose, pose), RationalInterval(Fraction(9, 5), Fraction(19, 10)))


@cache
def _excluded_cover() -> TwoSquareCover:
    return prove_two_square_cover(_root())


def _refuses(operation: Callable[[], object], kind: str | None = None) -> None:
    try:
        operation()
    except ExactLPError as error:
        if kind is not None:
            assert error.kind == kind
    else:
        raise AssertionError("an incomplete cover or invalid proof was accepted")


def _max_residual(lp: ExactLP, point: tuple[Fraction, ...]) -> Fraction:
    return max(
        sum(
            (
                coefficient * value
                for coefficient, value in zip(row.coefficients, point, strict=True)
            ),
            Fraction(0),
        )
        - bound
        for row, bound in zip(lp.rows, lp.rhs, strict=True)
    )


def test_complete_positive_width_cover_replays_all_eight_alternatives() -> None:
    cover = _excluded_cover()
    gaps = check_two_square_cover(_root(), cover)
    assert len(gaps) == 8
    assert all(gap > 0 for gap in gaps)
    alternatives = {
        (
            leaf.cell.descriptor.choices[0].axis_position,
            leaf.cell.descriptor.choices[0].orientation,
        )
        for leaf in cover.leaves
    }
    assert alternatives == {(0, -1), (0, 1), (1, -1), (1, 1), (2, -1), (2, 1), (3, -1), (3, 1)}
    assert all(leaf.cell.descriptor.poses == cover.root.poses for leaf in cover.leaves)
    assert all(leaf.cell.descriptor.side == cover.root.side for leaf in cover.leaves)
    assert (
        check_two_square_cover(cover.root, replace(cover, leaves=cover.leaves[::-1]))
        == gaps[::-1]
    )


def test_zero_width_touching_is_feasible_in_every_directed_alternative() -> None:
    center = RationalInterval(Fraction(1, 2), Fraction(3, 2))
    pose = PoseBox(center, center, RationalInterval(0, 0))
    root = TwoSquareRoot((pose, pose), RationalInterval(2, 2))
    # At zero angle edge_axes is (vertical, negative horizontal) for either square.
    normals = ((0, 1), (-1, 0), (0, 1), (-1, 0))
    for axis, direction in product(range(4), (-1, 1)):
        dx, dy = (Fraction(direction * coordinate) for coordinate in normals[axis])
        point = (1 - dx / 2, 1 + dx / 2, 1 - dy / 2, 1 + dy / 2, Fraction(2))
        descriptor = UniformCellDescriptor(
            root.poses, root.side, (PairChoice(0, 1, axis, direction),)
        )
        cell = build_uniform_cell(descriptor)
        assert _max_residual(cell.lp, point) == 0
    _refuses(lambda: prove_two_square_cover(root), "feasible")


def test_missing_and_duplicate_alternatives_cannot_close_the_root() -> None:
    cover = _excluded_cover()
    for leaves in (
        cover.leaves[:-1],
        cover.leaves + cover.leaves[-1:],
        cover.leaves[:-1] + cover.leaves[:1],
    ):
        _refuses(
            lambda chosen=leaves: check_two_square_cover(
                cover.root, replace(cover, leaves=chosen)
            ),
            "cover-alternatives",
        )


def test_every_leaf_requires_its_own_independent_positive_gap() -> None:
    cover = _excluded_cover()
    for index, leaf in enumerate(cover.leaves):
        bad = replace(leaf, multipliers=(Fraction(0),) * len(leaf.multipliers))
        leaves = (*cover.leaves[:index], bad, *cover.leaves[index + 1 :])
        _refuses(
            lambda chosen=leaves: check_two_square_cover(
                cover.root, replace(cover, leaves=chosen)
            )
        )


def test_valid_restricted_leaf_cannot_replace_a_root_seam_or_subdomain() -> None:
    cover = _excluded_cover()
    first = cover.root.poses[0]
    original = cover.leaves[0]
    narrower = (
        replace(first, half_angle=RationalInterval(Fraction(1, 100000), Fraction(1, 50000))),
        replace(first, x=RationalInterval(Fraction(3, 5), first.x.upper)),
    )
    descriptors = (
        *(
            replace(original.cell.descriptor, poses=(pose, cover.root.poses[1]))
            for pose in narrower
        ),
        replace(
            original.cell.descriptor, side=RationalInterval(Fraction(19, 10), Fraction(19, 10))
        ),
    )
    for descriptor in descriptors:
        cell = build_uniform_cell(descriptor)
        certificate = prove_infeasible(cell.lp, rational_sign)
        assert check_uniform_cell(cell, certificate.multipliers) > 0
        leaf = UniformCoverLeaf(cell, certificate.multipliers)
        changed = replace(cover, leaves=(leaf, *cover.leaves[1:]))
        _refuses(
            lambda packet=changed: check_two_square_cover(cover.root, packet), "root-mismatch"
        )


def test_reflected_or_substituted_proof_root_does_not_change_the_requested_root() -> None:
    cover = _excluded_cover()
    first = cover.root.poses[0]
    reflected = replace(first, half_angle=RationalInterval(-first.half_angle.upper, 0))
    reflected_root = replace(cover.root, poses=(reflected, cover.root.poses[1]))
    reflected_cover = prove_two_square_cover(reflected_root)
    assert all(gap > 0 for gap in check_two_square_cover(reflected_root, reflected_cover))
    _refuses(lambda: check_two_square_cover(cover.root, reflected_cover), "root-mismatch")
    substituted = replace(cover.root, side=RationalInterval(Fraction(19, 10), Fraction(19, 10)))
    _refuses(lambda: check_two_square_cover(substituted, cover), "root-mismatch")


def test_widened_root_refuses_stale_geometry_and_rebuilt_rows_with_stale_duals() -> None:
    cover = _excluded_cover()
    poses = tuple(
        replace(pose, half_angle=RationalInterval(Fraction(-1, 10), Fraction(1, 10)))
        for pose in cover.root.poses
    )
    wide_root = replace(cover.root, poses=poses)
    _refuses(lambda: check_two_square_cover(wide_root, cover), "root-mismatch")
    wide_leaves = tuple(
        UniformCoverLeaf(
            build_uniform_cell(replace(leaf.cell.descriptor, poses=poses)), leaf.multipliers
        )
        for leaf in cover.leaves
    )
    # The common-center point is a feasible outer-LP witness, though not a packing.
    point = (Fraction(19, 20),) * 4 + (Fraction(19, 10),)
    assert all(_max_residual(leaf.cell.lp, point) <= 0 for leaf in wide_leaves)
    _refuses(lambda: check_two_square_cover(wide_root, TwoSquareCover(wide_root, wide_leaves)))


def test_flat_packet_refuses_references_circular_records_and_symmetry_metadata() -> None:
    cover = _excluded_cover()
    circular: dict[str, Any] = {"root": cover.root, "leaves": cover.leaves}
    circular["reference"] = circular
    _refuses(lambda: check_two_square_cover(cover.root, cast(Any, circular)), "bad-cover")
    referenced = replace(cover, leaves=(cast(Any, "leaf:previous"), *cover.leaves[1:]))
    _refuses(lambda: check_two_square_cover(cover.root, referenced), "bad-cover")
    for field in ("reference", "parent_ids", "reflection", "symmetry", "open_lower"):
        try:
            cast(Any, TwoSquareCover)(cover.root, cover.leaves, **{field: "unsupported"})
        except TypeError:
            pass
        else:
            raise AssertionError("unsupported proof metadata was silently accepted")


def test_root_and_leaf_storage_refuse_lossy_or_malformed_data() -> None:
    cover = _excluded_cover()
    _refuses(
        lambda: TwoSquareRoot(cast(Any, list(cover.root.poses)), cover.root.side), "bad-cover"
    )
    _refuses(
        lambda: TwoSquareRoot(cast(Any, cover.root.poses[:1]), cover.root.side), "bad-cover"
    )
    for value in (True, 1.8, float("nan")):
        side = RationalInterval(Fraction(9, 5), Fraction(19, 10))
        object.__setattr__(side, "lower", value)
        _refuses(lambda changed=side: TwoSquareRoot(cover.root.poses, changed), "bad-cover")
    first = cover.leaves[0]
    malformed = replace(first, multipliers=cast(Any, list(first.multipliers)))
    _refuses(
        lambda: check_two_square_cover(
            cover.root, replace(cover, leaves=(malformed, *cover.leaves[1:]))
        ),
        "bad-cover",
    )
