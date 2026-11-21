"""C3 and C4: the case orbits, and the cases that real packings of 18 squares reach.

Usage:
  python -I r1050_orbits.py --rack stabs18-endpoint-window.json --out orbits.json
  python -I r1050_orbits.py --rack ... --construction six-tilt18.json --witness-out w.json

C3. The three unoccupied marks of a case form a 3-subset of the 21 marks. Its orbit under
the eight symmetries of the box is named by its canonical form: the least, over the
symmetries, of the sorted tuple of the images' lattice coordinates. The count is
confirmed by Burnside's lemma.

C4. A real packing in [0, U]^2 lies in some case: each tile chooses a mark nearest in its
own rotated maximum norm (S3). The construction is placed in [0, U]^2 at nine offsets
and under the eight symmetries; every tile's nearest marks are found exactly in
Q(sqrt 7), every tie is kept, and every injective choice gives a case. Then each tile is
moved alone in steps of 1/1000 along +-x and +-y while the packing stays valid in
[0, U]^2 (checked exactly at every step), and the cases reached are recorded. Every case
reached here contains a packing in the test box, so the source must not refute it.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from r1050_q7 import Q7, Tile, Vec, load_construction, pair_slack, wall_slacks  # noqa: E402
from r1050_rack import d4, load_rack  # noqa: E402

Lat = tuple[int, int]


def canonical(s: tuple[Lat, ...], scale: int) -> tuple[Lat, ...]:
    images = [tuple(sorted(d4(x, y, scale)[k] for x, y in s)) for k in range(8)]
    return min(images)


def enumerate_orbits(lattice: list[Lat], scale: int) -> tuple[list[tuple[Lat, ...]], int]:
    forms = {canonical(s, scale) for s in itertools.combinations(lattice, 3)}
    # Burnside: average number of 3-subsets fixed setwise by each symmetry.
    fixed = 0
    for k in range(8):
        for s in itertools.combinations(lattice, 3):
            if tuple(sorted(d4(x, y, scale)[k] for x, y in s)) == tuple(sorted(s)):
                fixed += 1
    assert fixed % 8 == 0
    return sorted(forms), fixed // 8


def sym_point(k: int, p: Vec, cap: Q7) -> Vec:
    x, y = p
    return [(x, y), (cap - x, y), (x, cap - y), (cap - x, cap - y),
            (y, x), (cap - y, x), (y, cap - x), (cap - y, cap - x)][k]


def sym_vec(k: int, p: Vec) -> Vec:
    a, b = p
    return [(a, b), (-a, b), (a, -b), (-a, -b), (b, a), (-b, a), (b, -a), (-b, -a)][k]


def nearest(t: Tile, marks: list[Vec]) -> tuple[list[int], Q7]:
    vals = [t.norm(m) for m in marks]
    best = vals[0]
    for v in vals[1:]:
        if v < best:
            best = v
    return [k for k, v in enumerate(vals) if v == best], best


def cases_of(tiles: list[Tile], marks: list[Vec], lattice: list[Lat],
             scale: int) -> tuple[set[tuple[Lat, ...]], list[str]]:
    """All cases reachable by nearest-mark choices; problems found on the way."""
    problems: list[str] = []
    options: list[list[int]] = []
    for t in tiles:
        ks, best = nearest(t, marks)
        if not best < Fraction(1, 2):
            problems.append(f"tile {t.tid}: nearest mark not interior")
        options.append(ks)
    reached: set[tuple[Lat, ...]] = set()
    for choice in itertools.product(*options):
        if len(set(choice)) != len(choice):
            problems.append(f"non-injective choice {choice}")
            continue
        free = tuple(sorted(lattice[k] for k in range(len(marks)) if k not in choice))
        reached.add(canonical(free, scale))
    return reached, problems


def valid_move(tiles: list[Tile], idx: int, cap: Q7) -> bool:
    t = tiles[idx]
    if any(s < 0 for s in wall_slacks(t, cap)):
        return False
    return all(not pair_slack(t, o) < 0 for j, o in enumerate(tiles) if j != idx)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rack", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--construction", type=Path, default=None)
    ap.add_argument("--witness-out", type=Path, default=None)
    ap.add_argument("--step", default="1/1000")
    args = ap.parse_args()

    cap_f, scale, _eps, lattice, _n = load_rack(args.rack)
    if args.out is not None:
        forms, burnside = enumerate_orbits(lattice, scale)
        rep = {"program": "r1050_orbits.py", "marks": len(lattice),
               "subsets": len(list(itertools.combinations(lattice, 3))),
               "orbits": len(forms), "burnside": burnside,
               "canonical_forms": [[list(p) for p in f] for f in forms]}
        args.out.write_text(json.dumps(rep) + "\n")
        print(f"orbits {len(forms)} burnside {burnside} subsets {rep['subsets']}")

    if args.construction is None:
        return 0
    side, base = load_construction(args.construction)
    cap = Q7(cap_f)
    marks: list[Vec] = [(Q7(Fraction(x) * cap_f / scale), Q7(Fraction(y) * cap_f / scale))
                        for x, y in lattice]
    slack = cap - side
    if not slack > 0:
        raise SystemExit("cap does not exceed the construction's side")
    offsets = [Q7(0), slack.scale(Fraction(1, 2)), slack]
    placements: dict[str, list[str]] = {}
    problems: list[str] = []
    for ox, oy in itertools.product(offsets, offsets):
        for k in range(8):
            moved = []
            for t in base:
                c = (t.c[0] + ox, t.c[1] + oy)
                moved.append(Tile(t.tid, sym_point(k, c, cap), sym_vec(k, t.u), sym_vec(k, t.v)))
            reached, probs = cases_of(moved, marks, lattice, scale)
            problems += probs
            for f in reached:
                placements.setdefault(json.dumps(f), []).append(
                    f"offset ({float(ox):.3e},{float(oy):.3e}) symmetry {k}")
    # Loose tiles, moved one at a time from the placement at offset 0, symmetry 0.
    step = Fraction(args.step)
    moves: dict[str, list[str]] = {}
    ranges: list[dict[str, object]] = []
    for idx, t in enumerate(base):
        for dname, (ax, ay) in (("+x", (1, 0)), ("-x", (-1, 0)), ("+y", (0, 1)), ("-y", (0, -1))):
            k = 0
            while k < round(1 / step):
                cand = t.moved(Q7(ax * step * (k + 1)), Q7(ay * step * (k + 1)))
                trial = base[:idx] + [cand] + base[idx + 1:]
                if not valid_move(trial, idx, cap):
                    break
                k += 1
                reached, probs = cases_of(trial, marks, lattice, scale)
                problems += probs
                for f in reached:
                    moves.setdefault(json.dumps(f), []).append(f"tile {t.tid} {dname} {k}*{step}")
            if k:
                ranges.append({"tile": t.tid, "direction": dname, "steps": k})
    witness_orbits = sorted(set(placements) | set(moves))
    rep2 = {
        "program": "r1050_orbits.py --construction",
        "placements": 9 * 8,
        "orbits_from_placements": {f: v[:4] + ([f"... {len(v)} in all"] if len(v) > 4 else [])
                                   for f, v in placements.items()},
        "loose_moves": ranges,
        "orbits_from_moves": {f: v[:4] + ([f"... {len(v)} in all"] if len(v) > 4 else [])
                              for f, v in moves.items()},
        "witness_orbits": [json.loads(f) for f in witness_orbits],
        "problems": sorted(set(problems))[:20],
        "verdict": "WITNESSES_CLASSIFIED" if not problems else "PROBLEMS",
    }
    assert args.witness_out is not None
    args.witness_out.write_text(json.dumps(rep2, indent=1) + "\n")
    print(rep2["verdict"], f"orbits from placements {len(placements)}",
          f"orbits from moves {len(moves)}", f"witness orbits {len(witness_orbits)}",
          f"loose directions {len(ranges)}")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
