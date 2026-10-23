"""Build the n = 40 candidates the source's examples run, from this repository's copies.

``examples/n40/prepare.py`` of the source fetches its two densities over the network.
This program is written here instead, reads the copies this repository already retains
(by path, each held to the SHA-256 the source pins), and writes sqverify-fast format T
candidates with the rows in the order ``prepare.py`` uses, so that a run on them searches
the same expanded rectangles in the same order:

- ``c6715``: Hosono's rect_n40_L67 density (T-145), every row of positive weight, in file
  order; core ``B = 199529/200000``.
- ``c6718``: Guzhou0806's 685-orbit density (T-157), its ``sites`` in file order, each
  inherited site equal to its pool row of rect_n40_L67 with no pool index used twice,
  each generated site in no pool row's D4 orbit, and no two sites in one orbit; core
  ``B = 3350/3359``.
- each candidate's control, every weight times 985/1000 (the source's controls).

With ``--n28-candidate`` and ``--n28-control`` (the two candidate files of T-192's release
asset, held to the SHA-256 values its README pins) it also decides that certificate's
facts: its format (rows ``{rectangle, mass}``, an empty ``points`` list, and the
``proof_net`` it declares), that every row is a nondegenerate rectangle in ``[0, L]^2``
with positive mass, that the masses sum to its ``total_mass``, its count of distinct D4
images, and that the control is the candidate with every mass times 985/1000, row by row.

Every number is read as its exact decimal or fraction (``parse_float=Fraction``). It
checks every row is a nondegenerate rectangle in ``[0, L]^2`` with positive weight, the
mass is ``3999/100`` (``total_mass`` is written, so admission rechecks the sum), and
counts the distinct D4 images, which is the ``expanded_rectangles`` a run prints. It
prints one JSON receipt with each candidate's SHA-256.

Usage::

    python -I candidates.py --rect-n40-l67 PATH.json.gz --guzhou-6718 PATH.json.gz OUT_DIR
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

L = F(67, 10)
M = F(3999, 100)
SHA_RECT_N40_L67 = "71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0"
SHA_GUZHOU_6718 = "984fcd3acc605fe3c50a84912eed77e0192ca5b7253b19b6aa31a4e28e1bf5c2"
SHA_N28 = "a2e47a39e310c695fafeb8d1c744f930a561b3be7d71bbdb359e362eaebacb8d"
SHA_N28_CONTROL = "28ea4d6667c1021d399de7ca1f164f41de562781bc6e15b5be229b269425cda2"


def read(path: Path, sha: str) -> dict:
    raw = path.read_bytes()
    data = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
    got = hashlib.sha256(data).hexdigest()
    if got != sha:
        raise SystemExit(f"{path}: SHA-256 {got}, expected {sha}")
    return json.loads(data, parse_float=F, parse_int=F)


def num(value: object) -> F:
    return value if isinstance(value, F) else F(str(value))


def images(r: tuple[F, F, F, F], side: F = L) -> list[tuple[F, F, F, F]]:
    """The eight images of [x1,x2] x [y1,y2] under the symmetries of [0, side]^2."""
    x1, y1, x2, y2 = r
    out = []
    for a1, b1, a2, b2 in ((x1, y1, x2, y2), (y1, x1, y2, x2)):
        for fx in (False, True):
            for fy in (False, True):
                xa, xb = (side - a2, side - a1) if fx else (a1, a2)
                ya, yb = (side - b2, side - b1) if fy else (b1, b2)
                out.append((xa, ya, xb, yb))
    return out


def n28_facts(candidate: Path, control: Path) -> dict:
    doc = read(candidate, SHA_N28)
    ctl = read(control, SHA_N28_CONTROL)
    side = num(doc["L"])
    rows = [(tuple(num(v) for v in row["rectangle"]), num(row["mass"])) for row in doc["rectangles"]]
    ctl_rows = [(tuple(num(v) for v in row["rectangle"]), num(row["mass"])) for row in ctl["rectangles"]]
    admissible = all(0 <= r[0] < r[2] <= side and 0 <= r[1] < r[3] <= side and m > 0 for r, m in rows)
    total = sum((m for _, m in rows), F(0))
    distinct = {image for r, _ in rows for image in images(r, side)}
    return {
        "keys": sorted(doc),
        "format": "M (rows of {rectangle, mass})" if all(isinstance(r, dict) for r in doc["rectangles"]) else "other",
        "points": doc.get("points"),
        "proof_net": {k: str(v) for k, v in doc.get("proof_net", {}).items()},
        "n": int(doc["n"]),
        "L": str(side),
        "B_field": str(num(doc["B"])),
        "rows": len(rows),
        "all_rows_admissible": admissible,
        "mass": str(total),
        "total_mass_matches": num(doc["total_mass"]) == total,
        "distinct_images": len(distinct),
        "control_is_mass_times_985_1000": len(ctl_rows) == len(rows)
        and all(cr == r and cm == m * F(985, 1000) for (r, m), (cr, cm) in zip(rows, ctl_rows, strict=True))
        and num(ctl["total_mass"]) == total * F(985, 1000),
        "control_keys_equal": sorted(ctl) == sorted(doc) and ctl.get("proof_net") == doc.get("proof_net"),
    }


def orbit(r: tuple[F, F, F, F]) -> frozenset:
    return frozenset(images(r))


def write(out: Path, name: str, core: F, rows: list, weights: list[F]) -> dict:
    for r, w in zip(rows, weights, strict=True):
        x1, y1, x2, y2 = r
        if not (0 <= x1 < x2 <= L and 0 <= y1 < y2 <= L and w > 0):
            raise SystemExit(f"{name}: row {r} with weight {w} is not admissible")
    total = sum(weights, F(0))
    if total != M:
        raise SystemExit(f"{name}: mass {total}, expected {M}")
    distinct = {image for r in rows for image in images(r)}
    receipt = {"orbits": len(rows), "mass": str(total), "expanded_rectangles": len(distinct), "files": {}}
    for label, scale in ((name, F(1)), (f"{name}_mass0985", F(985, 1000))):
        doc = {
            "n": 40,
            "L": str(L),
            "B": str(core),
            "total_mass": str(total * scale),
            "rectangles": [[str(v) for v in r] for r in rows],
            "weights": [str(w * scale) for w in weights],
        }
        text = json.dumps(doc).encode()
        (out / f"{label}.json").write_bytes(text)
        receipt["files"][f"{label}.json"] = {
            "sha256": hashlib.sha256(text).hexdigest(),
            "total_mass": str(total * scale),
        }
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rect-n40-l67", type=Path, required=True)
    parser.add_argument("--guzhou-6718", type=Path, required=True)
    parser.add_argument("--n28-candidate", type=Path, default=None)
    parser.add_argument("--n28-control", type=Path, default=None)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    receipt: dict[str, object] = {}

    pool_doc = read(args.rect_n40_l67, SHA_RECT_N40_L67)
    pool = [tuple(num(v) for v in r) for r in pool_doc["rectangles"]]
    pool_weights = [num(w) for w in pool_doc["weights"]]
    rows = [r for r, w in zip(pool, pool_weights, strict=True) if w > 0]
    weights = [w for w in pool_weights if w > 0]
    receipt["c6715"] = write(args.out, "c6715", F(199529, 200000), rows, weights)
    receipt["c6715"]["source_rows"] = len(pool)

    doc = read(args.guzhou_6718, SHA_GUZHOU_6718)
    pool_orbits = {orbit(r) for r in pool}
    seen: set = set()
    used: set = set()
    kinds = {"inherited": 0, "generated": 0}
    rows, weights = [], []
    for site in doc["sites"]:
        box = tuple(num(v) for v in site["box"])
        o = orbit(box)
        if o in seen:
            raise SystemExit("c6718: two sites in one orbit")
        seen.add(o)
        kinds[site["kind"]] += 1
        if site["kind"] == "inherited":
            index = int(site["source_index"])
            if index in used or pool[index] != box:
                raise SystemExit(f"c6718: inherited site {index} is not its pool row")
            used.add(index)
        elif o in pool_orbits:
            raise SystemExit("c6718: a generated site lies in a pool orbit")
        rows.append(box)
        weights.append(num(site["weight"]))
    receipt["c6718"] = write(args.out, "c6718", F(3350, 3359), rows, weights)
    receipt["c6718"]["sites"] = kinds
    if args.n28_candidate is not None and args.n28_control is not None:
        receipt["n28"] = n28_facts(args.n28_candidate, args.n28_control)
    json.dump(receipt, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
