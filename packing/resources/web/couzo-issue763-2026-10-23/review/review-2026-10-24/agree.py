"""Hold this review's checker to the maintained replay at every number they share.

Stage 4 review of 24 October 2026 (bead think-zjus). Written after the reviewer read the
23 October review at 303, which does the same for its certificate; it decides nothing.
It reads, as data:

* this review's receipt, out/check-certificates.json, written by check_certificates.py;
* the packet's maintained replay receipt, receipts/exact-certification.json.xz, written
  by devtools.upper_bound_reports on both maintained routes (exact_verify and
  independent), whose code this review did not read;
* the two certificates, parsed again by check_certificates.py's own reader, loaded by
  path.

For each certificate it checks that the maintained run read the same side and the same
n poses (x, y, t), literal by literal as exact rationals; that both maintained routes
decided every pair, as route A did; and that their least wall clearance and least pair
gap equal route A's exactly. It also checks that the maintained receipt's two controls
are refused by both routes.

Run from packing/:

    uv run --frozen --all-extras --group dev python -I \\
      resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/agree.py \\
      --out resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/out/agree.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import lzma
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent.parent


def load_checker():  # noqa: ANN201
    sys.dont_write_bytecode = True  # leave no __pycache__ beside the kept programs
    spec = importlib.util.spec_from_file_location("review_checker", HERE / "check_certificates.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["review_checker"] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    checker = load_checker()
    ours = json.loads((HERE / "out" / "check-certificates.json").read_text(encoding="utf-8"))
    theirs = json.loads(lzma.open(PACKET / "receipts" / "exact-certification.json.xz").read())
    checks: list[dict[str, object]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:  # noqa: FBT001
        checks.append({"check": name, "equal": ok, "detail": detail})
        print(f"  {'EQUAL' if ok else 'DIFFER'}  {name}{': ' + detail if detail else ''}")

    for mine in ours["results"]:
        n = mine["n"]
        print(f"n = {n}")
        cases = {c["control"]: c for c in theirs["cases"] if c["n"] == n}
        pos = cases["positive"]
        packing = checker.parse_certificate(
            (PACKET / "source" / "certificates" / "best" / f"n{n}.cert").read_text("ascii"))
        side_in = Fraction(pos["checker_input"]["side"])
        check(f"{n}: side read by the maintained run", side_in == packing.side)
        poses = pos["checker_input"]["poses"]
        same_poses = len(poses) == packing.n and all(
            checker.square_from_tangent(Fraction(x), Fraction(y), Fraction(t))
            == sq for (x, y, t), sq in zip(poses, packing.squares, strict=True))
        check(f"{n}: {len(poses)} poses read by the maintained run, as exact rationals",
              same_poses)
        route_a = mine["positive"]["route_a"]
        gap_a = Fraction(route_a["least_pair_gap"])
        clear_a = Fraction(route_a["least_wall_clearance"])
        for route in ("exact_verify", "independent"):
            r = pos[route]
            check(f"{n}: {route} accepted", r["verification_passed"] is True
                  and not r["failures"])
            check(f"{n}: {route} pairs tested = route A's pairs", r["pairs_tested"]
                  == route_a["pairs_decided"], f"{r['pairs_tested']} and "
                  f"{route_a['pairs_decided']}")
            check(f"{n}: {route} least pair gap = route A's", Fraction(
                r["minimum_best_pair_gap"]) == gap_a, f"{float(gap_a):.6e}")
            check(f"{n}: {route} least wall clearance = route A's and route B's", Fraction(
                r["minimum_containment_clearance"]) == clear_a == Fraction(
                mine["positive"]["route_b"]["least_wall_clearance"]), f"{float(clear_a):.3e}")
        for control in ("duplicate-square-overlap", "square-translated-outside-container"):
            c = cases[control]
            check(f"{n}: maintained control {control} refused by both routes",
                  not c["exact_verify"]["verification_passed"]
                  and not c["independent"]["verification_passed"])
    equal = sum(1 for c in checks if c["equal"])
    print(f"{equal} of {len(checks)} checks equal")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"program": "agree.py", "equal": equal,
                                    "checks_total": len(checks), "checks": checks},
                                   indent=1) + "\n", encoding="utf-8")
    return 0 if equal == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
