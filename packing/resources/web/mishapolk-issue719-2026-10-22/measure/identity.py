"""Measure #719's packings at 105 and 204 pose by pose against the record's, for credit.

Written for the stage 3 registration of issue 719's two in-corpus certificates
(think-xyhn). A measurement for credit; it decides nothing. Each #719 packing is read from
this packet's derived fact, admitted by `devtools.upper_bound_reports.read_facts` (custody
held, the fact rebuilt from the digest the packet pins); the packings it is compared with
are read from their own packets:

- T-174 at 105: PingYou Ltd's PR 574 fact (pingyou-pr574-certificates-2026-10-13), the
  house witness's packing;
- T-183 at 105 and 204: Polkovskyi's own issue-593 facts (mishapolk-records-2026-10-14);
- T-225 at 204: Evan Daniel's view of 0075967 (evand-regularized-2026-10-20), the house;
- T-223 at 204: Francisco Couzo's issue-678 certificate (couzo-issue678-2026-10-18);
- T-186 at 204: Polkovskyi's KKT refinement (mishapolk-kkt-refinements-2026-10-14).

The measures are those of the evand-regularized-2026-10-20 packet's measure/identity.py,
loaded from its file unchanged: the nearest centre under each of the box's eight
symmetries, kept only where one to one (`devtools.check_half_angle_area.arrangement_gap`),
and an optimal assignment (least total squared centre displacement under each symmetry,
scipy in binary64): the largest move, the squares moved beyond each bound and the largest
turn. Exact sides and their differences are exact.

Usage, from packing/ with the project interpreter:
    python resources/web/mishapolk-issue719-2026-10-22/measure/identity.py \
        --out resources/web/mishapolk-issue719-2026-10-22/measure/identity.json
"""

from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

from devtools import upper_bound_reports as reports  # noqa: E402
from sqpack.yamlio import load_yaml  # noqa: E402

WEB = reports.WEB
PACKET = WEB / "mishapolk-issue719-2026-10-22"
REGULARIZED = WEB / "evand-regularized-2026-10-20/source/search/regularize/lists/certs"
OWN_593 = WEB / "mishapolk-records-2026-10-14/facts"
MEASURES = WEB / "evand-regularized-2026-10-20/measure/identity.py"


def _measures() -> object:
    spec = importlib.util.spec_from_file_location("evand_regularized_identity", MEASURES)
    if spec is None or spec.loader is None:
        raise SystemExit(f"{MEASURES} is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m = _measures()
area = m.area  # type: ignore[attr-defined]


def fact(packet: Path, n: int) -> tuple[Fraction, list[tuple[Fraction, ...]]]:
    """A packet's admitted derived fact, as the measures read a packing."""
    certificate = reports.read_facts(packet, {n})[n]
    return certificate.side, area.placed([(p.x, p.y, p.t) for p in certificate.poses])


def witness(path: Path) -> tuple[Fraction, list[tuple[Fraction, ...]]]:
    """A retained centre-basis witness, each basis held to the unit circle."""
    document = load_yaml(gzip.decompress(path.read_bytes()).decode("utf-8"))["witness"]
    squares = []
    for square in document["squares"]:
        x, y = (Fraction(str(value)) for value in square["center"])
        c, s = (Fraction(str(value)) for value in square["basis"])
        squares.append((x, y, *area.unit_basis(c, s)))
    return Fraction(str(document["side"])), squares


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    ours = {n: fact(PACKET, n) for n in (105, 204)}
    others = {
        "T-174 (PR 574)": (105, fact(WEB / "pingyou-pr574-certificates-2026-10-13", 105)),
        "T-183 (#593) at 105": (105, witness(OWN_593 / "n-105.yaml.gz")),
        "T-225 (evand 0075967)": (
            204,
            m.certificate(REGULARIZED / "n-204.cert.gz"),  # type: ignore[attr-defined]
        ),
        "T-223 (#678)": (
            204,
            m.certificate(  # type: ignore[attr-defined]
                WEB / "couzo-issue678-2026-10-18/source/certificates/best/n204.cert"
            ),
        ),
        "T-186 (70a033f)": (
            204,
            witness(WEB / "mishapolk-kkt-refinements-2026-10-14/facts/n-204.yaml.gz"),
        ),
        "T-183 (#593) at 204": (204, witness(OWN_593 / "n-204.yaml.gz")),
    }
    pairs = [
        {"n": n, "view": "#719", "against": label, **m.measure(ours[n], packing)}  # type: ignore[attr-defined]
        for label, (n, packing) in others.items()
    ]
    tilted = {
        str(n): sum(1 for _x, _y, _c, s in packing[1] if s != 0) for n, packing in ours.items()
    }
    result = {"format": "mishapolk-719-identity-v1", "tilted_squares": tilted, "pairs": pairs}
    text = json.dumps(result, indent=1) + "\n"
    args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
