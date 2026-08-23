"""Basin identity: the thing that makes "basin" a noun rather than an impression.

A **basin** is the preimage of one quench endpoint. Two quench runs land in the same
basin when they land on the *same packing*, and until something decides that question,
every basin count is a count of floating-point strings and every discovery curve is an
artifact of the tolerance used to compare them ([D-020](../defects.md)).

Deciding it needs two things this module supplies, at two different prices:

1. **A geometric key** — quantize, canonicalise over the container's symmetries and over
   square relabelling, hash. Cheap, and the fast path for deduplication.
2. **A contact-graph certificate** — the combinatorial structure, canonical up to
   isomorphism. Expensive, and the ground truth: it is what "the same *arrangement*"
   actually means, and it survives the continuous wobble the geometric key does not.

## Which is authoritative, and how each fails

They fail in opposite directions, which is the reason to carry both.

- The **geometric key can split one basin into two**. Two coordinates either side of a
  quantization boundary hash differently while being equal to well within tolerance. The
  contact certificate resolves those: same certificate, adjacent sides, one basin.
- The **contact certificate can merge two basins into one**. Two genuinely different
  packings can share a contact graph — the graph forgets the metric entirely. The
  geometric key separates those.

So: **two configurations are the same basin when both keys agree.** Disagreement is not
an error, it is information, and `BasinKey.agrees_with` reports which kind.

## What this does not do

It does not decide whether a configuration is a local optimum, and it does not verify
validity. Feed it quench output; route anything that will claim a record through
`sqpack.verify`, which is the only thing here entitled to the word `exact`.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass

from sqpack.quench import angle_classes, contacts

QUARTER = math.pi / 2

# Well above the quench's ~1e-11 noise floor (D-021) and far below any distinction
# between real basins, which differ in the side by 1e-3 and up at the n this is aimed at.
DEFAULT_QUANTUM = 1e-6


def _fold(theta: float) -> float:
    """A unit square is invariant under a quarter turn, so only theta mod pi/2 is real."""
    return theta % QUARTER


def d4_images(
    x: list[float], y: list[float], theta: list[float], side: float
) -> list[tuple[list[float], list[float], list[float]]]:
    """The eight images of a configuration under the container's symmetry group.

    The container is a square, so a packing and its reflection are the same packing;
    counting them separately would inflate every basin count by up to eight.

    Angles work out simply because of the quarter-turn invariance above: the four
    rotations leave `theta mod pi/2` **unchanged**, and the four reflections send it to
    `-theta`. So only the centres really move.
    """
    out = []
    for flip in (False, True):
        for turn in range(4):
            nx, ny = list(x), list(y)
            for _ in range(turn):
                nx, ny = ny, [side - v for v in nx]
            if flip:
                nx = [side - v for v in nx]
            nt = [_fold(-t if flip else t) for t in theta]
            out.append((nx, ny, nt))
    return out


def _quantize_angle(theta: float, quantum: float) -> int:
    """Quantize an angle ON A CIRCLE, so the seam at pi/2 is not a discontinuity.

    An angle is periodic with period pi/2 -- a unit square is invariant under a quarter
    turn -- and quantizing a periodic quantity with plain `round(t / quantum)` splits it
    at the wrap-around. An axis-aligned square whose angle floats one ULP BELOW pi/2
    then keys as 1570796 while its identical twin at 0.0 keys as 0, and the two are
    recorded as different basins.

    That is not hypothetical: it was live, and the n = 3 golden caught it. Two quenches
    of the trivial three-in-a-2x2 packing produced squares at identical positions, one
    set at 0 degrees and one at 90, and the atlas stored them as two distinct basins.
    Every basin count anywhere near an axis-aligned optimum was inflated by it, and the
    annealer makes it common by accumulating rotations without wrapping.

    Working in integer steps of the period makes the modulo exact: `STEPS` steps span
    exactly one quarter turn, so step `STEPS` and step `0` are the same angle by
    construction rather than by a tolerance.

    The trailing `% steps` does all the folding on its own, negative angles included
    (Python's modulo is floored), so there is deliberately no `theta % QUARTER` in front
    of it. There was one; it was dead code, and it cost a negative control the day it
    stopped being reachable -- the control mutated it, nothing changed, and the suite
    reported a guard that no longer guarded anything.
    """
    steps = max(1, round(QUARTER / quantum))
    return round(theta / QUARTER * steps) % steps


def geometric_key(
    x: list[float],
    y: list[float],
    theta: list[float],
    side: float,
    *,
    quantum: float = DEFAULT_QUANTUM,
) -> str:
    """A digest invariant under container symmetry and square relabelling.

    Relabelling is handled by sorting the squares rather than by trying permutations:
    the sorted tuple of (quantized x, y, angle) is the same list whatever order the
    squares arrived in. Container symmetry is handled by taking the smallest digest over
    all eight images. Angles are quantized on the circle -- see `_quantize_angle`.
    """
    best = None
    for ix, iy, it in d4_images(x, y, theta, side):
        squares = sorted(
            (round(a / quantum), round(b / quantum), _quantize_angle(t, quantum))
            for a, b, t in zip(ix, iy, it, strict=True)
        )
        payload = repr((round(side / quantum), squares)).encode()
        digest = hashlib.blake2b(payload, digest_size=16).hexdigest()
        if best is None or digest < best:
            best = digest
    assert best is not None
    return best


def _boundary_touches(
    x: list[float], y: list[float], theta: list[float], side: float, tol: float
) -> list[int]:
    """How many container walls each square touches.

    A strong, cheap and geometrically meaningful node attribute: the squares pinned
    against the frame are exactly the ones a packing's structure hangs from.
    """
    out = []
    for cx, cy, t in zip(x, y, theta, strict=True):
        half = (abs(math.cos(t)) + abs(math.sin(t))) / 2
        out.append(
            sum(
                1
                for v in (cx - half, side - (cx + half), cy - half, side - (cy + half))
                if abs(v) <= tol
            )
        )
    return out


def _refine(colours: list[int], adjacency: list[set[int]]) -> list[int]:
    """One-dimensional Weisfeiler-Leman: recolour by (own colour, sorted neighbour
    colours) until nothing changes. Cheap, and usually enough on its own."""
    while True:
        signature = [
            (colours[v], tuple(sorted(colours[u] for u in adjacency[v])))
            for v in range(len(colours))
        ]
        ranks = {s: i for i, s in enumerate(sorted(set(signature)))}
        new = [ranks[s] for s in signature]
        if new == colours:
            return colours
        colours = new


def _certificate(colours: list[int], adjacency: list[set[int]]) -> str:
    """Canonical form by individualization-refinement.

    Refinement alone leaves ties wherever the graph has symmetry. The standard fix, and
    the one `nauty` is built on: pick the smallest ambiguous colour class, individualise
    each of its vertices in turn, recurse, and keep the lexicographically smallest
    result. Exhaustive, so the answer is a genuine canonical form rather than a hash
    that usually works -- and at the `n <= 12` this campaign runs, cheap.
    """
    colours = _refine(colours, adjacency)
    classes: dict[int, list[int]] = {}
    for v, c in enumerate(colours):
        classes.setdefault(c, []).append(v)

    ambiguous = [vs for vs in classes.values() if len(vs) > 1]
    if not ambiguous:
        order = sorted(range(len(colours)), key=lambda v: colours[v])
        position = {v: i for i, v in enumerate(order)}
        edges = sorted(
            tuple(sorted((position[u], position[v])))
            for u in range(len(colours))
            for v in adjacency[u]
            if u < v
        )
        return repr((sorted(colours), edges))

    smallest = min(ambiguous, key=len)
    return min(
        _certificate([c * 2 + (v == pick) for v, c in enumerate(colours)], adjacency)
        for pick in smallest
    )


def contact_certificate(
    x: list[float],
    y: list[float],
    theta: list[float],
    side: float,
    *,
    tol: float = 1e-9,
) -> str:
    """The contact graph, canonical up to isomorphism, with geometric node attributes.

    Nodes carry their angle class and their count of container-wall contacts. Those
    attributes are not decoration: without them two structurally different packings that
    happen to share a contact *graph* would certify identically, and with them the graph
    already separates almost everything before the search below has to run.
    """
    n = len(x)
    adjacency: list[set[int]] = [set() for _ in range(n)]
    for i, j in contacts(x, y, theta, tol=tol):
        adjacency[i].add(j)
        adjacency[j].add(i)

    # Angle classes are labelled by size then by representative angle, so the labelling
    # does not depend on the order the squares happened to arrive in.
    groups = angle_classes(theta)
    ordered = sorted(groups, key=lambda g: (len(g), round(_fold(theta[g[0]]), 9)))
    angle_of = {v: rank for rank, group in enumerate(ordered) for v in group}

    walls = _boundary_touches(x, y, theta, side, tol)
    initial = [(angle_of[v], walls[v], len(adjacency[v])) for v in range(n)]
    ranks = {a: i for i, a in enumerate(sorted(set(initial)))}
    digest = _certificate([ranks[a] for a in initial], adjacency).encode()
    return hashlib.blake2b(digest, digest_size=16).hexdigest()


@dataclass(frozen=True)
class BasinKey:
    """What identifies a basin, at both prices. See the module docstring for which
    is authoritative when they disagree."""

    n: int
    geometric: str
    contact: str
    side: float
    angle_signature: tuple[int, ...]
    contact_count: int

    def agrees_with(self, other: BasinKey) -> str:
        """`same`, or the direction of the disagreement, named so a caller can act.

        `same-arrangement-different-metric` and `same-metric-different-arrangement` are
        both real answers rather than errors: the first is usually one basin the
        quantizer split, the second is two basins the contact graph merged.
        """
        if self.geometric == other.geometric and self.contact == other.contact:
            return "same"
        if self.contact == other.contact:
            return "same-arrangement-different-metric"
        if self.geometric == other.geometric:
            return "same-metric-different-arrangement"
        return "different"


def canonical_key(
    x: list[float],
    y: list[float],
    theta: list[float],
    side: float,
    *,
    quantum: float = DEFAULT_QUANTUM,
    tol: float = 1e-9,
) -> BasinKey:
    """Both keys for one configuration, plus the descriptors that come free with them."""
    folded = [_fold(t) for t in theta]
    sizes = tuple(sorted(len(g) for g in angle_classes(folded)))
    return BasinKey(
        n=len(x),
        geometric=geometric_key(x, y, folded, side, quantum=quantum),
        contact=contact_certificate(x, y, folded, side, tol=tol),
        side=side,
        angle_signature=sizes,
        contact_count=len(contacts(x, y, folded, tol=tol)),
    )
