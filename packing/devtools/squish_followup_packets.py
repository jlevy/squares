"""Retain the pinned SQUISH update as reported facts without changing prior evidence.

Use ``acquire --source PATH`` for the upstream submission directory, then ``check``.
The bounded source parser is shared with the original packet. This command admits
source claims and compares geometry; it never certifies feasibility or runs a producer.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import squish_upper_bound_packets as original

REPO = original.REPO
PACKET = REPO / "packing/resources/web/squish-401-update-2026-10-07"
REVISION = "5e32bbd7028b6e3b869979278079cd37ed6770aa"
NUMBERS = (123, 126, 129, 153, 154, 155, 179, 208, 237, 238, 239, 258, 263)
NEW_NUMBERS = (123, 179, 208, 237, 239, 258, 263)
REPLACEMENTS = (126, 129, 154, 155, 238)
SOURCE_KEY = "[SQUISH update 2026-10-07]"
SOURCE_ROOT = (
    f"https://github.com/itsnaka/squish-certs/blob/{REVISION}/squish-submission-2026-10-07"
)
DISPLAY_PLACES = 16
# Author-reported seed attribution, from issue 401's pinned update comment.
SEEDS = {
    123: "Francisco Couzo's s(102), grafted into n's Kingbird record",
    126: "Francisco Couzo's s(105), grafted into n's Kingbird record",
    129: "Francisco Couzo's s(131), squares removed",
    153: "SQUISH's own s(154), squares removed",
    154: "SQUISH's own s(155), squares removed",
    155: "Francisco Couzo's s(156), squares removed",
    179: "Francisco Couzo's s(180), squares removed",
    208: "Francisco Couzo's s(209), squares removed",
    237: "Francisco Couzo's s(238), squares removed",
    238: "SQUISH's own s(239), squares removed",
    239: "Francisco Couzo's s(210), grafted into n's Kingbird record",
    258: "Francisco Couzo's s(259), squares removed",
    263: "Francisco Couzo's s(297), carved down to n's Kingbird record",
}


def json_bytes(value: object) -> bytes:
    """Serialize derived records deterministically, with no source prose copied."""
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def save(path: Path, data: bytes) -> None:
    """Publish each derived artifact atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(data)


def display(side: str) -> str:
    """Round the claimed exact side upward, never below its rational value."""
    scale = 10**DISPLAY_PLACES
    value = Fraction(side) * scale
    ceiling = -(-value.numerator // value.denominator)
    integer, fractional = divmod(ceiling, scale)
    return f"{integer}.{fractional:0{DISPLAY_PLACES}d}"


def fact_path(n: int) -> Path:
    """Locate the revision-specific normalized geometry."""
    return PACKET / "facts" / f"n-{n:03d}.json.gz"


def read_fact(n: int) -> dict[str, Any]:
    """Re-admit retained triples through the existing strict source parser."""
    if fact_path(n).stat().st_size > original.MAX_SOURCE_BYTES:
        raise original.PacketError("compressed update facts exceed byte ceiling")
    with gzip.open(fact_path(n), "rb") as stream:
        data = stream.read(original.MAX_SOURCE_BYTES + 1)
    if len(data) > original.MAX_SOURCE_BYTES:
        raise original.PacketError("update facts exceed byte ceiling")
    fact = json.loads(data, object_pairs_hook=original.unique_json_object)
    if type(fact) is not dict or set(fact) != {"n", "side", "printed_side", "squares"}:
        raise original.PacketError("invalid update fact schema")
    entries = fact["squares"]
    if type(entries) is not list or any(
        type(entry) is not dict or set(entry) != {"x", "y", "t"} for entry in entries
    ):
        raise original.PacketError("invalid update triple roster")
    source = {
        "n": fact["n"],
        "s_exact": fact["side"],
        "s_decimal": fact["printed_side"],
        "note": "Derived geometric facts; no producer prose retained.",
        "squares": [[entry[key] for key in ("x", "y", "t")] for entry in entries],
    }
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "source.json"
        path.write_bytes(json_bytes(source))
        normalized, _raw = original.parse_source(path, n)
    if fact != normalized:
        raise original.PacketError("update facts are not normalized")
    return normalized


def claims(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Keep the unchanged n153 comparison outside the new result's scope."""
    return {
        "results": [
            {"n": row["n"], "offered_side": display(row["exact_side"])}
            for row in cases
            if row["n"] != 153
        ]
    }


def n153_comparison(fact: dict[str, Any]) -> dict[str, Any]:
    """Compare exact side and every ordered triple to the immutable attachment facts."""
    prior = original.read_fact(153)
    return {
        "n": 153,
        "prior_facts": original.fact_path(153).relative_to(REPO).as_posix(),
        "update_facts": fact_path(153).relative_to(REPO).as_posix(),
        "same_exact_side": fact["side"] == prior["side"],
        "same_ordered_rational_triples": fact["squares"] == prior["squares"],
        "prior_printed_side": prior["printed_side"],
        "update_printed_side": fact["printed_side"],
        "prior_evidence_preserved": True,
        "new_assurance_claimed": False,
    }


def acquire(source: Path) -> None:
    """Parse the entire revision before writing attributed derived facts."""
    parsed = [(n, *original.parse_source(source / f"n{n}/n{n}.cert.json", n)) for n in NUMBERS]
    cases = []
    for n, fact, raw in parsed:
        save(fact_path(n), gzip.compress(json_bytes(fact), mtime=0))
        cases.append(
            {
                "n": n,
                "exact_side": fact["side"],
                "side": fact["printed_side"],
                "source_url": f"{SOURCE_ROOT}/n{n}/n{n}.cert.json",
                "source_file": f"n{n}.cert.json",
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "source_bytes": len(raw),
                "facts": fact_path(n).relative_to(REPO).as_posix(),
                "raw_asset_retained": False,
                "reported_seed": SEEDS[n],
            }
        )
    save(
        PACKET / "acquisition/sources.json",
        json_bytes(
            {
                "format": "external-source-acquisition-v1",
                "retrieved": "2026-10-07",
                "source_commit": REVISION,
                "raw_asset_retained": False,
                "producer_checker_replayed": False,
                "cases": cases,
            }
        ),
    )
    save(PACKET / "acquisition/update-claims.json", json_bytes(claims(cases)))
    save(
        PACKET / "acquisition/n153-comparison.json", json_bytes(n153_comparison(read_fact(153)))
    )


def check(source: Path | None = None) -> None:
    """Check provenance and exact retained identity, optionally against upstream bytes."""
    acquisition = original.read_json(PACKET / "acquisition/sources.json")
    if (
        acquisition["source_commit"] != REVISION
        or acquisition["raw_asset_retained"] is not False
        or acquisition["producer_checker_replayed"] is not False
        or acquisition["format"] != "external-source-acquisition-v1"
        or acquisition["retrieved"] != "2026-10-07"
    ):
        raise original.PacketError("update source provenance mismatch")
    cases = acquisition["cases"]
    if [row["n"] for row in cases] != list(NUMBERS):
        raise original.PacketError("update acquisition roster mismatch")
    for row in cases:
        n = row["n"]
        fact = read_fact(n)
        if (
            row["facts"] != fact_path(n).relative_to(REPO).as_posix()
            or row["exact_side"] != fact["side"]
            or row["side"] != fact["printed_side"]
            or row["source_url"] != f"{SOURCE_ROOT}/n{n}/n{n}.cert.json"
            or row["reported_seed"] != SEEDS[n]
            or row["raw_asset_retained"] is not False
        ):
            raise original.PacketError(f"n={n} update provenance/facts mismatch")
        if source is not None:
            upstream, raw = original.parse_source(source / f"n{n}/n{n}.cert.json", n)
            if (
                upstream != fact
                or row["source_sha256"] != hashlib.sha256(raw).hexdigest()
                or row["source_bytes"] != len(raw)
            ):
                raise original.PacketError(
                    f"n={n} upstream bytes differ from pinned acquisition"
                )
    if original.read_json(PACKET / "acquisition/update-claims.json") != claims(cases):
        raise original.PacketError("update claims mismatch")
    comparison_record = original.read_json(PACKET / "acquisition/frontier-comparison.json")
    comparisons = comparison_record["cases"]
    if [row["n"] for row in comparisons] != [n for n in NUMBERS if n != 153]:
        raise original.PacketError("historical frontier comparison roster mismatch")
    for row in comparisons:
        n = row["n"]
        fact = read_fact(n)
        prior = row["prior_reported"]
        if (
            row["new_exact_side"] != fact["side"]
            or row["new_safe_display"] != display(fact["side"])
            or row["reported_seed"] != SEEDS[n]
            or not prior["source_key"]
            or type(prior["found_by"]) is not list
            or Fraction(prior["value"]) <= Fraction(fact["side"])
        ):
            raise original.PacketError(f"n={n} historical frontier comparison mismatch")
        if n in REPLACEMENTS:
            preceding = original.read_fact(n)
            if prior["exact_form"] != preceding["side"]:
                raise original.PacketError(f"n={n} predecessor differs from retained release")
    comparison = n153_comparison(read_fact(153))
    if original.read_json(PACKET / "acquisition/n153-comparison.json") != comparison:
        raise original.PacketError("n153 exact geometry comparison mismatch")
    if not comparison["same_exact_side"] or not comparison["same_ordered_rational_triples"]:
        raise original.PacketError("n153 differs; register new geometry separately")


def main(argv: list[str] | None = None) -> int:
    """Expose acquisition and bounded revision checks without a feasibility claim."""
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="command", required=True)
    acquisition = sub.add_parser("acquire", allow_abbrev=False)
    acquisition.add_argument("--source", type=Path, required=True)
    checking = sub.add_parser("check", allow_abbrev=False)
    checking.add_argument("--source", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "acquire":
            acquire(args.source)
        else:
            check(args.source)
    except (original.PacketError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"SQUISH update packet: {error}", file=sys.stderr)
        return 1
    if args.command == "acquire":
        print("SQUISH update packet: reported facts retained; run check for consistency")
    else:
        print("SQUISH update packet: consistency checked; feasibility not decided")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
