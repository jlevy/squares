#!/usr/bin/env python3
"""Read a retained record and take structure off it, at a chosen level of detail.

The structure ladder's data source. The point of the ladder is that the *amount* of
structure handed to a search is the independent variable: the full contact structure of a
record is the answer, and realising it is an LP, so the question worth asking is how
little suffices. This module produces the rungs.

Nothing here is used to steer a search that then reports a result against the same record
without saying so. A run is labelled by exactly what it was given.

Usage, from `packing/`:
    uv run --frozen python -m devtools.known_structure --n 11 17
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np

from devtools.divide_and_concur import (
    Array,
    corners_of,
    edge_axes,
    pair_separation,
    wall_clearance,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
WITNESSES = ROOT / "witnesses/known-best"


def record(n: int) -> tuple[Array, float]:
    """The retained best-known packing for `n`, as poses and a side."""
    payload = safe_load((WITNESSES / f"n-{n:03d}.yaml").read_text(encoding="utf-8"))["witness"]
    poses = np.array(
        [
            [
                float(s["center"][0]),
                float(s["center"][1]),
                math.radians(float(s["angle"])),
            ]
            for s in payload["squares"]
        ]
    )
    return poses, float(payload["side"])


def contact_edges(poses: Array, tol: float = 1e-9) -> list[tuple[int, int]]:
    """Which pairs touch. The labelled contact graph, rung four of the ladder."""
    v = corners_of(poses)
    n = len(poses)
    ia, ib = np.triu_indices(n, 1)
    close = np.abs(pair_separation(v[ia], v[ib])) < tol
    return [(int(i), int(j)) for i, j, k in zip(ia, ib, close, strict=True) if k]


def wall_contacts(poses: Array, side: float, tol: float = 1e-9) -> list[int]:
    """Which squares touch the container."""
    v = corners_of(poses)
    return [i for i, c in enumerate(wall_clearance(v, side)) if abs(float(c)) < tol]


def angle_classes(poses: Array, tol: float = 1e-6) -> list[list[int]]:
    """Which squares share an orientation, modulo the square's own quarter turn.

    The lowest rung: for `n = 11` this is the two numbers "six at one angle, five at
    another", naming neither the angle nor which square is which.
    """
    reduced = np.mod(poses[:, 2], math.pi / 2)
    classes: list[list[int]] = []
    for i, a in enumerate(reduced):
        for group in classes:
            b = reduced[group[0]]
            if min(abs(a - b), math.pi / 2 - abs(a - b)) < tol:
                group.append(i)
                break
        else:
            classes.append([i])
    return classes


def thinned(
    edges: list[tuple[int, int]], keep: int, rng: np.random.Generator
) -> list[tuple[int, int]]:
    """A random subset of a contact graph -- the rungs between "nothing" and "all of it"."""
    if keep >= len(edges):
        return list(edges)
    picked = rng.choice(len(edges), size=keep, replace=False)
    return [edges[int(i)] for i in sorted(picked)]


def rewired(
    edges: list[tuple[int, int]], n: int, swaps: int, rng: np.random.Generator
) -> list[tuple[int, int]]:
    """A contact graph with `swaps` edges replaced by pairs that do NOT touch at the record.

    The control the ladder needs. A search handed the record's own graph is being told the
    answer's shape; one handed a graph of the same size and degree that is *wrong* is being
    told a lie of the same length, and the difference between the two is what says whether
    the structure carried information or the constraint count merely helped.
    """
    have = {(min(i, j), max(i, j)) for i, j in edges}
    absent = [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in have]
    out = list(edges)
    for _ in range(min(swaps, len(out), len(absent))):
        out.pop(int(rng.integers(len(out))))
        out.append(absent.pop(int(rng.integers(len(absent)))))
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="+", required=True)
    o = ap.parse_args()
    for n in o.n:
        poses, side = record(n)
        edges = contact_edges(poses)
        walls = wall_contacts(poses, side)
        classes = angle_classes(poses)
        print(
            f"n = {n:3d}  side {side:.12f}  {len(edges)} pair contacts, "
            f"{len(walls)} squares on a wall, {len(classes)} angle classes "
            f"{[len(c) for c in classes]}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def contact_kinds(poses: Array, tol: float = 1e-7) -> dict[tuple[int, int], str]:
    """Classify each contact as edge-edge, corner-edge or corner-corner.

    The middle rung of the ladder, and the one that buys the most constraint per bit. A
    bare adjacency says two squares touch and leaves their relative orientation entirely
    free; an **edge-edge** contact pins it to a multiple of a quarter turn, which is a
    strong statement about the configuration made without naming a single angle. Corner
    contacts say nothing about orientation, so the same graph can be loose in some places
    and tight in others -- which is the flexibility worth keeping.

    The classification counts how many corners of each square lie on the contact line: two
    is an edge, one is a corner.
    """
    v = corners_of(poses)
    kinds: dict[tuple[int, int], str] = {}
    for i, j in contact_edges(poses, tol=tol):
        u = _contact_axis(v[i], v[j])
        on_i = int((np.abs(v[i] @ u - (v[i] @ u).max()) < tol).sum())
        on_j = int((np.abs(v[j] @ u - (v[j] @ u).min()) < tol).sum())
        if (v[j] @ u).min() < (v[i] @ u).min():
            on_i = int((np.abs(v[i] @ u - (v[i] @ u).min()) < tol).sum())
            on_j = int((np.abs(v[j] @ u - (v[j] @ u).max()) < tol).sum())
        name = {(2, 2): "edge-edge", (1, 1): "corner-corner"}.get((on_i, on_j), "corner-edge")
        kinds[(i, j)] = name
    return kinds


def _contact_axis(va: Array, vb: Array) -> Array:
    """The direction along which a touching pair is separated, from its own edge normals."""
    axes = np.concatenate([edge_axes(va[None]), edge_axes(vb[None])], axis=-2)[0]
    a, b = va @ axes.T, vb @ axes.T
    gap = np.maximum(a.min(0) - b.max(0), b.min(0) - a.max(0))
    return axes[int(gap.argmax())]
