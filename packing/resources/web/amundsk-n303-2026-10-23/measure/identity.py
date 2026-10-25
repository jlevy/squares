"""Measure #755's packing at 303 pose by pose against the record's, for credit and lineage.

Written for the stage 1 triage and stage 3 registration of issue 755 (think-tqb5). A
measurement for credit; it decides nothing. #755's packing is read from this packet's
derived fact, admitted by `devtools.upper_bound_reports.read_facts` (custody held to the
digest the packet pins); the packings it is compared with are read from their own
packets:

- T-230: Evan Daniel's #728 certificate (evand-n303-2026-10-22), the house best packing
  at 303, from which the issue says the search started;
- T-186: Mykhailo Polkovskyi's KKT refinement (mishapolk-kkt-refinements-2026-10-14);
- T-174: PingYou Ltd's PR 574 fact (pingyou-pr574-certificates-2026-10-13);
- T-162: Daniil Ostashev's #562 certificate (dostashev-compositions-2026-10-12);
- T-146: Evan Daniel's regularization of Nate Chaoweeraprasit's packing
  (evand-regularized-2026-10-10).

The measures are the #728 packet's measure/identity.py, loaded from its file unchanged:
the evand-regularized-2026-10-20 packet's nearest centre under each of the box's eight
symmetries, kept only where one to one, and optimal assignment (least total squared
centre displacement under each symmetry, scipy in binary64), with that program's tilt
classes and band pairing by the sign of each tilt.

With ``--checkout DIR``, a checkout of the gist at the pin, the binary64 packing the
issue says the certificate was dilated from (``s303_amund.input.txt``) is read too, after
its SHA-256 is held to the digest the packet's manifest pins, and compared with the
certificate: the input side times 1 + delta against the exact side, and each centre and
angle against the dilated input, in exact arithmetic where the inputs are exact.
Without it, the dilation block is left out and the output says so.

Usage, from packing/ with the project interpreter:
    python resources/web/amundsk-n303-2026-10-23/measure/identity.py \
        --checkout GIST_CHECKOUT \
        --out resources/web/amundsk-n303-2026-10-23/measure/identity.json
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

from devtools import upper_bound_reports as reports  # noqa: E402

WEB = reports.WEB
PACKET = WEB / "amundsk-n303-2026-10-23"
PROGRAM = WEB / "evand-n303-2026-10-22/measure/identity.py"
INPUT = "s303_amund.input.txt"
#: The dilation's delta as `dilate_cert.py` reads it: the double nearest 10^-12.
DELTA = Fraction(1e-12)
N = 303


def _program() -> object:
    spec = importlib.util.spec_from_file_location("evand_728_identity", PROGRAM)
    if spec is None or spec.loader is None:
        raise SystemExit(f"{PROGRAM} is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p = _program()


def _pinned_digest(name: str) -> str:
    manifest = PACKET / "acquisition/upstream-subtree.sha256"
    for line in manifest.read_text("utf-8").splitlines():
        digest, path = line.split(maxsplit=1)
        if path in (name, f"./{name}"):
            return digest
    raise SystemExit(f"{name} is not in the manifest")


def dilation(checkout: Path) -> dict[str, object]:
    """The certificate against its binary64 input dilated by 1 + delta."""
    raw = (checkout / INPUT).read_bytes()
    if hashlib.sha256(raw).hexdigest() != _pinned_digest(INPUT):
        raise SystemExit(f"{INPUT}: not the bytes the packet pins")
    lines = raw.decode("ascii").split("\n")
    count, side = lines[0].split()
    rows = [line.split() for line in lines[1:] if line.strip()]
    if int(count) != N or len(rows) != N:
        raise SystemExit(f"{INPUT}: not {N} squares")
    certificate = reports.read_facts(PACKET, {N})[N]
    scale = 1 + DELTA
    input_side = Fraction(Decimal(side))
    centre = max(
        max(
            abs(pose.x - Fraction(Decimal(x)) * scale),
            abs(pose.y - Fraction(Decimal(y)) * scale),
        )
        for pose, (x, y, _a) in zip(certificate.poses, rows, strict=True)
    )
    turn = 0.0
    for pose, (_x, _y, angle) in zip(certificate.poses, rows, strict=True):
        exact = math.degrees(2 * math.atan(float(pose.t)))
        folded = (exact - float(angle) + 45.0) % 90.0 - 45.0
        turn = max(turn, abs(folded))
    side_ceiling_30 = Fraction(math.ceil(input_side * scale * 10**30), 10**30)
    return {
        "input_side": side,
        "input_side_times_1_plus_delta_rounded_up_at_30_places_equals_side": (
            side_ceiling_30 == certificate.side
        ),
        "side_minus_input_side": f"{float(certificate.side - input_side):.6e}",
        "largest_centre_offset_from_dilated_input": f"{float(centre):.3e}",
        "largest_angle_offset_degrees_mod_90": f"{turn:.3e}",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    ours = p.fact(PACKET)  # type: ignore[attr-defined]
    others = {
        "T-230 (#728), the house": p.fact(WEB / "evand-n303-2026-10-22"),  # type: ignore[attr-defined]
        "T-186 (70a033f)": p.witness(  # type: ignore[attr-defined]
            WEB / "mishapolk-kkt-refinements-2026-10-14/facts/n-303.yaml.gz"
        ),
        "T-174 (PR 574)": p.witness(  # type: ignore[attr-defined]
            WEB / "pingyou-pr574-certificates-2026-10-13/facts/n-303.yaml.gz"
        ),
        "T-162 (#562)": p.sqcert(  # type: ignore[attr-defined]
            WEB / "dostashev-compositions-2026-10-12/source/records/n0303.sqcert"
        ),
        "T-146 (ea1a2f2)": p.fact(WEB / "evand-regularized-2026-10-10"),  # type: ignore[attr-defined]
    }
    pairs = [
        {
            "view": "#755",
            "against": label,
            **p.m.measure(ours, packing),  # type: ignore[attr-defined]
            "bands": p.bands(ours, packing),  # type: ignore[attr-defined]
        }
        for label, packing in others.items()
    ]
    result: dict[str, object] = {
        "format": "amundsk-755-identity-v1",
        "tilts": {"#755": p.tilts(ours)}  # type: ignore[attr-defined]
        | {label: p.tilts(packing) for label, packing in others.items()},  # type: ignore[attr-defined]
        "pairs": pairs,
        "dilation": dilation(args.checkout) if args.checkout else "not measured: no --checkout",
    }
    text = json.dumps(result, indent=1, default=str) + "\n"
    args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
