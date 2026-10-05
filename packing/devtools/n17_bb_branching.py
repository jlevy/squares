"""Optional branching rules for the n17 sub-pattern branch and bound.

A rule changes only which node is split and where; every closure and every bound move is
still the pilot's outward-rounded `dual_bound`, and a recorded certificate keeps the
pilot's format. The standing verifier accepts any split point inside the parent interval.

- `mid`: score each square by the number of pairs that overlap (separating-axis depth on
  the four axes of the two squares) at the LP centres with every angle at its interval
  midpoint; bisect the highest-scoring square among those at least `split_ratio` of the
  widest, ties to the wider. Pair splits are the pilot's.
- `b2`: as `mid` until any weight is learned. Every node closed by the LP passes each
  positive multiplier's share `y / sum(y)` of a pair-owned row to both squares of the
  pair; a node closed by `disc` or `pair` adds 1 to both squares. Angle splits then
  bisect the eligible square with the largest weight, ties to the wider.
- `--decay G` (b2 only): each closure scales the weight of later closures by `G`, so old
  evidence fades; 1.1 is the measured best (B2d).

Usage, from `packing/`, with the same arguments as `devtools.n17_bb_native`:

    python -m devtools.n17_bb_branching --rule b2 [--decay 1.1] --native-dir DIR \\
        --cells ... [--save-certificate DIR]
"""

from __future__ import annotations

import argparse
import math
from collections import defaultdict
from collections.abc import Sequence
from typing import cast

from devtools import n17_bb_native as native
from devtools import pilot_n17_subpattern_bb as pilot

RULES = ("mid", "b2")
RESCALE_AT = 1e200


def _half(theta: float, phi: float) -> float:
    a = theta - phi
    return 0.5 * (abs(math.cos(a)) + abs(math.sin(a)))


def mid_overlap(node: pilot.Node, point: Sequence[float], i: int, j: int) -> float:
    """Overlap depth of squares i and j at the LP centres and midpoint angles; > 0 overlaps."""
    ti = 0.5 * sum(node.angles[i])
    tj = 0.5 * sum(node.angles[j])
    dx, dy = point[2 * j] - point[2 * i], point[2 * j + 1] - point[2 * i + 1]
    depth = math.inf
    for phi in (ti, ti + math.pi / 2, tj, tj + math.pi / 2):
        projection = abs(math.cos(phi) * dx + math.sin(phi) * dy)
        depth = min(depth, _half(ti, phi) + _half(tj, phi) - projection)
    return depth


def _relax_violation(term: pilot.PairTerm, point: Sequence[float], i: int, j: int) -> float:
    dx, dy = point[2 * j] - point[2 * i], point[2 * j + 1] - point[2 * i + 1]
    return min(r - (nx * dx + ny * dy) for nx, ny, r in term.planes)


def _bisect(node: pilot.Node, boxes: tuple[pilot.Box, ...], s: int) -> list[pilot.Node]:
    lo, hi = node.angles[s]
    mid = 0.5 * (lo + hi)
    kids: list[pilot.Node] = []
    for part in ((lo, mid), (mid, hi)):
        angles = list(node.angles)
        angles[s] = part
        kids.append(
            pilot.Node(tuple(angles), boxes, node.windows, node.depth + 1, node.share / 2)
        )
    return kids


class Weights:
    """B2's learned weight per square, with optional decay."""

    def __init__(self, decay: float) -> None:
        self.decay = decay
        self.scale = 1.0
        self.weight: defaultdict[int, float] = defaultdict(float)

    def learn(self, pattern: pilot.Pattern, evaluation: pilot.Evaluation) -> None:
        if evaluation.pruned is None or not evaluation.blame:
            return
        for owner, share in evaluation.blame.items():
            if owner >= 0:
                i, j = pattern.pairs[owner]
                self.weight[i] += share * self.scale
                self.weight[j] += share * self.scale
        if self.decay != 1.0:
            self.scale *= self.decay
            if self.scale > RESCALE_AT:
                for q in self.weight:
                    self.weight[q] /= self.scale
                self.scale = 1.0


def install(rule: str, decay: float = 1.0) -> None:
    """Replace `Solver.children` (and, for b2, wrap `Solver.assess`) with the named rule."""
    if rule not in RULES:
        raise ValueError(f"unknown rule {rule!r}; expected one of {RULES}")
    original_children = pilot.Solver.children
    original_assess = pilot.Solver.assess
    weights: dict[int, Weights] = {}

    def learned(solver: pilot.Solver) -> Weights:
        return weights.setdefault(id(solver), Weights(decay))

    def children_mid(
        self: pilot.Solver, node: pilot.Node, evaluation: pilot.Evaluation
    ) -> tuple[str, list[pilot.Node]] | None:
        pattern, point = self.pattern, evaluation.point
        if point is None:
            return original_children(self, node, evaluation)
        score = [0.0] * pattern.k
        chosen: tuple[float, int, pilot.PairTerm] | None = None
        for index, term in evaluation.terms:
            i, j = pattern.pairs[index]
            if mid_overlap(node, point, i, j) > 0:
                score[i] += 1.0
                score[j] += 1.0
            violation = _relax_violation(term, point, i, j)
            if (
                violation > pilot.VIOLATED
                and term.kind == "undecided"
                and (chosen is None or violation > chosen[0])
            ):
                chosen = (violation, index, term)
        if chosen is not None:
            _, index, term = chosen
            kids: list[pilot.Node] = []
            for option in term.options:
                windows = list(node.windows)
                windows[index] = option
                kids.append(
                    pilot.Node(
                        node.angles,
                        evaluation.boxes,
                        tuple(windows),
                        node.depth + 1,
                        node.share / len(term.options),
                    )
                )
            return "pair", kids
        widths = [hi - lo for lo, hi in node.angles]
        widest = max(widths)
        if widest < self.settings.floor:
            return None
        ratio = self.settings.split_ratio
        s = max(
            range(pattern.k), key=lambda q: (widths[q] >= ratio * widest, score[q], widths[q])
        )
        return "angle", _bisect(node, evaluation.boxes, s)

    def children_b2(
        self: pilot.Solver, node: pilot.Node, evaluation: pilot.Evaluation
    ) -> tuple[str, list[pilot.Node]] | None:
        outcome = children_mid(self, node, evaluation)
        weight = learned(self).weight
        if outcome is None or outcome[0] != "angle" or not weight:
            return outcome
        widths = [hi - lo for lo, hi in node.angles]
        widest = max(widths)
        ratio = self.settings.split_ratio
        s = max(
            range(self.pattern.k),
            key=lambda q: (widths[q] >= ratio * widest, weight[q], widths[q]),
        )
        return "angle", _bisect(node, evaluation.boxes, s)

    def assess_b2(self: pilot.Solver, node: pilot.Node) -> pilot.Evaluation:
        evaluation = original_assess(self, node)
        learned(self).learn(self.pattern, evaluation)
        return evaluation

    if rule == "mid":
        pilot.Solver.children = children_mid
    else:
        pilot.Solver.children = children_b2
        pilot.Solver.assess = assess_b2


def main(argv: list[str] | None = None) -> int:
    """Install a rule, then forward the remaining arguments to `devtools.n17_bb_native`."""
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    _ = parser.add_argument("--rule", choices=RULES, required=True)
    _ = parser.add_argument("--decay", type=float, default=1.0)
    args, rest = parser.parse_known_args(argv)
    install(cast(str, args.rule), cast(float, args.decay))
    return native.main(rest)


if __name__ == "__main__":
    raise SystemExit(main())
