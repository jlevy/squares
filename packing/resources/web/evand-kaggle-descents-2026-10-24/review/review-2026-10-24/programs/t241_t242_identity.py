"""Pose-by-pose identity of the T-241 and T-242 packings against the packings their credit names.

A program of the stage 4 mathematical review of T-241 and T-242 (bead think-vm3m). It
is a measurement for credit and decides no bound. It was written from the geometry
alone: it does not read or import the packets' measure/identity.py or
devtools.measure_identity, and it reads every packing file as data.

For packings A and B of one count, each in its own box [0, S]^2, and for each of the
box's eight symmetries g, it maps B by g in B's box and compares centres with A's:

- nearest centres: for each square of A the nearest centre of g(B), and whether that
  map is one to one;
- the optimal assignment: the one-to-one pairing that minimises the sum of centre
  distances (scipy.optimize.linear_sum_assignment), and, as a check, the one that
  minimises the sum of squared distances.

For the symmetry with the least assignment cost it reports the squares moved beyond
1e-1, 1e-3, 1e-6 and 1e-9, the largest move, and the largest turn of a paired square
(orientations compared modulo 90 degrees; a reflection reverses them). Two placements
are measured: both boxes anchored at the origin (corner), and box-centred, which
shifts B by half the difference of the sides.

Run from packing/ with the project interpreter, for example
    python -I resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/programs/t241_t242_identity.py \
        --out resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/outputs/t241_t242_identity.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import re
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment

HERE = Path(__file__).resolve().parent
PACKING = HERE.parents[5]
TOKEN = re.compile(r"[+-]?[0-9]+(?:/[0-9]+)?")
WEB = "resources/web"
EVAND = f"{WEB}/evand-kaggle-descents-2026-10-24/source/search/packer/candidates"
COUZO = f"{WEB}/couzo-issue763-2026-10-23/source/certificates"

# name: (path relative to packing/, reader, expected n, what it is)
PACKINGS = {
    "T-242 268": (f"{EVAND}/s268_lightning.cert", "cert", 268, "Daniel's certificate at 268 (8a8879a)"),
    "#763 268": (f"{COUZO}/best/n268.cert", "cert", 268, "#763's entry at 268, Couzo's 964ee2b certificate"),
    "T-174 268": ("witnesses/known-best/n-268.yaml", "witness", 268, "the house at 268, PingYou's PR 574 certificate (T-174)"),
    "Tymchishin 268": (
        f"{COUZO}/parents/85dbd707746197d31f62dd52b4e580dfb90097498a4970c577f776ce7de2df46.cert",
        "cert", 268, "#763's parent: Tymchishin's EDA+Seam LP v4 packing, Couzo's best at fa6237e",
    ),
    "Lavrentev 268 (Daniel input)": (f"{EVAND}/s268_lightning.input.txt", "degrees", 268,
                                     "Daniel's binary64 input, which his commit names Lavrentev's public packing"),
    "Daniel predescent 268": (f"{EVAND}/s268_lightning.predescent.txt", "degrees", 268,
                              "Daniel's s268_lightning.predescent.txt"),
    "T-242 268 regularized view": (f"{EVAND}/s268_lightning_regularized.cert", "cert", 268,
                                   "Daniel's regularized display view at 268"),
    "T-241 304": (f"{COUZO}/best/n304.cert", "cert", 304, "Couzo's fa6237e certificate at 304 (T-241)"),
    "T-242 304": (f"{EVAND}/s304_pub.cert", "cert", 304, "Daniel's certificate at 304 (8a8879a)"),
    "T-186 304": ("witnesses/known-best/n-304.yaml", "witness", 304,
                  "the house at 304, Polkovskyi's 70a033f certificate (T-186), the manifest's previous source"),
    "T-175 304": (f"{WEB}/dostashev-merged-bands-2026-10-13/source/records/n0304.sqcert", "sqcert", 304,
                  "Ostashev's #575 certificate at 304 (T-175)"),
    "Daniel input 304": (f"{EVAND}/s304_pub.input.txt", "degrees", 304,
                         "Daniel's binary64 input, which his commit names the public Kaggle packing at 17.9268989004"),
}

COMPARISONS = (
    ("T-242 268", "#763 268"),
    ("T-242 268", "T-174 268"),
    ("T-242 268", "Tymchishin 268"),
    ("T-242 268", "Lavrentev 268 (Daniel input)"),
    ("T-242 268", "Daniel predescent 268"),
    ("T-242 268", "T-242 268 regularized view"),
    ("#763 268", "Tymchishin 268"),
    ("#763 268", "Lavrentev 268 (Daniel input)"),
    ("#763 268", "T-174 268"),
    ("Tymchishin 268", "Lavrentev 268 (Daniel input)"),
    ("Tymchishin 268", "Daniel predescent 268"),
    ("Tymchishin 268", "T-174 268"),
    ("T-241 304", "T-186 304"),
    ("T-241 304", "T-175 304"),
    ("T-241 304", "Daniel input 304"),
    ("T-242 304", "T-241 304"),
    ("T-242 304", "Daniel input 304"),
    ("T-242 304", "T-186 304"),
    ("T-186 304", "T-175 304"),
)

SYMMETRIES = (
    "identity",
    "rotation 90",
    "rotation 180",
    "rotation 270",
    "mirror x to S-x",
    "mirror y to S-y",
    "diagonal (x,y) to (y,x)",
    "anti-diagonal (x,y) to (S-y,S-x)",
)
THRESHOLDS = (1e-1, 1e-3, 1e-6, 1e-9)


def rational(token: str) -> Fraction:
    if TOKEN.fullmatch(token) is None:
        raise ValueError(f"not a rational: {token[:40]!r}")
    return Fraction(token)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if path.suffix == ".gz":
        raw = gzip.decompress(raw)
    return raw.decode("ascii")


def load(path: Path, kind: str) -> tuple[float, np.ndarray]:
    """Side and an (n, 3) array of x, y and orientation in degrees modulo 90."""
    rows: list[tuple[float, float, float]] = []
    side: float
    if kind in ("cert", "degrees"):
        lines = [ln.split() for ln in read_text(path).splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
        n = int(lines[0][0])
        side = float(rational(lines[0][1])) if kind == "cert" else float(lines[0][1])
        for tokens in lines[1:]:
            if kind == "cert":
                x, y, t = (rational(tok) for tok in tokens)
                rows.append((float(x), float(y), math.degrees(2 * math.atan(float(t)))))
            else:
                rows.append((float(tokens[0]), float(tokens[1]), float(tokens[2])))
    elif kind == "sqcert":
        side = math.nan
        n = -1
        for line in read_text(path).splitlines():
            tokens = line.split()
            if not tokens or tokens[0].startswith("#"):
                continue
            if tokens[0] == "n":
                n = int(tokens[1])
            elif tokens[0] == "s":
                side = float(rational(tokens[1]))
            else:
                x, y, t = (rational(tok) for tok in tokens)
                rows.append((float(x), float(y), math.degrees(2 * math.atan(float(t)))))
    elif kind == "witness":
        text = read_text(path)
        side_match = re.search(r"^  side: (\S+)$", text, re.MULTILINE)
        if side_match is None:
            raise ValueError("no side")
        side = float(rational(side_match.group(1).strip("'\"")))
        body = text.split("\n  squares:\n", 1)[1].split("\n  claim:\n", 1)[0]
        blocks = body.split("\n  - id: ")
        for block in blocks:
            values = re.findall(r"^    - '?([^'\s]+)'?$", block, re.MULTILINE)
            if len(values) != 4:
                continue
            x, y, c, s = (float(rational(v)) for v in values)
            rows.append((x, y, math.degrees(math.atan2(s, c))))
        n = len(rows)
    else:
        raise ValueError(kind)
    array = np.array(rows, dtype=float)
    if len(array) != n:
        raise ValueError(f"{path}: {len(array)} squares, header {n}")
    array[:, 2] = np.mod(array[:, 2], 90.0)
    return side, array


def apply(k: int, side: float, p: np.ndarray) -> np.ndarray:
    x, y, a = p[:, 0], p[:, 1], p[:, 2]
    s = side
    maps = (
        (x, y, a),
        (s - y, x, a),
        (s - x, s - y, a),
        (y, s - x, a),
        (s - x, y, -a),
        (x, s - y, -a),
        (y, x, -a),
        (s - y, s - x, -a),
    )
    mx, my, ma = maps[k]
    return np.stack([mx, my, np.mod(ma, 90.0)], axis=1)


def turn(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.abs(np.mod(a - b + 45.0, 90.0) - 45.0)


def measure(side_a: float, pa: np.ndarray, side_b: float, pb: np.ndarray, anchor: str) -> dict[str, object]:
    rows = []
    for k in range(8):
        gb = apply(k, side_b, pb)
        if anchor == "centred":
            gb[:, 0] += (side_a - side_b) / 2
            gb[:, 1] += (side_a - side_b) / 2
        diff = pa[:, None, :2] - gb[None, :, :2]
        dist = np.sqrt((diff**2).sum(axis=2))
        nearest = dist.argmin(axis=1)
        one_to_one = len(set(nearest.tolist())) == len(nearest)
        r, c = linear_sum_assignment(dist)
        moves = dist[r, c]
        r2, c2 = linear_sum_assignment(dist**2)
        turns = turn(pa[r, 2], gb[c, 2])
        rows.append(
            {
                "symmetry": SYMMETRIES[k],
                "nearest_one_to_one": one_to_one,
                "nearest_largest": float(dist[np.arange(len(pa)), nearest].max()),
                "assignment_cost": float(moves.sum()),
                "beyond": {f"{t:g}": int((moves > t).sum()) for t in THRESHOLDS},
                "largest_move": float(moves.max()),
                "largest_turn_degrees": float(turns.max()),
                "largest_turn_within_0.1_degrees": float(turns[moves <= 0.1].max()) if (moves <= 0.1).any() else None,
                "squared_assignment_beyond": {f"{t:g}": int((dist[r2, c2] > t).sum()) for t in THRESHOLDS},
                "squared_assignment_largest_move": float(dist[r2, c2].max()),
                "squared_assignment_same_pairing": bool((c2 == c).all()),
                "nearest_agrees_with_assignment": bool((nearest[r] == c).all()),
            }
        )
    best = min(range(8), key=lambda k: rows[k]["assignment_cost"])
    return {"best": rows[best], "all": rows}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    started = time.process_time()
    loaded: dict[str, tuple[float, np.ndarray]] = {}
    inputs = {}
    for name, (rel, kind, n, what) in PACKINGS.items():
        path = PACKING / rel
        side, poses = load(path, kind)
        if len(poses) != n:
            raise AssertionError(f"{name}: {len(poses)} squares, not {n}")
        loaded[name] = (side, poses)
        inputs[name] = {"path": rel, "sha256": sha256(path), "what": what, "side": side, "n": n}
    results = []
    for a, b in COMPARISONS:
        side_a, pa = loaded[a]
        side_b, pb = loaded[b]
        entry = {
            "a": a,
            "b": b,
            "side_difference": side_a - side_b,
            "corner": measure(side_a, pa, side_b, pb, "corner"),
            "centred": measure(side_a, pa, side_b, pb, "centred"),
        }
        results.append(entry)
        for anchor in ("corner", "centred"):
            best = entry[anchor]["best"]
            print(
                f"{a} vs {b} [{anchor}]: {best['symmetry']}; nearest one-to-one {best['nearest_one_to_one']}; "
                f"beyond 0.1/1e-3/1e-6/1e-9 = {best['beyond']['0.1']}/{best['beyond']['0.001']}/"
                f"{best['beyond']['1e-06']}/{best['beyond']['1e-09']}; largest {best['largest_move']:.3g}; "
                f"turn {best['largest_turn_degrees']:.3g} deg; squared same {best['squared_assignment_same_pairing']}"
                f" (squared: beyond 0.1 {best['squared_assignment_beyond']['0.1']}, "
                f"largest {best['squared_assignment_largest_move']:.6g})",
                flush=True,
            )
    report = {
        "program": "t241_t242_identity.py",
        "program_sha256": sha256(Path(__file__)),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "inputs": inputs,
        "comparisons": results,
        "cpu_seconds": round(time.process_time() - started, 2),
    }
    if args.out:
        args.out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(f"cpu seconds: {report['cpu_seconds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
