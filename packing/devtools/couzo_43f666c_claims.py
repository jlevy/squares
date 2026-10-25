"""Re-derive the claims of Francisco Couzo's 43f666c from the indexes its packet retains
(think-gn29).

franciscouzo/square-packing's commit 43f666c ("Land the 24 October per-puzzle board and the
live records since 964ee2b", committed 2026-10-24T00:55:44Z) was pushed with 73eac5b and
1c17153 at 2026-10-24T06:10:44Z, as GitHub's activity log records it. No issue or comment
reports it, so by the owner's rule of 14 October 2026 each certificate it publishes is a
report from its first commit, dated by the push that made that commit public
(`devtools.beyond_horizon_replay.PUSHED_LATER`), and an import of its own (result-import.md,
stage 1). The ``couzo-43f666c-2026-10-24`` packet pins the head 1c17153, whose indexes the
two later commits leave unchanged at every bound, and retains ``certified_bounds.json`` and
``certificates/best/manifest.json`` there.

**The rule.** A claim is a count whose certified entry at the pin, a certificate or a
construction, states a bound strictly below the one ``certified_bounds.json`` states at
964ee2b, the pin of issue #763, as the ``couzo-issue763-2026-10-23`` packet retains it: the
live records since #763's pin, which is how the commit's subject names them. Each is
decided exactly, as a rational. The receipt, ``receipts/claim-map.json`` in the packet,
lists them as ``lowered``, each with its kind (a certificate, a deletion, which reads a
larger count's certificate less its last squares, or a square tiling and L-border recipe of
a certificate), its certificate path and SHA-256 as the index states them, its exact bound
and 12-place print, the recipe of a construction, its credit and the packing the credit
says it refines (``refines``), the seed credit and ``previous_source`` the manifest states
for a certificate at its own count, and 964ee2b's entry with the margin below it.

Read on 24 October 2026 the derivation gives the stage 1 triage's counts (think-cncq;
`CONTROLS`): 957 counts lowered, 126 from 325 to 1024 (108 own-count certificates, 690 as
691's certificate less its last square, and 17 recipes) and 831 above 1024, every one a
recipe; every one is credited to Couzo, 125 as refinements of packings the credit names
(`REFINES_CONTROLS`). Whether each is recorded is the report-order walk's
(``campaign/issue-intake/upper-bounds-couzo-43f666c-20261024``), which takes its starts from
the record on ``main`` after #795. It runs no code of the source and decides nothing about
the packings.

From ``packing/``, with the project interpreter::

    python -m devtools.couzo_43f666c_claims derive [--write]
    python -m devtools.couzo_43f666c_claims check
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import acquire_source
from devtools import couzo_763_claims as claims_763
from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_text
from sqpack.retained_json import dumps as retained_dumps

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/couzo-43f666c-2026-10-24"
ARCHIVE = PACKET / "source"
RECEIPT = PACKET / "receipts/claim-map.json"
FORMAT = "couzo-43f666c-claim-map-v1"
SOURCE = "https://github.com/franciscouzo/square-packing"
#: The commit the packet pins, the head of the push of 06:10:44Z.
PIN = "1c1715399709bc955e9b402947ab8b52bbacdfc3"
#: The commit that first states every claim; 73eac5b and 1c17153 change no bound.
COMMIT = "43f666c23933fbc5cc418fa4e851218268fed0ed"
#: The index the claims are lowered from: #763's pin, retained in its packet.
PREVIOUS_COMMIT = claims_763.PIN
PREVIOUS = claims_763.ARCHIVE / claims_763.CERTIFIED
CERTIFIED = "certified_bounds.json"
MANIFEST = "certificates/best/manifest.json"
HORIZON, LIMIT, PLACES = claims_763.HORIZON, claims_763.LIMIT, claims_763.PLACES
#: The stage 1 triage's counts (think-cncq), which the derivation must reproduce.
CONTROLS: dict[str, Any] = {
    "rows": 957,
    "at_or_below_limit": 126,
    "above_limit": 831,
    "certificates": 108,
    "deletions": [690],
    "constructions": [
        367,
        444,
        487,
        632,
        683,
        732,
        733,
        737,
        744,
        787,
        788,
        792,
        800,
        844,
        845,
        903,
        964,
    ],
    "constructions_above_limit": 831,
}
#: The packings the credits of the 126 at or below 1024 say they refine, by how the credit
#: names each, with how many (the triage's credit lines; one is Couzo's own).
REFINES_CONTROLS: dict[str, int] = {
    'Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11': 76,
    'Kirill Tymchishin (kirilltym), Kaggle "CPU Alternating Reclosure" v3': 40,
    'kyleluecke, Kaggle notebook "inos-v0-6-k-mosh-squares-in-squares-22-366222" '
    "run 361592092": 3,
    'Kirill Tymchishin (kirilltym), Kaggle notebook "22-3662-cpu-cuda-mps-eda-union" '
    "run 361576574": 2,
    'alexchilton, Kaggle notebook "fault-line-dp-basin-hopping-lb-22-3747" run 361412241': 2,
    'aqibrazadev, Kaggle notebook "squares-in-squares-top-lb-blending-visualization" '
    "run 361516058": 1,
    "Mykhailo Polkovskyi (Mishapolk)": 1,
    "own": 1,
}
_REFINES = re.compile(r"refines the packing of ([^;]+)")


class ClaimError(ValueError):
    """Refuse an index entry or a receipt that does not hold."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ClaimError(message)


def read_indexes(
    archive: Path = ARCHIVE,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """The certified index at the pin, its manifest's witnesses, and the certified index at
    964ee2b, each read from its packet's retained copy, which ``acquire_source --check``
    binds to its pin."""
    if archive == ARCHIVE:
        for packet in (PACKET, claims_763.PACKET):
            problems = acquire_source.check(packet, REPO)
            _require(not problems, f"{packet.name} custody: " + "; ".join(problems))
    certified = json.loads(read_retained_text(archive / CERTIFIED))["entries"]
    witnesses = json.loads(read_retained_text(archive / MANIFEST))["witnesses"]
    previous = json.loads(read_retained_text(PREVIOUS))["entries"]
    return certified, witnesses, previous


def refines(credit: str) -> str | None:
    """The packing a credit says it refines, as the credit names it, or None."""
    match = _REFINES.search(credit)
    return None if match is None else match[1].strip()


def seed_of(entry: Mapping[str, Any], witnesses: Mapping[str, Any]) -> dict[str, Any]:
    """What the manifest states of a certificate's start at its own count: the seed credit
    and the side it replaced (``previous_source``), where the witness at the count names
    the entry's certificate; nothing for a recipe or a deletion, whose own count's witness
    is another certificate's."""
    witness = witnesses.get(str(entry["n"]))
    if not isinstance(witness, Mapping) or witness.get("certificate") != entry["certificate"]:
        return {}
    _require(
        witness.get("certificate_sha256") == entry["certificate_sha256"],
        f"{entry['n']}: the manifest's witness names another digest",
    )
    provenance = witness.get("provenance") or {}
    stated = provenance.get("source_provenance") or {}
    found: dict[str, Any] = {}
    if stated.get("seed_credit"):
        found["seed_credit"] = stated["seed_credit"]
    previous = provenance.get("previous_source")
    if isinstance(previous, Mapping):
        found["previous_source"] = {
            key: previous[key]
            for key in ("certificate", "certificate_sha256", "bound", "credit")
            if key in previous
        }
    return found


def row(
    n: int, entry: Mapping[str, Any], before: Mapping[str, Any], witnesses: Mapping[str, Any]
) -> dict[str, Any]:
    """One lowered count as the receipt keeps it."""
    side = Fraction(str(entry["bound"]))
    was = Fraction(str(before["bound"]))
    found: dict[str, Any] = {
        "n": n,
        "kind": claims_763.kind_of(entry),
        "certificate": entry["certificate"],
        "certificate_sha256": entry["certificate_sha256"],
        "source_n": int(entry["source_n"]),
        "deleted_squares": int(entry["deleted_squares"]),
        "exact": legacy.literal(side),
        "ceiling_12": legacy.ceiling_decimal(side, PLACES),
        "index_print": entry.get("rounded_up", ""),
        "credit": entry["credit"],
        "refines": refines(str(entry["credit"])),
        "previous": {
            "commit": PREVIOUS_COMMIT,
            "kind": claims_763.kind_of(before),
            "bound": legacy.literal(was),
            "ceiling_12": legacy.ceiling_decimal(was, PLACES),
            "credit": before.get("credit", ""),
        },
        "margin": claims_763.Bound(was).minus(side),
    }
    if "construction" in entry:
        recipe = entry["construction"]
        found["construction"] = {
            key: recipe[key]
            for key in ("kind", "source_n", "tiles_per_side", "layers", "capacity")
        }
    found |= seed_of(entry, witnesses)
    return found


def claim_map(
    certified: Mapping[str, Any], witnesses: Mapping[str, Any], previous: Mapping[str, Any]
) -> dict[str, Any]:
    """Every count whose certified bound is lowered below 964ee2b's (the module's rule)."""
    lowered: list[dict[str, Any]] = []
    for key in sorted(certified, key=int):
        entry, n = certified[key], int(key)
        if n <= HORIZON or entry.get("kind") not in ("certificate", "construction"):
            continue
        before = previous.get(key)
        _require(isinstance(before, Mapping), f"{key}: no entry at 964ee2b")
        assert isinstance(before, Mapping)
        if not Fraction(str(entry["bound"])) < Fraction(str(before["bound"])):
            continue
        _require(int(entry["n"]) == n, f"{key}: the entry names n={entry['n']}")
        _require(
            claims_763.is_own(str(entry["credit"])),
            f"{key}: a lowered bound not credited to Couzo",
        )
        lowered.append(row(n, entry, before, witnesses))
    return {
        "format": FORMAT,
        "publication": f"{SOURCE}/tree/{COMMIT}",
        "source_commit": PIN,
        "commit": COMMIT,
        "previous_commit": PREVIOUS_COMMIT,
        "indexes": [CERTIFIED, MANIFEST],
        "previous_index": PREVIOUS.relative_to(REPO).as_posix() + ".gz",
        "program": "packing/devtools/couzo_43f666c_claims.py",
        "summary": summary(lowered),
        "lowered": lowered,
    }


def summary(lowered: list[dict[str, Any]]) -> dict[str, Any]:
    """The counts the triage states (`CONTROLS`) and the packings the credits name."""
    inside = [item for item in lowered if item["n"] <= LIMIT]
    return {
        "rows": len(lowered),
        "at_or_below_limit": len(inside),
        "above_limit": len(lowered) - len(inside),
        "certificates": sum(1 for item in inside if item["kind"] == "certificate"),
        "deletions": [item["n"] for item in inside if item["kind"] == "deletion"],
        "constructions": [item["n"] for item in inside if item["kind"] == "construction"],
        "constructions_above_limit": sum(
            1 for item in lowered if item["n"] > LIMIT and item["kind"] == "construction"
        ),
        "refines": dict(sorted(Counter(item["refines"] or "own" for item in inside).items())),
        "distinct_parents_above_limit": sorted(
            {item["construction"]["source_n"] for item in lowered if item["n"] > LIMIT}
        ),
    }


def control_problems(record: Mapping[str, Any]) -> list[str]:
    """Where the derivation does not give the triage's counts."""
    found = record["summary"]
    problems = [
        f"the derivation gives {key} = {found[key]}, the triage {value}"
        for key, value in CONTROLS.items()
        if found[key] != value
    ]
    if found["refines"] != dict(sorted(REFINES_CONTROLS.items())):
        problems.append(f"the credits name {found['refines']}, not the triage's")
    return problems


def derive(archive: Path = ARCHIVE) -> dict[str, Any]:
    """The claim map from the retained indexes, refused unless it gives the triage's
    counts."""
    record = claim_map(*read_indexes(archive))
    problems = control_problems(record)
    _require(not problems, "; ".join(problems))
    return record


def check() -> list[str]:
    """Problems with the receipt; empty when a fresh derivation gives it exactly."""
    try:
        fresh = derive()
    except ClaimError as error:
        return [str(error)]
    if not RECEIPT.is_file():
        return [f"{RECEIPT.relative_to(REPO)}: missing"]
    kept = json.loads(RECEIPT.read_text(encoding="utf-8"))
    return [] if kept == fresh else [f"{RECEIPT.relative_to(REPO)}: differs from its rebuild"]


def write(record: Mapping[str, Any]) -> None:
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(RECEIPT) as temporary:
        Path(temporary).write_text(retained_dumps(record, sort_keys=True), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("derive")
    run.add_argument("--write", action="store_true")
    commands.add_parser("check")
    args = parser.parse_args(argv)
    if args.command == "check":
        problems = check()
        for problem in problems:
            print(problem)
        print("FAILED" if problems else "OK: the claim map is a fresh derivation")
        return 1 if problems else 0
    record = derive()
    if args.write:
        write(record)
    print(json.dumps(record["summary"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
