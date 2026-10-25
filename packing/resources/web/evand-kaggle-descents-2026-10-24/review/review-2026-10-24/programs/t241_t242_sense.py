"""Decide the three certificates again under the other rotation sense.

A program of the stage 4 mathematical review of T-241 and T-242 (bead think-vm3m),
written after the review's findings, once it had read the stage 4 review of #763's
certificates and its RF-11. It decides nothing about the bounds: it reads every
rotation the other way, (c, s) = ((1 - t^2)/(1 + t^2), -2t/(1 + t^2)), and counts the
pairs that then overlap, to show that a checker which misread the sense would refuse
each certificate. It loads t241_t242_exact.py beside it by path and uses its decide().

Run from packing/:
    python -I resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/programs/t241_t242_sense.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKING = HERE.parents[5]


def load_checker():  # noqa: ANN201
    spec = importlib.util.spec_from_file_location("t241_t242_exact", HERE / "t241_t242_exact.py")
    if spec is None or spec.loader is None:
        raise ImportError("t241_t242_exact.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["t241_t242_exact"] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    exact = load_checker()
    for spec in exact.CERTIFICATES:
        cert = exact.read_certificate(PACKING / spec["path"])
        if cert.sha256 != spec["sha256"]:
            raise AssertionError(f"{spec['key']}: not the pinned certificate")
        for sense, sign in (("counter-clockwise, as the headers state", 1), ("clockwise", -1)):
            squares = [exact.square_from_pose(x, y, sign * t) for x, y, t in cert.poses]
            result = exact.decide(squares, cert.side)
            overlapping = result["method_b_clipped_areas"]["near_pairs_with_positive_overlap_area"]
            print(f"{spec['key']}, {sense}: valid={result['valid']} methods_agree={result['methods_agree']} "
                  f"overlapping pairs={overlapping} contained={result['method_a_separating_axes']['contained']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
