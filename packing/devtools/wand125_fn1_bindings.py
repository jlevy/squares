"""Bind FN-1's eight original gzip inputs to the existing check2 records.

This reads complete retained inputs and old receipts afresh. It decides only byte
custody: no geometric verifier runs, bounds, ratings, or native records change.
Run ``python -m devtools.wand125_fn1_bindings`` from packing/.
"""

from __future__ import annotations

import hashlib
import json
import sys
import zlib
from pathlib import Path
from typing import Any

from devtools import acquire_source
from devtools import audit_wand125_declared_net as declared
from devtools.retained_data import compressed_path, git_blob, gunzip_bytes, read_retained_bytes

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "wand125-fn1-input-bindings-2026-10-07"
EXISTING = WEB / "wand125-mixed-bounds-check2-2026-10-06"
SOURCE_REVISION = "b73473fcf60421222b739294d3f7d9c4a8b8da07"
PRIOR_REVISION = "2fad66e02f54a492835dc41ac37a9184e1e7a662"
CERTIFICATE_KEYS = (
    "n19-L4825",
    "n20-L4905",
    "n26-L5545",
    "n27-L56435",
    "n28-L5735",
    "n30-L58835",
    "n39-L665",
    "n41-L6775",
)
MAX_INPUT_BYTES = 16 * 1024 * 1024
MAX_DECOMPRESSED_BYTES = 64 * 1024 * 1024


class BindingError(ValueError):
    """A complete source, input, or native-record binding is missing or different."""


def require(condition: object, message: str) -> None:
    if not condition:
        raise BindingError(message)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _json(data: bytes) -> Any:
    return json.loads(data, object_pairs_hook=_pairs)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _private_path(path: Path, repository: Path) -> None:
    require(
        path.resolve().is_relative_to(repository.resolve()), "input resolves outside repository"
    )
    try:
        relative = path.relative_to(repository)
    except ValueError as error:
        raise BindingError("input is not a declared repository path") from error
    cursor = repository
    for part in relative.parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), "input must remain an independent private path")


def _read(path: Path, repository: Path, limit: int = MAX_INPUT_BYTES) -> bytes:
    _private_path(path, repository)
    require(path.is_file(), f"input must be an independent regular file: {path}")
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    require(len(data) <= limit, f"input exceeds {limit} bytes: {path}")
    return data


def _retained(path: Path, repository: Path) -> bytes:
    # Both representations are inputs when both exist; neither can be an outside link.
    candidates = (path, compressed_path(path))
    found = [
        candidate for candidate in candidates if candidate.exists() or candidate.is_symlink()
    ]
    require(bool(found), f"retained input is absent: {path}")
    for candidate in found:
        _private_path(candidate, repository)
        require(candidate.is_file(), "retained input is not a regular private file")
    return read_retained_bytes(path, limit=MAX_DECOMPRESSED_BYTES)


def verify(
    packet: Path | None = None,
    existing: Path | None = None,
    repository: Path | None = None,
) -> dict[str, Any]:
    """Check the full eight-case custody chain without cached admissions."""
    packet = PACKET if packet is None else packet
    existing = EXISTING if existing is None else existing
    repository = REPO if repository is None else repository
    _private_path(packet, repository)
    for path in packet.rglob("*"):
        _private_path(path, repository)
    problems = acquire_source.check(packet, repository)
    require(not problems, f"source acquisition differs: {problems}")
    source = _json(_read(packet / acquire_source.RECORD, repository))["sources"][0]
    require(source["source_commit"] == SOURCE_REVISION, "source provenance changed")
    upstream = packet / "square-packing-bounds"
    manifest = _json(_read(upstream / "verification/fn1/input-bindings.json", repository))
    require(
        set(manifest) == {"schema", "retained_revision", "scope", "entries"},
        "manifest keys changed",
    )
    require(manifest["schema"] == "recorded-gzip-input-binding-v1", "manifest schema changed")
    require(manifest["retained_revision"] == PRIOR_REVISION, "prior source provenance changed")
    require(
        isinstance(manifest["scope"], str) and bool(manifest["scope"]), "manifest scope missing"
    )
    entries = manifest["entries"]
    require(
        isinstance(entries, list) and len(entries) == len(CERTIFICATE_KEYS),
        "full eight-input roster required",
    )
    expected_names = [declared.CERTIFICATES[key].name for key in CERTIFICATE_KEYS]
    require(
        all(isinstance(entry, dict) for entry in entries), "manifest entries must be objects"
    )
    require(
        [entry.get("certificate") for entry in entries] == expected_names,
        "certificate roster or order changed",
    )
    require(
        source.get("original_gzip")
        == [
            f"square-packing-bounds/certificates/{name}/check2/recorded-input.json.gz"
            for name in expected_names
        ],
        "original gzip roster changed",
    )
    prior_record = _json(_read(existing / acquire_source.RECORD, repository))
    require(
        prior_record["sources"][0]["source_commit"] == PRIOR_REVISION,
        "existing source pin changed",
    )
    outcomes = []
    for key, entry in zip(CERTIFICATE_KEYS, entries, strict=True):
        require(
            set(entry)
            == {
                "certificate",
                "input_file",
                "published_candidate",
                "compressed_sha256",
                "decompressed_sha256",
                "candidate_digest",
                "size_bytes",
            },
            f"{key}: entry keys changed",
        )
        name = declared.CERTIFICATES[key].name
        original = f"certificates/{name}/check2/recorded-input.json.gz"
        candidate_path = f"certificates/{name}/candidate.json"
        require(
            entry["input_file"] == original and entry["published_candidate"] == candidate_path,
            f"{key}: input path changed",
        )
        raw = _read(upstream / original, repository)
        require(
            type(entry["size_bytes"]) is int and entry["size_bytes"] == len(raw),
            f"{key}: compressed byte count changed",
        )
        old_directory = existing / "square-packing-bounds/certificates" / name
        receipt = _json(_retained(old_directory / "check2/receipt.json", repository))
        compressed = _sha(raw)
        require(
            compressed
            == entry["compressed_sha256"]
            == declared.UNPUBLISHED_RUN_INPUTS.get(key)
            == receipt["verifier_summary"]["premises"]["input_sha256"],
            f"{key}: compressed input is not the original logged bytes",
        )
        decoded = gunzip_bytes(raw, limit=MAX_DECOMPRESSED_BYTES, name=key)
        candidate = _retained(old_directory / "candidate.json", repository)
        require(
            decoded == candidate,
            f"{key}: decompression differs from the retained candidate bytes",
        )
        decoded_digest = _sha(decoded)
        require(
            decoded_digest == entry["decompressed_sha256"] == receipt["file_sha256"],
            f"{key}: decompressed candidate hash changed",
        )
        mathematical = declared.semantic_digest(_json(decoded))
        require(
            mathematical == entry["candidate_digest"] == receipt["candidate_digest"],
            f"{key}: mathematical candidate digest changed",
        )
        outcomes.append(
            {
                "certificate": name,
                "compressed_sha256": compressed,
                "decompressed_sha256": decoded_digest,
                "candidate_digest": mathematical,
                "compressed_bytes": len(raw),
                "source_blob": git_blob(raw),
            }
        )
    return {
        "schema": "wand125-fn1-input-binding/v1",
        "input_count": len(outcomes),
        "geometry_replay": False,
        "bounds_changed": False,
        "entries": outcomes,
    }


def private_input_paths() -> tuple[Path, ...]:
    """Explicit complete scientific inputs for an independently mutable worker copy."""
    source = PACKET / "square-packing-bounds"
    paths = [
        PACKET / "README.md",
        PACKET / acquire_source.DECLARATION,
        PACKET / acquire_source.RECORD,
        PACKET / acquire_source.MANIFEST,
        source / "LICENSE",
        source / "verification/fn1/README.md",
        source / "verification/fn1/input-bindings.json",
        EXISTING / acquire_source.RECORD,
    ]
    for key in CERTIFICATE_KEYS:
        name = declared.CERTIFICATES[key].name
        paths.append(source / "certificates" / name / "check2/recorded-input.json.gz")
        old = EXISTING / "square-packing-bounds/certificates" / name
        # These are the fixed stored names in the previously acquired check2 packet.
        paths.extend((old / "candidate.json.gz", old / "check2/receipt.json"))
    return tuple(paths)


def main() -> int:
    try:
        result = verify()
    except (OSError, ValueError, KeyError, TypeError, zlib.error) as error:
        print(f"FN1_INPUT_BINDING_REFUSED: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
