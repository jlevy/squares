"""Does narrowing the centre boxes before the search shrink the tree? (lane P2, a measurement)

`diagnose_n17_bb_losses` found most pair terms at open nodes with every normal of a square
live, so that their rows vanish, and conjectured that narrower centre boxes would leave
fewer normals live. This tool pre-splits the root's centre boxes and estimates the whole
tree by Knuth's method.

Pre-splits. A sub-root is the root with smaller centre boxes. The sub-roots' boxes cover
every cell's box, so searching each sub-root is sound and their trees together decide the
pattern. Forms:

* `meet`: every cell box that contains the point where the axis cells meet, (U/2, U/2),
  is split through it, in each axis it lies strictly inside;
* `bisect-1`: every centre box is bisected once, across its longer side;
* `bisect-2`: every centre box is bisected in both axes.

The estimate, stratified. A part of a centre box that misses its cell (exact clipping)
closes every sub-root using it at contraction, so of the `M` sub-roots only the `L` built
from parts that meet their cells are live; the others are one closed node each. A dive
picks a live sub-root uniformly and runs the pilot's dive, and the tree's size is
estimated by `(M - 1) + (M - L) + L * (1 + b_0 + b_0 b_1 + ...)`, the pre-split's own
nodes counted as a binary tree over the `M` leaves.

With `--enumerate`, every live sub-root is assessed first, so the count `O` of sub-roots
that stay open is exact rather than sampled, and the dives start from uniformly chosen
open sub-roots: `(M - 1) + (M - O) + O * (1 + b_0 + b_0 b_1 + ...)`. When most sub-roots
close at once, ten plain dives can all miss the open ones; this stratification cannot.

Live normals. At each open node on a dive, every pair term's live normals are counted
(as `diagnose_n17_bb_losses` does): whether some square has all four turns live, and
whether all eight normals are.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from collections import Counter
from pathlib import Path
from typing import Any

from devtools import pilot_n17_subpattern_bb as bb

SCHEMA = "n17-bb-presplit-estimate/v1"
FORMS = ("none", "meet", "bisect-1", "bisect-2")


def split_box(box: bb.Box, form: str, meet: float) -> list[bb.Box]:
    """A cover of one centre box by the form's parts."""
    xl, xh, yl, yh = box
    if form == "none":
        return [box]
    if form == "meet":
        xs = [(xl, meet), (meet, xh)] if xl < meet < xh else [(xl, xh)]
        ys = [(yl, meet), (meet, yh)] if yl < meet < yh else [(yl, yh)]
    elif form == "bisect-1":
        if xh - xl >= yh - yl:
            mid = 0.5 * (xl + xh)
            xs, ys = [(xl, mid), (mid, xh)], [(yl, yh)]
        else:
            mid = 0.5 * (yl + yh)
            xs, ys = [(xl, xh)], [(yl, mid), (mid, yh)]
    elif form == "bisect-2":
        mx, my = 0.5 * (xl + xh), 0.5 * (yl + yh)
        xs, ys = [(xl, mx), (mx, xh)], [(yl, my), (my, yh)]
    else:
        raise ValueError(form)
    return [(x[0], x[1], y[0], y[1]) for x in xs for y in ys]


def sub_root_parts(solver: bb.Solver, form: str) -> tuple[int, list[list[bb.Box]]]:
    """All sub-roots' count, and each square's parts that meet its cell."""
    meet = float(solver.pattern.cap) / 2
    every = [split_box(box, form, meet) for box in solver.cell_boxes]
    live = [
        [part for part in parts if bb.clip_to_box(polygon, part) is not None]
        for parts, polygon in zip(every, solver.pattern.polygons, strict=True)
    ]
    return math.prod(len(parts) for parts in every), live


def live_normals(
    node: bb.Node, boxes: tuple[bb.Box, ...], pair: tuple[int, int], index: int
) -> list[int]:
    """How many of each square's four turns can separate the pair at this node."""
    i, j = pair
    dx, dy = bb.difference_box(boxes[i], boxes[j])
    squared = bb.squared_range(dx, dy)
    g_lo = bb.gap_lower(node.angles[i], node.angles[j])
    d_max = bb.up(math.sqrt(squared[1]))
    counts: list[int] = []
    for square in (i, j):
        theta = node.angles[square]
        live = 0
        for k in range(4):
            shift = bb.HALF_PI_MULTIPLES[k]
            base = (bb.dn(theta[0] + shift[0]), bb.up(theta[1] + shift[1]))
            if any(
                bb.option_planes(*part, dx, dy, d_max=d_max, g_lo=g_lo)
                for part in bb.in_window(base, node.windows[index])
            ):
                live += 1
        counts.append(live)
    return counts


def estimate(
    pattern: bb.Pattern, form: str, dives: int, *, seed: int, enumerate_roots: bool = False
) -> dict[str, Any]:
    rng = random.Random(seed)
    solver = bb.Solver(pattern, bb.Settings())
    sub_roots, parts = sub_root_parts(solver, form)
    live_roots = math.prod(len(p) for p in parts)
    root = solver.root()
    started, cpu = time.perf_counter(), time.process_time()
    closed_reasons: Counter[str] = Counter()
    open_roots: list[tuple[bb.Box, ...]] | None = None
    if enumerate_roots:
        open_roots = []
        for boxes in itertools.product(*parts):
            pruned = solver.assess(bb.Node(root.angles, boxes, root.windows, 0)).pruned
            if pruned is None:
                open_roots.append(boxes)
            else:
                closed_reasons[pruned] += 1
    enumeration_cpu = time.process_time() - cpu
    sizes: list[float] = []
    depths: list[int] = []
    terms = some_square_all = all_eight = open_nodes = closed_at_sub_root = evaluated = 0
    for _ in range(dives if open_roots is None or open_roots else 0):
        if open_roots is None:
            boxes = tuple(rng.choice(choices) for choices in parts)
        else:
            boxes = open_roots[rng.randrange(len(open_roots))]
        node = bb.Node(root.angles, boxes, root.windows, 0)
        weight, size = 1.0, 1.0
        first = True
        while True:
            evaluated += 1
            evaluation = solver.assess(node)
            if evaluation.pruned is not None:
                closed_at_sub_root += int(first)
                break
            first = False
            open_nodes += 1
            for index, _ in evaluation.terms:
                counts = live_normals(node, evaluation.boxes, pattern.pairs[index], index)
                terms += 1
                some_square_all += int(max(counts) == 4)
                all_eight += int(min(counts) == 4)
            outcome = solver.children(node, evaluation) if node.depth < bb.MAX_DEPTH else None
            if outcome is None:
                break
            kids = outcome[1]
            weight *= len(kids)
            size += weight
            node = kids[rng.randrange(len(kids))]
        if open_roots is None:
            sizes.append((sub_roots - 1) + (sub_roots - live_roots) + live_roots * size)
        else:
            stays = len(open_roots)
            sizes.append((sub_roots - 1) + (sub_roots - stays) + stays * size)
        depths.append(node.depth)
    if not sizes:
        sizes.append(2.0 * sub_roots - 1)
        depths.append(0)
    ordered = sorted(sizes)
    seconds = time.perf_counter() - started
    return {
        "form": form,
        "sub_roots": sub_roots,
        "live_sub_roots": live_roots,
        "dives": dives,
        "seed": seed,
        "enumerated": enumerate_roots,
        "open_sub_roots": None if open_roots is None else len(open_roots),
        "sub_roots_closed_by": dict(sorted(closed_reasons.items())),
        "enumeration_cpu_seconds": round(enumeration_cpu, 3),
        "estimated_nodes_mean": sum(sizes) / len(sizes),
        "estimated_nodes_median": ordered[len(ordered) // 2],
        "estimated_nodes_max": ordered[-1],
        "dives_closed_at_sub_root": closed_at_sub_root,
        "mean_leaf_depth_below_sub_root": sum(depths) / len(depths),
        "open_nodes": open_nodes,
        "pair_terms": terms,
        "share_some_square_all_turns_live": some_square_all / terms if terms else None,
        "share_all_eight_normals_live": all_eight / terms if terms else None,
        "seconds_per_node": seconds / max(evaluated, 1),
        "wall_seconds": round(seconds, 3),
        "cpu_seconds": round(time.process_time() - cpu, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--cells", required=True, help="comma-separated cell names")
    _ = parser.add_argument("--forms", default=",".join(FORMS))
    _ = parser.add_argument("--dives", type=int, default=10)
    _ = parser.add_argument("--seed", type=int, default=2)
    _ = parser.add_argument(
        "--enumerate", action="store_true", help="assess every sub-root before the dives"
    )
    _ = parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    pattern = bb.cover_pattern(arguments.cells.split(","))
    results = [
        estimate(
            pattern,
            form,
            arguments.dives,
            seed=arguments.seed,
            enumerate_roots=arguments.enumerate,
        )
        for form in arguments.forms.split(",")
    ]
    receipt = {
        "schema": SCHEMA,
        "pattern": list(pattern.names),
        "module_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "pilot_sha256": hashlib.sha256(Path(bb.__file__).read_bytes()).hexdigest(),
        "results": results,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    _ = arguments.output.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    for result in results:
        print(
            json.dumps(
                {
                    k: result[k]
                    for k in (
                        "form",
                        "sub_roots",
                        "open_sub_roots",
                        "estimated_nodes_mean",
                        "estimated_nodes_median",
                        "share_all_eight_normals_live",
                    )
                }
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
