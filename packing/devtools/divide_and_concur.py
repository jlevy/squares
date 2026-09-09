#!/usr/bin/env python3
"""Divide and concur, searched with relaxed-reflect-reflect, for unit squares in a square.

The mechanism the [2026-09-09 simulation
survey](../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)
ranks first, and the one nobody has run on squares in a bounded container. It is the only
method in either survey with a cold, whole-benchmark result on the sibling problem: Gravel
and Elser ran it on `n` equal disks in a unit square for every `n` from 2 to 200, reaching
the best known within `1e-9` on 143 of 197 and beating it on 38, using no information
about the packings beyond their densities.

It needs no potential, no derivative and no smoothness -- only two projections and their
reflection. That is the property that matters here. The penalty physics measured on
2026-09-08 could not produce a single feasible arrangement in 48 runs, because a penalty
force settles where the springs balance the walls and the leftover overlap there is
pressure divided by stiffness. A projection has no such floor: it either lands on the
constraint set or it does not, and the fixed points of this iteration are packings.

**The state is corners, not poses**, which is Kallus's formulation and is load-bearing.
Each square carries one replica per constraint it takes part in -- one for each of the
other `n - 1` squares, one for the container -- and a replica is four points, free to stop
being a square in between projections.

- The **divide** projection asks each constraint alone to be satisfied, in corner space,
  where both constraints are easy and exact: a pair is separated by moving only the
  corners that cross the cheapest separating line onto it, and the container is satisfied
  by clamping corners into the box.
- The **concur** projection asks all the replicas of one square to agree *and* to be a
  unit square. Averaging then rigidifying is the exact projection onto that set, because
  the squared distance splits into spread-about-the-mean plus mean-to-square.

Rigidifying on the concur side rather than the divide side is what makes rotation happen
at all, and two cheaper arrangements were built and measured before this one. A pose-space
version with translation-only projections leaves every angle frozen at its random initial
value forever, because nothing in either projection ever changes an angle. A pose-space
version that rigidifies inside the divide step separates an overlapping pair by only half
of what it needs -- measured at a residual depth of `0.688` over random overlapping pairs,
against `1.7e-16` for this one -- because the fit averages the corners it moved against
the corners it did not.

The iteration is `x <- x + beta (P_B(2 P_A(x) - x) - P_A(x))`.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]
Index = NDArray[np.intp]
"""Integer index arrays, kept distinct from `Array` so the type checker can tell a
replica lookup from a coordinate."""

LOCAL = np.array([[0.5, 0.5], [-0.5, 0.5], [-0.5, -0.5], [0.5, -0.5]])
"""Body-frame corners, in a fixed order. This order is the correspondence the rigidifying
fit relies on, so it must not be permuted between the two ends of a step."""

BISECTIONS = 24
"""Steps used to place a separating line. Feasibility does not depend on this number --
corners are pushed *onto* whatever line is chosen, so the divide step separates exactly at
any precision -- only how much motion it costs. Measured residual depth at 24 steps is
`1.7e-16` over 400 random overlapping pairs."""


def corners_of(pose: Array) -> Array:
    """Corners of each pose, shaped `(..., 4, 2)`."""
    c, s = np.cos(pose[..., 2]), np.sin(pose[..., 2])
    lx, ly = LOCAL[:, 0], LOCAL[:, 1]
    x = pose[..., 0, None] + lx * c[..., None] - ly * s[..., None]
    y = pose[..., 1, None] + lx * s[..., None] + ly * c[..., None]
    return np.stack([x, y], axis=-1)


def pose_of(v: Array) -> Array:
    """The unit square nearest a set of four labelled corners, as `(x, y, theta)`.

    Orthogonal Procrustes in two dimensions, closed form: the centre is the centroid and
    the angle is the arctangent of the summed cross and dot products against the body
    frame. Scale is not a free parameter -- the squares are congruent, which is the whole
    problem -- so this fits rotation and translation only.
    """
    mean = v.mean(axis=-2)
    d = v - mean[..., None, :]
    num = (LOCAL[:, 0] * d[..., 1] - LOCAL[:, 1] * d[..., 0]).sum(axis=-1)
    den = (LOCAL[:, 0] * d[..., 0] + LOCAL[:, 1] * d[..., 1]).sum(axis=-1)
    return np.stack([mean[..., 0], mean[..., 1], np.arctan2(num, den)], axis=-1)


def _edge_axes(v: Array) -> Array:
    """The four outward edge normals of each quadrilateral, shaped `(..., 4, 2)`."""
    e = np.roll(v, -1, axis=-2) - v
    u = np.stack([e[..., 1], -e[..., 0]], axis=-1)
    return u / np.maximum(np.linalg.norm(u, axis=-1, keepdims=True), 1e-12)


def _axis_spans(va: Array, vb: Array) -> tuple[Array, Array, Array]:
    """Both corner sets resolved along every candidate separating direction."""
    axes = np.concatenate([_edge_axes(va), _edge_axes(vb)], axis=-2)
    return axes, np.einsum("pkc,pac->pka", axes, va), np.einsum("pkc,pac->pka", axes, vb)


def project_pairs(va: Array, vb: Array) -> tuple[Array, Array]:
    """Project a pair of corner sets onto "a line separates these two".

    The candidate lines are the sixteen signed edge normals of the two quadrilaterals.
    That is the separating-axis theorem's own list: for convex bodies, if a separating
    line exists then one of these directions carries it. For each direction the offset
    that costs least total squared corner motion is found by bisection, because the
    derivative of that cost is monotone and piecewise linear and nothing subtler is
    needed. Only the corners that cross the winning line move, and they move onto it.
    """
    base, _, _ = _axis_spans(va, vb)
    axes = np.concatenate([base, -base], axis=-2)
    a = np.einsum("pkc,pac->pka", axes, va)
    b = np.einsum("pkc,pac->pka", axes, vb)

    lo = np.minimum(a.min(-1), b.min(-1))
    hi = np.maximum(a.max(-1), b.max(-1))
    for _ in range(BISECTIONS):
        mid = 0.5 * (lo + hi)
        slope = np.maximum(0.0, mid[..., None] - b).sum(-1) - np.maximum(
            0.0, a - mid[..., None]
        ).sum(-1)
        lo = np.where(slope < 0, mid, lo)
        hi = np.where(slope < 0, hi, mid)
    off = 0.5 * (lo + hi)

    push_a = np.maximum(0.0, a - off[..., None])
    push_b = np.maximum(0.0, off[..., None] - b)
    best = ((push_a**2).sum(-1) + (push_b**2).sum(-1)).argmin(-1)

    idx = np.arange(axes.shape[0])
    u = axes[idx, best]
    return (
        va - push_a[idx, best][..., None] * u[:, None, :],
        vb + push_b[idx, best][..., None] * u[:, None, :],
    )


def pair_separation(va: Array, vb: Array) -> Array:
    """Signed clearance of each pair: positive apart, negative overlapping."""
    _, a, b = _axis_spans(va, vb)
    return np.maximum(a.min(-1) - b.max(-1), b.min(-1) - a.max(-1)).max(-1)


def wall_clearance(v: Array, side: float) -> Array:
    """Signed room each square has against the container: positive inside."""
    return np.minimum(v.min(axis=(-2, -1)), side - v.max(axis=(-2, -1)))


def violation(poses: Array, side: float) -> float:
    """How far this arrangement is from being a packing, in units of the square's side.

    The larger of two quantities: how far any corner lies outside the container, and the
    deepest pairwise penetration by the separating-axis theorem. Zero means a packing.

    This is the number the penalty calibration of 2026-09-08 had no way to drive to zero,
    and the reason its reported container sides were smaller than geometry allows. Every
    side this module reports is one at which this number is zero.
    """
    v = corners_of(poses)
    wall = -float(wall_clearance(v, side).min())
    n = len(poses)
    if n > 1:
        ia, ib = np.triu_indices(n, 1)
        depth = -float(pair_separation(v[ia], v[ib]).min())
    else:
        depth = 0.0
    return max(0.0, wall, depth)
