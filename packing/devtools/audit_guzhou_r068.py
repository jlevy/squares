"""Audit Guzhou0806's R067 and R068 lower bounds for s(17) against Overbeck's 4.66001.

Two releases of github.com/Guzhou0806/n17-square-packing continue Overbeck's public
``466001/100000`` certificate (SHA-256 ``280af3d4…e6e5``): R067 at ``d4e2c287`` claims
``s(17) > 233009/50000`` and R068 at ``815b1626`` claims ``s(17) > 116511/25000``. Both
packages are retained byte-identical in ``resources/web/n17-guzhou-r068-2026-09-28/``,
their large files as deterministic gzip, and read here through `read_retained_bytes`.

``structure`` measures what a release's certificate changes relative to the 4.66001 one:
the parent side and target, every edited or appended point orbit with its ``D4`` images,
site indices, rule references and budget contribution, whether the rule orbits are
unchanged, the budget difference those edits account for, and how the new angle chain
refines the 2,168 original intervals.

``compare`` reads a paired replay's partition records (``cpp-i.json`` and ``node-i.json``,
plain or gzip) and the published ones, checks each partition's identity and range,
reduces every ledger to ``(interval, minimum_units, cells)`` and compares all of them
row by row. It gives two digests of each reduced ledger, both ``json.dumps`` with compact
separators: of the list of objects, the form the 4.66001 packet's receipts used, and of
the list of ``[interval, minimum, cells]`` triples, the form the R067/R068 review used.
It also reports the C++ records' header counts, which every partition must share.

Neither mode decides the certificate. The exact sweep is the source's own two checkers,
run by its own launcher; this tool checks the claims the packet README makes about the
certificates and about the replay's output.

Usage (from ``packing/``)::

    .venv/bin/python3 -m devtools.audit_guzhou_r068 structure R068
    .venv/bin/python3 -m devtools.audit_guzhou_r068 compare R068 FRESH_DIR --output OUT.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.retained_data import read_retained_bytes, retained_exists

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "n17-guzhou-r068-2026-09-28"
SOURCE_ROOT = PACKET / "n17-square-packing"
BASELINE = (
    WEB
    / "n17-kleddamag-466001-2026-09-27/kleddamag-17-squares-certified-bound"
    / "bounds/4.66001/certificate.json"
)
BASELINE_SHA256 = "280af3d46150ca990917d714d83ee73baf4e6c45a0563090bf35588fb22de6e5"
N = 17
#: The folded orientation range every angle chain must cover, past sqrt(2) - 1.
FINAL_HALF_TANGENT = Fraction(207107, 500000)
CPP_STATUSES = frozenset(
    {"PASS_INTERVAL_PARTITION", "PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION"}
)
NODE_STATUSES = frozenset(
    {"PASS_INDEPENDENT_INTERVAL_PARTITION", "PASS_INDEPENDENT_GLOBAL_THRESHOLD_CERTIFICATE"}
)
_SYMMETRIES = ("id", "flip-x", "flip-y", "rot180", "swap", "rot90", "rot270", "anti-swap")


@dataclass(frozen=True, slots=True)
class Release:
    commit: str
    package: Path
    certificate: Path
    sha256: str
    published: Path
    target: Fraction
    intervals: int


RELEASES = {
    "R067": Release(
        "d4e2c287408b416683f7d1b7f19e69fb7c592d73",
        SOURCE_ROOT / "certificates/R067-4.66018",
        SOURCE_ROOT / "certificates/R067-4.66018/certificate.json",
        "101dd164906c7b71dc1397eaa32e25626548cd71995e532113823f434f8e5d26",
        SOURCE_ROOT / "certificates/R067-4.66018/evidence",
        Fraction(233009, 50000),
        2808,
    ),
    "R068": Release(
        "815b16261f852e389968513eec94b4b9e5b3206d",
        SOURCE_ROOT / "certificates/R068-C010",
        SOURCE_ROOT / "certificates/R068-C010/accepted/4.66044/certificate.json",
        "cf70f74ddb47071b1d7333d8a43885d2915f43d45f26f6084a106dfdb0c5205f",
        SOURCE_ROOT / "certificates/R068-C010/accepted/4.66044/paired_replay",
        Fraction(116511, 25000),
        4991,
    ),
}


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key {key}")
        result[key] = value
    return result


def load_json(path: Path, sha256: str | None = None) -> dict[str, Any]:
    """A retained JSON object, plain or gzip, optionally held to its pinned digest."""
    data = read_retained_bytes(path)
    if sha256 is not None:
        _require(hashlib.sha256(data).hexdigest() == sha256, f"{path.name} is not the pin")
    loaded = json.loads(data, object_pairs_hook=_unique_object)
    _require(isinstance(loaded, dict), f"{path.name} is not a JSON object")
    return loaded


def d4_images(x: int, y: int, side: int) -> list[tuple[int, int, str]]:
    """The distinct images of ``(x, y)`` sorted as the source checkers sort them.

    Each image carries the first symmetry that produces it, so two orbits whose sorted
    label sequences agree assign every site index the same geometric role.
    """
    candidates = (
        (x, y),
        (side - x, y),
        (x, side - y),
        (side - x, side - y),
        (y, x),
        (side - y, x),
        (y, side - x),
        (side - y, side - x),
    )
    seen: dict[tuple[int, int], str] = {}
    for label, point in zip(_SYMMETRIES, candidates, strict=True):
        seen.setdefault(point, label)
    return sorted((px, py, label) for (px, py), label in seen.items())


def _site_ranges(orbits: list[list[int]], side: int) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start = 0
    for x, y, _weight in orbits:
        count = len(d4_images(x, y, side))
        ranges.append((start, start + count))
        start += count
    return ranges


def _rules_touching(rules: list[dict[str, Any]], span: tuple[int, int]) -> int:
    return sum(
        any(span[0] <= site < span[1] for image in rule["sets"] for site in image)
        for rule in rules
    )


def _orbit_change(
    index: int,
    old: list[int] | None,
    new: list[int],
    *,
    side: int,
    span: tuple[int, int],
    rules: list[dict[str, Any]],
) -> dict[str, Any]:
    images = d4_images(new[0], new[1], side)
    change: dict[str, Any] = {
        "index": index,
        "old": old,
        "new": new,
        "weight": new[2],
        "images": len(images),
        "sites": list(span),
        "rule_orbits_referencing": _rules_touching(rules, span),
        "budget_units": new[2] * len(images),
    }
    if old is not None:
        before = d4_images(old[0], old[1], side)
        change["delta"] = [new[0] - old[0], new[1] - old[1]]
        change["old_budget_units"] = old[2] * len(before)
        change["same_image_order"] = [label for *_, label in before] == [
            label for *_, label in images
        ]
    return change


def angle_chain(entries: list[list[str]]) -> list[tuple[Fraction, Fraction]]:
    """A certificate's half-angle intervals, held to cover ``[0, 207107/500000]`` gaplessly."""
    chain = [(Fraction(entry[0]), Fraction(entry[1])) for entry in entries]
    _require(chain[0][0] == 0, "the angle chain does not start at zero")
    _require(
        chain[-1][1] == FINAL_HALF_TANGENT, "the angle chain does not end at 207107/500000"
    )
    _require(all(a < b for a, b in chain), "an angle interval is empty")
    _require(
        all(chain[i][1] == chain[i + 1][0] for i in range(len(chain) - 1)),
        "the angle chain has a gap or an overlap",
    )
    return chain


def refinement(
    base: list[tuple[Fraction, Fraction]], new: list[tuple[Fraction, Fraction]]
) -> dict[str, Any]:
    """How ``new`` subdivides ``base``: pieces per original interval, and bisections."""
    pieces: list[int] = []
    bisected = 0
    position = 0
    for a, b in base:
        _require(new[position][0] == a, f"original endpoint {a} is not a new endpoint")
        start = position
        while new[position][1] < b:
            position += 1
        _require(new[position][1] == b, f"original endpoint {b} is not a new endpoint")
        position += 1
        pieces.append(position - start)
        if position - start == 2 and new[start][1] == (a + b) / 2:
            bisected += 1
    _require(position == len(new), "the new chain runs past the original one")
    return {
        "original_intervals": len(base),
        "new_intervals": len(new),
        "pieces_per_original": {str(k): v for k, v in sorted(Counter(pieces).items())},
        "exact_bisections": bisected,
    }


def structure(name: str) -> dict[str, Any]:
    """What the release's certificate changes relative to Overbeck's 4.66001."""
    release = RELEASES[name]
    base = load_json(BASELINE, BASELINE_SHA256)
    cert = load_json(release.certificate, release.sha256)
    for field in ("L", "coordinate_denominator", "weight_denominator"):
        _require(cert[field] == base[field], f"{field} differs from the baseline")
    side_fraction = Fraction(cert["L"]) * cert["coordinate_denominator"]
    _require(side_fraction.denominator == 1, "the container side is not on the site grid")
    side = side_fraction.numerator
    parent = Fraction(cert["A"])
    target = Fraction(cert["normalized_target"])
    _require(target == release.target, "normalized_target is not the release's claim")
    _require(Fraction(cert["L"]) / parent == target, "L / A is not the normalized target")
    old_orbits, new_orbits = base["point_orbits"], cert["point_orbits"]
    _require(len(new_orbits) >= len(old_orbits), "point orbits were removed")
    old_ranges = _site_ranges(old_orbits, side)
    new_ranges = _site_ranges(new_orbits, side)
    rules = cert["threshold_orbits"]
    changes = [
        _orbit_change(
            index,
            old_orbits[index] if index < len(old_orbits) else None,
            new_orbits[index],
            side=side,
            span=new_ranges[index],
            rules=rules,
        )
        for index in range(len(new_orbits))
        if index >= len(old_orbits) or new_orbits[index] != old_orbits[index]
    ]
    moved_sites = [c for c in changes if c["old"] is not None]
    _require(
        all(new_ranges[c["index"]] == old_ranges[c["index"]] for c in moved_sites),
        "an edited orbit changed its image count, shifting later site indices",
    )
    point_delta = sum(c["budget_units"] - c.get("old_budget_units", 0) for c in changes)
    budget_delta = cert["budget_units"] - base["budget_units"]
    rules_unchanged = rules == base["threshold_orbits"]
    new_chain = angle_chain(cert["entries"])
    _require(len(new_chain) == release.intervals, "the interval count is not the claim")
    return {
        "schema": "GuzhouR068PacketStructure/v1",
        "release": name,
        "source_commit": release.commit,
        "certificate_sha256": release.sha256,
        "baseline_sha256": BASELINE_SHA256,
        "target": str(target),
        "parent_side": str(parent),
        "baseline_parent_side": base["A"],
        "point_orbits": len(new_orbits),
        "baseline_point_orbits": len(old_orbits),
        "sites": new_ranges[-1][1],
        "baseline_sites": old_ranges[-1][1],
        "point_orbit_changes": changes,
        "rule_orbits": len(rules),
        "rule_orbits_unchanged": rules_unchanged,
        "budget_units": cert["budget_units"],
        "baseline_budget_units": base["budget_units"],
        "budget_delta_units": budget_delta,
        "point_orbit_budget_delta_units": point_delta,
        "budget_delta_accounted": rules_unchanged and budget_delta == point_delta,
        "requested_minimum_units": cert["minimum_units"],
        "requested_surplus_units": N * cert["minimum_units"] - cert["budget_units"],
        "angle_chain": refinement(angle_chain(base["entries"]), new_chain),
    }


def partitions(directory: Path) -> dict[str, list[dict[str, Any]]]:
    """The ``cpp-i`` and ``node-i`` partition records in ``directory``, in index order."""
    found: dict[str, list[dict[str, Any]]] = {"cpp": [], "node": []}
    for kind, records in found.items():
        while retained_exists(directory / f"{kind}-{len(records)}.json"):
            records.append(load_json(directory / f"{kind}-{len(records)}.json"))
        _require(records, f"no {kind} partition records in {directory}")
    return found


def ledger(records: list[dict[str, Any]], kind: str, release: Release) -> list[dict[str, int]]:
    """Every row of one checker's partitions as ``(interval, minimum_units, cells)``."""
    rows: list[dict[str, int]] = []
    allowed = CPP_STATUSES if kind == "cpp" else NODE_STATUSES
    for record in records:
        _require(record["status"] in allowed, f"{kind} partition status {record['status']}")
        _require(record["certificate_sha256"] == release.sha256, f"{kind} certificate identity")
        _require(record["total_intervals"] == release.intervals, f"{kind} interval total")
        _require(record["start"] == len(rows), f"{kind} partitions are not contiguous")
        _require(
            len(record["rows"]) == record["end_exclusive"] - record["start"],
            f"{kind} partition is incomplete",
        )
        rows.extend(
            {
                "interval": int(row["interval"]),
                "minimum_units": int(row["minimum_units"]),
                "cells": int(row["cells"]),
            }
            for row in record["rows"]
        )
    _require(len(rows) == release.intervals, f"{kind} rows do not cover every interval")
    _require(
        [row["interval"] for row in rows] == list(range(release.intervals)),
        f"{kind} rows are missing, duplicated or reordered",
    )
    return rows


def _compact_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def canonical_sha256(rows: list[dict[str, int]]) -> str:
    """SHA-256 of the compact JSON of the reduced rows, the 4.66001 packet's form."""
    return _compact_sha256(rows)


def triples_sha256(rows: list[dict[str, int]]) -> str:
    """SHA-256 of the compact JSON of ``[interval, minimum, cells]`` triples."""
    return _compact_sha256([[r["interval"], r["minimum_units"], r["cells"]] for r in rows])


def cpp_header(records: list[dict[str, Any]]) -> dict[str, Any]:
    """The site, signed-term and strict-margin figures every C++ partition must share."""
    headers = {
        (record["sites"], record["signed_terms"], record["minimum_strict_margin"])
        for record in records
    }
    _require(len(headers) == 1, "the C++ partitions disagree on their header figures")
    sites, terms, margin = headers.pop()
    return {"sites": sites, "signed_terms": terms, "minimum_strict_margin": margin}


def compare(
    name: str, fresh: Path, published: Path | None = None, *, release: Release | None = None
) -> dict[str, Any]:
    """Every fresh and published ledger row by row, against the published C++ one.

    ``release`` defaults to ``RELEASES[name]``; `devtools.audit_guzhou_r071` passes its
    own, from a later packet.
    """
    release = release or RELEASES[name]
    cert = load_json(release.certificate, release.sha256)
    sets = {"fresh": partitions(fresh), "published": partitions(published or release.published)}
    ledgers = {
        f"{origin}-{kind}": ledger(records, kind, release)
        for origin, found in sets.items()
        for kind, records in found.items()
    }
    reference = ledgers["published-cpp"]
    mismatches = [
        {"ledger": label, "interval": i, "row": row, "published_cpp": reference[i]}
        for label, rows in ledgers.items()
        for i, row in enumerate(rows)
        if row != reference[i]
    ]
    minima = [row["minimum_units"] for row in ledgers["fresh-cpp"]]
    minimum = min(minima)
    return {
        "schema": "GuzhouR068ReplayComparison/v1",
        "release": name,
        "certificate_sha256": release.sha256,
        "partitions": {
            origin: {kind: len(records) for kind, records in found.items()}
            for origin, found in sets.items()
        },
        "ledgers_compared": len(ledgers),
        "rows_per_ledger": release.intervals,
        "mismatches": len(mismatches),
        "first_mismatches": mismatches[:20],
        "canonical_rows_sha256": {
            label: canonical_sha256(rows) for label, rows in ledgers.items()
        },
        "triples_sha256": {label: triples_sha256(rows) for label, rows in ledgers.items()},
        "cpp_headers": {origin: cpp_header(found["cpp"]) for origin, found in sets.items()},
        "minimum_units": minimum,
        "intervals_at_minimum": minima.count(minimum),
        "next_minimum_units": min((m for m in minima if m > minimum), default=None),
        "cells": sum(row["cells"] for row in ledgers["fresh-cpp"]),
        "budget_units": cert["budget_units"],
        "surplus_units": N * minimum - cert["budget_units"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    shape = commands.add_parser("structure", help="the certificate against Overbeck's 4.66001")
    shape.add_argument("release", choices=sorted(RELEASES))
    shape.add_argument("--output", type=Path)
    replay = commands.add_parser("compare", help="a paired replay against the published rows")
    replay.add_argument("release", choices=sorted(RELEASES))
    replay.add_argument("fresh", type=Path)
    replay.add_argument("--published", type=Path)
    replay.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "structure":
        receipt = structure(args.release)
    else:
        receipt = compare(args.release, args.fresh, args.published)
    text = json.dumps(receipt, indent=2) + "\n"
    if args.output is not None:
        with atomic_output_file(args.output) as temporary:
            Path(temporary).write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 1 if receipt.get("mismatches") else 0


if __name__ == "__main__":
    raise SystemExit(main())
