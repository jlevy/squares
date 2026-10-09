"""Retain and recover the complete reviewed refinement replay across a release boundary.

Fast admission checks the complete source-derived deciding inputs and actual result
fields kept in Git. Explicit recovery downloads the full file roster, compares every
byte with the published manifest, and re-derives the compact record from those bytes.
Neither command runs a geometry predicate or assigns assurance.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import lzma
import tarfile
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

from devtools import refinement_packets as packets
from devtools.squish_upper_bound_packets import checker_input
from sqpack.hosted_data import (
    GhClient,
    HostedObject,
    Manifest,
    fetch,
    load_manifest,
    render_manifest,
)

REPO = packets.REPO
MANIFEST = REPO / "packing/hosted/refinement-evidence-425-428-v1.yaml"
INDEX = packets.COUZO.packet / "receipts/admission.json.xz"
TAG = "data/refinement-evidence-425-428-v1"
ASSET = "refinement-evidence-425-428-v1.tar.xz"
RUN_ID = "run-1791419042804620000"
ENGINEERING = "squares-425-engineering-preparation"
NAMES = (
    "positive",
    "duplicate-square-overlap",
    "outside-container",
    "tiny-overlap",
    "tiny-wall-protrusion",
)
FORMAT = "refinement-complete-replay-admission-v1"
# The compact object derived from complete external replay custody. Final assurance
# awaits separate review against the hosted archive; this is not a Git identity.
ADMISSION_SHA256 = "3721f285370a76bfd4d841789d2768dd294fa42bc2232756c690a8b1d40e3d10"
MAX_ARCHIVE = 64_000_000
MAX_UNPACKED = 256_000_000


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_index() -> dict[str, Any]:
    if not INDEX.resolve().is_relative_to(REPO.resolve()) or INDEX.stat().st_size > 64_000:
        raise ValueError("compact admission must remain bounded and private")
    with lzma.open(INDEX, "rb") as stream:
        raw = stream.read(64_001)
    if len(raw) > 64_000 or digest(raw) != ADMISSION_SHA256:
        raise ValueError("compact admission differs from the pinned external replay catalogue")
    return json.loads(raw)


def read_json(path: Path) -> Any:
    if path.stat().st_size > 16_000_000:
        raise ValueError("custody JSON exceeds byte ceiling")
    return json.loads(path.read_bytes())


def source_for(n: int) -> packets.Source:
    return next(source for source in packets.SOURCES.values() if n in source.numbers)


def n68_input(name: str) -> dict[str, Any]:
    facts = packets.read_fact(packets.N68, 68)
    data = {
        "schema": "packing-n/exact-v1",
        "n": 68,
        "container_side": facts["side"],
        "squares": copy.deepcopy(facts["squares"]),
        "metadata": facts["source_metadata"],
    }
    if name == "duplicate-square-overlap":
        data["squares"][1] = copy.deepcopy(data["squares"][0])
    elif name == "outside-container":
        data["squares"][0]["x"] = str(-2 * Fraction(facts["side"]))
    elif name != "positive":
        raise ValueError("unknown complete n68 recipe")
    return data


def deciding_input(n: int, name: str) -> dict[str, Any]:
    """Recover all ten reviewed deciding inputs without evaluating predicates."""
    witness = packets.to_witness(source_for(n), n)
    if name not in NAMES or n not in packets.COUZO.numbers:
        raise ValueError("unknown frozen refinement recipe")
    first = [[Fraction(value) for value in point] for point in witness["squares"][0]["corners"]]
    epsilon = Fraction(1, 10**100)
    if name == "duplicate-square-overlap":
        witness["squares"][1]["corners"] = copy.deepcopy(witness["squares"][0]["corners"])
    elif name == "tiny-overlap":
        edge = [first[1][axis] - first[0][axis] for axis in (0, 1)]
        witness["squares"][1]["corners"] = [
            [str(point[axis] + (1 - epsilon) * edge[axis]) for axis in (0, 1)]
            for point in first
        ]
    elif name in {"outside-container", "tiny-wall-protrusion"}:
        shift = (
            -max(point[0] for point in first) - 1
            if name == "outside-container"
            else -min(point[0] for point in first) - epsilon
        )
        witness["squares"][0]["corners"] = [
            [str(point[0] + shift), str(point[1])] for point in first
        ]
    return checker_input(witness)


def compact(root: Path, n68_receipt: Path | None = None) -> dict[str, Any]:
    """Bind compact custody to every full actual receipt, input and child stdout."""
    host = root / ENGINEERING / "host-v3"
    run = host / "runs" / RUN_ID
    rows = []
    for n in packets.COUZO.numbers:
        raw = (host / "source" / packets.COUZO.upstream_path(n)).read_bytes()
        if digest(raw) != packets.SOURCE_SHA256[n] or packets.parse_source(
            raw, packets.COUZO, n
        ) != packets.read_fact(packets.COUZO, n):
            raise ValueError("recovered raw source differs from pinned canonical facts")
        for name in NAMES:
            filename = f"n-{n:03d}-{name}.json"
            receipt_path = run / "receipts" / filename
            receipt = read_json(receipt_path)
            prepared = read_json(host / "inputs" / filename)
            logged = read_json(run / "logs" / filename.replace(".json", ".log"))
            if (
                receipt["job"] != prepared
                or receipt != logged
                or receipt["runtime"] != read_json(host / "runtime-identity.json")
                or receipt["job"]["checker_input"] != deciding_input(n, name)
                or receipt["run_id"] != RUN_ID
            ):
                raise ValueError(
                    "actual receipt, full deciding input, runtime or stdout differs"
                )
            rows.append(
                {
                    "n": n,
                    "name": name,
                    "input_sha256": digest(packets.json_bytes(receipt["job"]["checker_input"])),
                    "receipt_sha256": digest(receipt_path.read_bytes()),
                    "verdict": receipt["verdict"],
                    "dual_route_wall_seconds": receipt["dual_route_wall_seconds"],
                }
            )
    source_root = root / "n68-upstream"
    raw = (source_root / packets.N68.upstream_path(68)).read_bytes()
    if digest(raw) != packets.SOURCE_SHA256[68] or packets.parse_source(
        raw, packets.N68, 68
    ) != packets.read_fact(packets.N68, 68):
        raise ValueError("n68 raw source differs from pinned canonical facts")
    for name, (_, expected) in packets.N68_PROGRAMS.items():
        if digest((source_root / packets.N68.prefix / name).read_bytes()) != expected:
            raise ValueError("recovered n68 source checker differs")
    receipt_path = n68_receipt or root / "n68-source-geometry.json.gz"
    receipt = json.loads(gzip.decompress(receipt_path.read_bytes()))
    if receipt["jobs"][0]["input"] != json.loads(raw):
        raise ValueError("n68 complete positive receipt input differs from raw source")
    n68_rows = []
    for row in receipt["jobs"]:
        expected = json.loads(raw)
        if row["name"] == "duplicate-square-overlap":
            expected["squares"][1] = copy.deepcopy(expected["squares"][0])
        elif row["name"] == "outside-container":
            expected["squares"][0]["x"] = str(-2 * Fraction(expected["container_side"]))
        elif row["name"] != "positive":
            raise ValueError("unexpected n68 control")
        if row["input"] != expected:
            raise ValueError("n68 complete control differs from its declared recipe")
        n68_rows.append(
            {
                "name": row["name"],
                "input_sha256": digest(packets.json_bytes(expected)),
                "routes": row["routes"],
            }
        )
    return {
        "format": FORMAT,
        "run_id": RUN_ID,
        "prepared_manifest_sha256": digest((host / "prepared-manifest.json").read_bytes()),
        "runtime_sha256": digest((host / "runtime-identity.json").read_bytes()),
        "process_outcomes": read_json(run / "process-outcomes.json"),
        "summary": read_json(run / "admitted-summary.json"),
        "couzo_jobs": rows,
        "n68_jobs": n68_rows,
        "n68_wall_seconds": receipt["wall_seconds"],
        "source_geometry_only": True,
        "assurance_assigned": False,
    }


def check_index(value: dict[str, Any]) -> None:
    """Check all full-roster outcomes and exact negative diagnostics; no new replay."""
    if value["format"] != FORMAT or value["run_id"] != RUN_ID:
        raise ValueError("compact replay identity differs")
    rows = value["couzo_jobs"]
    roster = [(n, name) for n in packets.COUZO.numbers for name in NAMES]
    outcomes = value["process_outcomes"]
    if (
        [(row["n"], row["name"]) for row in rows] != roster
        or outcomes["complete"] is not True
        or [(row["n"], row["name"]) for row in outcomes["processes"]] != roster
        or any(
            row["child_exit_code"] != 0 or row["timed_out"] is not False
            for row in outcomes["processes"]
        )
        or value["summary"]["full_jobs"] != 10
        or value["summary"]["positive_pairs_per_route"] != 47946
        or value["summary"]["all_job_pairs_per_route"] != 239730
        or value["summary"]["feasibility_replay_completed"] is not True
    ):
        raise ValueError("complete ten-job process or coverage admission differs")
    epsilon = Fraction(1, 10**100)
    for row in rows:
        n, name = row["n"], row["name"]
        if row["input_sha256"] != digest(packets.json_bytes(deciding_input(n, name))):
            raise ValueError("private complete deciding input differs from actual receipt")
        routes = row["verdict"]["routes"]
        if set(routes) != {"independent", "exact_verify"}:
            raise ValueError("both complete deciding routes required")
        for result in routes.values():
            if (
                type(result["verification_passed"]) is not bool
                or result["verification_passed"] != (name == "positive")
                or result["n"] != n
                or result["pairs_tested"] != n * (n - 1) // 2
                or Fraction(result["side"])
                != Fraction(packets.read_fact(packets.COUZO, n)["side"])
            ):
                raise ValueError("actual route verdict, side or complete coverage differs")
            wall = Fraction(result["minimum_containment_clearance"])
            gap = Fraction(result["minimum_best_pair_gap"])
            if name == "positive" and (wall < 0 or gap < 0 or result["failures"]):
                raise ValueError("positive route has a negative diagnostic")
            if name == "duplicate-square-overlap" and gap >= 0:
                raise ValueError("overlap control lacks actual negative pair gap")
            if name == "outside-container" and wall >= 0:
                raise ValueError("outside control lacks actual negative wall gap")
            if name == "tiny-wall-protrusion" and wall != -epsilon:
                raise ValueError("tiny wall control lacks its exact actual minimum")
        if (
            name == "tiny-overlap"
            and Fraction(row["verdict"]["independent_designated_pair_gap"]) != -epsilon
        ):
            raise ValueError("tiny overlap lacks its exact designated gap")
        if (
            name == "tiny-overlap"
            and ["overlap", "squares 0 and 1 overlap"] not in routes["exact_verify"]["failures"]
        ):
            raise ValueError("native tiny overlap lacks the designated pair failure")
    if [row["name"] for row in value["n68_jobs"]] != list(NAMES[:3]):
        raise ValueError("complete n68 three-job roster required")
    for row in value["n68_jobs"]:
        if row["input_sha256"] != digest(packets.json_bytes(n68_input(row["name"]))):
            raise ValueError("complete private n68 input differs from actual receipt")
        if [route["source_program"] for route in row["routes"]] != list(packets.N68_PROGRAMS):
            raise ValueError("both pinned n68 routes required")
        for route in row["routes"]:
            result = route["result"]
            passed = result.get("valid_exact", result.get("valid"))
            if (
                type(passed) is not bool
                or passed != (row["name"] == "positive")
                or result["pairs_checked"] != 2278
                or result["n"] != 68
                or route["source_sha256"] != packets.N68_PROGRAMS[route["source_program"]][1]
            ):
                raise ValueError("n68 actual route verdict or pair coverage differs")
            gap = Fraction(
                result.get("minimum_pair_gap", result.get("minimum_pair_margin_rational"))
            )
            wall = Fraction(
                result.get("minimum_wall_gap", result.get("minimum_wall_clearance_rational"))
            )
            side = Fraction(result.get("container_side", result.get("container_side_rational")))
            if side != Fraction(packets.read_fact(packets.N68, 68)["side"]):
                raise ValueError("n68 deciding route exact side differs")
            if row["name"] == "positive" and (gap < 0 or wall < 0):
                raise ValueError("n68 positive route has a negative diagnostic")
            if row["name"] == "duplicate-square-overlap" and gap != -1:
                raise ValueError("n68 duplicate control lacks its actual negative gap")
            if row["name"] == "outside-container" and wall >= 0:
                raise ValueError("n68 outside control lacks a negative wall clearance")


def external_directory(path: Path) -> Path:
    root = Path("/Volumes/spud-ext1")
    if not root.is_mount() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("mounted external storage destination required")
    path.mkdir(parents=True, exist_ok=True)
    return path


def pack(checkpoint: Path, output: Path) -> None:
    external_directory(output.parent)
    if output.exists():
        raise ValueError("custody asset already exists; use a fresh version")
    files: dict[str, Path] = {}
    for relative in (
        f"{ENGINEERING}/frozen-v2",
        f"{ENGINEERING}/host-v3",
        "squares-425-binding-review",
        "squares-425-complete-input-math-review",
    ):
        for path in (checkpoint / relative).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                if path.is_symlink():
                    raise ValueError("custody includes a source symlink")
                files[path.relative_to(checkpoint).as_posix()] = path
    for relative in (
        f"{ENGINEERING}/couzo_replay.py",
        f"{ENGINEERING}/couzo_refinement_packets.py",
        f"{ENGINEERING}/host-rebind-review-input.json",
        *(
            f"n68-upstream/{packets.N68.prefix}/{name}"
            for name in ("n68.json", *packets.N68_PROGRAMS)
        ),
    ):
        files[relative] = checkpoint / relative
    files["n68-source-geometry.json.gz"] = (
        packets.N68.packet / "receipts/source-geometry.json.gz"
    )
    files["host-rebind-review.md"] = (
        REPO / "docs/project/reviews/review-2026-10-07-refinement-host-rebind.md"
    )
    records = [
        {"path": name, "size": path.stat().st_size, "sha256": digest(path.read_bytes())}
        for name, path in sorted(files.items())
    ]
    manifest_bytes = packets.json_bytes(records)
    if sum(row["size"] for row in records) > MAX_UNPACKED:
        raise ValueError("custody file roster exceeds unpacked ceiling")
    with tarfile.open(output, "w:xz", preset=6) as archive:
        for name, data in [
            ("files.json", manifest_bytes),
            *((name, path.read_bytes()) for name, path in sorted(files.items())),
        ]:
            member = tarfile.TarInfo(name)
            member.size = len(data)
            member.mode = 0o444
            archive.addfile(member, io.BytesIO(data))
    index = compact(checkpoint, files["n68-source-geometry.json.gz"])
    check_index(index)
    index["file_manifest_sha256"] = digest(manifest_bytes)
    packets.save(INDEX, lzma.compress(packets.json_bytes(index)))
    manifest = Manifest(
        "jlevy/squares",
        TAG,
        (
            HostedObject(
                f"attic/refinement-evidence/{ASSET}",
                ASSET,
                output.stat().st_size,
                digest(output.read_bytes()),
            ),
        ),
        "Complete #425/#428 source, frozen protocols, actual full-roster replay, "
        "runtime and accepted review custody; no assurance assigned by publication.",
    )
    packets.save(MANIFEST, render_manifest(manifest, MANIFEST).encode())
    print(
        f"{len(records)} complete files; {sum(row['size'] for row in records)} raw bytes; "
        f"{output.stat().st_size} archived bytes"
    )


def recover(destination: Path, archive_path: Path | None = None) -> Path:
    external_directory(destination)
    manifest = load_manifest(MANIFEST)
    if archive_path is None:
        fetch(manifest, destination, GhClient())
        archive_path = destination / manifest.objects[0].path
    item = manifest.objects[0]
    if (
        archive_path.stat().st_size != item.size
        or digest(archive_path.read_bytes()) != item.sha256
    ):
        raise ValueError("external custody archive differs from pinned manifest")
    index = read_index()
    landing = destination / "recovered"
    if landing.exists():
        raise ValueError("recovery destination exists; select a fresh external directory")
    with tarfile.open(archive_path, "r:xz") as archive:
        members = archive.getmembers()
        if any(
            not member.isfile()
            or PurePosixPath(member.name).is_absolute()
            or ".." in PurePosixPath(member.name).parts
            for member in members
        ):
            raise ValueError("custody archive contains a non-regular or escaping member")
        if (
            len({member.name for member in members}) != len(members)
            or sum(member.size for member in members) > MAX_UNPACKED
        ):
            raise ValueError("custody duplicate member or unpacked ceiling")
        roster_file = archive.extractfile("files.json")
        if roster_file is None:
            raise ValueError("custody file manifest absent")
        manifest_bytes = roster_file.read()
        if digest(manifest_bytes) != index["file_manifest_sha256"]:
            raise ValueError("inner file manifest differs from admitted custody")
        records = json.loads(manifest_bytes)
        if {member.name for member in members} != {
            "files.json",
            *(row["path"] for row in records),
        }:
            raise ValueError("custody member roster differs from full file manifest")
        for row in records:
            stream = archive.extractfile(row["path"])
            if stream is None:
                raise ValueError("custody file missing")
            data = stream.read()
            if len(data) != row["size"] or digest(data) != row["sha256"]:
                raise ValueError("recovered bytes differ from original full file manifest")
            path = landing / row["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    expected = dict(index)
    del expected["file_manifest_sha256"]
    if compact(landing) != expected:
        raise ValueError("recovered actual replay differs from canonical complete admission")
    check_index(index)
    print(
        f"Recovered {len(records)} byte-identical files; all 13 full input/result jobs "
        "bind to the canonical facts"
    )
    return landing


def main() -> None:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    packing = commands.add_parser("pack", allow_abbrev=False)
    packing.add_argument("--checkpoint", type=Path, required=True)
    packing.add_argument("--output", type=Path, required=True)
    recovery = commands.add_parser("recover", allow_abbrev=False)
    recovery.add_argument("--destination", type=Path, required=True)
    recovery.add_argument("--archive", type=Path)
    commands.add_parser("check", allow_abbrev=False)
    args = parser.parse_args()
    if args.command == "pack":
        pack(args.checkpoint, args.output)
    elif args.command == "recover":
        recover(args.destination, args.archive)
    else:
        check_index(read_index())
        print("13 complete replay jobs structurally admitted; no new scientific execution")


if __name__ == "__main__":
    main()
