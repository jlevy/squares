"""Measure how far the n = 204 certificate (T-231) lies from other packings of 204 squares.

Whether two certificates are the same packing is not decided here. For each reference
the program applies the box's eight symmetries to the reference in its own box and
measures, under each: whether nearest centres pair the squares one to one; under the
assignment that minimizes the total squared centre displacement (its own Hungarian
algorithm), how many squares move beyond each threshold, decided exactly over the
rationals, and how far squares turn modulo 90 degrees; and the bottleneck, the least
largest displacement over all one-to-one pairings (bisection over its own Hopcroft-Karp
matching). Assignments and turns are computed in binary64; every displacement count is
then decided exactly with ``Fraction`` on the assigned pairs.

It also measures the certificate against itself undilated: if the certificate is a
solved packing scaled by ``1 + 1e-20`` about the origin, dividing every centre by that
factor brings each contact to within the rounding of the literals.

Input formats: Evan Daniel's text format (``n S`` then ``x y t`` rows, ``#`` comments,
optionally gzip-compressed). Standard library only; nothing from the repository.

Usage (``python3 -I``)::

    identity_t231.py --test CERT --ref NAME=CERT [--ref NAME=CERT ...] --out OUT.json
    identity_t231.py --self-test
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import random
import sys
import time
from collections import deque
from fractions import Fraction
from pathlib import Path
from typing import Any

PROGRAM = Path(__file__).resolve()
THRESHOLDS = ("1e-20", "1e-15", "1e-12", "1e-9", "1e-6", "1e-3", "1e-2", "1e-1", "5e-1")
SYMMETRIES = (
    ("identity", True),
    ("quarter turn", True),
    ("half turn", True),
    ("three-quarter turn", True),
    ("mirror x", False),
    ("mirror y", False),
    ("transpose", False),
    ("anti-transpose", False),
)


class Packing:
    def __init__(self, side: Fraction, rows: list[tuple[Fraction, Fraction, Fraction]]) -> None:
        self.side = side
        self.rows = rows
        self.n = len(rows)
        self.angles = [angle_mod_90(t) for _, _, t in rows]

    def centre(self, k: int) -> tuple[Fraction, Fraction]:
        return self.rows[k][0], self.rows[k][1]


def read_text_certificate(path: Path) -> Packing:
    data = path.read_bytes()
    if path.suffix == ".gz":
        data = gzip.decompress(data)
    lines = [line for line in data.decode("ascii").splitlines() if line.strip() and not line.startswith("#")]
    head = lines[0].split()
    n, side = int(head[0]), Fraction(head[1])
    rows = []
    for line in lines[1 : 1 + n]:
        x, y, t = (Fraction(value) for value in line.split())
        rows.append((x, y, t))
    if len(rows) != n or len(lines) != n + 1:
        msg = f"{path}: {len(rows)} rows for n = {n}"
        raise ValueError(msg)
    return Packing(side, rows)


def angle_mod_90(t: Fraction) -> float:
    """theta = 2 atan(t) in degrees, reduced to (-45, 45]."""
    theta = math.degrees(2 * math.atan2(t.numerator, t.denominator))
    reduced = math.fmod(theta, 90.0)
    if reduced <= -45:
        reduced += 90
    elif reduced > 45:
        reduced -= 90
    return reduced


def turn(first: float, second: float) -> float:
    difference = math.fmod(first - second, 90.0)
    if difference <= -45:
        difference += 90
    elif difference > 45:
        difference -= 90
    return difference


def transform(
    symmetry: str, side: Fraction, x: Fraction, y: Fraction
) -> tuple[Fraction, Fraction]:
    return {
        "identity": (x, y),
        "quarter turn": (side - y, x),
        "half turn": (side - x, side - y),
        "three-quarter turn": (y, side - x),
        "mirror x": (side - x, y),
        "mirror y": (x, side - y),
        "transpose": (y, x),
        "anti-transpose": (side - y, side - x),
    }[symmetry]


def hungarian(cost: list[list[float]]) -> list[int]:
    """Minimum-cost perfect assignment; returns, for each row, its column."""
    n = len(cost)
    inf = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [inf] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = inf
            j1 = 0
            row = cost[i0 - 1]
            ui0 = u[i0]
            for j in range(1, n + 1):
                if not used[j]:
                    current = row[j - 1] - ui0 - v[j]
                    if current < minv[j]:
                        minv[j] = current
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    assignment = [0] * n
    for j in range(1, n + 1):
        assignment[p[j] - 1] = j - 1
    return assignment


def has_perfect_matching(adjacency: list[list[int]], n: int) -> bool:
    """Hopcroft-Karp on a bipartite graph with n vertices on each side."""
    match_left = [-1] * n
    match_right = [-1] * n
    dist = [0] * n

    def bfs() -> bool:
        queue: deque[int] = deque()
        found = False
        for left in range(n):
            if match_left[left] == -1:
                dist[left] = 0
                queue.append(left)
            else:
                dist[left] = -1
        while queue:
            left = queue.popleft()
            for right in adjacency[left]:
                partner = match_right[right]
                if partner == -1:
                    found = True
                elif dist[partner] == -1:
                    dist[partner] = dist[left] + 1
                    queue.append(partner)
        return found

    def dfs(left: int) -> bool:
        for right in adjacency[left]:
            partner = match_right[right]
            if partner == -1 or (dist[partner] == dist[left] + 1 and dfs(partner)):
                match_left[left] = right
                match_right[right] = left
                return True
        dist[left] = -1
        return False

    matched = 0
    while bfs():
        for left in range(n):
            if match_left[left] == -1 and dfs(left):
                matched += 1
    return matched == n


def bottleneck(distance: list[list[float]]) -> float:
    n = len(distance)
    values = sorted({value for row in distance for value in row})
    low, high = 0, len(values) - 1
    while low < high:
        middle = (low + high) // 2
        limit = values[middle]
        adjacency = [[j for j in range(n) if distance[i][j] <= limit] for i in range(n)]
        if has_perfect_matching(adjacency, n):
            high = middle
        else:
            low = middle + 1
    return values[low]


def measure(test: Packing, reference: Packing, symmetry: str, proper: bool) -> dict[str, Any]:
    n = test.n
    ref_centres = [
        transform(symmetry, reference.side, *reference.centre(k)) for k in range(reference.n)
    ]
    ref_float = [(float(x), float(y)) for x, y in ref_centres]
    test_float = [(float(x), float(y)) for x, y in (test.centre(k) for k in range(n))]
    squared = [
        [(tx - rx) ** 2 + (ty - ry) ** 2 for rx, ry in ref_float] for tx, ty in test_float
    ]
    nearest = [min(range(n), key=row.__getitem__) for row in squared]
    one_to_one = len(set(nearest)) == n
    assignment = hungarian(squared)
    ref_angles = [angle if proper else -angle for angle in reference.angles]
    exact_squared = []
    for i, j in enumerate(assignment):
        dx = test.rows[i][0] - ref_centres[j][0]
        dy = test.rows[i][1] - ref_centres[j][1]
        exact_squared.append(dx * dx + dy * dy)
    within = {}
    for label in THRESHOLDS:
        limit = Fraction(label)
        within[label] = sum(1 for value in exact_squared if value <= limit * limit)
    moves = [math.sqrt(float(value)) for value in exact_squared]
    turns = [turn(test.angles[i], ref_angles[j]) for i, j in enumerate(assignment)]
    reversed_tilts = sum(
        1
        for i, j in enumerate(assignment)
        if abs(ref_angles[j]) > 1
        and abs(test.angles[i]) > 1
        and (ref_angles[j] > 0) != (test.angles[i] > 0)
        and abs(abs(ref_angles[j]) - abs(test.angles[i])) < 1
    )
    total = sum(squared[i][j] for i, j in enumerate(assignment))
    return {
        "symmetry": symmetry,
        "nearest_one_to_one": one_to_one,
        "assignment_total_squared": total,
        "rms": math.sqrt(total / n),
        "largest_move": max(moves),
        "largest_move_square": max(range(n), key=moves.__getitem__),
        "within": within,
        "beyond": {label: n - count for label, count in within.items()},
        "turned_beyond_1_degree": [
            [i, assignment[i], round(turns[i], 6)] for i in range(n) if abs(turns[i]) > 1
        ],
        "largest_turn_degrees": max(abs(value) for value in turns),
        "tilt_reversed": reversed_tilts,
        "assignment": assignment,
        "moves": moves,
        "turns": turns,
    }


def compare(test: Packing, reference: Packing) -> dict[str, Any]:
    rows = [measure(test, reference, symmetry, proper) for symmetry, proper in SYMMETRIES]
    rows.sort(key=lambda row: row["assignment_total_squared"])
    best = rows[0]
    ref_centres = [
        transform(best["symmetry"], reference.side, *reference.centre(k))
        for k in range(reference.n)
    ]
    distance = [
        [
            math.hypot(float(test.rows[i][0] - ref_centres[j][0]), float(test.rows[i][1] - ref_centres[j][1]))
            for j in range(reference.n)
        ]
        for i in range(test.n)
    ]
    best["bottleneck"] = bottleneck(distance)
    return {
        "side_difference": str(test.side - reference.side),
        "side_difference_approx": float(test.side - reference.side),
        "best": {key: value for key, value in best.items() if key not in ("moves", "turns")},
        "moves_by_square": [round(value, 15) for value in best["moves"]],
        "turns_by_square": [round(value, 9) for value in best["turns"]],
        "others": [
            {
                "symmetry": row["symmetry"],
                "rms": row["rms"],
                "nearest_one_to_one": row["nearest_one_to_one"],
                "beyond_1e-1": row["beyond"]["1e-1"],
            }
            for row in rows[1:]
        ],
    }


def undilated(test: Packing, factor: Fraction) -> Packing:
    return Packing(
        test.side / factor, [(x / factor, y / factor, t) for x, y, t in test.rows]
    )


def self_test() -> dict[str, Any]:
    rng = random.Random(7)
    failures = []
    for trial in range(300):
        n = rng.randint(2, 7)
        cost = [[rng.random() for _ in range(n)] for _ in range(n)]
        best = min(
            (sum(cost[i][perm[i]] for i in range(n)), perm) for perm in permutations(n)
        )
        got = hungarian(cost)
        if abs(sum(cost[i][got[i]] for i in range(n)) - best[0]) > 1e-12:
            failures.append(f"hungarian {trial}")
        brute = min(max(cost[i][perm[i]] for i in range(n)) for perm in permutations(n))
        if bottleneck(cost) != brute:
            failures.append(f"bottleneck {trial}")
    side = Fraction(10)
    packing = Packing(side, [(Fraction(1, 2), Fraction(3, 2), Fraction(1, 3)), (Fraction(7, 2), Fraction(1, 2), Fraction(0))])
    for symmetry, proper in SYMMETRIES:
        moved = Packing(
            side,
            [
                (*transform(symmetry, side, x, y), t if proper else -t)
                for x, y, t in packing.rows
            ],
        )
        if not any(
            measure(moved, packing, other, other_proper)["within"]["1e-20"] == 2
            and max(abs(value) for value in measure(moved, packing, other, other_proper)["turns"]) < 1e-9
            for other, other_proper in SYMMETRIES
        ):
            failures.append(f"symmetry {symmetry}")
    return {"trials": 300, "failures": failures, "passed": not failures}


def permutations(n: int) -> list[list[int]]:
    if n == 1:
        return [[0]]
    out = []
    for perm in permutations(n - 1):
        for position in range(n):
            out.append([*perm[:position], n - 1, *perm[position:]])
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--test", type=Path)
    parser.add_argument("--ref", action="append", default=[])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--undilate", action="store_true", help="divide the test's centres and side by 1 + 1e-20"
    )
    args = parser.parse_args()
    started = time.process_time()
    if args.self_test:
        result = self_test()
        sys.stdout.write(json.dumps(result) + "\n")
        if args.out:
            args.out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        return 0 if result["passed"] else 1
    test = read_text_certificate(args.test)
    if args.undilate:
        test = undilated(test, 1 + Fraction(1, 10**20))
    record: dict[str, Any] = {
        "program": PROGRAM.name,
        "program_sha256": hashlib.sha256(PROGRAM.read_bytes()).hexdigest(),
        "python": sys.version,
        "test": {
            "path": str(args.test),
            "sha256": hashlib.sha256(args.test.read_bytes()).hexdigest(),
            "undilated_by_1_plus_1e-20": args.undilate,
        },
        "references": {},
    }
    for item in args.ref:
        name, _, path_text = item.partition("=")
        path = Path(path_text)
        reference = read_text_certificate(path)
        result = compare(test, reference)
        result["path"] = str(path)
        result["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        record["references"][name] = result
        best = result["best"]
        sys.stdout.write(
            json.dumps(
                {
                    "ref": name,
                    "symmetry": best["symmetry"],
                    "one_to_one": best["nearest_one_to_one"],
                    "within": best["within"],
                    "largest": round(best["largest_move"], 9),
                    "bottleneck": round(best["bottleneck"], 9),
                    "rms": round(best["rms"], 9),
                    "turned>1": len(best["turned_beyond_1_degree"]),
                    "max_turn": round(best["largest_turn_degrees"], 4),
                    "reversed": best["tilt_reversed"],
                    "next": [(o["symmetry"], round(o["rms"], 4)) for o in result["others"][:2]],
                }
            )
            + "\n"
        )
        sys.stdout.flush()
    factor = 1 + Fraction(1, 10**20)
    record["undilated_side"] = str(test.side / factor)
    record["cpu_seconds"] = round(time.process_time() - started, 3)
    if args.out:
        args.out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
