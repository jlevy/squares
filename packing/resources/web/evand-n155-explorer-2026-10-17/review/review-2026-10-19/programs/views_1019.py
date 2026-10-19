"""Decide the source's three regularized display views on this review's third route.

#669, #659 and #664 each publish, beside the certificate their claim rests on, the same
packing regularized for display at the same exact side (``*_regularized.cert``), which
the packets retain and T-197's artifacts list. No maintained route replayed them. This
program decides each with `third_route_1019`'s parser and `decide`, imported from the
file beside it, and holds its side to the main certificate's; it runs no controls.

Usage, from ``packing/`` with the project interpreter::

    python -I views_1019.py --json OUT.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import third_route_1019 as route  # noqa: E402

VIEWS = (
    ("#669 n155", "evand-n155-explorer-2026-10-17", 155, "s155_ex2"),
    ("#659 n236", "evand-n236-2026-10-16", 236, "s236_bm3c"),
    ("#664 n271", "evand-n271-2026-10-17", 271, "s271_ex1"),
)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    report: dict[str, object] = {}
    bad = []
    for key, packet, n, stem in VIEWS:
        started = time.monotonic()
        folder = route.WEB / packet / "source/search/packer/candidates"
        side, poses, _comments = route.parse((folder / f"{stem}_regularized.cert").read_text(encoding="ascii"), n)
        main_side, _main_poses, _ = route.parse((folder / f"{stem}.cert").read_text(encoding="ascii"), n)
        decision = route.decide(side, poses)
        wall = decision["wall"]
        closest = decision["closest"]
        assert isinstance(wall, route.Fraction) and isinstance(closest, tuple)
        row = {
            "passed": decision["passed"],
            "same_side_as_certificate": side == main_side,
            "pairs": decision["pairs"],
            "measured_pairs": decision["measured"],
            "contacts": decision["contacts"],
            "least_wall_clearance": route.decimal(wall),
            "least_distance": route.sqrt_decimal(closest[0]),
            "wall_seconds": round(time.monotonic() - started, 2),
        }
        report[key] = row
        if not (row["passed"] and row["same_side_as_certificate"]):
            bad.append(key)
        print(key, json.dumps(row), flush=True)
    args.json.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
