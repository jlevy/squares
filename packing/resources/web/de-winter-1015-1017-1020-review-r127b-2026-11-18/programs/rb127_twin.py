"""Conversions between the two forms, and the twin relation (lane r127b-1118).

Decides nothing about a packing. A pose ``(cx, cy, c, s)`` has the corners
``C - u/2 - v/2, C + u/2 - v/2, C + u/2 + v/2, C - u/2 + v/2`` in counterclockwise order,
with ``u = (c, s)`` and ``v = (-s, c)``. Four corners give back a pose as their mean and
the edge from the first to the second; that edge is a unit vector exactly when the
corners are a unit square, which both methods check for themselves.

Two listings are the same square when one is a cyclic rotation of the other, in either
sense. All arithmetic is in ``fractions.Fraction``, and values are handed back as
``(p, q)`` pairs in lowest terms with ``q > 0``.
"""

from __future__ import annotations

from fractions import Fraction

Q = tuple[int, int]


def fr(v: Q) -> Fraction:
    return Fraction(v[0], v[1])


def pq(f: Fraction) -> Q:
    return f.numerator, f.denominator


def corners_of_pose(row: tuple[Q, Q, Q, Q]) -> list[tuple[Fraction, Fraction]]:
    cx, cy, c, s = (fr(v) for v in row)
    ux, uy = c / 2, s / 2
    vx, vy = -s / 2, c / 2
    return [
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
    ]


def corners_pq(row: tuple[Q, Q, Q, Q]) -> tuple[tuple[Q, Q], ...]:
    return tuple((pq(x), pq(y)) for x, y in corners_of_pose(row))


def pose_of_corners(corners: tuple[tuple[Q, Q], ...]) -> tuple[Q, Q, Q, Q]:
    pts = [(fr(x), fr(y)) for x, y in corners]
    cx = sum((p[0] for p in pts), Fraction(0)) / 4
    cy = sum((p[1] for p in pts), Fraction(0)) / 4
    ex = pts[1][0] - pts[0][0]
    ey = pts[1][1] - pts[0][1]
    return pq(cx), pq(cy), pq(ex), pq(ey)


def match(listing: tuple[tuple[Q, Q], ...], ref: list[tuple[Fraction, Fraction]]) -> tuple[int, int] | None:
    """``(offset, sense)`` with ``listing[k] == ref[(offset + sense*k) % 4]``, or ``None``."""
    pts = [(fr(x), fr(y)) for x, y in listing]
    if len(pts) != 4:
        return None
    for sense in (1, -1):
        for offset in range(4):
            if all(pts[k] == ref[(offset + sense * k) % 4] for k in range(4)):
                return offset, sense
    return None


def twin(rows: list[tuple[Q, Q, Q, Q]], corners: list[tuple[tuple[Q, Q], ...]]) -> dict:
    """Whether square ``k`` of the corner file is the square of row ``k``, for every ``k``."""
    if len(rows) != len(corners):
        return {"holds": False, "reason": "different counts", "failures": []}
    failures = []
    kinds: dict[str, int] = {}
    for k, (row, listing) in enumerate(zip(rows, corners, strict=True), 1):
        m = match(listing, corners_of_pose(row))
        if m is None:
            failures.append(k)
        else:
            key = f"offset {m[0]}, {'counterclockwise' if m[1] > 0 else 'clockwise'}"
            kinds[key] = kinds.get(key, 0) + 1
    return {"holds": not failures, "failures": failures, "listings": kinds}
