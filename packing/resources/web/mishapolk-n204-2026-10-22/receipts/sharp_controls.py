"""Sharp controls on the lower 204 certificate through both maintained exact routes.

Written for the stage 4 replay of the release's second 204 file, `certificates/n204.cert`
at 12fc466 (think-h01y). The receipt of record, `exact-certification.json.xz`, holds the
kernel's two gross controls, a duplicated square (gap -1) and a square moved outside the
box; this certificate clears every wall by exactly 5e-21 and every pair by about 1e-20,
below the binary64 spacing of its coordinates, so a route rounding at binary64 or
tolerating 1e-15 would pass it as retained, and the gross controls cannot tell. These
controls go to exact contact and 1e-30 past it:

- `side-lowered-past-wall-contact` and `tightest-pair-closed-past-contact`, the kernel's
  two (`devtools.evand_arrangement_reports.sharp_input`): the side lowered by the least
  far-wall clearance, and the second square of the least-gap pair moved along the face
  normal that closes the gap;
- `squares-moved-past-near-wall-contact`, written here: every square translated toward
  the near wall, left or bottom, whichever is closer, by the least near-wall clearance,
  so a corner lies on that wall at contact and crosses it by 1e-30 past it, as the 22
  October review of T-229 moved its squares.

Each control is decided by `sqpack`'s exact verifier and the independent rational corner
checker, the two maintained routes, through the kernel's own entry points
(`run_sharp`, `to_witness`, `legacy.exact_verify`, `legacy.independent.check_squares`).
At contact both routes must accept with the margin exactly 0; past it both must refuse
with the margin exactly -1e-30. The program decides nothing about the certificate
itself: it shows that each route meets the certificate's own scale.

Usage, from packing/ with the project interpreter:
    python resources/web/mishapolk-n204-2026-10-22/receipts/sharp_controls.py \
        --out resources/web/mishapolk-n204-2026-10-22/receipts/sharp-controls.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

from devtools import evand_arrangement_reports as kernel  # noqa: E402
from devtools import evand_exact_certificates as legacy  # noqa: E402
from devtools import upper_bound_reports as reports  # noqa: E402

PACKET = reports.WEB / "mishapolk-n204-2026-10-22"
N = 204
NEAR_WALL = "squares-moved-past-near-wall-contact"
EPSILON = kernel.SHARP_EPSILON


def _literal(value: object) -> str:
    return legacy.literal(Fraction(str(value)))


def near_wall(certificate: legacy.Certificate, *, past: bool) -> legacy.Certificate:
    """Every square moved toward the closer near wall by its least clearance, and past."""
    corners = legacy.corner_squares(certificate)
    left = min(x for square in corners for x, _y in square)
    bottom = min(y for square in corners for _x, y in square)
    step = min(left, bottom) + (EPSILON if past else Fraction(0))
    dx, dy = (step, Fraction(0)) if left <= bottom else (Fraction(0), step)
    poses = tuple(replace(pose, x=pose.x - dx, y=pose.y - dy) for pose in certificate.poses)
    return replace(certificate, poses=poses)


def decide(certificate: legacy.Certificate, **profile: str) -> dict[str, dict[str, Any]]:
    first, _report = legacy.exact_verify(kernel.to_witness(certificate, **profile))
    second = legacy.independent.check_squares(
        legacy.corner_squares(certificate), certificate.side
    )
    return {
        route: {
            "passed": bool(verdict["verification_passed"]),
            "wall": _literal(verdict["minimum_containment_clearance"]),
            "gap": _literal(verdict["minimum_best_pair_gap"]),
        }
        for route, verdict in (("exact_verify", first), ("independent", second))
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    declaration = reports.load_declaration(PACKET)
    profile = {
        "witness_prefix": declaration["witness_prefix"],
        "claim_limitations": declaration["claim_limitations"],
    }
    certificate = reports.read_facts(PACKET, {N})[N]
    rows: list[dict[str, Any]] = []
    for control in (*kernel.SHARP_CONTROLS, NEAR_WALL):
        margin = "wall" if control != "tightest-pair-closed-past-contact" else "gap"
        for past in (False, True):
            started = time.process_time()
            if control == NEAR_WALL:
                verdicts = decide(near_wall(certificate, past=past), **profile)
            else:
                raw = kernel.run_sharp(certificate, control, past=past, **profile)
                verdicts = {
                    route: {
                        "passed": bool(verdict["passed"]),
                        "wall": legacy.literal(verdict["wall"]),
                        "gap": legacy.literal(verdict["gap"]),
                    }
                    for route, verdict in raw.items()
                }
            expected = -EPSILON if past else Fraction(0)
            ok = all(
                verdict["passed"] is not past and Fraction(verdict[margin]) == expected
                for verdict in verdicts.values()
            )
            rows.append(
                {
                    "control": control,
                    "where": "past-contact" if past else "at-contact",
                    "margin": margin,
                    "expected_margin": legacy.literal(expected),
                    "expected": "refused" if past else "accepted",
                    "routes": verdicts,
                    "as_expected": ok,
                    "cpu_seconds": round(time.process_time() - started, 3),
                }
            )
    result = {
        "format": "mishapolk-n204-sharp-controls-v1",
        "n": N,
        "certificate": "source/certificates/n204.cert",
        "side": legacy.literal(certificate.side),
        "epsilon": legacy.literal(EPSILON),
        "routes": list(kernel.ROUTES),
        "controls": rows,
        "all_as_expected": all(row["as_expected"] for row in rows),
    }
    text = json.dumps(result, indent=1) + "\n"
    args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0 if result["all_as_expected"] else 1


if __name__ == "__main__":
    sys.exit(main())
