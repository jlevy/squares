"""Exact index replay for Bui's Section 3.1 S-to-T replacement count."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise


class CountControlError(ValueError):
    """A typed refusal at the source-index control boundary."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True)
class CountReceipt:
    """Exact bookkeeping receipt for one admissible index instance."""

    m: int
    c: Fraction
    thresholds: tuple[int, ...]
    replacement_j_range: tuple[int, int]
    rows: int
    before_final_deletion: int
    after_final_deletion: int
    retained_s: int
    retained_t: int
    deleted_coordinate: tuple[int, int]
    deleted_label: str


def _ceiling(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def replay_count(
    m: int,
    c: Fraction,
    *,
    replacement_last_j: int | None = None,
) -> CountReceipt:
    """Replay the intended finite replacement range and exact retained-square count.

    The paper writes ``j >= 2`` even though its initial grid has only columns ``1..m``.
    Its later labels, Lemma 2 range, and final row description force the intended range
    ``2 <= j <= m``. A caller must not silently extend that range.
    """
    if isinstance(m, bool) or not isinstance(m, int) or m < 2:
        raise CountControlError("parameter-domain", "m must be an integer at least 2")
    if not isinstance(c, Fraction) or c <= 0:
        raise CountControlError("parameter-domain", "c must be a positive Fraction")
    last_j = m if replacement_last_j is None else replacement_last_j
    if last_j != m:
        raise CountControlError(
            "source-index-range",
            "the finite m-column construction requires the replacement range 2..m",
        )

    thresholds = tuple(_ceiling(Fraction(j - 1) * c) + 1 for j in range(1, m + 1))
    if any(right < left for left, right in pairwise(thresholds)):
        raise AssertionError("positive c produced a decreasing threshold")
    rows = thresholds[-1]
    cells = {(row, column): "S" for row in range(1, rows + 1) for column in range(1, m + 1)}

    for j in range(2, last_j + 1):
        column = j - 1
        threshold = thresholds[j - 1]
        for row in range(threshold, rows + 1):
            if cells.get((row, column)) != "S":
                raise AssertionError("replacement encountered a missing or duplicate S cell")
            cells[(row, column)] = "T"

    expected_coordinates = {
        (row, column) for row in range(1, rows + 1) for column in range(1, m + 1)
    }
    if set(cells) != expected_coordinates:
        raise AssertionError("replacement grid has a gap or out-of-range coordinate")
    final = (rows, m)
    if cells.get(final) != "S":
        raise AssertionError("the named final S square is absent before deletion")

    retained_s = sum(label == "S" for label in cells.values())
    retained_t = sum(label == "T" for label in cells.values())
    expected_t = sum(rows - threshold + 1 for threshold in thresholds[1:])
    if retained_t != expected_t or retained_s != m * rows - expected_t:
        raise AssertionError("replacement labels do not match the threshold partition")
    before_final_deletion = len(cells)
    deleted_label = cells.pop(final)
    if set(cells) != expected_coordinates - {final}:
        raise AssertionError("final deletion removed the wrong grid coordinate")
    return CountReceipt(
        m=m,
        c=c,
        thresholds=thresholds,
        replacement_j_range=(2, m),
        rows=rows,
        before_final_deletion=before_final_deletion,
        after_final_deletion=len(cells),
        retained_s=retained_s,
        retained_t=retained_t,
        deleted_coordinate=final,
        deleted_label=deleted_label,
    )
