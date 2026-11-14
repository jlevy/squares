"""Lane L163 lineage, after the freeze: rebuild each issue's seed from its stated source.

Usage: l163_lineage.py N404.cert N229.yaml H147.yaml H148.yaml OUTDIR OUT.json

- #984: Couzo's n = 404 certificate, under each of the box's eight symmetries ("mirror
  it"), less every square with 13.8 <= x + y < 23.8, the squares beyond translated by
  (-5, -5), in the box of side S_404 - 5.
- #985: the n = 229 house witness, less every square with 13 <= x + y < 19, the squares
  beyond translated by (-3, -3), in the box of side S_229 - 3.

For each seed it counts the squares, and decides every pair and wall exactly by method A
(`l163_sat`): the deepest overlap is the most negative margin. It writes each seed as an
exact `.cert` text (`n S`, then `x y t`) for `devtools.measure_identity`. It also asks
whether the 147 house's squares are the 148 house's less one. Decides no certificate.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction as F  # noqa: E402

import l163_geom as geom  # noqa: E402
import l163_sat as sat  # noqa: E402
import yaml  # noqa: E402
from l163_reader import read_cert  # noqa: E402

Pose = tuple[F, F, F]  # cx, cy, t


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def symmetries(side: F) -> list[tuple[str, object]]:
    def mk(fx, ft):  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        return lambda p: (*fx(p[0], p[1]), ft(p[2]))  # pyright: ignore[reportUnknownLambdaType]

    same = lambda t: t  # noqa: E731
    neg = lambda t: -t  # noqa: E731
    return [
        ("identity", mk(lambda x, y: (x, y), same)),
        ("quarter turn", mk(lambda x, y: (side - y, x), same)),
        ("half turn", mk(lambda x, y: (side - x, side - y), same)),
        ("three-quarter turn", mk(lambda x, y: (y, side - x), same)),
        ("mirror x", mk(lambda x, y: (side - x, y), neg)),
        ("mirror y", mk(lambda x, y: (x, side - y), neg)),
        ("transpose", mk(lambda x, y: (y, x), neg)),
        ("anti-transpose", mk(lambda x, y: (side - y, side - x), neg)),
    ]


def cut(poses: list[Pose], lo: F, hi: F, shift: F) -> list[Pose]:
    out: list[Pose] = []
    for x, y, t in poses:
        s = x + y
        if lo <= s < hi:
            continue
        out.append((x - shift, y - shift, t) if s >= hi else (x, y, t))
    return out


def judge(poses: list[Pose], side: F) -> dict[str, object]:
    rows = [geom.row(x, y, t) for x, y, t in poses]
    sq = [sat.prepare(r) for r in rows]
    n = len(sq)
    worst = F(0)
    worst_pair = None
    over = 0
    for i in range(n):
        for j in range(i + 1, n):
            m = sat.margin(sq[i], sq[j])
            if m < 0:
                over += 1
                if m < worst:
                    worst, worst_pair = m, [i + 1, j + 1]
    wall = min(min(sat.clearances(s, (side.numerator, side.denominator))) for s in sq)
    return {
        "squares": n,
        "overlapping_pairs": over,
        "deepest_overlap": geom.sci(-worst) if worst < 0 else "0",
        "deepest_pair": worst_pair,
        "least_wall_clearance": geom.sci(wall),
    }


def write_cert(path: str, poses: list[Pose], side: F, note: str) -> None:
    lines = [f"# {note}", f"{len(poses)} {side.numerator}/{side.denominator}"]
    for x, y, t in poses:
        lines.append(f"{x.numerator}/{x.denominator} {y.numerator}/{y.denominator} {t.numerator}/{t.denominator}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def read_center_basis(path: str) -> tuple[F, list[Pose]]:
    with open(path, encoding="utf-8") as fh:
        w = yaml.safe_load(fh)["witness"]
    if w["representation"] != "center-basis" or w["scalar"]["kind"] != "rational":
        raise SystemExit("not a rational center-basis witness")
    poses: list[Pose] = []
    for s in w["squares"]:
        x, y = (F(str(c)) for c in s["center"])
        c, sn = (F(str(b)) for b in s["basis"])
        if c * c + sn * sn != 1 or c == -1:
            raise SystemExit("basis not a unit vector with a half-angle tangent")
        poses.append((x, y, sn / (1 + c)))
    return F(str(w["side"])), poses


def decimal_squares(path: str) -> list[tuple[str, str, str]]:
    with open(path, encoding="utf-8") as fh:
        w = yaml.safe_load(fh)["witness"]
    return [(str(s["center"][0]), str(s["center"][1]), str(s["angle"])) for s in w["squares"]]


def main() -> None:
    n404, n229, h147, h148, outdir, out = sys.argv[1:7]
    t0 = time.process_time()
    rec: dict[str, object] = {"lane": "L163", "program": "l163_lineage.py"}
    rec["inputs"] = {os.path.relpath(p) if not p.startswith("/tmp") else os.path.basename(p): sha(p) for p in (n404, n229, h147, h148)}
    # 228 from 404
    c404 = read_cert(n404, lowest=False)
    s404 = F(*c404.side)
    poses404 = [(F(r[0], r[1]), F(r[2], r[3]), F(r[4], r[5])) for r in c404.squares]
    res228 = []
    for name, f in symmetries(s404):
        p = [f(q) for q in poses404]  # pyright: ignore[reportCallIssue]
        seed = cut(p, F(138, 10), F(238, 10), F(5))
        entry: dict[str, object] = {"symmetry": name, "squares": len(seed)}
        sums = [q[0] + q[1] for q in p]
        entry["within_0.05_of_13.8_or_23.8"] = sum(1 for s in sums if abs(s - F(138, 10)) < F(5, 100) or abs(s - F(238, 10)) < F(5, 100))
        side5 = s404 - 5
        entry["centres_outside_new_box"] = sum(1 for x, y, _ in seed if not (0 <= x <= side5 and 0 <= y <= side5))
        entry["crossing_a_wall"] = sum(
            1 for x, y, t in seed if min(sat.clearances(sat.prepare(geom.row(x, y, t)), (side5.numerator, side5.denominator))) < 0
        )
        if len(seed) == 228:
            entry.update(judge(seed, s404 - 5))
            path = os.path.join(outdir, f"seed-n228-{name.replace(' ', '-')}.cert")
            write_cert(path, seed, s404 - 5, f"L163 seed: n404 under {name}, 13.8 <= x + y < 23.8 removed, beyond shifted by (-5, -5)")
            entry["written"] = os.path.basename(path)
        kept = [q for q in seed if 0 <= q[0] <= side5 and 0 <= q[1] <= side5]
        if len(kept) == 228 and len(seed) != 228:
            dropped = [[geom.floor_places(q[0], 3), geom.floor_places(q[1], 3)] for q in seed if q not in kept]
            entry["dropping_centres_outside"] = {"squares": 228, "dropped_centres": dropped, **judge(kept, side5)}
            if name in ("mirror x", "mirror y"):
                path = os.path.join(outdir, f"seed-n228-{name.replace(' ', '-')}-dropped.cert")
                write_cert(path, kept, side5, f"L163 seed: n404 under {name}, 13.8 <= x + y < 23.8 removed, beyond shifted by (-5, -5), two centres outside dropped")
                entry["dropping_centres_outside"]["written"] = os.path.basename(path)  # pyright: ignore[reportIndexIssue]
        res228.append(entry)
    rec["n228_from_n404"] = {"source_side": geom.floor_places(s404, 12), "seed_side": geom.floor_places(s404 - 5, 12), "by_symmetry": res228}
    # 147 from 229
    s229, poses229 = read_center_basis(n229)
    seed147 = cut(poses229, F(13), F(19), F(3))
    e147: dict[str, object] = {"squares": len(seed147), "source_side": geom.floor_places(s229, 12), "seed_side": geom.floor_places(s229 - 3, 12)}
    if len(seed147) == 147:
        e147.update(judge(seed147, s229 - 3))
        path = os.path.join(outdir, "seed-n147.cert")
        write_cert(path, seed147, s229 - 3, "L163 seed: n229 house, 13 <= x + y < 19 removed, beyond shifted by (-3, -3)")
        e147["written"] = os.path.basename(path)
    removed = [q for q in poses229 if F(13) <= q[0] + q[1] < F(19)]
    e147["removed_tilted_beyond_1e-6"] = sum(1 for q in removed if abs(q[2]) > F(1, 10**6))
    e147["source_tilted_beyond_1e-6"] = sum(1 for q in poses229 if abs(q[2]) > F(1, 10**6))
    rec["n147_from_n229"] = e147
    # the 147 house within the 148 house
    a, b = decimal_squares(h147), decimal_squares(h148)
    sb = set(b)
    rec["house147_within_house148"] = {
        "squares_147_found_in_148": sum(1 for s in a if s in sb),
        "of": len(a),
        "squares_148_not_in_147": [list(s) for s in b if s not in set(a)],
    }
    rec["cpu_seconds"] = round(time.process_time() - t0, 1)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    print(json.dumps({k: rec[k] for k in ("n147_from_n229", "house147_within_house148")})[:900])
    for e in res228:
        print(e)


if __name__ == "__main__":
    main()
