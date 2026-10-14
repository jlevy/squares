"""Decide square and rectangle certificates exactly, with the controls that must fail.

    python3 -I -B rectangle_check.py CERT [CERT ...] [--all-pairs] [--control NAME]
        [--expect-side S] [--expect-box AxB]

For each certificate it prints the count, the exact width and height, the integer box,
the waste, the exact squeeze ``min(a - W, b - H)`` and its float, the least wall
clearance and the least pair gap with the squares that attain them, how many pairs the
axis test decided and how many the distance test, and the verdict. ``--all-pairs``
decides every pair by the axis test. ``--control duplicate`` copies square 0 over
square 1 and ``--control outside`` moves square 0 through the right wall, the two
mutations that any sound checker must refuse. ``--expect-side`` and ``--expect-box``
hold the header to a stated side or box and fail otherwise.

Exit status 0 when every certificate is strict-valid (or, with a control, every one is
refused), 1 otherwise. Written for the review of 14 October 2026; see ../README.md.
"""

from __future__ import annotations

import argparse
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from squares_exact import (
    Certificate,
    check_strict,
    duplicate_control,
    outside_control,
    parse_certificate,
    scientific,
)


def say(line: str) -> None:
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


def describe(path: Path, cert: Certificate) -> None:
    a, b = cert.box
    say(f"{path.name}: n = {cert.n}, box {a} x {b}, waste {cert.waste}")
    say(f"  W = {cert.width} (= {float(cert.width):.15f})")
    if not cert.is_square:
        say(f"  H = {cert.height} (= {float(cert.height):.15f})")
    say(f"  squeeze min(a - W, b - H) = {cert.squeeze} (= {float(cert.squeeze):.12f})")


def run(path: Path, args: argparse.Namespace) -> bool:
    cert = parse_certificate(path.read_text(encoding="utf-8"))
    describe(path, cert)
    ok = True
    if args.expect_side is not None and cert.width != Fraction(args.expect_side):
        say(f"  EXPECTED side {args.expect_side}, header states {cert.width}")
        ok = False
    if args.expect_box is not None:
        a, b = (int(part) for part in args.expect_box.lower().split("x"))
        if cert.box != (a, b) or math.ceil(cert.width) != a or math.ceil(cert.height) != b:
            say(f"  EXPECTED box {a} x {b}, header gives {cert.box}")
            ok = False
    if args.control == "duplicate":
        cert = duplicate_control(cert)
    elif args.control == "outside":
        cert = outside_control(cert)
    started = time.process_time()
    verdict = check_strict(cert, all_pairs=args.all_pairs)
    seconds = time.process_time() - started
    say(
        f"  least wall clearance {verdict.least_wall_clearance} "
        f"(= {scientific(verdict.least_wall_clearance)}, square {verdict.wall_square})"
    )
    say(
        f"  least pair gap {verdict.least_pair_gap} "
        f"(= {scientific(verdict.least_pair_gap)}, squares {verdict.gap_pair})"
    )
    say(
        f"  pairs: {verdict.pairs_by_axes} by the axis test, "
        f"{verdict.pairs_by_distance} by centre distance > sqrt 2, "
        f"{cert.n * (cert.n - 1) // 2} in all; {seconds:.1f} CPU s"
    )
    for failure in verdict.failures[:3]:
        say(f"  failure: {failure}")
    if len(verdict.failures) > 3:
        say(f"  ... {len(verdict.failures)} failures")
    if args.control:
        refused = not verdict.strict_valid
        say(f"  control {args.control}: {'REFUSED' if refused else 'NOT REFUSED'}")
        return ok and refused
    say(f"  verdict: {'STRICT_VALID' if verdict.strict_valid else 'INVALID'}")
    return ok and verdict.strict_valid


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument("certificates", nargs="+", type=Path)
    parser.add_argument("--all-pairs", action="store_true", help="decide every pair by axes")
    parser.add_argument("--control", choices=("duplicate", "outside"), default=None)
    parser.add_argument("--expect-side", default=None, help="an exact rational side")
    parser.add_argument("--expect-box", default=None, help="the integer box, as 17x16")
    args = parser.parse_args(argv)
    results = [run(path, args) for path in args.certificates]
    say(f"{sum(results)} of {len(results)} as required")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
