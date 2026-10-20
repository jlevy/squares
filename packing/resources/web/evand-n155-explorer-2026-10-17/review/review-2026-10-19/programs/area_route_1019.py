"""Decide the five certificates on `devtools.check_half_angle_area` too (19 October review).

A driver written for this review. `devtools.check_half_angle_area` is this repository's
registered third route (V-check-half-angle-area): unit circle, containment by each
square's half-extent, then pairs by the circumscribed-disc rule, else by the exact area
of one square clipped by the other's closed half-planes. Its tables name none of these
five packets, so this driver adds nothing to them and calls only its per-certificate
functions: `parse_certificate` on the retained bytes, then `verdict`, which decides the
certificate, measures its least wall clearance and least Euclidean distance, and runs
the route's six controls. Each packet is first admitted by
`upper_bound_reports.read_facts`, which holds every retained file to its manifest.

Usage, from ``packing/`` with the project interpreter::

    python -I area_route_1019.py --json OUT.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from devtools import check_half_angle_area as area  # noqa: E402
from devtools import upper_bound_reports as upper  # noqa: E402

WEB = Path.cwd() / "resources/web"
CERTIFICATES = (
    ("#669 n155", "evand-n155-explorer-2026-10-17", 155, "search/packer/candidates/s155_ex2.cert"),
    ("#674 n229 opening", "evand-n229-dilation-2026-10-17", 229, "search/packer/candidates/s229.cert"),
    ("#674 n229 update", "evand-n229-dilation-update-2026-10-18", 229, "search/packer/candidates/s229_v2.cert"),
    ("#659 n236", "evand-n236-2026-10-16", 236, "search/packer/candidates/s236_bm3c.cert"),
    ("#664 n271", "evand-n271-2026-10-17", 271, "search/packer/candidates/s271_ex1.cert"),
)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    report: dict[str, object] = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    bad = []
    for key, packet, n, path in CERTIFICATES:
        upper.read_facts(WEB / packet)
        text = (WEB / packet / "source" / path).read_text(encoding="utf-8")
        side, poses = area.parse_certificate(text, n)
        found = area.verdict(side, area.placed(poses))
        report[key] = found
        controls = found["controls"]
        ok = found["passed"] and all(controls.values())
        if not ok:
            bad.append(key)
        print(
            f"{key}: passed={found['passed']} pairs={found['pairs']} clipped={found['clipped_pairs']} "
            f"wall={float(area.literal(found['wall_clearance'])):.4e} distance={found['least_distance']} "
            f"controls={sum(controls.values())}/{len(controls)} {found['wall_seconds']} s",
            flush=True,
        )
    report["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    report["refused_or_control_failed"] = bad
    args.json.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
