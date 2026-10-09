"""Retain and replay the centered rational refinements requested in issues 425/428.

Acquisition and input conversion decide no packing predicate. The explicit replay
command runs the two retained upstream n68 geometry checkers on the complete source
and two complete mutant rosters. Restricted analytic claims are outside its scope.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
import re
import time
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.import_half_angle_witness import half_angle_corners, unique_json_object

REPO = Path(__file__).resolve().parents[2]
MAX_BYTES = 1_000_000
MAX_LITERAL = 1024
RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


@dataclass(frozen=True)
class Source:
    """Immutable scientific release and the selected request scope."""

    issue: int
    repository: str
    revision: str
    packet_name: str
    key: str
    numbers: tuple[int, ...]
    prefix: str
    metadata_keys: frozenset[str]

    @property
    def packet(self) -> Path:
        return REPO / "packing/resources/web" / self.packet_name

    def upstream_path(self, n: int) -> str:
        if type(n) is not int or n not in self.numbers:
            raise ValueError("count is outside the selected immutable request")
        return f"{self.prefix}/n{n}.json"

    def url(self, n: int) -> str:
        return (
            f"https://github.com/{self.repository}/blob/{self.revision}/{self.upstream_path(n)}"
        )


COUZO = Source(
    425,
    "lollipoll/couzo-five-exact-certificates",
    "bc389ddf7d65277cd19a9b08fb285d86346d6806",
    "rehwaldt-couzo-refinements-2026-10-07",
    "[Rehwaldt Couzo refinements 2026-10-07]",
    (105, 292),
    "reviewed/witnesses",
    frozenset(
        {"method", "source_author", "center_expansion", "estimated_contact_side", "optimality"}
    ),
)
N68 = Source(
    428,
    "lollipoll/certified-square-packing-68",
    "fded686668e29258dad2eb29d0482fa3fd51bd6b",
    "rehwaldt-n68-refinement-2026-10-07",
    "[Rehwaldt n68 refinement 2026-10-07]",
    (68,),
    "refinement-v1.1.0",
    frozenset(
        {
            "source_construction",
            "square_labels",
            "method",
            "estimated_contact_limit",
            "center_expansion",
            "rounding_denominator",
            "offered_side_decimal",
            "optimality",
        }
    ),
)
SOURCES = {source.issue: source for source in (COUZO, N68)}
SOURCE_SHA256 = {
    105: "ff52d891b7ce26df78a514753b0fdee88d9b9d450fcad00e17814e2ac2552ec5",
    292: "b8d55be6e49b524bb1035b6bcc660316e35c0faa580ad57f715798815e43679e",
    68: "6d4f72debae83b5825e91f7b090e0cee08851ad7b85400343c0dee52f468dff9",
}
N68_PROGRAMS = {
    "verify.py": ("verify", "911b9822334636ffc49472e4df32e38cb162efbfad9a4684879f006b1c90e7f9"),
    "independent_support_check.py": (
        "check",
        "48e1ae336855ba5cc05c3fd161bf51ef71cab24ebc33ae590be040f78a932423",
    ),
}
# These identities bind normalized facts to the independently pinned source above.
# The source-to-fact conversion is reviewed independently; source custody is a trust boundary.
FACT_SHA256 = {
    105: "c8c8c2d158f209e146e5758cdb8f6c277718a4a8aa6a408db1d7abfa4f66a154",
    292: "ba8dc6bd179813558aeb7b1188592f54eb80223c3de2d3d4def9ef9de6fa4664",
    68: "6d3204ff2adfe4ab53c0b864188b79884ff18f561ca8eef4c2982f128747193c",
}


def rational(value: Any) -> Fraction:
    """Admit bounded exact literals, with no decimal or floating conversion."""
    if type(value) is not str or len(value) > MAX_LITERAL or RATIONAL.fullmatch(value) is None:
        raise ValueError("bounded exact rational string required")
    return Fraction(value)


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def save(path: Path, data: bytes) -> None:
    """Atomically publish task-owned output inside the checkout."""
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise ValueError("packet output escapes the checkout")
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(data)


def parse_source(raw: bytes, source: Source, n: int) -> dict[str, Any]:
    source.upstream_path(n)
    if len(raw) > MAX_BYTES:
        raise ValueError("source exceeds byte ceiling")
    data = json.loads(raw, object_pairs_hook=unique_json_object)
    if type(data) is not dict or set(data) != {
        "schema",
        "n",
        "container_side",
        "squares",
        "metadata",
    }:
        raise ValueError("source must contain the exact schema fields")
    if data["schema"] != "packing-n/exact-v1" or type(data["n"]) is not int or data["n"] != n:
        raise ValueError("source schema/count identity differs")
    side = rational(data["container_side"])
    if side <= 0 or type(data["squares"]) is not list or len(data["squares"]) != n:
        raise ValueError("positive side and complete source roster required")
    triples = []
    for row in data["squares"]:
        if type(row) is not dict or set(row) != {"x", "y", "t"}:
            raise ValueError("complete typed source triple required")
        triples.append({key: str(rational(row[key])) for key in ("x", "y", "t")})
    metadata = data["metadata"]
    if (
        type(metadata) is not dict
        or set(metadata) != source.metadata_keys
        or any(type(value) is not str or len(value) > 2048 for value in metadata.values())
    ):
        raise ValueError("bounded source-specific quoted metadata required")
    return {"n": n, "side": str(side), "squares": triples, "source_metadata": metadata}


def fact_path(source: Source, n: int) -> Path:
    source.upstream_path(n)
    return source.packet / "facts" / f"n-{n:03d}.json.gz"


def read_fact(source: Source, n: int) -> dict[str, Any]:
    path = fact_path(source, n)
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("compressed facts exceed byte ceiling")
    with gzip.open(path, "rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("decoded facts exceed byte ceiling")
    facts = json.loads(raw, object_pairs_hook=unique_json_object)
    if type(facts) is not dict or set(facts) != {"n", "side", "squares", "source_metadata"}:
        raise ValueError("normalized fact fields differ")
    reconstructed = {
        "schema": "packing-n/exact-v1",
        "n": facts["n"],
        "container_side": facts["side"],
        "squares": facts["squares"],
        "metadata": facts["source_metadata"],
    }
    if parse_source(json_bytes(reconstructed), source, n) != facts:
        raise ValueError("normalized facts differ from strict re-admission")
    if hashlib.sha256(json_bytes(facts)).hexdigest() != FACT_SHA256[n]:
        raise ValueError(
            "facts differ from the independently pinned complete source conversion"
        )
    return facts


def exact_decimal(side: str) -> str:
    """Display the complete terminating side, preserving tiny strict improvements."""
    value = rational(side)
    denominator = value.denominator
    for prime in (2, 5):
        while denominator % prime == 0:
            denominator //= prime
    if denominator != 1:
        raise ValueError("this release requires a terminating exact display")
    with localcontext() as context:
        context.prec = MAX_LITERAL * 2
        return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def to_witness(source: Source, n: int) -> dict[str, Any]:
    """Translate the already repaired centered frame by S/2 exactly once."""
    facts = read_fact(source, n)
    side = rational(facts["side"])
    squares = []
    for index, row in enumerate(facts["squares"], 1):
        corners = half_angle_corners(
            rational(row["x"]) + side / 2, rational(row["y"]) + side / 2, rational(row["t"])
        )
        squares.append({"id": index, "corners": [[str(x), str(y)] for x, y in corners]})
    return {
        "id": f"W-rehwaldt-{source.issue}-n{n:03d}",
        "n": n,
        "side": str(side),
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": squares,
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": (
                "Reported finite rational feasibility witness; no optimality, rigidity "
                "or human oversight assurance."
            ),
        },
        "source": {
            "key": source.key,
            "path": fact_path(source, n).relative_to(REPO).as_posix(),
            "url": source.url(n),
            "revision": source.revision,
            "retrieved": "2026-10-08",
        },
    }


def acquire(source: Source, root: Path) -> None:
    """Keep derived geometric facts and custody; execute no producer or checker."""
    rows = []
    admitted = []
    for n in source.numbers:
        path = root / source.upstream_path(n)
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256[n]:
            raise ValueError("source bytes differ from independently pinned custody")
        facts = parse_source(raw, source, n)
        admitted.append((n, raw, facts))
    for n, raw, facts in admitted:
        stored = gzip.compress(json_bytes(facts), mtime=0)
        save(fact_path(source, n), stored)
        rows.append(
            {
                "n": n,
                "exact_side": facts["side"],
                "offered_side": exact_decimal(facts["side"]),
                "source_path": source.upstream_path(n),
                "source_url": source.url(n),
                "source_bytes": len(raw),
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "facts": fact_path(source, n).relative_to(REPO).as_posix(),
            }
        )
    save(
        source.packet / "acquisition/sources.json",
        json_bytes(
            {
                "format": "external-source-acquisition-v1",
                "source_commit": source.revision,
                "repository": source.repository,
                "source_issue": f"https://github.com/jlevy/squares/issues/{source.issue}",
                "retrieved_at_utc": "2026-10-08",
                "raw_asset_retained": False,
                "producer_checker_replayed": False,
                "cases": rows,
            }
        ),
    )
    save(source.packet / "acquisition/claims.json", json_bytes({"results": rows}))


def replay_n68(source_root: Path, output: Path) -> None:
    """Complete producer-code geometry replay with two full-roster controls per route."""
    raw = (source_root / N68.upstream_path(68)).read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256[68] or __debug__ is False:
        raise ValueError("pinned full source and assertions enabled are required")
    parse_source(raw, N68, 68)
    positive = json.loads(raw, object_pairs_hook=unique_json_object)
    modules = []
    for filename, (function, expected_digest) in N68_PROGRAMS.items():
        path = source_root / N68.prefix / filename
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected_digest:
            raise ValueError("upstream program differs from the reviewed immutable source")
        spec = importlib.util.spec_from_file_location(f"rehwaldt_n68_{function}", path)
        if spec is None or spec.loader is None:
            raise ValueError("upstream geometry module cannot be loaded")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules.append(
            (filename, getattr(module, function), hashlib.sha256(path.read_bytes()).hexdigest())
        )
    jobs = {"positive": positive}
    duplicate = copy.deepcopy(positive)
    duplicate["squares"][1] = copy.deepcopy(positive["squares"][0])
    jobs["duplicate-square-overlap"] = duplicate
    outside = copy.deepcopy(positive)
    outside["squares"][0]["x"] = str(-2 * rational(positive["container_side"]))
    jobs["outside-container"] = outside
    rows = []
    started = time.monotonic()
    for name, data in jobs.items():
        route_rows = []
        for filename, function, digest in modules:
            route_started = time.monotonic()
            result = function(data, 68)
            valid = result.get("valid_exact", result.get("valid"))
            if (
                type(valid) is not bool
                or valid != (name == "positive")
                or result["pairs_checked"] != 2278
            ):
                raise ValueError("upstream geometry verdict or complete pair coverage differs")
            margin_key = (
                "minimum_pair_gap"
                if filename == "verify.py"
                else "minimum_pair_margin_rational"
            )
            wall_key = (
                "minimum_wall_gap"
                if filename == "verify.py"
                else "minimum_wall_clearance_rational"
            )
            if name == "duplicate-square-overlap" and Fraction(result[margin_key]) >= 0:
                raise ValueError("overlap mutant lacks an actual negative pair gap")
            if name == "outside-container" and Fraction(result[wall_key]) >= 0:
                raise ValueError("outside mutant lacks an actual negative wall gap")
            route_rows.append(
                {
                    "source_program": filename,
                    "source_sha256": digest,
                    "wall_seconds": time.monotonic() - route_started,
                    "result": result,
                }
            )
        rows.append({"name": name, "input": data, "routes": route_rows})
    save(
        output,
        gzip.compress(
            json_bytes(
                {
                    "format": "rehwaldt-n68-source-geometry-replay-v1",
                    "source_revision": N68.revision,
                    "source_sha256": hashlib.sha256(raw).hexdigest(),
                    "source_programs_replayed": True,
                    "complete_jobs": 3,
                    "positive_pairs_per_route": 2278,
                    "all_job_pairs_per_route": 6834,
                    "total_pair_decisions": 13668,
                    "wall_seconds": time.monotonic() - started,
                    "assurance_assigned": False,
                    "jobs": rows,
                }
            ),
            mtime=0,
        ),
    )
    print(
        "n68 complete source geometry replay: 2 positive routes, 4 mutant refusals; "
        f"13668 pair decisions; {time.monotonic() - started:.3f}s"
    )


def main() -> None:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    acquire_parser = commands.add_parser("acquire", allow_abbrev=False)
    acquire_parser.add_argument("--issue", type=int, choices=sorted(SOURCES), required=True)
    acquire_parser.add_argument("--source-root", type=Path, required=True)
    replay_parser = commands.add_parser("replay-n68", allow_abbrev=False)
    replay_parser.add_argument("--source-root", type=Path, required=True)
    replay_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "acquire":
        acquire(SOURCES[args.issue], args.source_root)
    else:
        replay_n68(args.source_root, args.output)


if __name__ == "__main__":
    main()
