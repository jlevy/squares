"""Prototype: coupling each pair's normal to its square's angle column (lane P2).

Not a certifier and not wired into certificates: a measurement of whether coupling pays.
`diagnose_n17_bb_losses` found most closable open boxes held by the normals' range: each
pair's planes take a square's normal anywhere in the box, independently of its other
pairs. Here the normal is tied to the angle offset `t_f` (the Taylor mode's columns).

The rows. A pair separated along the normal of square `f` at turn `k` has, with the
piece's normal angles `[lo, hi]`, a float reference `phi0` in it, `tau = phi - phi0 =
t_f + e` (`e` an enclosed constant), `p = n(phi0) . d` and `q = n_perp(phi0) . d`:

    g <= n(phi) . d = p cos tau + q sin tau <= p + tau q + R,
    R = |d|max (tau_m^2 / 2 + tau_m^3 / 6),

and McCormick's two upper envelopes of `tau q` on `[tau_lo, tau_hi] x [q_lo, q_hi]`
(`tau q <= tau_hi q + q_lo tau - tau_hi q_lo`, and the same with lo and hi swapped) give
two rows linear in the centres and `t_f`. The float normals' distance to the enclosed
ones, the constant `e` and the floats' own rounding are charged on the right side, so the
rows are valid (outward) wherever the pair uses that piece. They are added when every
possible piece of the pair belongs to one square and turn; otherwise the pair keeps only
the interval form's cuts. The loss is first order in the angle width times the d-box's
tangential width, which bound tightening shrinks.

`estimate` here is the pilot's Knuth estimator on this solver; `coverage` counts how many
pair terms got coupled rows.

Branching on the separating square. Almost every pair at an open node can be separated
by a normal of either square, and a convex relaxation of that choice loses the coupling
(each side leaves the other square's angle free). `BranchingCoupledSolver` resolves it by
a new branch type: a pair whose interval cuts are tight at the LP point, and whose live
normals are one turn of each square, splits into "separated by square i's normal" and
"by square j's normal" (the separating axis theorem's two cases, so the children cover
the node). In a labelled child the pair's coupled rows use that square only, and a label
with no live normal closes the child.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devtools import pilot_n17_subpattern_bb as bb

SCHEMA = "n17-bb-coupled-prototype/v1"


def interval_dot(n: tuple[bb.Iv, bb.Iv], dx: bb.Iv, dy: bb.Iv) -> bb.Iv:
    return bb.iadd(bb.imul(n[0], dx), bb.imul(n[1], dy))


class CoupledSolver(bb.Solver):
    """The pilot's solver with McCormick rows tying single-piece pairs to angle columns.

    Needs `Settings(taylor=True)` for the angle columns; `taylor_rows` keeps or drops the
    Taylor mode's own gap cuts and wall rows.
    """

    def __init__(
        self, pattern: bb.Pattern, settings: bb.Settings, *, taylor_rows: bool = False
    ) -> None:
        if not settings.taylor:
            raise ValueError("the coupled rows need the angle columns of Taylor mode")
        super().__init__(pattern, settings)
        self.taylor_rows = taylor_rows
        self.coverage = {"pair_terms": 0, "coupled": 0}

    def pair_taylor(self, *args: Any, **kwargs: Any) -> Any:
        return super().pair_taylor(*args, **kwargs) if self.taylor_rows else []

    def wall_rows(self, boxes: tuple[bb.Box, ...]) -> list[bb.Row]:
        return super().wall_rows(boxes) if self.taylor_rows else []

    def relaxation(
        self, node: bb.Node, boxes: tuple[bb.Box, ...]
    ) -> tuple[bb.Evaluation, list[bb.Row]]:
        evaluation, rows = super().relaxation(node, boxes)
        if evaluation.pruned is None:
            for index, _ in evaluation.terms:
                self.coverage["pair_terms"] += 1
                try:
                    coupled = self.coupled_rows(node, boxes, index)
                except EmptyFamilyError:
                    # The labelled square has no normal any pose can use: the node is empty.
                    return bb.Evaluation("pair", blame={index: 1.0}), rows
                if coupled:
                    self.coverage["coupled"] += 1
                    rows.extend(coupled)
        return evaluation, rows

    def family(self, node: bb.Node, index: int) -> int | None:
        """The square whose normal separates the pair in this node, when labelled."""
        del node, index
        return None

    def live_normals(
        self, node: bb.Node, boxes: tuple[bb.Box, ...], index: int
    ) -> list[tuple[int, int, float, float]]:
        """`(square, turn, lo, hi)` of every normal piece of the pair a pose can use."""
        i, j = self.pattern.pairs[index]
        dx, dy = bb.difference_box(boxes[i], boxes[j])
        squared = bb.squared_range(dx, dy)
        g_lo = bb.gap_lower(node.angles[i], node.angles[j])
        d_max = bb.up(math.sqrt(squared[1]))
        live: list[tuple[int, int, float, float]] = []
        for square in (i, j):
            theta = node.angles[square]
            for k in range(4):
                shift = bb.HALF_PI_MULTIPLES[k]
                base = (bb.dn(theta[0] + shift[0]), bb.up(theta[1] + shift[1]))
                live.extend(
                    (square, k, part[0], part[1])
                    for part in bb.in_window(base, node.windows[index])
                    if bb.option_planes(*part, dx, dy, d_max=d_max, g_lo=g_lo)
                )
        return live

    def coupled_rows(
        self, node: bb.Node, boxes: tuple[bb.Box, ...], index: int
    ) -> list[bb.Row]:
        i, j = self.pattern.pairs[index]
        dx, dy = bb.difference_box(boxes[i], boxes[j])
        squared = bb.squared_range(dx, dy)
        if squared[0] >= 2.0:
            return []
        g_lo = bb.gap_lower(node.angles[i], node.angles[j])
        d_max = bb.up(math.sqrt(squared[1]))
        live = self.live_normals(node, boxes, index)
        label = self.family(node, index)
        if label is not None:
            live = [piece for piece in live if piece[0] == label]
            if not live:
                raise EmptyFamilyError(index)
        if not live or len({(square, k) for square, k, _, _ in live}) != 1:
            return []
        square, k = live[0][0], live[0][1]
        lo, hi = min(p[2] for p in live), max(p[3] for p in live)
        if bb.up(hi - lo) >= bb.HALF_PI[0]:
            return []
        assert self.taylor is not None
        centre = self.taylor.centres[square]
        phi0 = 0.5 * (lo + hi)
        shift = bb.HALF_PI_MULTIPLES[k]
        # tau = phi - phi0 = t_f + e, with e enclosed.
        e = (bb.dn(bb.dn(centre + shift[0]) - phi0), bb.up(bb.up(centre + shift[1]) - phi0))
        offset = self.taylor.offsets[square]
        tau = (
            max(bb.dn(lo - phi0), bb.dn(offset[0] + e[0])),
            min(bb.up(hi - phi0), bb.up(offset[1] + e[1])),
        )
        if tau[0] > tau[1]:
            return []
        tau_m = max(-tau[0], tau[1])
        c, s = bb.cos_sin(phi0)
        normal = (c, s)
        perp = (bb.ineg(s), c)
        q = interval_dot(perp, dx, dy)
        eps = max(bb.up(c[1] - c[0]), bb.up(s[1] - s[0]))
        reach = bb.up_add(bb.magnitude(dx), bb.magnitude(dy))
        slack = bb.up_mul(eps, reach)
        remainder = bb.up_mul(
            d_max, bb.up_add(bb.up(tau_m * tau_m) / 2, bb.up(bb.up(tau_m * tau_m) * tau_m) / 6)
        )
        rows: list[bb.Row] = []
        for t_end, q_end in ((tau[1], q[0]), (tau[0], q[1])):
            # nbar . d + t_end nbar_perp . d + q_end t_f >= g_lo - R + t_end q_end
            #   - max(q_end e) - slack (1 + |t_end|) - the float vector's rounding.
            vx = bb.iadd(normal[0], bb.imul((t_end, t_end), perp[0]))
            vy = bb.iadd(normal[1], bb.imul((t_end, t_end), perp[1]))
            ux, uy = 0.5 * (vx[0] + vx[1]), 0.5 * (vy[0] + vy[1])
            spread = max(bb.up(vx[1] - vx[0]), bb.up(vy[1] - vy[0]))
            charges = bb.up_add(
                bb.up_mul(slack, bb.up_add(1.0, abs(t_end))), bb.up_mul(spread, reach)
            )
            constant = bb.imul((q_end, q_end), e)[1]
            rhs = bb.dn(g_lo - remainder)
            rhs = bb.dn(rhs + bb.imul((t_end, t_end), (q_end, q_end))[0])
            rhs = bb.dn(bb.dn(rhs - constant) - charges)
            k_squares = self.pattern.k
            values = (ux, uy, -ux, -uy, -q_end)
            rows.append(
                bb.Row(
                    (2 * i, 2 * i + 1, 2 * j, 2 * j + 1, 2 * k_squares + square),
                    values,
                    -rhs,
                    1.0,
                    tuple((value, value) for value in values),
                    (-rhs, -rhs),
                    index,
                )
            )
        return rows


class EmptyFamilyError(Exception):
    """A pair's labelled square has no normal piece that any pose of the node can use."""


@dataclass(frozen=True)
class LabelledNode(bb.Node):
    """A node with, per pair, the square whose normal separates it (None: either)."""

    families: tuple[int | None, ...] = ()


class BranchingCoupledSolver(CoupledSolver):
    """Coupled rows, plus branching on which square's normal separates a pair."""

    def root(self) -> bb.Node:
        return self.labelled(super().root(), (None,) * len(self.pattern.pairs))

    @staticmethod
    def labelled(node: bb.Node, families: tuple[int | None, ...]) -> LabelledNode:
        return LabelledNode(
            node.angles, node.boxes, node.windows, node.depth, node.share, families
        )

    def family(self, node: bb.Node, index: int) -> int | None:
        return node.families[index] if isinstance(node, LabelledNode) else None

    def children(
        self, node: bb.Node, evaluation: bb.Evaluation
    ) -> tuple[str, list[bb.Node]] | None:
        families = (
            node.families
            if isinstance(node, LabelledNode)
            else (None,) * len(self.pattern.pairs)
        )
        outcome = super().children(node, evaluation)
        if outcome is not None and outcome[0] == "pair":
            return outcome[0], [self.labelled(kid, families) for kid in outcome[1]]
        pick = self.family_pick(node, evaluation, families)
        if pick is not None:
            kids: list[bb.Node] = []
            for square in self.pattern.pairs[pick]:
                labels = list(families)
                labels[pick] = square
                kids.append(
                    LabelledNode(
                        node.angles,
                        evaluation.boxes,
                        node.windows,
                        node.depth + 1,
                        node.share / 2,
                        tuple(labels),
                    )
                )
            return "family", kids
        if outcome is None:
            return None
        return outcome[0], [self.labelled(kid, families) for kid in outcome[1]]

    def family_pick(
        self, node: bb.Node, evaluation: bb.Evaluation, families: tuple[int | None, ...]
    ) -> int | None:
        """The unlabelled pair, one turn per square, whose interval cuts bind most."""
        point = evaluation.point
        if point is None:
            return None
        best: tuple[float, int] | None = None
        for index, term in evaluation.terms:
            if families[index] is not None or not term.cuts:
                continue
            turns: dict[int, set[int]] = {}
            for square, k, _, _ in self.live_normals(node, evaluation.boxes, index):
                turns.setdefault(square, set()).add(k)
            if len(turns) != 2 or any(len(ks) != 1 for ks in turns.values()):
                continue
            i, j = self.pattern.pairs[index]
            dx, dy = point[2 * j] - point[2 * i], point[2 * j + 1] - point[2 * i + 1]
            slack = min(ux * dx + uy * dy - v for ux, uy, v in term.cuts)
            if slack <= 1e-7 and (best is None or slack < best[0]):
                best = (slack, index)
        return None if best is None else best[1]


def estimate(
    pattern: bb.Pattern,
    dives: int,
    *,
    seed: int,
    coupled: bool,
    taylor_rows: bool,
    branching: bool = False,
) -> dict[str, Any]:
    """Knuth's estimate (as `bb.estimate`) with the coupled solver or the interval one."""
    rng = random.Random(seed)
    solver: bb.Solver
    if not coupled:
        solver = bb.Solver(pattern, bb.Settings())
    elif branching:
        solver = BranchingCoupledSolver(
            pattern, bb.Settings(taylor=True), taylor_rows=taylor_rows
        )
    else:
        solver = CoupledSolver(pattern, bb.Settings(taylor=True), taylor_rows=taylor_rows)
    started, cpu = time.perf_counter(), time.process_time()
    sizes: list[float] = []
    depths: list[int] = []
    evaluated = 0
    for _ in range(dives):
        node, weight, size = solver.root(), 1.0, 1.0
        while True:
            evaluated += 1
            evaluation = solver.assess(node)
            if evaluation.pruned is not None:
                break
            outcome = solver.children(node, evaluation) if node.depth < bb.MAX_DEPTH else None
            if outcome is None:
                break
            kids = outcome[1]
            weight *= len(kids)
            size += weight
            node = kids[rng.randrange(len(kids))]
        sizes.append(size)
        depths.append(node.depth)
    ordered = sorted(sizes)
    seconds = time.perf_counter() - started
    return {
        "dives": dives,
        "seed": seed,
        "coupled": coupled,
        "branching": branching,
        "taylor_rows": taylor_rows,
        "estimated_nodes_mean": sum(sizes) / len(sizes),
        "estimated_nodes_median": ordered[len(ordered) // 2],
        "estimated_nodes_max": ordered[-1],
        "mean_leaf_depth": sum(depths) / len(depths),
        "seconds_per_node": seconds / max(evaluated, 1),
        "coverage": getattr(solver, "coverage", None),
        "wall_seconds": round(seconds, 3),
        "cpu_seconds": round(time.process_time() - cpu, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--cells", required=True, help="comma-separated cell names")
    _ = parser.add_argument("--dives", type=int, default=10)
    _ = parser.add_argument("--seed", type=int, default=2)
    _ = parser.add_argument("--interval", action="store_true", help="the uncoupled baseline")
    _ = parser.add_argument("--taylor-rows", action="store_true")
    _ = parser.add_argument(
        "--branch-family", action="store_true", help="branch on the separating square"
    )
    _ = parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    pattern = bb.cover_pattern(arguments.cells.split(","))
    result = estimate(
        pattern,
        arguments.dives,
        seed=arguments.seed,
        coupled=not arguments.interval,
        taylor_rows=arguments.taylor_rows,
        branching=arguments.branch_family,
    )
    receipt = {
        "schema": SCHEMA,
        "pattern": list(pattern.names),
        "module_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "pilot_sha256": hashlib.sha256(Path(bb.__file__).read_bytes()).hexdigest(),
        **result,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    _ = arguments.output.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("pattern", "coupled", "estimated_nodes_mean")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
