"""Which loss holds a branch-and-bound node open (lane P2): a diagnostic, not a certifier.

The branch and bound (`pilot_n17_subpattern_bb`) relaxes each angle box in three ways
that this tool separates on a sample of open nodes:

* **Decoupled normals.** Each pair's planes take a square's normal anywhere in the box,
  independently of the square's other pairs, so the LP may separate one pair with the
  square at one end of its interval and another pair with it at the other end.
* **The hull gap.** A pair with several possible planes enters the LP through the convex
  hull of their union, so the LP point may satisfy none of them.
* **Genuine width.** The box holds angle settings at which the same machinery cannot
  refute the node at all; no relaxation of the box could close it, and it must be split.

The sample. Nodes come from Knuth dives (`estimate`'s random root-to-leaf paths), so
every depth is represented; each open node on a dive is diagnosed.

The point checks. The node is re-assessed with every square's angle fixed at one point,
the box centre and `points` random points of the box, keeping its windows and its
tightened boxes. That is the crude "force the normals to agree" check: at a point every
pair sees the same angle for a square. A point that closes is refuted there by the same
sound machinery; one that stays open is not. A node whose every point closes is
*closable*: a relaxation that coupled the angles perfectly would close it at this width.

The LP point's evidence, at the box LP's centres: for each pair, the possible planes the
centre difference satisfies. A pair satisfying none sits in its hull gap. Otherwise each
satisfied plane's normal angle, taken back to its square, gives a position in that
square's angle interval (0 at the low end, 1 at the high end); a pair whose satisfied
planes all belong to one square needs that square in the span of their positions. A
square whose pairs need spans that miss each other by more than `SPREAD` of its width is
decoupled at the LP point.

Loss switches. Each open box is also re-assessed with one loss of its pair planes
removed, by diagnostic variants that are *not* sound relaxations: `gap` uses the gap at
the box centre's angles for every pair instead of its least value over the box; `chord`
drops the chord plane's factor `cos x`; `both` does both. A closable box that closes under
a switch is held open by that loss. One that closes under none, while every angle point
closes, is held open by what remains: the planes' normals ranging over the box, pair by
pair (decoupling, and the hull of the wider normal sets).

Read this as planning evidence about where the relaxation loses, not as a proof of
anything; every closure the branch and bound itself makes stays exactly as sound, and the
switches are confined to the diagnostic's own solvers.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import math
import random
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devtools import pilot_n17_subpattern_bb as bb

SCHEMA = "n17-bb-loss-diagnosis/v1"
SPREAD = 0.25
SATISFIED = 1e-9


@dataclass(frozen=True)
class PlaneSeen:
    """A possible plane of a pair: its square, its position in that square's interval."""

    square: int
    position: float
    satisfied: bool


def pair_planes(
    node: bb.Node,
    boxes: tuple[bb.Box, ...],
    pair: tuple[int, int],
    index: int,
    point: list[float],
) -> list[PlaneSeen]:
    """Every possible plane of one pair at the LP point, labelled by square and position.

    A base piece (square `f`, turn `k`) covers the normals `theta_f + k pi/2`; its parts in
    the window are the pieces the solver uses, with the same planes (`option_planes`).
    """
    i, j = pair
    dx, dy = bb.difference_box(boxes[i], boxes[j])
    squared = bb.squared_range(dx, dy)
    g_lo = bb.gap_lower(node.angles[i], node.angles[j])
    d_max = bb.up(math.sqrt(squared[1]))
    d = (point[2 * j] - point[2 * i], point[2 * j + 1] - point[2 * i + 1])
    window = node.windows[index]
    seen: list[PlaneSeen] = []
    for square in (i, j):
        theta = node.angles[square]
        width = theta[1] - theta[0]
        for k in range(4):
            shift = bb.HALF_PI_MULTIPLES[k]
            base = (bb.dn(theta[0] + shift[0]), bb.up(theta[1] + shift[1]))
            for turns in (-1, 0, 1):
                offset = turns * 2 * math.pi
                lo, hi = base[0] + offset, base[1] + offset
                if window is not None:
                    lo, hi = max(lo, window[0]), min(hi, window[1])
                if lo > hi:
                    continue
                for angle, plane in angled_planes(lo, hi, dx, dy, d_max=d_max, g_lo=g_lo):
                    nx, ny, r = plane
                    position = (angle - offset - base[0]) / width if width > 0 else 0.5
                    seen.append(
                        PlaneSeen(
                            square,
                            min(1.0, max(0.0, position)),
                            nx * d[0] + ny * d[1] >= r - SATISFIED,
                        )
                    )
    return seen


def angled_planes(
    lo: float, hi: float, dx: bb.Iv, dy: bb.Iv, *, d_max: float, g_lo: float
) -> list[tuple[float, bb.Halfplane]]:
    """`option_planes` with each plane's normal angle (lo, hi or m; m for a wide piece)."""
    pieces = bb.chord_pieces(lo, hi, g_lo)
    found: list[tuple[float, bb.Option]] = []
    if pieces:
        found = [
            (angle, bb.piece_option(lo, hi, angle, rhs, dx=dx, dy=dy))
            for angle, rhs in pieces
            if bb.piece_possible(angle, rhs, dx, dy)
        ]
    else:
        m = 0.5 * (lo + hi)
        found = [(m, bb.relax(lo, hi, dx, dy, d_max=d_max, g_lo=g_lo))]
    return [
        (angle, (option.nx, option.ny, option.bound))
        for angle, option in found
        if bb.option_possible(option, dx, dy)
    ]


def lp_evidence(solver: bb.Solver, node: bb.Node, evaluation: bb.Evaluation) -> dict[str, Any]:
    """Hull-gap pairs and the worst decoupling spread at the box LP's point."""
    point = evaluation.point
    if point is None:
        return {"hull_gap_pairs": 0, "spread": 0.0, "decoupled_squares": 0}
    needs: dict[int, list[tuple[float, float]]] = {}
    gaps = 0
    for index, _ in evaluation.terms:
        pair = solver.pattern.pairs[index]
        seen = pair_planes(node, evaluation.boxes, pair, index, point)
        satisfied = [plane for plane in seen if plane.satisfied]
        if not satisfied:
            gaps += 1
            continue
        squares = {plane.square for plane in satisfied}
        if len(squares) == 1:
            square = squares.pop()
            positions = [plane.position for plane in satisfied]
            needs.setdefault(square, []).append((min(positions), max(positions)))
    spreads = {
        square: max(lo for lo, _ in spans) - min(hi for _, hi in spans)
        for square, spans in needs.items()
    }
    return {
        "hull_gap_pairs": gaps,
        "spread": max(spreads.values(), default=0.0),
        "decoupled_squares": sum(spread > SPREAD for spread in spreads.values()),
    }


def point_checks(
    solver: bb.Solver,
    node: bb.Node,
    evaluation: bb.Evaluation,
    rng: random.Random,
    points: int,
) -> tuple[int, bool]:
    """How many of the centre and `points` random angle points stay open; the centre's fate."""
    settings: list[tuple[float, ...]] = [tuple(0.5 * (lo + hi) for lo, hi in node.angles)]
    settings.extend(tuple(rng.uniform(lo, hi) for lo, hi in node.angles) for _ in range(points))
    still_open = 0
    centre_closes = False
    for number, angles in enumerate(settings):
        fixed = bb.Node(
            tuple((a, a) for a in angles), evaluation.boxes, node.windows, node.depth
        )
        closed = solver.assess(fixed).pruned is not None
        if number == 0:
            centre_closes = closed
        still_open += int(not closed)
    return still_open, centre_closes


SWITCHES = ("gap", "chord", "both")


def piece_structure(
    node: bb.Node, boxes: tuple[bb.Box, ...], pair: tuple[int, int], index: int
) -> tuple[str, int]:
    """Which normals can separate a pair: one square at one turn, both squares, or turns.

    `one` is what a single coupled normal can serve; `both-squares` needs a disjunction
    between the two squares' columns, `turns` one between turns of one square. The
    second value is the most live turns of either square (4: every normal is live).
    """
    i, j = pair
    dx, dy = bb.difference_box(boxes[i], boxes[j])
    squared = bb.squared_range(dx, dy)
    g_lo = bb.gap_lower(node.angles[i], node.angles[j])
    d_max = bb.up(math.sqrt(squared[1]))
    live: set[tuple[int, int]] = set()
    for square in (i, j):
        theta = node.angles[square]
        for k in range(4):
            shift = bb.HALF_PI_MULTIPLES[k]
            base = (bb.dn(theta[0] + shift[0]), bb.up(theta[1] + shift[1]))
            if any(
                bb.option_planes(*part, dx, dy, d_max=d_max, g_lo=g_lo)
                for part in bb.in_window(base, node.windows[index])
            ):
                live.add((square, k))
    squares = {square for square, _ in live}
    most = max((sum(1 for sq, _ in live if sq == square) for square in squares), default=0)
    if len(live) <= 1:
        return "one", most
    if len(squares) == 2:
        return "both-squares", most
    return "turns", most


@contextlib.contextmanager
def switched(name: str) -> Iterator[None]:
    """Remove a loss from the pilot's pair planes for the duration (diagnostic only)."""
    saved_gap, saved_chord = bb.gap_lower, bb.chord_pieces

    def centre_gap(ti: bb.Iv, tj: bb.Iv) -> float:
        alpha = 0.5 * (tj[0] + tj[1]) - 0.5 * (ti[0] + ti[1])
        return 0.5 + (abs(math.cos(alpha)) + abs(math.sin(alpha))) / 2

    def no_chord_loss(lo: float, hi: float, g_lo: float) -> list[tuple[float, float]]:
        return [(angle, g_lo) for angle, _ in saved_chord(lo, hi, g_lo)]

    if name in ("gap", "both"):
        bb.gap_lower = centre_gap
    if name in ("chord", "both"):
        bb.chord_pieces = no_chord_loss
    try:
        yield
    finally:
        bb.gap_lower, bb.chord_pieces = saved_gap, saved_chord


def switch_checks(
    solvers: dict[str, bb.Solver], node: bb.Node, evaluation: bb.Evaluation
) -> dict[str, bool]:
    """Whether the box closes with each loss switched off (its windows, tightened boxes)."""
    box = bb.Node(node.angles, evaluation.boxes, node.windows, node.depth)
    closes: dict[str, bool] = {}
    for name in SWITCHES:
        with switched(name):
            closes[name] = solvers[name].assess(box).pruned is not None
    return closes


def classify(open_points: int, closes: dict[str, bool]) -> str:
    """The loss holding a box open: width, a switchable loss, or the normals' range."""
    if open_points:
        return "open-points"
    if closes["gap"] and closes["chord"]:
        return "closable-gap-or-chord"
    if closes["gap"]:
        return "closable-gap"
    if closes["chord"]:
        return "closable-chord"
    if closes["both"]:
        return "closable-gap-and-chord"
    return "closable-normals"


def diagnose(
    pattern: bb.Pattern, settings: bb.Settings, dives: int, *, seed: int, points: int
) -> dict[str, Any]:
    """Diagnose every open node on `dives` random root-to-leaf paths."""
    rng = random.Random(seed)
    solver = bb.Solver(pattern, settings)
    solvers = {name: bb.Solver(pattern, settings) for name in SWITCHES}
    wall, cpu = time.perf_counter(), time.process_time()
    classes: dict[str, int] = {}
    by_depth: dict[str, dict[str, int]] = {}
    centre_closes = spreads_over = gap_nodes = nodes = 0
    structure: dict[str, int] = {}
    turns: dict[str, int] = {}
    slacks: list[float] = []
    without_cuts = terms = 0
    spreads: list[float] = []
    for _ in range(dives):
        node = solver.root()
        while True:
            evaluation = solver.assess(node)
            if evaluation.pruned is not None:
                break
            nodes += 1
            evidence = lp_evidence(solver, node, evaluation)
            open_points, centre = point_checks(solver, node, evaluation, rng, points)
            kind = classify(open_points, switch_checks(solvers, node, evaluation))
            point = evaluation.point
            for index, term in evaluation.terms:
                pair = solver.pattern.pairs[index]
                shape, most = piece_structure(node, evaluation.boxes, pair, index)
                structure[shape] = structure.get(shape, 0) + 1
                turns[str(most)] = turns.get(str(most), 0) + 1
                terms += 1
                if not term.cuts or point is None:
                    without_cuts += 1
                    continue
                i, j = pair
                dx, dy = point[2 * j] - point[2 * i], point[2 * j + 1] - point[2 * i + 1]
                slacks.append(min(ux * dx + uy * dy - v for ux, uy, v in term.cuts))
            classes[kind] = classes.get(kind, 0) + 1
            bucket = by_depth.setdefault(str(10 * (node.depth // 10)), {})
            bucket[kind] = bucket.get(kind, 0) + 1
            centre_closes += int(centre)
            spreads.append(evidence["spread"])
            spreads_over += int(evidence["decoupled_squares"] > 0)
            gap_nodes += int(evidence["hull_gap_pairs"] > 0)
            # `children` reads only the node and its own evaluation, which the point
            # checks (fresh evaluations of other nodes) leave unchanged.
            outcome = solver.children(node, evaluation) if node.depth < bb.MAX_DEPTH else None
            if outcome is None:
                break
            kids = outcome[1]
            node = kids[rng.randrange(len(kids))]
    ordered = sorted(spreads)
    closable = sum(v for k, v in classes.items() if k.startswith("closable"))
    return {
        "dives": dives,
        "seed": seed,
        "points": points,
        "open_nodes": nodes,
        "classes": dict(sorted(classes.items())),
        "closable_share": closable / nodes if nodes else None,
        "normals_share_of_closable": (
            classes.get("closable-normals", 0) / closable if closable else None
        ),
        "centre_closes": centre_closes,
        "pair_piece_structure": dict(sorted(structure.items())),
        "pair_terms": {
            "count": terms,
            "most_live_turns_per_square": dict(sorted(turns.items())),
            "without_cuts": without_cuts,
            "cut_slack_at_lp_point": quantiles(slacks),
        },
        "lp_point": {
            "nodes_with_a_hull_gap_pair": gap_nodes,
            "nodes_with_a_decoupled_square": spreads_over,
            "spread_median": ordered[len(ordered) // 2] if ordered else None,
            "spread_p90": ordered[int(0.9 * (len(ordered) - 1))] if ordered else None,
        },
        "by_depth": dict(sorted(by_depth.items(), key=lambda item: int(item[0]))),
        "wall_seconds": round(time.perf_counter() - wall, 3),
        "cpu_seconds": round(time.process_time() - cpu, 3),
    }


def quantiles(values: list[float]) -> dict[str, float] | None:
    if not values:
        return None
    ordered = sorted(values)
    return {
        f"q{int(100 * q)}": ordered[int(q * (len(ordered) - 1))] for q in (0.0, 0.1, 0.5, 0.9)
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--cells", required=True, help="comma-separated cell names")
    _ = parser.add_argument("--dives", type=int, default=20)
    _ = parser.add_argument("--points", type=int, default=4)
    _ = parser.add_argument("--seed", type=int, default=1)
    _ = parser.add_argument("--taylor", action="store_true")
    _ = parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    pattern = bb.cover_pattern(arguments.cells.split(","))
    settings = bb.Settings(taylor=arguments.taylor)
    result = diagnose(
        pattern, settings, arguments.dives, seed=arguments.seed, points=arguments.points
    )
    receipt = {
        "schema": SCHEMA,
        "pattern": list(pattern.names),
        "settings": {"taylor": settings.taylor, "spread": SPREAD},
        "module_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "pilot_sha256": hashlib.sha256(Path(bb.__file__).read_bytes()).hexdigest(),
        **result,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    _ = arguments.output.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("pattern", "open_nodes", "classes")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
