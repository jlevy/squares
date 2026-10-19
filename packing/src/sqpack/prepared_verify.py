"""Complete packing verification with invocation-local prepared projections.

This explicitly selected execution preserves the reference verifier's shapes,
container, pair enumeration, tolerance-aware projections, and complete Report. It
reuses a square's own-axis arithmetic only within one fresh call. The reference
module remains unchanged for consumers bound to its reviewed source bytes.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from sqpack import verify


class _ProjectionCache:
    """Reuse only a square's own-axis arithmetic within one packing check."""

    def __init__(self, squares: Sequence[verify.Square], sign: Callable) -> None:
        self._squares = squares
        self._sign = sign
        self._axes: dict[int, list] = {}
        self._own_intervals: dict[tuple[int, int], tuple] = {}

    def _axes_for(self, index: int) -> list:
        if index not in self._axes:
            self._axes[index] = verify.edge_axes(self._squares[index])
        return self._axes[index]

    def _own_projection(self, index: int, slot: int, axis) -> tuple:
        key = (index, slot)
        if key not in self._own_intervals:
            self._own_intervals[key] = verify.project(self._squares[index], axis, self._sign)
        return self._own_intervals[key]

    def separated(self, i: int, j: int) -> int | None:
        a, b = self._squares[i], self._squares[j]
        # Match separated: both complete axis lists precede the first projection,
        # but a later projection must remain uncomputed after a strict separation.
        axes_a, axes_b = self._axes_for(i), self._axes_for(j)
        best = None
        for owner, axes in ((i, axes_a), (j, axes_b)):
            for slot, axis in enumerate(axes):
                alo, ahi = (
                    self._own_projection(i, slot, axis)
                    if owner == i
                    else verify.project(a, axis, self._sign)
                )
                blo, bhi = (
                    verify.project(b, axis, self._sign)
                    if owner == i
                    else self._own_projection(j, slot, axis)
                )
                gap = max(self._sign(blo - ahi), self._sign(alo - bhi))
                if gap > 0:
                    return 1
                if gap == 0:
                    best = 0
        return best


def prepared_verify_packing(
    squares: Sequence[verify.Square],
    side,
    sign=verify.exact_sign,
    *,
    check_shapes: bool = True,
    bucket: bool = False,
) -> verify.Report:
    """Check that `squares` is a valid packing of unit squares in [0, side]^2.

    With `sign` = :func:`sqpack.verify.exact_sign` over a
    :class:`sqpack.field.NumberField` this is a proof. With
    :func:`sqpack.verify.float_sign` it is not, and cannot be made
    one by raising precision: a valid tight packing has pairs whose
    separation is exactly zero, so any tolerance large enough to accept those
    contacts also accepts overlaps smaller than the tolerance, and a
    tolerance of zero rejects the valid packing outright.

    Coordinates and arithmetic precision must stay fixed during the call, and
    `sign` must deterministically classify a given scalar value. A square's
    own-axis projections are reused only within this call.
    """
    report = verify.Report(valid=True, n=len(squares))
    if check_shapes:
        report.failures.extend(verify.check_unit_squares(squares, sign))

    for i, sq in enumerate(squares):
        for px, py in sq:
            for value, edge in (
                (px, "x>=0"),
                (py, "y>=0"),
                (side - px, "x<=s"),
                (side - py, "y<=s"),
            ):
                s = sign(value)
                if s < 0:
                    report.failures.append(("container", f"square {i} violates {edge}"))
                elif s == 0:
                    report.container_contacts += 1

    projections = _ProjectionCache(squares, sign)
    for i, j in verify.candidate_pairs(squares, bucket=bucket):
        report.pairs_tested += 1
        verdict = projections.separated(i, j)
        if verdict is None:
            report.failures.append(("overlap", f"squares {i} and {j} overlap"))
        elif verdict == 0:
            report.touching_pairs += 1
            report.touching_pair_indices.append((i, j))
        else:
            report.strict_pairs += 1

    report.valid = not report.failures
    return report
