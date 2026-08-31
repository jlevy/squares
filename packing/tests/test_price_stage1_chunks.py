"""Pin the counted half of the chunk-level stage-1 price (BC-095, D-405 follow-up).

The measured half (prefilter rate, per-candidate cost) is a runtime measurement and
deliberately unpinned; these tests hold the closed-form combinatorics still, which is
also the omission control the eventual enumerator must match family by family.
"""

from __future__ import annotations

from devtools.price_stage1_chunks import (
    class_assignments,
    partitions,
    priced_families,
    skeleton_count,
)


def test_partition_families_at_n11() -> None:
    assert len(partitions(11, 11, 6)) == 44
    assert len(partitions(11, 11, 3)) == 16
    assert partitions(2, 2, 1) == [(2,)]


def test_skeleton_counts_are_the_grammar() -> None:
    # size: rectangles a x b (a <= b) plus corner Ls with arms >= 2.
    assert skeleton_count(1) == 1
    assert skeleton_count(2) == 1
    assert skeleton_count(3) == 2  # 1x3 bar, L(2,2)
    assert skeleton_count(4) == 3  # 1x4, 2x2, L(2,3)
    assert skeleton_count(6) == 4  # 1x6, 2x3, L(2,5), L(3,4)


def test_class_assignments_cap_and_symmetry() -> None:
    # One chunk: frame, or tilted (class names swap-equivalent).
    assert class_assignments(1) == 2
    # Two chunks, at most two tilted, up to swapping the tilt classes:
    # (0,0); (0,t); (t,0); (t,t) same class; (t,t') split -- five orbits.
    assert class_assignments(2) == 5
    assert class_assignments(0) == 1


def test_priced_families_monotone_in_scope() -> None:
    raw_small, floor_small, families_small = priced_families(3, 6)
    raw_big, floor_big, families_big = priced_families(6, 16)
    assert families_small == 16
    assert families_big == 44
    assert raw_small == 24_611_472
    assert raw_small < raw_big
    assert float(floor_small) < float(floor_big)
