"""Measure each 70a033f certificate against the packings it would be credited after.

For each count, every certificate is read through ``devtools.upper_bound_reports`` from its
own packet, so a derived fact and a retained file are read alike and each passes its
packet's custody check. The 70a033f certificate is compared with each other certificate
under the box's 8 symmetries: every centre is matched greedily to the nearest unused
centre of the other packing, as the 14 October ledger's review program
``campaign/issue-intake/upper-bounds-20261014/review/compare_geometry.py`` does, and the
best symmetry's largest centre distance and the counts of squares within 1e-6, 1e-3 and
0.1 are printed, with the number of squares whose half-angle tangent differs by more than
1e-6 under that matching. A geometric measurement for credit only; it decides nothing.

From ``packing/``, with the project interpreter: with no argument it measures the twelve
70a033f certificates the per-count rule records; with a packet, a count and other packets
it measures that packet's certificate at that count against theirs, as for issue #606::

    python resources/web/mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py
    python resources/web/mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py \\
        evand-n146-2026-10-14 146 barnett-refinements-2026-10-11 \\
        pingyou-pr574-certificates-2026-10-13 ...
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path

PACKING = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PACKING))

from devtools import upper_bound_reports as reports  # noqa: E402

THIS = "mishapolk-kkt-refinements-2026-10-14"
PR574 = "pingyou-pr574-certificates-2026-10-13"
#: The 46f638c certificate each 70a033f file replaces (#593), and at each count the
#: standing certificate of the 14 October ledger's best now: PR #574's where it holds the
#: count, Couzo's #586 at 154 and his #583/#586 certificate at 302, Ostashev's #575 at 304.
OLD = "mishapolk-records-2026-10-14"
AGAINST: dict[int, tuple[tuple[str, str], ...]] = {
    129: (("PR #574", PR574), ("#562", "dostashev-compositions-2026-10-12")),
    154: (("#586", "couzo-certificates-2026-10-13"),),
    156: (("PR #574", PR574), ("#561", "couzo-certificates-2026-10-12")),
    175: (("PR #574", PR574), ("#528", "dostashev-records-2026-10-12")),
    176: (("PR #574", PR574), ("#575", "dostashev-merged-bands-2026-10-13")),
    204: (("PR #574", PR574), ("#562", "dostashev-compositions-2026-10-12")),
    232: (("PR #574", PR574), ("#528", "dostashev-records-2026-10-12")),
    264: (("PR #574", PR574), ("#528", "dostashev-records-2026-10-12")),
    271: (("PR #574", PR574), ("#561", "couzo-certificates-2026-10-12")),
    302: (("#583, #586", "couzo-certificates-2026-10-13"),),
    303: (("PR #574", PR574), ("#562", "dostashev-compositions-2026-10-12")),
    304: (("#575", "dostashev-merged-bands-2026-10-13"),),
}
Pose = tuple[Fraction, Fraction, Fraction]


def poses(packet: str, n: int) -> tuple[Fraction, list[Pose]]:
    certificate = reports.read_facts(reports.packet_path(packet), {n})[n]
    return certificate.side, [(pose.x, pose.y, pose.t) for pose in certificate.poses]


def symmetries(side: Fraction) -> list[Callable[[Fraction, Fraction], tuple[Fraction, Fraction]]]:
    return [
        lambda x, y: (x, y),
        lambda x, y: (side - x, y),
        lambda x, y: (x, side - y),
        lambda x, y: (side - x, side - y),
        lambda x, y: (y, x),
        lambda x, y: (side - y, x),
        lambda x, y: (y, side - x),
        lambda x, y: (side - y, side - x),
    ]


def matched(points: list[tuple[Fraction, Fraction]], others: list[Pose]) -> list[tuple[float, int]]:
    """Each point's distance to the nearest unused point of ``others``, and that point."""
    used: set[int] = set()
    found = []
    for x, y in points:
        index, distance = min(
            (
                (j, math.hypot(float(x - ox), float(y - oy)))
                for j, (ox, oy, _t) in enumerate(others)
                if j not in used
            ),
            key=lambda pair: pair[1],
        )
        used.add(index)
        found.append((distance, index))
    return found


def compare(this: tuple[Fraction, list[Pose]], other: tuple[Fraction, list[Pose]]) -> str:
    side_a, squares_a = this
    side_b, squares_b = other
    best: tuple[int, float, list[tuple[float, int]]] | None = None
    for index, transform in enumerate(symmetries(side_a)):
        pairs = matched([transform(x, y) for x, y, _t in squares_a], squares_b)
        largest = max(distance for distance, _ in pairs)
        if best is None or largest < best[1]:
            best = (index, largest, pairs)
    assert best is not None
    index, largest, pairs = best
    distances = [distance for distance, _ in pairs]
    within = [sum(d < tolerance for d in distances) for tolerance in (1e-6, 1e-3, 0.1)]
    # A tangent is compared only under the identity, where it is unchanged by the symmetry.
    turned = (
        sum(
            abs(float(t - squares_b[j][2])) > 1e-6
            for (_x, _y, t), (_d, j) in zip(squares_a, pairs, strict=True)
        )
        if index == 0
        else "n/a"
    )
    return (
        f"side diff {float(side_a - side_b):+.3e}; best symmetry {index}: max centre distance "
        f"{largest:.3e}; within 1e-6: {within[0]}, 1e-3: {within[1]}, 0.1: {within[2]} of "
        f"{len(squares_a)}; tangents moved > 1e-6: {turned}"
    )


def main(argv: list[str]) -> int:
    if argv:
        packet, count, *others = argv
        n = int(count)
        this = poses(packet, n)
        for other in others:
            print(f"n={n} {packet} vs {other}: {compare(this, poses(other, n))}")
        return 0
    for n, against in AGAINST.items():
        this = poses(THIS, n)
        for label, packet in (*against, ("#593 at 46f638c", OLD)):
            print(f"n={n} vs {label} ({packet}): {compare(this, poses(packet, n))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
