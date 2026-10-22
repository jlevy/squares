"""Measure each retained view pose by pose against the packings its credit names.

Written for the stage 3 registration of Evan Daniel's regularized views at 204, 227, 229
and 260 (evand/square-packing@0075967, think-ql4v). A measurement for credit; it decides
nothing. Each view is read from its retained original gzip by the project's certificate
reader (`devtools.evand_exact_certificates.parse`); the packings it is compared with are
read from their own packets:

- T-223 at 204 and 260: Francisco Couzo's issue-678 certificates (couzo-issue678-2026-10-18);
- T-199 at 229: Evan Daniel's #674 update (evand-n229-dilation-update-2026-10-18);
- T-196 at 227 and 260: Joost de Winter's #668 centre-basis witnesses
  (de-winter-upper-bounds-227-229-260-2026-10-17), each basis held to the unit circle;
- #672 at 227: Francisco Couzo's certificates/n227.cert at
  franciscouzo/square-packing@af8cb7959aead318c0cf5e9f873de3caa763f77a, which no packet
  retains. It is read from a copy fetched at that commit (``--couzo-672 PATH``), refused
  unless its SHA-256 is the one #672's metadata names.

For each pair it reports `devtools.check_half_angle_area.arrangement_gap` (the nearest
centre under each of the box's eight symmetries, kept only where one to one) and an
optimal assignment (least total squared centre displacement under each symmetry, scipy in
binary64, the least kept): the largest move, the squares moved beyond each bound and the
largest turn. Exact sides and their differences are exact.

Usage, from packing/ with the project interpreter:
    python resources/web/evand-regularized-2026-10-20/measure/identity.py \
        --couzo-672 N227_CERT \
        --out resources/web/evand-regularized-2026-10-20/measure/identity.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

import numpy as np  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

from devtools import check_half_angle_area as area  # noqa: E402
from devtools import evand_exact_certificates as ev  # noqa: E402

WEB = Path("resources/web")
PACKET = WEB / "evand-regularized-2026-10-20"
COUZO_672_SHA256 = "65b03df883e75f890eca985232252a6340b9b5da3437c41275c9201df03d8c17"
BOUNDS = ("1e-9", "1e-6", "1e-3", "1e-2", "1e-1")
Placed = tuple[Fraction, Fraction, Fraction, Fraction]
Packing = tuple[Fraction, list[Placed]]


def certificate(path: Path) -> Packing:
    raw = path.read_bytes()
    if path.suffix == ".gz":
        raw = gzip.decompress(raw)
    cert = ev.parse(raw.decode("ascii"))
    return cert.side, area.placed([(p.x, p.y, p.t) for p in cert.poses])


def centre_basis(path: Path) -> Packing:
    document = json.loads(gzip.decompress(path.read_bytes()))
    squares: list[Placed] = []
    for square in document["squares"]:
        x, y = (Fraction(value) for value in square["center"])
        c, s = (Fraction(value) for value in square["basis"])
        squares.append((x, y, *area.unit_basis(c, s)))
    return Fraction(document["side"]), squares


def assignment(first: Packing, second: Packing) -> dict[str, object]:
    _side, left = first
    other_side, right = second
    a = np.array([[float(x), float(y)] for x, y, _c, _s in left])
    best: tuple[float, int, list[Placed], np.ndarray, np.ndarray, np.ndarray] | None = None
    for k in range(8):
        mapped = [area.symmetric(other_side, square, k) for square in right]
        b = np.array([[float(u), float(v)] for u, v, _p, _q in mapped])
        cost = ((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
        rows, cols = linear_sum_assignment(cost)
        total = float(cost[rows, cols].sum())
        if best is None or total < best[0]:
            best = (total, k, mapped, cost, rows, cols)
    assert best is not None
    _total, k, mapped, cost, rows, cols = best
    moves = np.sqrt(cost[rows, cols])
    turns = []
    for i, j in zip(rows, cols, strict=True):
        _x, _y, c, s = left[i]
        _u, _v, p, q = mapped[j]
        turns.append(float(min(abs(c * q - s * p), abs(c * p + s * q))))
    return {
        "symmetry": k,
        "largest_move": f"{float(moves.max()):.6g}",
        "moved_beyond": {bound: int((moves > float(bound)).sum()) for bound in BOUNDS},
        "largest_turn_degrees": f"{math.degrees(math.asin(min(1.0, max(turns)))):.4g}",
        "turned_beyond_1e-6": sum(1 for turn in turns if turn > 1e-6),
    }


def gap(first: Packing, second: Packing) -> dict[str, object]:
    try:
        found = area.arrangement_gap(first, second)
    except area.AreaRouteError as error:
        return {"one_to_one": False, "refusal": str(error)}
    return {
        "one_to_one": True,
        "symmetry": found["symmetry"],
        "largest_displacement": found["largest_displacement"],
        "largest_turn_degrees": (
            f"{math.degrees(math.asin(min(1.0, float(found['largest_orientation_sine'])))):.4g}"
        ),
        "moved_beyond": found["moved_beyond"],
        "turned_beyond_1e-6": found["turned_beyond_1e-6"],
    }


def measure(first: Packing, second: Packing) -> dict[str, object]:
    difference = first[0] - second[0]
    return {
        "side_difference": f"{float(difference):.6e}",
        "side_difference_exact": str(difference),
        "nearest_centre": gap(first, second),
        "assignment": assignment(first, second),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--couzo-672", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    raw = args.couzo_672.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != COUZO_672_SHA256:
        parser.error(f"#672's n227.cert has SHA-256 {digest}, not {COUZO_672_SHA256}")
    certs = PACKET / "source/search/regularize/lists/certs"
    views = {n: certificate(certs / f"n-{n:03d}.cert.gz") for n in (204, 227, 229, 260)}
    couzo = WEB / "couzo-issue678-2026-10-18/source/certificates/best"
    winter = WEB / "de-winter-upper-bounds-227-229-260-2026-10-17/source"
    daniel = WEB / "evand-n229-dilation-update-2026-10-18/source/search/packer/candidates"
    t223 = {n: certificate(couzo / f"n{n}.cert") for n in (204, 260)}
    t196 = {n: centre_basis(winter / f"n{n}/n{n}_exact.json.gz") for n in (227, 260)}
    t199 = certificate(daniel / "s229_v2.cert")
    p672 = certificate(args.couzo_672)
    result = {
        "format": "evand-regularized-1020-identity-v1",
        "couzo_672": {
            "source": "franciscouzo/square-packing@af8cb7959aead318c0cf5e9f873de3caa763f77a"
            ":certificates/n227.cert",
            "sha256": digest,
            "side": str(p672[0]),
        },
        "pairs": [
            {
                "n": 204,
                "view": "evand 0075967",
                "against": "T-223 (#678)",
                **measure(views[204], t223[204]),
            },
            {"n": 227, "view": "evand 0075967", "against": "#672", **measure(views[227], p672)},
            {
                "n": 227,
                "view": "evand 0075967",
                "against": "T-196 (#668)",
                **measure(views[227], t196[227]),
            },
            {"n": 227, "view": "#672", "against": "T-196 (#668)", **measure(p672, t196[227])},
            {
                "n": 229,
                "view": "evand 0075967",
                "against": "T-199 (#674 update)",
                **measure(views[229], t199),
            },
            {
                "n": 260,
                "view": "evand 0075967",
                "against": "T-223 (#678)",
                **measure(views[260], t223[260]),
            },
            {
                "n": 260,
                "view": "evand 0075967",
                "against": "T-196 (#668)",
                **measure(views[260], t196[260]),
            },
        ],
    }
    text = json.dumps(result, indent=1) + "\n"
    args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
