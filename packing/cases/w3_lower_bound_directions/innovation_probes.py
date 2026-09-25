"""Bounded exact W3 diagnostics; no coverage sweep and no frontier conclusion.

Run with the project Python 3.14 interpreter. Outputs distinguish finite-source
diagnostics from global claims. Tokens are actual distinct site indices.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path


def read_json(path: Path) -> tuple[dict, str]:
    raw = path.read_bytes()
    return json.loads(raw), sha256(raw).hexdigest()


def capacity(features: list[tuple[frozenset[int], int, int]]) -> tuple[int, int]:
    sites = sorted(set().union(*(s for s, _, _ in features)))
    if len(sites) > 8:
        raise ValueError("this bounded diagnostic permits at most eight sites")
    index = {s: i for i, s in enumerate(sites)}
    masks = [(sum(1 << index[s] for s in support), k, w) for support, k, w in features]
    full = (1 << len(sites)) - 1
    values = [
        sum(w for mask, k, w in masks if (mask & part).bit_count() >= k)
        for part in range(full + 1)
    ]
    best = [0] * (full + 1)
    for mask in range(1, full + 1):
        first = mask & -mask
        part = mask
        while part:
            if part & first:
                best[mask] = max(best[mask], values[part] + best[mask ^ part])
            part = (part - 1) & mask
    return best[-1], sum((len(s) // k) * w for s, k, w in features)


def token_groups(source: Path, deadline: float) -> dict:
    # Every maximum over partitions bounds traces of disjoint closed cores.
    five = frozenset(range(5))
    if capacity([(five, 2, 1), (five, 4, 1)]) != (2, 3):
        raise RuntimeError("five-token joint-budget control failed")
    if capacity([(five, 2, 1), (five, 3, 1)]) != (3, 3):
        raise RuntimeError("two-plus-three no-gain control failed")
    if capacity([(frozenset((0, 1, 2)), 2, 1), (frozenset((2, 3, 4)), 2, 3)]) != (4, 4):
        raise RuntimeError("capacity-one no-gain control failed")
    data, digest = read_json(source)
    physical = []
    anchors = []
    for orbit_index, orbit in enumerate(data["charge_orbits"]):
        if orbit["weight"] <= 0:
            continue
        for image_index, sites in enumerate(orbit["sets"]):
            feature = (frozenset(sites), orbit["threshold"], orbit["weight"])
            if len(feature[0]) != len(sites):
                raise ValueError("a feature repeated a site")
            physical.append((orbit_index, image_index, feature))
            if image_index == 0 and len(sites) == 5 and orbit["threshold"] == 2:
                anchors.append(len(physical) - 1)
    rows = []
    seen = set()
    for anchor_index in anchors:
        anchor = physical[anchor_index][2][0]
        candidates = [
            (i, len(anchor & f[0]))
            for i, (_, _, f) in enumerate(physical)
            if i != anchor_index and len(anchor & f[0]) >= 2 and len(anchor | f[0]) <= 8
        ]
        candidates.sort(key=lambda x: (-x[1], x[0]))
        for partner, _ in candidates[:32]:
            universe = anchor | physical[partner][2][0]
            signature = tuple(sorted(universe))
            if signature in seen:
                continue
            seen.add(signature)
            ids = [i for i, (_, _, f) in enumerate(physical) if f[0] <= universe]
            features = [physical[i][2] for i in ids]
            exact, separate = capacity(features)
            rows.append(
                {
                    "sites": signature,
                    "features": [list(physical[i][:2]) for i in ids],
                    "joint_capacity_units": exact,
                    "separate_capacity_units": separate,
                    "saving_units": separate - exact,
                }
            )
            if time.monotonic() >= deadline:
                raise TimeoutError("token-group ceiling reached; no complete summary")
    return {
        "status": "COMPLETE_BOUNDED_DIAGNOSTIC",
        "source_sha256": digest,
        "controls": "PASS",
        "selection": (
            "one representative of each positive 2-of-5 orbit; at most 32 partners "
            "sharing >=2 sites; union <=8; include all positive features contained "
            "in the union"
        ),
        "anchors": len(anchors),
        "groups": len(rows),
        "groups_with_strict_saving": sum(r["saving_units"] > 0 for r in rows),
        "max_saving_units": max((r["saving_units"] for r in rows), default=0),
        "scope": (
            "arbitrary token partitions; no geometry, no complete support-family "
            "enumeration, no stronger packing bound"
        ),
        "rows": rows,
    }


def d4(x: Fraction, y: Fraction, side: Fraction) -> set[tuple[Fraction, Fraction]]:
    return {(a, b) for u, v in ((x, y), (y, x)) for a in (u, side - u) for b in (v, side - v)}


def cplus(u: Fraction) -> Fraction:
    return (1 + 2 * u - u * u) / (1 + u * u)


def weak_pose_graph(
    source: Path, cells_path: Path, deadline: float, target_side: Fraction | None = None
) -> dict:
    data, digest = read_json(source)
    raw = cells_path.read_bytes()
    cells = [json.loads(line) for line in raw.splitlines()]
    if len(cells) != len(data["entries"]) or sorted(c["row"] for c in cells) != list(
        range(len(cells))
    ):
        raise ValueError("row coverage mismatch in retained witness file")
    selected = [r for r in cells if r["minimum_units"] <= data["minimum_units"] + 100_000]
    side, parent = Fraction(data["L"]), Fraction(data["A"])
    points: dict[tuple[Fraction, Fraction], list[int]] = {}
    for row in selected:
        a, b, _, _ = map(Fraction, data["entries"][row["row"]])
        inset = parent * min(cplus(a), cplus(b)) / 2
        x, y = Fraction(row["centre_x"]), Fraction(row["centre_y"])
        if not (inset <= x <= side - inset and inset <= y <= side - inset):
            raise ValueError("witness outside the actual endpoint parent domain")
        for p in d4(x, y, side):
            points.setdefault(p, []).append(row["row"])
    vertices = sorted(points)
    size = len(vertices)
    edges = [set() for _ in vertices]
    for i, j in combinations(range(size), 2):
        dx = vertices[i][0] - vertices[j][0]
        dy = vertices[i][1] - vertices[j][1]
        if dx * dx + dy * dy < parent * parent:
            edges[i].add(j)
            edges[j].add(i)
        if time.monotonic() >= deadline:
            raise TimeoutError("finite-graph ceiling reached; no complete summary")
    remaining = set(range(size))
    cliques = []
    while remaining:
        pivot = max(remaining, key=lambda i: (len(edges[i] & remaining), -i))
        clique = [pivot]
        possible = remaining & edges[pivot]
        while possible:
            nxt = max(possible, key=lambda i: (len(edges[i] & possible), -i))
            clique.append(nxt)
            possible &= edges[nxt]
        if any(j not in edges[i] for i, j in combinations(clique, 2)):
            raise RuntimeError("clique verification failed")
        remaining -= set(clique)
        cliques.append(clique)
    if sorted(v for clique in cliques for v in clique) != list(range(size)):
        raise RuntimeError("clique cover not a partition")
    largest_squared = max(
        (
            (vertices[i][0] - vertices[j][0]) ** 2 + (vertices[i][1] - vertices[j][1]) ** 2
            for clique in cliques
            for i, j in combinations(clique, 2)
        ),
        default=Fraction(0),
    )
    margins = []
    for label, test_parent in [("source", parent)] + (
        [("proposed-target", side / target_side)] if target_side is not None else []
    ):
        squared_slack = test_parent * test_parent - largest_squared
        # For d <= A, A-d = (A^2-d^2)/(A+d) >= squared_slack/(2A).
        # Expanding each endpoint by eps <= squared_slack/(8A) is safely smaller
        # than half this available radial slack; no square-root rounding is used.
        radius = max(Fraction(0), squared_slack / (8 * test_parent))
        grid = 10**12
        radius_grid = Fraction((radius * grid).numerator // (radius * grid).denominator, grid)
        slack_grid = Fraction(
            (squared_slack * grid).numerator // (squared_slack * grid).denominator, grid
        )
        margins.append(
            {
                "label": label,
                "parent_side": str(test_parent),
                "minimum_squared_slack": str(squared_slack),
                "minimum_squared_slack_float": float(squared_slack),
                "squared_slack_lower_grid": str(slack_grid),
                "euclidean_radius": str(radius_grid),
                "euclidean_radius_float": float(radius_grid),
                "clique_neighbourhoods_valid": squared_slack > 0 and radius_grid > 0,
            }
        )
    return {
        "status": "COMPLETE_FINITE_WITNESS_DIAGNOSTIC",
        "source_sha256": digest,
        "witness_sha256": sha256(raw).hexdigest(),
        "parent_side": str(parent),
        "charge_window_units": 100_000,
        "selected_rows": [r["row"] for r in selected],
        "distinct_centres_with_D4": size,
        "disc_conflict_edges": sum(map(len, edges)) // 2,
        "greedy_clique_cover_bound": len(cliques),
        "clique_sizes": list(map(len, cliques)),
        "neighbourhoods": margins,
        "cliques": cliques,
        "vertices": [
            {"x": str(x), "y": str(y), "source_rows": points[x, y]} for x, y in vertices
        ],
        "scope": (
            "finite stored argmin centres only; no continuum bad-pose coverage, no "
            "certificate at a new side, no bound on all low-charge poses"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("token-groups", "weak-pose-graph"))
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cells", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--target-side", type=Fraction)
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 14):
        raise SystemExit("use the project Python 3.14 interpreter")
    if args.output.exists():
        raise SystemExit("refusing to overwrite a diagnostic receipt")
    start = time.monotonic()
    if args.mode == "token-groups":
        result = token_groups(args.source, start + args.seconds)
    else:
        if args.cells is None:
            raise SystemExit("--cells is required")
        result = weak_pose_graph(
            args.source, args.cells, start + args.seconds, args.target_side
        )
    result["seconds"] = time.monotonic() - start
    result["python"] = sys.version
    result["command"] = sys.argv
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    summary = {
        k: v
        for k, v in result.items()
        if k not in {"rows", "vertices", "cliques", "command", "neighbourhoods"}
    }
    if "neighbourhoods" in result:
        summary["neighbourhoods"] = [
            {k: v for k, v in m.items() if k != "minimum_squared_slack"}
            for m in result["neighbourhoods"]
        ]
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
