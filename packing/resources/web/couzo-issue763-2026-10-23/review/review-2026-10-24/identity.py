"""Identity and lineage of the #763 packings at 268 and 303, by optimal assignment.

Stage 4 review of 24 October 2026 (bead think-zjus). Written by the reviewer from
the definition below; it imports nothing from the source or from this repository's
measurement tools, and reads every packing as data.

For two packings A and B of the same n, each in its own box [0, s_A]^2 and
[0, s_B]^2, and for each of the 8 symmetries g of the square, A's centres are mapped
about the box centres,

    q_k = g(p_k - (s_A/2, s_A/2)) + (s_B/2, s_B/2),

and squares of A are paired with squares of B by the assignment that minimises the
sum of squared centre distances (scipy's linear_sum_assignment, exact for the
float costs). The symmetry with the least sum is reported. A square's move is the
distance between its mapped centre and its partner's centre; its turn is the
difference of orientations modulo 90 degrees, after g's action on angles (a
reflection reverses them).

Four variants test how far the counts hang on the alignment and the cost, each at
the primary's symmetry: `scaled` also scales A's offsets by s_B/s_A; `anchored`
maps about A's own box centre, so that the boxes share their lower-left corner
instead of their centre; `sum_of_distances` minimises the sum of distances instead
of squared distances; and `refit` re-centres A by the mean displacement of the
current assignment and re-assigns until the assignment is stable (a translation fit
that suits refinements and overstates moves between different arrangements). The
runner-up symmetry's counts are recorded too, since a packing close to symmetric
under a reflection gives two symmetries of nearly equal cost.

Added after the reviewer read the 23 October review at 303, to speak the record's
words: whether nearest centres pair the squares one to one (under the best symmetry,
and under which symmetries at all), the bottleneck (the least largest move over all
assignments, by binary search on perfect matchings), and how many squares tilted
beyond 1 degree in both packings have their tilts reversed.

Inputs: rational certificates ('n side' then 'x y t', t = tan(theta/2)), this
repository's Witness/v2 files (centre and unit basis), and Evan Daniel's text
packings ('n side' then 'x y angle-in-degrees'), each named on the command line or
in COMPARISONS below. Paths outside this repository are given with --evand, a
checkout of evand/square-packing at 8a8879a; their SHA-256 are recorded.

Run from packing/:

    uv run --frozen --all-extras --group dev python -I \\
      resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/identity.py \\
      --evand PATH/TO/evand-square-packing-at-8a8879a \\
      --out resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/out/identity.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import sys
import time
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent.parent
PACKING = PACKET.parent.parent.parent  # packing/
REPO = PACKING.parent


@dataclass(frozen=True)
class Layout:
    label: str
    n: int
    side: float
    xy: np.ndarray  # (n, 2)
    deg: np.ndarray  # (n,), orientation in degrees modulo 90
    path: str
    sha256: str


def frac(token: str) -> Fraction:
    return Fraction(token)


def load_cert(label: str, path: Path) -> Layout:
    raw = path.read_bytes()
    rows = [ln.split() for ln in raw.decode("ascii").splitlines()
            if ln.strip() and not ln.startswith("#")]
    n, side = int(rows[0][0]), float(frac(rows[0][1]))
    body = rows[1:]
    if len(body) != n:
        msg = f"{path}: {len(body)} rows for n = {n}"
        raise ValueError(msg)
    xy = np.array([[float(frac(r[0])), float(frac(r[1]))] for r in body])
    deg = np.array([math.degrees(2 * math.atan(float(frac(r[2])))) for r in body]) % 90.0
    return Layout(label, n, side, xy, deg, rel(path), hashlib.sha256(raw).hexdigest())


def load_witness(label: str, path: Path) -> Layout:
    raw = path.read_bytes()
    text = gzip.decompress(raw).decode() if path.suffix == ".gz" else raw.decode()
    doc = yaml.load(text, Loader=yaml.CSafeLoader)["witness"]
    if doc.get("representation") != "center-basis":
        msg = f"{path}: representation {doc.get('representation')!r}"
        raise ValueError(msg)
    squares = doc["squares"]
    xy = np.array([[float(frac(str(s["center"][0]))), float(frac(str(s["center"][1])))]
                   for s in squares])
    deg = np.array([math.degrees(math.atan2(float(frac(str(s["basis"][1]))),
                                            float(frac(str(s["basis"][0])))))
                    for s in squares]) % 90.0
    return Layout(label, int(doc["n"]), float(frac(str(doc["side"]))), xy, deg, rel(path),
                  hashlib.sha256(raw).hexdigest())


def load_text_degrees(label: str, path: Path) -> Layout:
    raw = path.read_bytes()
    rows = [ln.split() for ln in raw.decode("ascii").splitlines()
            if ln.strip() and not ln.startswith("#")]
    n, side = int(rows[0][0]), float(rows[0][1])
    body = rows[1:]
    if len(body) != n:
        msg = f"{path}: {len(body)} rows for n = {n}"
        raise ValueError(msg)
    xy = np.array([[float(r[0]), float(r[1])] for r in body])
    deg = np.array([float(r[2]) for r in body]) % 90.0
    return Layout(label, n, side, xy, deg, rel(path), hashlib.sha256(raw).hexdigest())


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO))
    except ValueError:
        return str(path)


SYMMETRIES = [
    ("identity", ((1, 0), (0, 1)), 1),
    ("rotate 90", ((0, -1), (1, 0)), 1),
    ("rotate 180", ((-1, 0), (0, -1)), 1),
    ("rotate 270", ((0, 1), (-1, 0)), 1),
    ("mirror x", ((-1, 0), (0, 1)), -1),
    ("mirror y", ((1, 0), (0, -1)), -1),
    ("mirror diagonal", ((0, 1), (1, 0)), -1),
    ("mirror antidiagonal", ((0, -1), (-1, 0)), -1),
]


def turn(a_deg: np.ndarray, b_deg: np.ndarray) -> np.ndarray:
    return np.abs((a_deg - b_deg + 45.0) % 90.0 - 45.0)


def assign(q: np.ndarray, b: np.ndarray, *, squared: bool = True) -> tuple[np.ndarray, float]:
    cost = ((q[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
    if not squared:
        cost = np.sqrt(cost)
    rows, cols = linear_sum_assignment(cost)
    order = np.empty(len(rows), dtype=int)
    order[rows] = cols
    return order, float(cost[rows, cols].sum())


def mapped(a: Layout, b: Layout, mat: np.ndarray, *, scale: float,
           anchored: bool = False) -> np.ndarray:
    ca = np.array([a.side / 2, a.side / 2])
    cb = ca if anchored else np.array([b.side / 2, b.side / 2])
    return ((a.xy - ca) @ mat.T) * scale + cb


def tilt(deg: np.ndarray) -> np.ndarray:
    """Signed tilt from the nearest axis, in (-45, 45] degrees."""
    return 45.0 - (45.0 - deg) % 90.0


def nearest_one_to_one(q: np.ndarray, b: np.ndarray) -> bool:
    """Whether every square's nearest centre in the other packing is a different one."""
    d2 = ((q[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
    nearest = d2.argmin(axis=1)
    return len(set(nearest.tolist())) == len(nearest)


def bottleneck(q: np.ndarray, b: np.ndarray) -> float:
    """The least largest move over all assignments (binary search on perfect matchings)."""
    dist = np.sqrt(((q[:, None, :] - b[None, :, :]) ** 2).sum(axis=2))
    levels = np.unique(dist)
    lo, hi = 0, len(levels) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        graph = csr_matrix(dist <= levels[mid])
        match = maximum_bipartite_matching(graph, perm_type="column")
        if (match >= 0).all():
            hi = mid
        else:
            lo = mid + 1
    return float(levels[lo])


def stats(q: np.ndarray, a_deg: np.ndarray, b: Layout, order: np.ndarray) -> dict[str, object]:
    moves = np.linalg.norm(q - b.xy[order], axis=1)
    turns = turn(a_deg, b.deg[order])
    k = int(np.argmax(moves))
    return {
        "moved_gt_0.1": int((moves > 0.1).sum()),
        "moved_within_0.09_to_0.11": int(((moves > 0.09) & (moves <= 0.11)).sum()),
        "squares_moved_gt_0.1": ([int(k) + 1 for k in np.flatnonzero(moves > 0.1)]
                                 if (moves > 0.1).sum() <= 12 else None),
        "moved_gt_1e-3": int((moves > 1e-3).sum()),
        "moved_gt_1e-6": int((moves > 1e-6).sum()),
        "moved_gt": {f"{t:g}": int((moves > t).sum())
                     for t in (1e-1, 3e-2, 1e-2, 1e-3, 1e-4, 1e-6, 1e-9)},
        "largest_move": float(moves[k]),
        "largest_move_square_a": k + 1,
        "largest_move_square_b": int(order[k]) + 1,
        "rms_move": float(np.sqrt((moves**2).mean())),
        "turned_gt_1deg": int((turns > 1.0).sum()),
        "tilts_reversed_gt_1deg": int(((np.abs(tilt(a_deg)) > 1.0)
                                       & (np.abs(tilt(b.deg[order])) > 1.0)
                                       & (np.sign(tilt(a_deg)) != np.sign(tilt(b.deg[order]))))
                                      .sum()),
        "tilted_gt_1deg_a": int((np.abs(tilt(a_deg)) > 1.0).sum()),
        "tilted_gt_1deg_b": int((np.abs(tilt(b.deg)) > 1.0).sum()),
        "largest_turn_deg": float(turns.max()),
    }


def compare(a: Layout, b: Layout) -> dict[str, object]:
    if a.n != b.n:
        msg = f"{a.label} has {a.n} squares, {b.label} {b.n}"
        raise ValueError(msg)
    trials = []
    for name, m, sense in SYMMETRIES:
        mat = np.array(m, dtype=float)
        q = mapped(a, b, mat, scale=1.0)
        order, total = assign(q, b.xy)
        trials.append((total, name, mat, sense, q, order))
    trials.sort(key=lambda t: t[0])
    total, name, mat, sense, q, order = trials[0]
    a_deg = (sense * a.deg) % 90.0
    primary = stats(q, a_deg, b, order)

    qs = mapped(a, b, mat, scale=b.side / a.side)
    order_s, _ = assign(qs, b.xy)
    scaled = stats(qs, a_deg, b, order_s)

    qr, order_r = q.copy(), order
    for _ in range(20):
        shift = (b.xy[order_r] - qr).mean(axis=0)
        qr = qr + shift
        new_order, _ = assign(qr, b.xy)
        if np.array_equal(new_order, order_r):
            break
        order_r = new_order
    refit = stats(qr, a_deg, b, order_r)
    refit["translation"] = [float(v) for v in (qr - q).mean(axis=0)]

    qa = mapped(a, b, mat, scale=1.0, anchored=True)
    order_a, _ = assign(qa, b.xy)
    anchored = stats(qa, a_deg, b, order_a)

    order_l, _ = assign(q, b.xy, squared=False)
    l1 = stats(q, a_deg, b, order_l)

    primary["nearest_one_to_one"] = nearest_one_to_one(q, b.xy)
    primary["bottleneck"] = bottleneck(q, b.xy)
    one_to_one_under = [nm for _, nm, _, _, qq, _ in trials if nearest_one_to_one(qq, b.xy)]

    ru_total, ru_name, ru_mat, ru_sense, ru_q, ru_order = trials[1]
    runner_up = stats(ru_q, (ru_sense * a.deg) % 90.0, b, ru_order)
    runner_up["symmetry"] = ru_name
    runner_up["sum_sq_cost"] = ru_total

    return {
        "a": a.label,
        "b": b.label,
        "side_a": a.side,
        "side_b": b.side,
        "side_a_minus_b": a.side - b.side,
        "symmetry": name,
        "sum_sq_cost": total,
        "next_symmetry": trials[1][1],
        "next_sum_sq_cost": trials[1][0],
        "same_assignment_scaled": bool(np.array_equal(order, order_s)),
        "same_assignment_refit": bool(np.array_equal(order, order_r)),
        "primary": primary,
        "scaled": scaled,
        "refit": refit,
        "anchored": anchored,
        "sum_of_distances": l1,
        "runner_up_symmetry": runner_up,
        "nearest_one_to_one_under": one_to_one_under,
    }


def main() -> int:  # noqa: PLR0915
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--evand", type=Path, required=True,
                        help="a checkout of evand/square-packing at 8a8879a")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    t0 = time.process_time()
    src = PACKET / "source" / "certificates"
    ev = args.evand / "search" / "packer" / "candidates"
    wit = PACKING / "witnesses" / "known-best"
    layouts = {
        "763@268": load_cert("#763 at 268 (n268.cert)", src / "best" / "n268.cert"),
        "v4@268": load_cert(
            "parent at 268, Tymchishin's EDA+Seam LP v4 (parents/85dbd707...)",
            src / "parents"
            / "85dbd707746197d31f62dd52b4e580dfb90097498a4970c577f776ce7de2df46.cert"),
        "T174@268": load_witness("house at 268, T-174 (W-known-best-n268)",
                                 wit / "n-268.yaml"),
        "evand@268": load_cert("evand 8a8879a s268_lightning.cert",
                               ev / "s268_lightning.cert"),
        "lavrentev@268": load_text_degrees(
            "evand 8a8879a s268_lightning.input.txt (Lavrentev's public packing as input)",
            ev / "s268_lightning.input.txt"),
        "predescent@268": load_text_degrees("evand 8a8879a s268_lightning.predescent.txt",
                                            ev / "s268_lightning.predescent.txt"),
        "763@303": load_cert("#763 at 303 (n303.cert)", src / "best" / "n303.cert"),
        "push@303": load_cert(
            "parent at 303, Couzo's Kaggle push (parents/22f07a7c...)",
            src / "parents"
            / "22f07a7c318328d257d1a7efd9c5acb05e3286650a94da751592b21014424244.cert"),
        "T230@303": load_cert(
            "T-230 (evand-n303-2026-10-22 s303_r303w0.cert)",
            PACKING / "resources" / "web" / "evand-n303-2026-10-22" / "source" / "search"
            / "packer" / "candidates" / "s303_r303w0.cert"),
        "T239@303": load_witness("house at 303, T-239 (W-known-best-n303)",
                                 wit / "n-303.yaml"),
        "deotte@303": load_cert("evand 8a8879a s303_cdeotte.cert (Deotte's public packing)",
                                ev / "s303_cdeotte.cert"),
    }
    pairs = [
        ("763@268", "v4@268"),
        ("763@268", "T174@268"),
        ("763@268", "evand@268"),
        ("763@268", "lavrentev@268"),
        ("763@268", "predescent@268"),
        ("v4@268", "T174@268"),
        ("v4@268", "lavrentev@268"),
        ("v4@268", "predescent@268"),
        ("lavrentev@268", "evand@268"),
        ("763@303", "push@303"),
        ("763@303", "T230@303"),
        ("763@303", "T239@303"),
        ("763@303", "deotte@303"),
        ("push@303", "T230@303"),
        ("push@303", "deotte@303"),
        ("T230@303", "T239@303"),
    ]
    root = str(args.evand.resolve())
    for key, lay in list(layouts.items()):
        if lay.path.startswith(root):
            layouts[key] = replace(
                lay, path="evand/square-packing@8a8879a:" + lay.path[len(root):].lstrip("/"))
    rows = []
    for ka, kb in pairs:
        r = compare(layouts[ka], layouts[kb])
        r["key"] = f"{ka} vs {kb}"
        rows.append(r)
        p, s, f = r["primary"], r["scaled"], r["refit"]
        an, l1 = r["anchored"], r["sum_of_distances"]
        assert isinstance(p, dict)
        assert isinstance(s, dict)
        assert isinstance(f, dict)
        assert isinstance(an, dict)
        assert isinstance(l1, dict)
        print(f"{ka:>15} vs {kb:<15} sym={r['symmetry']:<19} >0.1: {p['moved_gt_0.1']:>3}"
              f" (scaled {s['moved_gt_0.1']}, anchored {an['moved_gt_0.1']}, sum-of-dist "
              f"{l1['moved_gt_0.1']}, refit {f['moved_gt_0.1']}; within 0.09-0.11: "
              f"{p['moved_within_0.09_to_0.11']})  >1e-3: {p['moved_gt_1e-3']:>3} (scaled "
              f"{s['moved_gt_1e-3']}, anchored {an['moved_gt_1e-3']}, sum-of-dist "
              f"{l1['moved_gt_1e-3']}, refit {f['moved_gt_1e-3']})  largest "
              f"{p['largest_move']:.3e} (scaled {s['largest_move']:.3e}, anchored "
              f"{an['largest_move']:.3e}, refit {f['largest_move']:.3e})  turned>1deg "
              f"{p['turned_gt_1deg']}  sides {r['side_a']:.12f} / {r['side_b']:.12f}")
    receipt = {
        "program": "identity.py",
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "inputs": {k: {"label": v.label, "path": v.path, "sha256": v.sha256, "n": v.n,
                       "side": v.side} for k, v in layouts.items()},
        "comparisons": rows,
        "cpu_seconds_total": round(time.process_time() - t0, 2),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    for r in rows:
        hist = r["primary"]["moved_gt"]  # type: ignore[index]
        print(f"  {r['key']}: squares moved beyond " + ", ".join(
            f"{k}: {v}" for k, v in hist.items()))
    for r in rows:
        p = r["primary"]
        assert isinstance(p, dict)
        print(f"  {r['key']}: nearest centres one to one under the best symmetry: "
              f"{p['nearest_one_to_one']} (one to one under: "
              f"{', '.join(r['nearest_one_to_one_under']) or 'none'}); bottleneck "  # type: ignore[arg-type]
              f"{p['bottleneck']:.4g}; tilts beyond 1 deg reversed {p['tilts_reversed_gt_1deg']}; "
              f"tilted beyond 1 deg {p['tilted_gt_1deg_a']} / {p['tilted_gt_1deg_b']}")
    for r in rows:
        ru = r["runner_up_symmetry"]
        assert isinstance(ru, dict)
        print(f"  {r['key']}: best {r['symmetry']} (cost {r['sum_sq_cost']:.6g}), runner-up "
              f"{ru['symmetry']} (cost {ru['sum_sq_cost']:.6g}): >0.1 {ru['moved_gt_0.1']}, "
              f">1e-3 {ru['moved_gt_1e-3']}, largest {ru['largest_move']:.3e}")
    print(f"cpu {receipt['cpu_seconds_total']} s; receipt {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
