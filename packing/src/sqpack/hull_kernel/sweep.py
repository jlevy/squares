"""The exact vertical sweep that proves a row domain is covered by a union of polygons.

A copy of `vertical_interval`, `edge_lines`, `covers_vertical` and `exact_union_cover`
from the frozen n11 mask-0 checker, with one change: `covers_vertical` skips a span
wholly below its cursor, which the frozen routine did not, so a single-point section is
no longer counted covered by a span ending below it (finding C2 of the n11 adversarial
review; `devtools/n11_closed_interval_cover.py` is the corrected reference). Between two
consecutive event abscissae (vertices and edge crossings) no edge ends and no two edges
cross, so the order of the edge lines is constant on the open slab; coverage of the
vertical section at the slab's midpoint then decides the whole open slab, and each event
line is checked on its own. The sweep is the reference form; the indexed and
degenerate-domain forms of the later n11 checkers are not lifted here.

The change alters no verdict of `exact_union_cover`. The two forms of `covers_vertical`
differ only on a single-point section, where the new one refuses what the old accepted
from a span ending below the point, and the sweep meets such a section only at the
domain's leftmost or rightmost abscissa, since its domain has positive area. The open
slab beside that abscissa is probed at an interior point, where the section has positive
length and both forms decide alike; a covered slab puts the extreme point in the closure
of a covered set, and a finite union of closed regions contains its limits, so some
region's span contains it and the new form accepts too. Only the abscissa named in the
refusal of an uncovered extreme point can move, to the extreme from the slab beside it.
"""

from __future__ import annotations

import time
from fractions import Fraction
from itertools import pairwise

from sqpack.hull_kernel.geometry import (
    Budget,
    IncompleteError,
    Polygon,
    RefusalError,
    area2,
    require,
)
from sqpack.hull_kernel.rational import Q

# The exact endpoint types: the kernel's `mpq`, its integer type (an `mpq`'s numerator's),
# and the standard library's `Fraction` and `int`; `bool` is not among them.
EXACT = frozenset({Q, type(Q().numerator), Fraction, int})


def vertical_interval(poly: Polygon, x: Q) -> tuple[Q, Q] | None:
    """The polygon's closed vertical section at `x`, or None when `x` misses it.

    Every ordinate taken is required to be exact (`EXACT`): a float coordinate, which
    `mpq` arithmetic turns into an `mpfr`, or a NaN, which `min` and `max` would pass
    over, is refused rather than compared.
    """
    ordinates: list[Q] = []
    for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
        if min(p[0], q[0]) <= x <= max(p[0], q[0]):
            if p[0] == q[0]:
                ordinates.extend((p[1], q[1]))
            else:
                ordinates.append(p[1] + (x - p[0]) * (q[1] - p[1]) / (q[0] - p[0]))
    require(all(type(y) in EXACT for y in ordinates), f"inexact coverage endpoint at x={x}")
    return (min(ordinates), max(ordinates)) if ordinates else None


def edge_lines(polygons: list[Polygon]) -> list[tuple[Q, Q, Q, Q]]:
    """Nonvertical edge as y=m*x+b over its closed x range."""
    lines: list[tuple[Q, Q, Q, Q]] = []
    for poly in polygons:
        for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
            if p[0] == q[0]:
                continue
            slope = (q[1] - p[1]) / (q[0] - p[0])
            lines.append((min(p[0], q[0]), max(p[0], q[0]), slope, p[1] - slope * p[0]))
    return lines


def covers_vertical(domain: Polygon, regions: list[Polygon], x: Q) -> bool:
    """Whether the regions' closed sections at `x` cover the domain's closed section.

    A span wholly below the cursor is skipped, as in `covers.covers_vertical_compiled`,
    so a single-point section `[y, y]` counts as covered only by a span containing `y`.
    The frozen n11 routine lacked that skip and accepted `[1, 1]` from `[0, 0]`. A
    section with an inexact endpoint is refused by `vertical_interval`.
    """
    target = vertical_interval(domain, x)
    if target is None:
        raise RefusalError("coverage probe outside domain")
    spans = [span for poly in regions if (span := vertical_interval(poly, x)) is not None]
    spans.sort()
    cursor = target[0]
    for low, high in spans:
        if high < cursor:
            continue
        if low > cursor:
            return False
        cursor = max(cursor, high)
        if cursor >= target[1]:
            return True
    return False


def exact_union_cover(
    domain: Polygon, regions: list[Polygon], *, budget: Budget
) -> dict[str, int]:
    """Exact vertical sweep at every edge event and between consecutive events."""
    require(area2(domain) > 0, "degenerate row domain needs a separate proof")
    require(bool(regions), "no eligible charge regions")
    polygons = [domain, *regions]
    left, right = min(p[0] for p in domain), max(p[0] for p in domain)
    events = {p[0] for poly in polygons for p in poly if left <= p[0] <= right}
    lines = edge_lines(polygons)
    for number, (a0, a1, m, b) in enumerate(lines):
        if time.monotonic() >= budget.deadline:
            raise IncompleteError(f"row event construction timed out after {number} edges")
        for z0, z1, n, d in lines[number + 1 :]:
            if m == n:
                continue
            start, stop = max(a0, z0, left), min(a1, z1, right)
            if start <= stop:
                crossing = (d - b) / (m - n)
                if start <= crossing <= stop:
                    events.add(crossing)
        if len(events) > budget.max_nodes:
            raise IncompleteError(f"row event ceiling: events={len(events)}")
    positions = sorted(events)
    require(positions[0] == left and positions[-1] == right, "row domain endpoint missing")
    probes = [positions[0]]
    for a, b in pairwise(positions):
        probes.extend(((a + b) / 2, b))
    if len(probes) > budget.max_nodes:
        raise IncompleteError(f"row probe ceiling: probes={len(probes)}")
    for number, x in enumerate(probes):
        if time.monotonic() >= budget.deadline:
            raise IncompleteError(f"row sweep timeout: checked={number}, total={len(probes)}")
        require(covers_vertical(domain, regions, x), f"row uncovered at exact x={x}")
    return {"events": len(positions), "probes": len(probes), "edge_segments": len(lines)}
