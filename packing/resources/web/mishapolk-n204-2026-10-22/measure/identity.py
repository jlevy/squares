"""Measure the lower 204 certificate pose by pose against the record's packings, for credit.

Written for the registration of the release's second 204 file, `certificates/n204.cert`
at 12fc466, which the author claimed on issue 719 (think-h01y). A measurement for credit;
it decides nothing. The certificate is read from this packet's retained file, admitted
by `devtools.upper_bound_reports.read_facts` (custody held to the digest the packet
pins); the packings it is compared with are read from their own packets:

- T-229 at 204: the release's `certificates/n-204.cert`, the case's house best packing
  since 23 October 2026, from the mishapolk-issue719-2026-10-22 packet's derived fact;
- T-223 at 204: Francisco Couzo's issue-678 certificate (couzo-issue678-2026-10-18),
  which the author's comment of 23 October names as the start of his solve;
- T-225 at 204: Evan Daniel's regularized view at 0075967 (evand-regularized-2026-10-20),
  the house from 22 to 23 October 2026.

The measures are those of the evand-regularized-2026-10-20 packet's measure/identity.py,
loaded from its file unchanged, as the #719 packet's measure/identity.py loads them: the
nearest centre under each of the box's eight symmetries, kept only where one to one
(`devtools.check_half_angle_area.arrangement_gap`), and an optimal assignment (least total
squared centre displacement under each symmetry, scipy in binary64): the largest move,
the squares moved beyond each bound and the largest turn. Exact sides and their
differences are exact.

Usage, from packing/ with the project interpreter:
    python resources/web/mishapolk-n204-2026-10-22/measure/identity.py \
        --out resources/web/mishapolk-n204-2026-10-22/measure/identity.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

from devtools import upper_bound_reports as reports  # noqa: E402

WEB = reports.WEB
PACKET = WEB / "mishapolk-n204-2026-10-22"
RELEASE = WEB / "mishapolk-issue719-2026-10-22"
REGULARIZED = WEB / "evand-regularized-2026-10-20/source/search/regularize/lists/certs"
COUZO_678 = WEB / "couzo-issue678-2026-10-18/source/certificates/best/n204.cert"
MEASURES = WEB / "evand-regularized-2026-10-20/measure/identity.py"
N = 204


def _measures() -> object:
    spec = importlib.util.spec_from_file_location("evand_regularized_identity", MEASURES)
    if spec is None or spec.loader is None:
        raise SystemExit(f"{MEASURES} is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m = _measures()
area = m.area  # type: ignore[attr-defined]


def fact(packet: Path) -> tuple[Fraction, list[tuple[Fraction, ...]]]:
    """A packet's admitted certificate at 204, as the measures read a packing."""
    certificate = reports.read_facts(packet, {N})[N]
    return certificate.side, area.placed([(p.x, p.y, p.t) for p in certificate.poses])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    ours = fact(PACKET)
    others = {
        "T-229 (#719 n-204.cert)": fact(RELEASE),
        "T-223 (#678)": m.certificate(COUZO_678),  # type: ignore[attr-defined]
        "T-225 (evand 0075967)": m.certificate(REGULARIZED / "n-204.cert.gz"),  # type: ignore[attr-defined]
    }
    pairs = [
        {"n": N, "view": "#719 n204.cert", "against": label, **m.measure(ours, packing)}  # type: ignore[attr-defined]
        for label, packing in others.items()
    ]
    tilted = sum(1 for _x, _y, _c, s in ours[1] if s != 0)
    result = {
        "format": "mishapolk-n204-identity-v1",
        "tilted_squares": {str(N): tilted},
        "pairs": pairs,
    }
    text = json.dumps(result, indent=1) + "\n"
    args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
