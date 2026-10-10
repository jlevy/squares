"""Couzo's later reports at n = 375 and 378, beyond the case corpus, at 2d32a6e.

Francisco Couzo's 2d32a6e (2026-10-08T22:12:27Z, parent ffd900d) rewrote two of the
twenty outside-horizon decimal poses that `devtools.couzo_extended_reports` keeps from
ffd900d: `n375.txt` and `n378.txt` now print smaller sides. A later revision is a new
packet (`campaign/result-import.md`, Stage 2), so the ffd900d packet and every pin in it
stay as they are, and its two rows become dated history in the source register. This
packet keeps the later two reports in the same derived-only form: numerical Witness/v2
facts parsed with the existing `parse_couzo` header parser, and attributed metadata,
with `raw_asset_retained: false`. The source states no licence, so no upstream byte
enters Git.

Every digest comparison here crosses one boundary (OR-16): Couzo's repository, whose
bytes stay outside Git. The expected values are the commit, tree and blob identities
that `devtools.couzo_followup_reports` recorded for these two inputs at the same commit
before they were imported, and the complete pinned tree rebuilt to its root. `acquire`
reads a local Git object store, never a checkout, holds each input to that record
before parsing it, and writes the packet. `check-packet` rebuilds each report's text
from the retained facts, the only retained witness of the unretained bytes, and re-runs
the export on it: every retained file must be what the export writes, byte for byte.
That catches an edited, rounded or dropped pose token, a changed side or identity, and
an altered record. No comparison names a file this repository wrote, decides geometry
or pins code.

From `packing/`, with the project interpreter::

    python -m devtools.couzo_extended_updates acquire --git-dir SCRATCH/couzo.git
    python -m devtools.couzo_extended_updates check-packet
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import couzo_extended_reports as extended
from devtools import couzo_followup_reports as followup
from sqpack.witness import validate_witness_document, witness_document, witness_envelope
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/couzo-extended-updates-2026-10-08"
REPOSITORY = extended.REPOSITORY
SOURCE_ID = "couzo-extended-range-updates-2026-10-08"
SOURCE_KEY = "[Couzo extended-range updates 2026-10-08]"
EVIDENCE = "E-couzo-extended-range-update-report"
REVISION = followup.REVISION
TREE = followup.TREE
PARENT = followup.PARENT
COMMITTED = followup.COMMITTED
RETRIEVED = "2026-10-09"
#: The two outside-horizon inputs 2d32a6e changed, as the follow-up packet records them.
COUNTS = followup.OUTSIDE_HORIZON
SCHEMA = "../../../../witnesses/witness.schema.yaml"
ACQUISITION_FORMAT = "external-source-acquisition-v1"
LICENSING_REVIEW = (
    "The pinned tree has no licence file and its README states no reuse terms. "
    "No redistribution permission or licence determination is asserted."
)
QUALIFICATION = (
    "Two author-reported decimal poses at n=375 and n=378, outside the 324-case corpus, "
    "each with a smaller side than the same count's ffd900d report, which stays a dated "
    "historical row. The retained facts rebuild each source TXT blob identity, length "
    "and SHA-256; no raw upstream byte is retained. No geometry, native replay, "
    "confirmation or optimality credit."
)
LIMITATIONS = (
    "Author-reported decimal poses carried verbatim from the source's 2d32a6e text file, "
    "whose bytes are not retained. The method and binary precision describe compatible "
    "coordinate representation, not verified author computation. The source states no "
    "feasibility tolerance or checker. No exact geometry, certificate or optimality "
    "claim. Outside the retained 1..324 case corpus; no geometry replay."
)
SOURCE_FIELDS = {
    "id",
    "source_url",
    "source_commit",
    "committed_utc",
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

#: Reads one pinned tree leaf's complete bytes.
Reader = Callable[[dict[str, Any]], bytes]


class UpdateError(ValueError):
    """Refuse an input, fact or record that is not the pinned later report."""


def fact_name(n: int) -> str:
    return f"facts/n-{n:03d}.yaml"


def fact(n: int, side: str, rows: list[tuple[str, str, str]]) -> dict[str, Any]:
    """The ffd900d packet's fact shape, with this revision's identity and source."""
    witness = extended.fact(n, side, rows)
    witness["id"] = f"W-couzo-extended-update-n{n:03d}"
    witness["claim"]["limitations"] = LIMITATIONS
    witness["source"] = {
        "key": SOURCE_KEY,
        "path": f"packing/resources/web/{PACKET.name}/acquisition/sources.json",
        "url": f"https://github.com/{REPOSITORY}/blob/{REVISION}/n{n}.txt",
        "retrieved": RETRIEVED,
        "revision": REVISION,
    }
    return witness


def recorded_identities() -> tuple[dict[str, Any], dict[int, dict[str, Any]]]:
    """The pinned tree and the two inputs' identities, as the follow-up packet holds them.

    `couzo_followup_reports.check_source` rebuilds that tree to its pinned root before
    anything is read from it.
    """
    source = followup.read_record(followup.sources_path())
    leaves = followup.check_source(source)
    outside = {row["n"]: row for row in source["outside_horizon"]}
    if tuple(outside) != COUNTS:
        raise UpdateError("the follow-up packet records other outside-horizon inputs")
    return leaves, outside


def prior_reports() -> dict[int, dict[str, Any]]:
    """Each count's ffd900d report, as the earlier packet's acquisition record holds it."""
    record = extended.read_json(extended.PACKET / "acquisition/sources.json")
    (source,) = record["sources"]
    if source["id"] != extended.SOURCE_ID or source["source_commit"] != extended.COMMITS[2]:
        raise UpdateError("the earlier packet's identity differs")
    cases = {row["n"]: row for row in source["cases"]}
    return {
        n: {
            "source_id": extended.SOURCE_ID,
            "source_commit": extended.COMMITS[2],
            "side": cases[n]["side"],
            "source_blob": cases[n]["source_blob"],
        }
        for n in COUNTS
    }


def pinned_commit() -> dict[str, Any]:
    return {"sha": REVISION, "tree": {"sha": TREE}, "parents": [{"sha": PARENT}]}


def export_contents(leaves: Any, read: Reader) -> dict[str, bytes]:
    """Hold both inputs to their recorded identities, then write every packet file.

    `leaves` must be the complete pinned tree exactly as the follow-up packet records
    it, and rebuild to the pinned root. Each input's bytes must have the blob identity
    and length that tree and the follow-up record give it, parse as the source's fixed
    layout with binary64 renderings, print the recorded side, and beat the same count's
    ffd900d report by exact comparison. Nothing is written by this function.
    """
    recorded, outside = recorded_identities()
    if type(leaves) is not dict or leaves != recorded:
        raise UpdateError("pinned tree differs from the follow-up packet's record")
    if extended.tree_root(leaves) != TREE:
        raise UpdateError("pinned tree does not rebuild its root")
    priors = prior_reports()
    outputs: dict[str, bytes] = {}
    cases = []
    for n in COUNTS:
        leaf = leaves[f"n{n}.txt"]
        if leaf["sha"] != outside[n]["blob"] or leaf["path"] != outside[n]["file"]:
            raise UpdateError(f"n{n}.txt: identity differs from the follow-up record")
        raw = read(leaf)
        if len(raw) != leaf["size"] or extended.git_identity("blob", raw) != leaf["sha"]:
            raise UpdateError(f"n{n}.txt: bytes differ from the pinned blob identity")
        side, rows = extended.parsed_pose(raw.decode("utf-8"), n)
        if side != outside[n]["printed_side"]:
            raise UpdateError(f"n{n}.txt: printed side differs from the follow-up record")
        prior = priors[n]
        if not Fraction(side) < Fraction(prior["side"]):
            raise UpdateError(f"n={n}: {side} does not beat the ffd900d {prior['side']}")
        text = witness_document(fact(n, side, rows), schema=SCHEMA)
        validate_witness_document(
            load_yaml(text),
            path=PACKET / fact_name(n),
            fallback_schema=ROOT / "witnesses/witness.schema.yaml",
        )
        outputs[fact_name(n)] = text.encode()
        cases.append(
            {
                "n": n,
                "file": leaf["path"],
                "side": side,
                "derived_fact": fact_name(n),
                "source_blob": leaf["sha"],
                "size": leaf["size"],
                "sha256": hashlib.sha256(raw).hexdigest(),
                "supersedes": prior,
            }
        )
    record = {
        "format": ACQUISITION_FORMAT,
        "sources": [
            {
                "id": SOURCE_ID,
                "source_url": f"https://github.com/{REPOSITORY}",
                "source_commit": REVISION,
                "committed_utc": COMMITTED,
                "source_key": SOURCE_KEY,
                "author": "Francisco Couzo",
                "licence": None,
                "retention_policy": "metadata-and-derived-numerical-facts-only",
                "raw_asset_retained": False,
                "licensing_review": LICENSING_REVIEW,
                "cases": cases,
                "custody": {
                    "repository": REPOSITORY,
                    "standing_horizon": 324,
                    "counts": list(COUNTS),
                    "commit": pinned_commit(),
                    "tree": {path: leaves[path] for path in sorted(leaves)},
                },
                "qualification": QUALIFICATION,
            }
        ],
    }
    outputs["acquisition/sources.json"] = (
        json.dumps(record, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    return outputs


def ensure_private(path: Path) -> None:
    """Refuse a path that leaves the repository or passes through a symlink inside it."""
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise UpdateError("derived packet files must remain ordinary and private")
    for parent in (path, *path.parents):
        if parent == REPO:
            break
        if parent.is_symlink():
            raise UpdateError("derived packet files must remain ordinary and private")


def acquire(git_dir: Path, destination: Path = PACKET) -> None:
    """Read the pinned commit from a local object store and write a fresh packet."""
    ensure_private(destination)
    if (destination / "facts").exists() or (destination / "acquisition").exists():
        raise UpdateError("acquisition writes a fresh derived packet only")
    followup.read_commit(git_dir)
    leaves = followup.read_tree(git_dir)
    outputs = export_contents(leaves, lambda leaf: followup.read_blob(git_dir, leaf))
    for name, raw in outputs.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        ensure_private(target.parent)
        with atomic_output_file(target) as temporary:
            temporary.write_bytes(raw)


def retained_bytes(path: Path) -> bytes:
    ensure_private(path)
    if not path.is_file():
        raise UpdateError(f"{path.name}: missing derived packet file")
    with path.open("rb") as stream:
        raw = stream.read(extended.MAX_DECODED_BYTES + 1)
    if len(raw) > extended.MAX_DECODED_BYTES:
        raise UpdateError(f"{path.name}: derived packet file exceeds its byte ceiling")
    return raw


def reconstructed_text(n: int, raw: bytes, path: Path) -> str:
    """One report's complete source text, rebuilt from its retained numerical fact."""
    document = load_yaml(raw.decode("utf-8"))
    if (
        not isinstance(document, dict)
        or document.get("softschema") != witness_envelope({}, schema=SCHEMA)["softschema"]
    ):
        raise UpdateError(f"n={n}: derived fact fixed schema envelope differs")
    witness = validate_witness_document(
        document, path=path, fallback_schema=ROOT / "witnesses/witness.schema.yaml"
    )
    if witness.get("n") != n or len(witness["squares"]) != n:
        raise UpdateError(f"n={n}: derived fact is not a complete pose")
    rows = [
        (square["center"][0], square["center"][1], square["angle"])
        for square in witness["squares"]
    ]
    return extended.canonical_pose(n, witness["side"], rows)


def check_packet(destination: Path = PACKET) -> dict[int, str]:
    """Rebuild both source texts from the facts, re-export, and require every byte.

    Returns each count's side, the claim the source register holds it to.
    """
    ensure_private(destination)
    expected = {"README.md", "acquisition/sources.json", *(fact_name(n) for n in COUNTS)}
    files = set()
    for path in destination.rglob("*"):
        ensure_private(path)
        if path.is_file():
            files.add(path.relative_to(destination).as_posix())
    if files != expected:
        raise UpdateError("unexpected or missing derived packet file")
    retained = {name: retained_bytes(destination / name) for name in expected - {"README.md"}}
    record = extended.metadata_object(retained["acquisition/sources.json"])
    sources = record.get("sources")
    if (
        set(record) != {"format", "sources"}
        or type(sources) is not list
        or len(sources) != 1
        or type(sources[0]) is not dict
        or set(sources[0]) != SOURCE_FIELDS
        or type(sources[0]["custody"]) is not dict
        or sources[0]["custody"].get("commit") != pinned_commit()
    ):
        raise UpdateError("one complete derived acquisition record is required")
    texts = {
        f"n{n}.txt": reconstructed_text(
            n, retained[fact_name(n)], destination / fact_name(n)
        ).encode()
        for n in COUNTS
    }
    rebuilt = export_contents(
        sources[0]["custody"].get("tree"), lambda leaf: texts[leaf["path"]]
    )
    for name, raw in sorted(rebuilt.items()):
        if retained[name] != raw:
            raise UpdateError(f"{name} differs from the export of the pinned reports")
    return {case["n"]: case["side"] for case in sources[0]["cases"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    acquiring = commands.add_parser("acquire")
    acquiring.add_argument("--git-dir", type=Path, required=True)
    commands.add_parser("check-packet")
    args = parser.parse_args()
    if args.command == "acquire":
        acquire(args.git_dir)
        print("Two derived reports and their source metadata retained; no raw upstream bytes")
    else:
        claims = check_packet()
        print(
            f"{len(claims)} later derived source claims rebuilt byte for byte; "
            "no geometry or standing credit"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
