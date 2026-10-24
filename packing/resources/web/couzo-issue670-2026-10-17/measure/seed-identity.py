"""Hold Couzo's account of the 204 seed and of his checker call to this record's files.

Written for the record of Francisco Couzo's answers on issue 670 of 2026-10-23T22:22:03Z
(issuecomment-6375905012) and on issue 675 of 22:22:34Z (issuecomment-6375912099),
think-t5hc. A measurement for lineage; it decides nothing. The answer on 670 names the
chain behind the 204 certificate this packet retains: Mykhailo Polkovskyi's
`certificates/square-204.cert` at `Mishapolk/square-packing-records@70a033f` (SHA-256
`f0885fa8…`), its decimal form `n204.txt` at `franciscouzo/square-packing@4e4c8ce`
(`3e7c2456…`), hop jobs 101216, 103222 and 105412, none of whose outputs was published,
then a quarter turn. This program checks the links this record holds:

- **The digests.** Each prefix the comments print against the SHA-256 a packet's
  manifest records: T-186's packet (mishapolk-kkt-refinements-2026-10-14) for
  `certificates/square-204.cert` and `certificates/n204.cert` at 70a033f, the
  couzo-index-2026-10-15 packet for `n204.txt` and `certificates/best/n204.cert` at
  4e4c8ce, and the #670 and #675 packets for the two certificates the answers name.
- **The seed's side.** The comment's printed digits of T-186's exact side, and the side
  `n204.txt` prints against that exact side.
- **The pairing.** `n204.txt`, read by `devtools.upper_bound_reports`' `calle-txt`
  adapter from the couzo-index packet's retained copy (every decimal exactly as
  printed, each `t = tan(theta/2)` rounded down at 40 places), against T-186's 204
  packing, that packet's admitted derived fact, by the measures of the
  evand-regularized-2026-10-20 packet's measure/identity.py, loaded from its file
  unchanged: the nearest centre under each of the box's eight symmetries, kept only
  where one to one, and an optimal assignment.
- **The checker call.** Answer 1 on 670 and the answer on 675: exact rational corners
  built from (x, y, t), passed to this repository's `sqpack.verify.verify_packing(...,
  bucket=True)` with an exact rational sign, in the closed box [0, S]^2. Its report's
  `container_contacts` counts the corner coordinates exactly on the boundary and
  `touching_pairs` the pairs at zero gap.

Usage, from packing/ with the project interpreter, in a few seconds:
    python resources/web/couzo-issue670-2026-10-17/measure/seed-identity.py \
        --out resources/web/couzo-issue670-2026-10-17/measure/seed-identity.json
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

from devtools import upper_bound_reports as reports  # noqa: E402
from sqpack import verify  # noqa: E402

WEB = reports.WEB
N = 204
ISSUE_670 = WEB / "couzo-issue670-2026-10-17"
ISSUE_675 = WEB / "couzo-issue675-2026-10-18"
T186 = WEB / "mishapolk-kkt-refinements-2026-10-14"
INDEX = WEB / "couzo-index-2026-10-15"
SEED = "n204.txt"
INDEX_COMMIT = "4e4c8ce23cb5e87f033021687010992c40575480"
MEASURES = WEB / "evand-regularized-2026-10-20/measure/identity.py"
HALF_ANGLE_PLACES = "40"
#: What the answers print: each file, the packet whose manifest binds it, and the prefix.
PREFIXES = (
    ("70a033f certificates/square-204.cert", T186, "certificates/square-204.cert", "f0885fa8"),
    ("4e4c8ce n204.txt", INDEX, SEED, "3e7c2456"),
    ("#670 certificates/n204.cert", ISSUE_670, "certificates/n204.cert", "f317d0c0"),
    ("#675 certificates/best/n204.cert", ISSUE_675, "certificates/best/n204.cert", "761af9ec"),
)
#: The digits of T-186's exact side that the answer on 670 prints before its ellipsis.
T186_SIDE_PRINT = "14.80866323438695656632"
#: What the answers report of the checker call: corner coordinates on the boundary.
REPORTED_CONTACTS = {"#670": 32, "#675": 88}


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
    rows = []
    for label, packet, path, prefix in PREFIXES:
        recorded = manifest(packet)[path]
        rows.append(
            {
                "file": label,
                "packet": packet.name,
                "path": path,
                "printed_prefix": prefix,
                "recorded_sha256": recorded,
                "matches": recorded.startswith(prefix),
            }
        )
    # The same bytes under the names 70a033f and 4e4c8ce give them.
    t186 = manifest(T186)
    index = manifest(INDEX)
    rows.append(
        {
            "file": "4e4c8ce certificates/best/n204.cert as 70a033f square-204.cert",
            "packet": INDEX.name,
            "path": "certificates/best/n204.cert",
            "recorded_sha256": index["certificates/best/n204.cert"],
            "matches": index["certificates/best/n204.cert"]
            == t186["certificates/square-204.cert"]
            == t186["certificates/n204.cert"],
        }
    )
    return rows


def seed() -> tuple[Fraction, Fraction, list[tuple[Fraction, ...]], str]:
    """The retained n204.txt: its printed side, exact; its packing; its SHA-256."""
    raw = (INDEX / "source" / SEED).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != manifest(INDEX)[SEED]:
        raise SystemExit(f"{SEED} has SHA-256 {digest}, not the manifest's")
    certificate = reports.parse_certificate(
        raw, N, "calle-txt", {reports.HALF_ANGLE_PLACES: HALF_ANGLE_PLACES}
    )
    printed = next(
        Fraction(Decimal(line.split("=", 1)[1].strip()))
        for line in raw.decode("ascii").splitlines()
        if line.startswith("# s =")
    )
    placed = area.placed([(p.x, p.y, p.t) for p in certificate.poses])
    return printed, certificate.side, placed, digest


def fact(packet: Path) -> tuple[Fraction, list[tuple[Fraction, ...]]]:
    """A packet's admitted certificate at 204, as the measures read a packing."""
    certificate = reports.read_facts(packet, {N})[N]
    return certificate.side, area.placed([(p.x, p.y, p.t) for p in certificate.poses])


def _leading_digits(value: Fraction, printed: str) -> bool:
    """Whether ``value`` starts with the decimal digits ``printed``, decided exactly."""
    whole, _, places = printed.partition(".")
    scale = 10 ** len(places)
    return value * scale // 1 == int(whole + places)


def _rational_sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def checker_call(packet: Path) -> dict[str, object]:
    """The author's call: exact corners from (x, y, t), bucketed, in the closed box."""
    certificate = reports.read_facts(packet, {N})[N]
    corners = [pose.corners() for pose in certificate.poses]
    report = verify.verify_packing(corners, certificate.side, _rational_sign, bucket=True)
    return {
        "valid": report.valid,
        "container_contacts": report.container_contacts,
        "touching_pairs": report.touching_pairs,
        "strict_pairs": report.strict_pairs,
        "pairs_tested": report.pairs_tested,
        "failures": len(report.failures),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    printed, read_side, placed, digest = seed()
    t186 = fact(T186)
    exact = t186[0]
    calls = {"#670": checker_call(ISSUE_670), "#675": checker_call(ISSUE_675)}
    for label, call in calls.items():
        call["reported_container_contacts"] = REPORTED_CONTACTS[label]
    result = {
        "format": "couzo-670-seed-identity-v1",
        "comments": {
            "670": "https://github.com/jlevy/squares/issues/670#issuecomment-6375905012",
            "675": "https://github.com/jlevy/squares/issues/675#issuecomment-6375912099",
        },
        "digests": digests(),
        "t186_side": {
            "exact": str(exact),
            "printed_in_comment": T186_SIDE_PRINT,
            "prefix_matches": _leading_digits(exact, T186_SIDE_PRINT),
        },
        "seed": {
            "source": f"franciscouzo/square-packing@{INDEX_COMMIT}:{SEED}",
            "sha256": digest,
            "squares": len(placed),
            "printed_side": str(printed),
            "printed_side_above_t186": f"{float(printed - exact):.6e}",
            "printed_side_above_t186_exact": str(printed - exact),
            "reader": f"upper_bound_reports calle-txt, half_angle_places {HALF_ANGLE_PLACES}",
            "read_side_is_printed": read_side == printed,
        },
        "pairs": [
            {
                "n": N,
                "view": "4e4c8ce n204.txt",
                "against": "T-186 (70a033f square-204.cert)",
                **m.measure((printed, placed), t186),  # type: ignore[attr-defined]
            }
        ],
        "checker_call": calls,
    }
    text = json.dumps(result, indent=1) + "\n"
    args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
