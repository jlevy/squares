"""Hold Couzo's answers of 24 October on issue 672 to this record's files.

Written for the record of Francisco Couzo's comment on issue 672 of 2026-10-24T06:10:57Z
(issuecomment-6380747582), think-mdfr. A measurement for lineage; it decides nothing. The
comment answers the two questions of the 22 October review. Answer 1 says Couzo made the
CT105 web submission behind the 227 certificate himself, and that the task was seeded from
the source's retained 227 witness `cdd08485…`, "which is de Winter's #668 certificate".
Answer 2 says how the source calls this repository's `sqpack/verify.py`. This program
checks the links this record holds:

- **The digests.** Each prefix the comment prints against the SHA-256 this packet's
  manifest records: the seed `certificates/parents/cdd08485….cert`, retained from the
  pin since 24 October, and the 227 and 229 certificates.
- **The seed.** Its exact side, read by `devtools.upper_bound_reports`' `evand-cert`
  adapter, against T-196's 227 side (Joost de Winter's #668 certificate, the
  de-winter-upper-bounds-227-229-260-2026-10-17 packet's admitted fact), against the side
  `certificates/n227.json` records for Evan Daniel's `alt/n-227.cert.gz`, and against
  #672's 227 certificate; and whether its bytes are de Winter's certificate, by the SHA-256
  the de Winter packet's manifest records for `n227/n227_record.cert`.
- **The pairings.** The seed against T-196's packing, #672's 227 against the seed, and
  #672's 227 against T-196's packing, so the three sit together, by the measures of the
  evand-regularized-2026-10-20 packet's measure/identity.py, loaded from its file
  unchanged: the nearest centre under each of the box's eight symmetries, kept only where
  one to one, and an optimal assignment.
- **The checker call.** Answer 2: exact rational corners built from (x, y, t), passed to
  this repository's `sqpack.verify.verify_packing(..., bucket=True)` with an exact
  rational sign, in the closed box [0, S]^2. Its report's `container_contacts` counts the
  corner coordinates exactly on the boundary and `touching_pairs` the pairs at zero gap;
  the comment reports 58 and none at 229, and a strict verdict of true at 227, which needs
  neither.

Usage, from packing/ with the project interpreter, in a few seconds:
    python resources/web/couzo-issue672-2026-10-17/measure/answers-2026-10-24.py \
        --out resources/web/couzo-issue672-2026-10-17/measure/answers-2026-10-24.json
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

from devtools import upper_bound_reports as reports  # noqa: E402
from sqpack import verify  # noqa: E402

WEB = reports.WEB
N = 227
ISSUE_672 = WEB / "couzo-issue672-2026-10-17"
T196 = WEB / "de-winter-upper-bounds-227-229-260-2026-10-17"
SEED = (
    "certificates/parents/cdd08485c2b7e97c59cae33f8a70923bf8eb95c878f0f998640b88c0eae1bcc0.cert"
)
MEASURES = WEB / "evand-regularized-2026-10-20/measure/identity.py"
#: What the comment prints: each file and the prefix of its SHA-256.
PREFIXES = (
    ("the retained 227 witness", SEED, "cdd08485"),
    ("#672 certificates/n227.cert", "certificates/n227.cert", "65b03df8"),
    ("#672 certificates/n229.cert", "certificates/n229.cert", "9ab667ec"),
)
#: What the comment reports of the checker call at each count.
REPORTED = {
    227: {"strict_verdict": True},
    229: {"strict_verdict": False, "container_contacts": 58, "touching_pairs": 0},
}


def _measures() -> object:
    spec = importlib.util.spec_from_file_location("evand_regularized_identity", MEASURES)
    if spec is None or spec.loader is None:
        raise SystemExit(f"{MEASURES} is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


m = _measures()
area = m.area  # type: ignore[attr-defined]


def manifest(packet: Path) -> dict[str, str]:
    """A packet's upstream manifest: each path's SHA-256."""
    lines = (packet / "acquisition/upstream-subtree.sha256").read_text(encoding="utf-8")
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split("  ", 1) for line in lines.splitlines())
    }


def digests() -> list[dict[str, object]]:
    recorded = manifest(ISSUE_672)
    return [
        {
            "file": label,
            "packet": ISSUE_672.name,
            "path": path,
            "printed_prefix": prefix,
            "recorded_sha256": recorded[path],
            "matches": recorded[path].startswith(prefix),
        }
        for label, path, prefix in PREFIXES
    ]


def _placed(certificate: object) -> list[tuple[Fraction, ...]]:
    return area.placed([(p.x, p.y, p.t) for p in certificate.poses])  # type: ignore[attr-defined]


def seed() -> tuple[Fraction, list[tuple[Fraction, ...]], str]:
    """The retained seed: its exact side, its packing and its SHA-256."""
    raw = (ISSUE_672 / "source" / SEED).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != manifest(ISSUE_672)[SEED]:
        raise SystemExit(f"{SEED} has SHA-256 {digest}, not the manifest's")
    certificate = reports.parse_certificate(raw, N, "evand-cert")
    return certificate.side, _placed(certificate), digest


def fact(packet: Path, n: int) -> tuple[Fraction, list[tuple[Fraction, ...]]]:
    """A packet's admitted certificate at n, as the measures read a packing."""
    certificate = reports.read_facts(packet, {n})[n]
    return certificate.side, _placed(certificate)


def daniel_alt_side() -> Fraction:
    """The side certificates/n227.json records for Daniel's alt/n-227.cert.gz."""
    record = json.loads((ISSUE_672 / "source/certificates/n227.json").read_text("utf-8"))
    witness = record["origin"]["web_seed"]["prior_retained_witness"]
    return Fraction(witness["source_credit"]["seed_certificate"]["side"])


def _gap(a: Fraction, b: Fraction) -> dict[str, str]:
    return {"float": f"{float(a - b):.6e}", "exact": str(a - b)}


def _rational_sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def checker_call(n: int) -> dict[str, object]:
    """The author's call: exact corners from (x, y, t), bucketed, in the closed box."""
    certificate = reports.read_facts(ISSUE_672, {n})[n]
    corners = [pose.corners() for pose in certificate.poses]
    report = verify.verify_packing(corners, certificate.side, _rational_sign, bucket=True)
    return {
        "valid": report.valid,
        "container_contacts": report.container_contacts,
        "touching_pairs": report.touching_pairs,
        "strict_pairs": report.strict_pairs,
        "pairs_tested": report.pairs_tested,
        "failures": len(report.failures),
        "reported": REPORTED[n],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    side, placed, digest = seed()
    t196 = fact(T196, N)
    issue = fact(ISSUE_672, N)
    alt = daniel_alt_side()
    de_winter_sha256 = manifest(T196)["n227/n227_record.cert"]
    result = {
        "format": "couzo-672-answers-v1",
        "comment": "https://github.com/jlevy/squares/issues/672#issuecomment-6380747582",
        "digests": digests(),
        "seed": {
            "source": f"franciscouzo/square-packing@af8cb79:{SEED}",
            "sha256": digest,
            "squares": len(placed),
            "exact_side": str(side),
            "is_de_winter_certificate": digest == de_winter_sha256,
            "de_winter_certificate_sha256": de_winter_sha256,
            "below_t196": _gap(t196[0], side),
            "below_daniel_alt": _gap(alt, side),
            "above_issue_672": _gap(side, issue[0]),
        },
        "pairs": [
            {
                "n": N,
                "view": "the seed (af8cb79 cdd08485)",
                "against": "T-196 (de Winter's #668 n227_record.cert)",
                **m.measure((side, placed), t196),  # type: ignore[attr-defined]
            },
            {
                "n": N,
                "view": "#672 certificates/n227.cert (T-227)",
                "against": "the seed (af8cb79 cdd08485)",
                **m.measure(issue, (side, placed)),  # type: ignore[attr-defined]
            },
            {
                "n": N,
                "view": "#672 certificates/n227.cert (T-227)",
                "against": "T-196 (de Winter's #668 n227_record.cert)",
                **m.measure(issue, t196),  # type: ignore[attr-defined]
            },
        ],
        "checker_call": {str(n): checker_call(n) for n in (227, 229)},
    }
    text = json.dumps(result, indent=1) + "\n"
    args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
