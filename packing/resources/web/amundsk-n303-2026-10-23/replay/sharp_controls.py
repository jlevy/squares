"""Run the kernel's sharp controls on #755's certificate at 303, on both maintained routes.

Written for the stage 3 replay of issue 755 (think-tqb5). The receipt's two controls
(`devtools.upper_bound_reports certify`) are gross: a duplicated square, gap -1, and a
square moved the side and 2 outside the box, which a route with a tolerance of 1e-8
refuses as surely as an exact one. This certificate clears every wall by about 6.0e-13
and every pair by about 1.2e-12, a dilation's margins, so the sharp controls of
`devtools.evand_arrangement_reports` (`SHARP_CONTROLS`, `run_sharp`) are what show that
the maintained routes decide it exactly: the side lowered by the least far-wall
clearance, and the tightest pair closed along the face normal that separates it, each
at exact contact (accepted, margin exactly 0) and `SHARP_EPSILON` = 1e-30 past it
(refused, margin exactly -1e-30). The certificate is the packet's derived fact, admitted
by `devtools.upper_bound_reports.read_facts`.

Usage, from packing/ with the project interpreter:
    python resources/web/amundsk-n303-2026-10-23/replay/sharp_controls.py \
        --out resources/web/amundsk-n303-2026-10-23/replay/sharp-controls.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

from devtools import evand_arrangement_reports as kernel  # noqa: E402
from devtools import upper_bound_reports as reports  # noqa: E402

PACKET = reports.WEB / "amundsk-n303-2026-10-23"
N = 303


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    declaration = reports.load_declaration(PACKET)
    certificate = reports.read_facts(PACKET, {N})[N]
    rows = []
    for control in kernel.SHARP_CONTROLS:
        margin = "wall" if control == "side-lowered-past-wall-contact" else "gap"
        for past in (False, True):
            started = time.process_time()
            verdicts = kernel.run_sharp(
                certificate,
                control,
                past=past,
                witness_prefix=declaration["witness_prefix"],
                claim_limitations=declaration["claim_limitations"],
            )
            expected = -kernel.SHARP_EPSILON if past else 0
            rows.append(
                {
                    "control": control,
                    "where": "past-contact" if past else "at-contact",
                    "margin": margin,
                    "expected_margin": str(expected),
                    "routes": {
                        route: {
                            "passed": verdict["passed"],
                            margin: str(verdict[margin]),
                            "as_expected": verdict["passed"] is not past
                            and verdict[margin] == expected,
                        }
                        for route, verdict in verdicts.items()
                    },
                    "cpu_seconds": round(time.process_time() - started, 2),
                }
            )
    result = {
        "format": "amundsk-755-sharp-controls-v1",
        "n": N,
        "epsilon": str(kernel.SHARP_EPSILON),
        "controls": rows,
        "all_as_expected": all(
            route["as_expected"] for row in rows for route in row["routes"].values()
        ),
    }
    text = json.dumps(result, indent=1) + "\n"
    args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0 if result["all_as_expected"] else 1


if __name__ == "__main__":
    sys.exit(main())
