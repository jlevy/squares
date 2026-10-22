"""Run the registered clipping-area route (`devtools.check_half_angle_area`,
V-check-half-angle-area) on the #689 and #694 certificates, with its six controls.

Written for the stage 4 review of 20 October 2026. The driver adds nothing to that
module's tables and changes no decision: it reads each certificate with the module's own
`read_evand_cert`, places the squares with `placed`, and prints `verdict`, which decides
containment by half-extents, far pairs by discs at centre distance sqrt 2, and every
closer pair by the exact area of one square clipped by the other's closed half-planes,
with its least distance and its controls.

Usage, from ``packing/`` with the project interpreter::

    python -I area_route_1020.py --json OUT.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from devtools import check_half_angle_area as area  # noqa: E402

WEB = Path("resources/web")
CERTS = {
    "#689 n308": (WEB / "evand-n308-2026-10-19/source/search/packer/candidates/s308_d308.cert", 308),
    "#694 n154": (WEB / "evand-n154-sweep-2026-10-20/source/search/packer/candidates/s154_sw.cert", 154),
}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    report: dict[str, object] = {}
    bad = 0
    for label, (path, n) in CERTS.items():
        started = time.time()
        side, poses = area.read_evand_cert(path.read_bytes(), n)
        verdict = area.verdict(side, area.placed(poses))
        verdict["seconds"] = round(time.time() - started, 1)
        verdict["side"] = str(side)
        report[label] = verdict
        controls = verdict.get("controls", {})
        ok = verdict.get("passed") is True and all(controls.values()) if isinstance(controls, dict) else False
        if not ok:
            bad += 1
        print(f"{label}: passed={verdict.get('passed')} controls={controls} {verdict['seconds']}s")
        print("   " + json.dumps({k: v for k, v in verdict.items() if k not in {"controls", "placements"}}, default=str)[:900])
    args.json.write_text(json.dumps(report, indent=1, default=str) + "\n", "utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
