"""Retain derived decimal facts from Couzo's twenty outside-horizon reports.

The complete ordinary-source preparation stays local. This module checks its pinned
Git custody without executing source programs, and exports numerical Witness/v2 facts
and attributed metadata only. It neither verifies geometry nor changes any case.

Every digest comparison here crosses one boundary (OR-16): Francisco Couzo's repository,
whose source bytes stay outside Git because redistribution is not established. The
expected values are the three commit and tree ids pinned at review in `PINS`, and the
blob ids those trees bind once each is rebuilt in full against its pinned root.
`check_ordinary` holds the acquired commit records and complete blob bytes against them,
which catches a substituted, altered or mislabelled source file. `check_packet` rebuilds
the retained trees and each report's text from the retained facts, and holds the text
against its tree-bound blob id, the only retained witness of the unretained bytes, which
catches an edited, rounded or dropped pose token. The retained commit block was written
from `PINS`, so it is compared whole rather than label by label. No comparison names a
file this repository wrote, decides geometry or pins code;
`devtools/integrity-ceremony.yaml` admits the module as a download.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import math
import re
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.upper_bound_packets import parse_couzo
from sqpack.witness import validate_witness_document, witness_document, witness_envelope
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/couzo-extended-reports-2026-10-09"
REPOSITORY = "franciscouzo/square-packing"
SOURCE_ID = "couzo-extended-range-reports-2026-10-09"
SOURCE_KEY = "[Couzo extended-range reports 2026-10-09]"
EVIDENCE = "E-couzo-extended-range-report"
REVIEWED = "2026-10-09"
LICENSING_REVIEW = "No redistribution permission or licence determination is asserted."
COMMITS = (
    "b10ad360f80ee82580e75330417e0171d1a9fb81",
    "74f7e8b3f8df9cd5c2277b54d3cd7fe00769a998",
    "ffd900dfff6d2674ad995359208c2f0714915c82",
)
PINS = {
    COMMITS[0]: (
        "a053167fa31856d71f9f08167f886ef48a264b76",
        "6042c56b43b64c09fe5a32c64879e698f399beaf",
    ),
    COMMITS[1]: ("e8e3f4abfdb85c35674619f1600bf21e1a913c0a", COMMITS[0]),
    COMMITS[2]: ("4f168283859262d0d813cc07e5f8fefef8b682a9", COMMITS[1]),
}
COUNTS = (327, 332, *range(335, 343), 364, 369, *range(372, 380))
REMOVED = (123, 126, 130, 154, 199, 207, 209, 236, 237, 238, 239, 263, 302, 303)
FORMAT = "couzo-extended-ordinary-source-v1"
ACQUISITION_FORMAT = "external-source-acquisition-v1"
MAX_COMPRESSED_BYTES = 1_000_000
MAX_DECODED_BYTES = 4_000_000
MAX_XZ_MEMORY = 32 * 1024 * 1024
MAX_SOURCE_BYTES = 8_000_000
MAX_LITERAL_CHARS = 128
SHA = re.compile(r"[0-9a-f]{40}")
ROW_KEYS = {"path", "mode", "type", "sha", "size", "url"}
CUSTODY_KEYS = {"repository", "standing_horizon", "counts", "trees", "inputs", "commits"}
SOURCE_KEYS = {
    "id",
    "source_url",
    "source_commit",
    "source_key",
    "author",
    "licence",
    "retention_policy",
    "raw_asset_retained",
    "licensing_review",
    "cases",
    "custody",
    "qualification",
}
QUALIFICATION = (
    "Twenty author-reported decimal poses, outside the 324-case corpus. "
    "No geometry, native replay, confirmation or optimality credit. "
    "Git trees bind paths/modes/blob identities, not author/message or size metadata. "
    "The local ordinary preparation checks every selected blob's complete bytes/size; "
    "this derived-only packet reconstructs the twenty current TXT identities. "
    "The other source roles retain pinned identities, not their raw bytes."
)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON number: {value}")


def finite_number(token: str) -> float:
    value = float(token)
    if not math.isfinite(value):
        raise ValueError("nonfinite JSON number")
    return value


def decode_xz(raw: bytes) -> dict[str, Any]:
    """One bounded XZ stream, strict UTF-8 and duplicate-refusing finite JSON."""
    if len(raw) > MAX_COMPRESSED_BYTES:
        raise ValueError("compressed source exceeds its byte ceiling")
    decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=MAX_XZ_MEMORY)
    try:
        data = decoder.decompress(raw, max_length=MAX_DECODED_BYTES + 1)
    except lzma.LZMAError as error:
        raise ValueError("invalid or memory-exceeding XZ source") from error
    if len(data) > MAX_DECODED_BYTES or not decoder.eof or decoder.unused_data:
        raise ValueError("oversized, truncated or trailing XZ source")
    value = json.loads(
        data.decode("utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
        parse_float=finite_number,
    )
    if type(value) is not dict:
        raise ValueError("ordinary source must be a JSON object")
    return value


def git_identity(kind: str, raw: bytes) -> str:
    return hashlib.sha1(
        f"{kind} {len(raw)}\0".encode() + raw, usedforsecurity=False
    ).hexdigest()


def path_parts(path: str) -> list[str]:
    if type(path) is not str or not path or "\\" in path:
        raise ValueError("invalid canonical Git path")
    parts = path.split("/")
    if any(part in {"", ".", ".."} for part in parts) or any(
        ord(char) < 32 or ord(char) == 127 for char in path
    ):
        raise ValueError("invalid canonical Git path")
    path.encode("utf-8")
    return parts


def tree_root(leaves: dict[str, Any]) -> str:
    """Reconstruct every nested Git tree with Git's bytewise directory ordering."""
    if type(leaves) is not dict or not leaves:
        raise ValueError("incomplete source tree")
    root: dict[str, Any] = {}
    for path, row in leaves.items():
        parts = path_parts(path)
        if (
            type(row) is not dict
            or set(row) != ROW_KEYS
            or row["path"] != path
            or row["type"] != "blob"
            or row["mode"] not in {"100644", "100755"}
            or type(row["size"]) is not int
            or not 0 <= row["size"] <= MAX_SOURCE_BYTES
            or type(row["sha"]) is not str
            or SHA.fullmatch(row["sha"]) is None
            or row["url"] != f"https://api.github.com/repos/{REPOSITORY}/git/blobs/{row['sha']}"
        ):
            raise ValueError("invalid source tree leaf")
        parent = root
        for part in parts[:-1]:
            child = parent.setdefault(part, {})
            if type(child) is not dict:
                raise ValueError("Git file/directory collision")
            parent = child
        if parts[-1] in parent:
            raise ValueError("duplicate Git path or file/directory collision")
        parent[parts[-1]] = (row["mode"], row["sha"])

    def encode(entries: dict[str, Any]) -> str:
        ordered = sorted(
            entries,
            key=lambda name: name.encode() + (b"/" if type(entries[name]) is dict else b""),
        )
        content = bytearray()
        for name in ordered:
            value = entries[name]
            mode, sha = ("40000", encode(value)) if type(value) is dict else value
            content.extend(mode.encode() + b" " + name.encode() + b"\0" + bytes.fromhex(sha))
        return git_identity("tree", bytes(content))

    return encode(root)


def input_roster() -> set[tuple[str, str, str]]:
    return (
        {(sha, "README.md", "source-context") for sha in COMMITS}
        | {
            (COMMITS[2], f"n{n}.{suffix}", "current-outside-horizon")
            for n in COUNTS
            for suffix in ("txt", "svg")
        }
        | {(COMMITS[0], f"n378.{suffix}", "superseded-n378") for suffix in ("txt", "svg")}
        | {
            (COMMITS[0], f"n{n}.{suffix}", "removed-source-history")
            for n in REMOVED
            for suffix in ("txt", "svg")
        }
    )


def check_structure(packet: dict[str, Any], *, acquired: bool = True) -> set[str]:
    """The pinned lineage, every tree rebuilt against its root, and the complete roster.

    An acquired preparation's commit records are held against `PINS` here. The retained
    packet's commit block was written from `PINS` by `export_contents`, so `check_packet`
    compares it whole instead and passes `acquired=False`; its trees are still rebuilt.
    """
    if (
        packet.get("repository") != REPOSITORY
        or type(packet.get("standing_horizon")) is not int
        or packet["standing_horizon"] != 324
        or packet.get("counts") != list(COUNTS)
        or any(type(n) is not int for n in packet["counts"])
        or type(packet.get("commits")) is not dict
        or set(packet["commits"]) != set(COMMITS)
        or type(packet.get("trees")) is not dict
        or set(packet["trees"]) != set(COMMITS)
    ):
        raise ValueError("fixed source scope or lineage differs")
    for sha, (root, parent) in PINS.items():
        commit = packet["commits"][sha]
        if acquired and (
            type(commit) is not dict
            or commit.get("sha") != sha
            or type(commit.get("tree")) is not dict
            or commit["tree"].get("sha") != root
            or type(commit.get("parents")) is not list
            or [item.get("sha") for item in commit["parents"] if type(item) is dict] != [parent]
            or len(commit["parents"]) != 1
        ):
            raise ValueError("pinned Git root or parent differs")
        if tree_root(packet["trees"][sha]) != root:
            raise ValueError("pinned Git root or parent differs")
    inputs = packet.get("inputs")
    if type(inputs) is not list:
        raise ValueError("missing complete input roster")
    triples = []
    for row in inputs:
        if type(row) is not dict or set(row) != ROW_KEYS | {"commit", "role"}:
            raise ValueError("invalid input descriptor")
        triple = (row["commit"], row["path"], row["role"])
        if any(type(item) is not str for item in triple):
            raise ValueError("invalid input identity")
        triples.append(triple)
        leaf = packet["trees"].get(row["commit"], {}).get(row["path"])
        if leaf != {key: row[key] for key in ROW_KEYS}:
            raise ValueError("input differs from its pinned tree")
    if len(triples) != len(set(triples)) or set(triples) != input_roster():
        raise ValueError("complete role roster differs")
    for sha in COMMITS[1:]:
        if any(
            f"n{n}.{suffix}" in packet["trees"][sha]
            for n in REMOVED
            for suffix in ("txt", "svg")
        ):
            raise ValueError("removed input remains in a later tree")
    if sum(row["size"] for row in inputs) > MAX_SOURCE_BYTES:
        raise ValueError("complete source occurrences exceed byte ceiling")
    return {row["sha"] for row in inputs}


def check_ordinary(packet: dict[str, Any]) -> None:
    if (
        set(packet)
        != {
            "format",
            "repository",
            "standing_horizon",
            "counts",
            "commits",
            "trees",
            "inputs",
            "blobs",
            "licensing",
            "qualification",
        }
        or packet["format"] != FORMAT
    ):
        raise ValueError("unexpected ordinary-source format")
    referenced = check_structure(packet)
    if type(packet["blobs"]) is not dict or set(packet["blobs"]) != referenced:
        raise ValueError("missing or orphan source blob")
    for row in packet["inputs"]:
        text = packet["blobs"][row["sha"]]
        if type(text) is not str:
            raise ValueError("source blob must retain complete UTF-8 text")
        raw = text.encode("utf-8")
        if len(raw) != row["size"] or git_identity("blob", raw) != row["sha"]:
            raise ValueError("source blob identity or size differs")


def read_ordinary(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ValueError("ordinary source must be an ordinary file")
    with path.open("rb") as stream:
        raw = stream.read(MAX_COMPRESSED_BYTES + 1)
    packet = decode_xz(raw)
    check_ordinary(packet)
    return packet


def canonical_pose(n: int, side: str, rows: list[tuple[str, str, str]]) -> str:
    """The fixed source header/row layout, reconstructed from numerical facts."""
    return f"# n = {n}\n# s = {side}\n# x y theta(rad)\n" + "".join(
        " ".join(row) + "\n" for row in rows
    )


def parsed_pose(text: str, expected_n: int) -> tuple[str, list[tuple[str, str, str]]]:
    n, side, rows = parse_couzo(text)
    if n != expected_n or canonical_pose(n, side, rows) != text:
        raise ValueError("source count or canonical pose layout differs")
    tokens = [side, *(token for row in rows for token in row)]
    try:
        if any(len(token) > MAX_LITERAL_CHARS for token in tokens):
            raise ValueError("oversized numerical literal")
        values = [Decimal(token) for token in tokens]
    except InvalidOperation as error:
        raise ValueError("invalid decimal pose") from error
    if any(not value.is_finite() or abs(value.adjusted()) > 1000 for value in values):
        raise ValueError("nonfinite or unbounded decimal pose")
    if values[0] <= 0:
        raise ValueError("reported side must be positive")
    return side, rows


def fact(n: int, side: str, rows: list[tuple[str, str, str]]) -> dict[str, Any]:
    claim = {
        "coordinate_provenance": "reported",
        "method": "numerical-f64",
        "precision": {
            "binary_bits": 53,
            "rounding": (
                "observed binary64-compatible coordinate encoding; "
                "decimal tokens retained verbatim, author computation precision unverified"
            ),
        },
        "tolerance": "not stated by the source",
        "limitations": (
            "Author-reported decimal poses carried verbatim from the source's text file, "
            "whose bytes are not retained. The method and binary precision describe "
            "compatible coordinate representation, not verified author computation. "
            "The source states no feasibility tolerance or checker. "
            "No exact geometry, certificate or optimality claim. "
            "Outside the retained 1..324 case corpus; no geometry replay."
        ),
    }
    return {
        "id": f"W-couzo-extended-n{n:03d}",
        "n": n,
        "side": side,
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "radians",
        },
        "squares": [
            {"id": i, "center": [x, y], "angle": theta}
            for i, (x, y, theta) in enumerate(rows, start=1)
        ],
        "claim": claim,
        "source": {
            "key": SOURCE_KEY,
            "path": f"packing/resources/web/{PACKET.name}/acquisition/sources.json",
            "url": f"https://github.com/{REPOSITORY}/blob/{COMMITS[2]}/n{n}.txt",
            "retrieved": REVIEWED,
            "revision": COMMITS[2],
        },
    }


def export_contents(packet: dict[str, Any]) -> dict[str, bytes]:
    """Preflight complete custody and facts before producing any output bytes."""
    check_ordinary(packet)
    outputs = {}
    cases = []
    for n in COUNTS:
        row = packet["trees"][COMMITS[2]][f"n{n}.txt"]
        side, poses = parsed_pose(packet["blobs"][row["sha"]], n)
        text = witness_document(
            fact(n, side, poses), schema="../../../../witnesses/witness.schema.yaml"
        )
        validate_witness_document(
            load_yaml(text),
            path=PACKET / "facts" / f"n-{n:03d}.yaml",
            fallback_schema=ROOT / "witnesses/witness.schema.yaml",
        )
        outputs[f"facts/n-{n:03d}.yaml"] = text.encode()
        cases.append(
            {
                "n": n,
                "side": side,
                "file": f"n{n}.txt",
                "derived_fact": f"facts/n-{n:03d}.yaml",
                "source_blob": row["sha"],
            }
        )
    custody = {
        key: deepcopy(packet[key])
        for key in ("repository", "standing_horizon", "counts", "trees", "inputs")
    }
    custody["commits"] = {
        sha: {"sha": sha, "tree": {"sha": root}, "parents": [{"sha": parent}]}
        for sha, (root, parent) in PINS.items()
    }
    record = {
        "format": ACQUISITION_FORMAT,
        "sources": [
            {
                "id": SOURCE_ID,
                "source_url": f"https://github.com/{REPOSITORY}",
                "source_commit": COMMITS[2],
                "source_key": SOURCE_KEY,
                "author": "Francisco Couzo",
                "licence": None,
                "retention_policy": "metadata-and-derived-numerical-facts-only",
                "raw_asset_retained": False,
                "licensing_review": LICENSING_REVIEW,
                "cases": cases,
                "custody": custody,
                "qualification": QUALIFICATION,
            }
        ],
    }
    outputs["acquisition/sources.json"] = (
        json.dumps(record, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    return outputs


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        raw = stream.read(MAX_DECODED_BYTES + 1)
    if len(raw) > MAX_DECODED_BYTES:
        raise ValueError("derived metadata exceeds byte ceiling")
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
        parse_float=finite_number,
    )
    if type(value) is not dict:
        raise ValueError("derived metadata must be an object")
    return value


def ordinary_packet_file(path: Path, destination: Path) -> None:
    if not path.is_file() or not path.resolve().is_relative_to(destination.resolve()):
        raise ValueError("derived packet files must remain ordinary and private")
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise ValueError("derived packet files cannot use symlinks")
        if parent == REPO:
            break


def check_packet(destination: Path = PACKET) -> dict[int, str]:
    """Reconstruct each complete source TXT identity from retained numerical facts."""
    if destination.is_symlink() or not destination.resolve().is_relative_to(REPO.resolve()):
        raise ValueError("derived packet must remain private")
    metadata = destination / "acquisition/sources.json"
    ordinary_packet_file(metadata, destination)
    value = read_json(metadata)
    if set(value) != {"format", "sources"} or value["format"] != ACQUISITION_FORMAT:
        raise ValueError("derived acquisition format differs")
    entries = value["sources"]
    if type(entries) is not list or len(entries) != 1 or type(entries[0]) is not dict:
        raise ValueError("one complete source record is required")
    source = entries[0]
    if (
        set(source) != SOURCE_KEYS
        or source.get("id") != SOURCE_ID
        or source.get("source_key") != SOURCE_KEY
        or source.get("source_url") != f"https://github.com/{REPOSITORY}"
        or source.get("source_commit") != COMMITS[2]
        or source.get("author") != "Francisco Couzo"
        or source.get("qualification") != QUALIFICATION
        or source.get("licence") is not None
        or source.get("raw_asset_retained") is not False
        or source.get("retention_policy") != "metadata-and-derived-numerical-facts-only"
        or source.get("licensing_review") != LICENSING_REVIEW
    ):
        raise ValueError("source or derived-only retention differs")
    custody = source.get("custody")
    if type(custody) is not dict or set(custody) != CUSTODY_KEYS:
        raise ValueError("derived custody cannot retain raw source fields")
    expected_commits = {
        sha: {"sha": sha, "tree": {"sha": root}, "parents": [{"sha": parent}]}
        for sha, (root, parent) in PINS.items()
    }
    if custody["commits"] != expected_commits:
        raise ValueError("derived commit metadata differs")
    check_structure(custody, acquired=False)
    cases = source.get("cases")
    if type(cases) is not list or [row.get("n") for row in cases if type(row) is dict] != list(
        COUNTS
    ):
        raise ValueError("complete derived count roster differs")
    expected_paths = {
        "acquisition/sources.json",
        "README.md",
        *(f"facts/n-{n:03d}.yaml" for n in COUNTS),
    }
    files = {
        path.relative_to(destination).as_posix()
        for path in destination.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if files != expected_paths:
        raise ValueError("unexpected or missing derived packet file")
    ordinary_packet_file(destination / "README.md", destination)
    claims = {}
    for n, row in zip(COUNTS, cases, strict=True):
        if (
            type(row) is not dict
            or set(row) != {"n", "side", "file", "derived_fact", "source_blob"}
            or type(row["n"]) is not int
            or type(row["side"]) is not str
            or row["file"] != f"n{n}.txt"
            or row["derived_fact"] != f"facts/n-{n:03d}.yaml"
        ):
            raise ValueError("derived source descriptor differs")
        path = destination / row["derived_fact"]
        ordinary_packet_file(path, destination)
        with path.open("rb") as stream:
            raw = stream.read(MAX_COMPRESSED_BYTES + 1)
        if len(raw) > MAX_COMPRESSED_BYTES:
            raise ValueError("derived fact exceeds byte ceiling")
        document = load_yaml(raw.decode("utf-8"))
        if (
            not isinstance(document, dict)
            or document.get("softschema")
            != witness_envelope({}, schema="../../../../witnesses/witness.schema.yaml")[
                "softschema"
            ]
        ):
            raise ValueError("derived fact fixed schema envelope differs")
        witness = validate_witness_document(
            document, path=path, fallback_schema=ROOT / "witnesses/witness.schema.yaml"
        )
        poses = [
            (square["center"][0], square["center"][1], square["angle"])
            for square in witness["squares"]
        ]
        reconstructed = canonical_pose(n, row["side"], poses)
        side, poses = parsed_pose(reconstructed, n)
        leaf = source["custody"]["trees"][COMMITS[2]][row["file"]]
        identity = git_identity("blob", reconstructed.encode())
        if (
            identity != leaf["sha"]
            or len(reconstructed.encode()) != leaf["size"]
            or row["source_blob"] != identity
        ):
            raise ValueError("derived pose differs from the complete pinned source")
        expected = witness_envelope(
            fact(n, side, poses), schema="../../../../witnesses/witness.schema.yaml"
        )
        if document != expected:
            raise ValueError("derived witness metadata differs")
        claims[n] = side
    return claims


def export(path: Path, destination: Path = PACKET) -> None:
    if (
        destination.exists()
        or not destination.resolve().is_relative_to(REPO.resolve())
        or any(parent.is_symlink() for parent in destination.parents)
    ):
        raise ValueError("export requires a new private packet directory")
    outputs = export_contents(read_ordinary(path))
    for name, raw in outputs.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(target) as temporary:
            temporary.write_bytes(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-ordinary", type=Path)
    mode.add_argument("--export", type=Path)
    mode.add_argument("--check-packet", action="store_true")
    parser.add_argument("--destination", type=Path, default=PACKET)
    args = parser.parse_args()
    if args.check_ordinary:
        packet = read_ordinary(args.check_ordinary)
        print(f"{len(packet['inputs'])} complete source roles; no scientific admission")
    elif args.check_packet:
        claims = check_packet(args.destination)
        print(f"{len(claims)} complete derived source claims; no geometry or standing credit")
    else:
        export(args.export, args.destination)
        print(
            "Derived facts and source metadata retained; "
            "no raw upstream bytes or geometry credit"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
