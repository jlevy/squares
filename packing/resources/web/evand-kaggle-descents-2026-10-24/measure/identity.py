"""Measure think-l49q's certificates pose by pose against the packings their credit names.

Written for the stage 3 registration of Evan Daniel's exact descents at 268 and 304
(evand/square-packing@8a8879a, this packet) and Francisco Couzo's 304 at
franciscouzo/square-packing@fa6237e (the couzo-n304-2026-10-23 packet). A measurement
for credit; it decides nothing. Each certificate is read by
`devtools.upper_bound_reports.read_facts` from its own packet, custody held to the digest
the packet pins, and the packings it is compared with from theirs:

- T-240 at 268 and 303: Couzo's issue-763 certificates, and the two Kaggle parents its
  manifest names, `certificates/parents/85dbd707…` at 268 (Kirill Tymchishin's
  "CPU/GPU/MPS EDA+Seam LP" v4) and `22f07a7c…` at 303 (Couzo's Kaggle push), read
  from the couzo-issue763-2026-10-23 packet;
- T-174 at 268 (PingYou Ltd's PR 574 fact) and T-186 at 304 (Mykhailo Polkovskyi's KKT
  refinement fact), the case houses, from their packets;
- the source's own binary64 files beside each certificate: `sNNN_*.input.txt`, the
  public packing it descends from, and at 268 `s268_lightning.predescent.txt`, each a
  header `n side` and one `x y degrees` row per square, read as exact binary64 values
  with the half-angle tangent of each angle in binary64; and at 268 the regularized
  display view `s268_lightning_regularized.cert`.

The measures are those of the evand-regularized-2026-10-20 packet's measure/identity.py,
loaded from its file unchanged, as the 204 and 303 packets' programs load them: the
nearest centre under each of the box's eight symmetries, kept only where one to one
(`devtools.check_half_angle_area.arrangement_gap`), and an optimal assignment (least total
squared centre displacement under each symmetry, scipy in binary64): the largest move, the
squares moved beyond each bound and the largest turn. Exact sides and their differences
are exact; a binary64 side is exact as the double it reads.

Usage, from packing/ with the project interpreter:
    python resources/web/evand-kaggle-descents-2026-10-24/measure/identity.py \
        --out resources/web/evand-kaggle-descents-2026-10-24/measure/identity.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

from devtools import check_half_angle_area as area  # noqa: E402
from devtools import evand_exact_certificates as ev  # noqa: E402
from devtools import upper_bound_reports as reports  # noqa: E402

THIS = reports.packet_path("evand-kaggle-descents-2026-10-24")
COUZO_304 = reports.packet_path("couzo-n304-2026-10-23")
COUZO_763 = reports.packet_path("couzo-issue763-2026-10-23")
PINGYOU_574 = reports.packet_path("pingyou-pr574-certificates-2026-10-13")
MISHAPOLK_KKT = reports.packet_path("mishapolk-kkt-refinements-2026-10-14")
CANDIDATES = THIS / "source/search/packer/candidates"
PARENTS = COUZO_763 / "source/certificates/parents"
PARENT_268 = "85dbd707746197d31f62dd52b4e580dfb90097498a4970c577f776ce7de2df46.cert"
PARENT_303 = "22f07a7c318328d257d1a7efd9c5acb05e3286650a94da751592b21014424244.cert"
PARENT_268_LABEL = "#763 268 parent (85dbd707, Tymchishin's EDA+Seam LP v4)"
MEASURES = reports.WEB / "evand-regularized-2026-10-20/measure/identity.py"
Placed = tuple[Fraction, Fraction, Fraction, Fraction]
Packing = tuple[Fraction, list[Placed]]


def _measures() -> ModuleType:
    spec = importlib.util.spec_from_file_location("evand_regularized_identity", MEASURES)
    if spec is None or spec.loader is None:
        raise SystemExit(f"{MEASURES} is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def imported(packet: Path, n: int) -> Packing:
    """One packet's admitted certificate at ``n``, as exact poses."""
    certificate = reports.read_facts(packet, {n})[n]
    return certificate.side, area.placed([(p.x, p.y, p.t) for p in certificate.poses])


def certificate(path: Path) -> Packing:
    cert = ev.parse(path.read_text(encoding="ascii"))
    return cert.side, area.placed([(p.x, p.y, p.t) for p in cert.poses])


def binary64(path: Path, n: int) -> Packing:
    """A header ``n side`` and ``x y degrees`` rows, each value the double it prints."""
    rows = [line.split() for line in path.read_text(encoding="ascii").splitlines() if line]
    head, body = rows[0], rows[1:]
    if int(head[0]) != n or len(body) != n or any(len(row) != 3 for row in body):
        raise SystemExit(f"{path}: not {n} rows of x y degrees")
    poses = []
    for x, y, degrees in body:
        t = math.tan(math.radians(float(degrees)) / 2)
        poses.append((Fraction(float(x)), Fraction(float(y)), Fraction(t)))
    return Fraction(float(head[1])), area.placed(poses)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    m = _measures()
    d268, d268_input = (
        "Daniel 268 (s268_lightning.cert)",
        "Daniel 268 input (s268_lightning.input.txt)",
    )
    d268_pre = "Daniel 268 predescent (s268_lightning.predescent.txt)"
    d268_view = "Daniel 268 regularized view (s268_lightning_regularized.cert)"
    t240_268, parent_268 = "T-240 268 (#763 n268.cert)", PARENT_268_LABEL
    d303, t240_303 = "Daniel 303 (s303_cdeotte.cert)", "T-240 303 (#763 n303.cert)"
    parent_303 = "#763 303 parent (22f07a7c, Couzo's Kaggle push)"
    d304, d304_input = "Daniel 304 (s304_pub.cert)", "Daniel 304 input (s304_pub.input.txt)"
    c304, t186 = "Couzo 304 (fa6237e certificates/best/n304.cert)", "T-186 304 (house)"
    packings: dict[str, Packing] = {
        d268: imported(THIS, 268),
        d268_input: binary64(CANDIDATES / "s268_lightning.input.txt", 268),
        d268_pre: binary64(CANDIDATES / "s268_lightning.predescent.txt", 268),
        d268_view: certificate(CANDIDATES / "s268_lightning_regularized.cert"),
        t240_268: imported(COUZO_763, 268),
        parent_268: certificate(PARENTS / PARENT_268),
        "T-174 268 (house)": imported(PINGYOU_574, 268),
        d303: imported(THIS, 303),
        t240_303: imported(COUZO_763, 303),
        parent_303: certificate(PARENTS / PARENT_303),
        d304: imported(THIS, 304),
        d304_input: binary64(CANDIDATES / "s304_pub.input.txt", 304),
        c304: imported(COUZO_304, 304),
        t186: imported(MISHAPOLK_KKT, 304),
    }
    pairs = [
        (d268, t240_268),
        (d268, d268_input),
        (d268, parent_268),
        (d268_pre, parent_268),
        (d268, d268_view),
        (d268, "T-174 268 (house)"),
        (d303, t240_303),
        (d303, parent_303),
        (d304, c304),
        (d304_input, c304),
        (d304, d304_input),
        (c304, t186),
        (d304, t186),
    ]
    rows = []
    for first, second in pairs:
        found = m.measure(packings[first], packings[second])
        rows.append({"first": first, "second": second, **found})
        sys.stdout.write(json.dumps({"first": first, "second": second}) + "\n")
        sys.stdout.flush()
    result = {
        "format": "think-l49q-identity-v1",
        "measures": MEASURES.relative_to(reports.ROOT).as_posix(),
        "pairs": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
