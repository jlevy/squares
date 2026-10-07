"""The n17 census under certified sub-patterns (H-267): what the admitted certificates exclude.

What it counts. On the unique-state cover `ring-3-voronoi-8-tabbed-unique` at cap
1169/250 there are 346,104 closed capacity-one states in 43,593 D4 orbits (H-266). A
sub-pattern proved infeasible excludes every state that contains it in any D4 image. This
tool counts, exactly, the states and orbits that survive every sub-pattern its ledger
*admits*, with the selector's consumer (`select_n17_sub_patterns.consume`), and nothing
else enters that count.

The ledger. A YAML file declares one entry per certified class:

- `name`, and `cells`: the pattern's cell names on the cover.
- `certifier`: `kernel` (the ownership-induction kernel, `check_n17_subpattern`) or
  `branch-and-bound` (the interval branch and bound, `pilot_n17_subpattern_bb`).
- `receipt`: the certifier's receipt. A `pending` entry may leave it null while its
  receipt is being produced.
- `certificate`: the directory of the saved proof objects, or null where the certifier
  keeps none. The objects themselves are hosted outside Git as release assets and listed
  in the ledger's `data_manifest`, a hosted-data manifest in `packing/hosted/` (contract
  `packing.squares:HostedData/v1`), which this tool reads through `sqpack.hosted_data`.
  The directory keeps the small files, such as the verification receipt.
- `status`: `admitted` or `pending`, and `evidence`: the document that admits the entry, a
  review or the experiment record holding a reviewed verifier's full pass, required once it
  is admitted. The census checks only that the file exists. It is a pointer for readers,
  not a check: what admits an entry is its verification.
- `verification`, required once admitted: `{receipt, verifier}`, the standing verifier's
  receipt (`verify_n17_kernel_certificate` or `verify_n17_bb_certificate`, written
  separately from the producers) and the `id` of the reviewed verifier listing it ran
  under.

The ledger's header lists, under `verifiers`, each reviewed verifier as `{id, certifier,
path, version, review}`: a name for the listing, the kind of certificate it checks, the
file, the version a review admitted, and the review document. `version` is information
for the reader (the revision the review read); nothing resolves it. A verification
counts under the listing its entry names when the listing checks the entry's kind of
certificate, and, where the receipt records which file ran (`devtools.provenance`), when
that file is the listing's path and its bytes were not recorded as uncommitted. That the
receipt ran the listed version is the reviewer's claim, recorded in the ledger; the
census reads no history (OR-18).

A listing may also carry `admits`, the names of the only entries it may verify; a
verification under it for any other entry is refused. This keeps a version later found
unsound to the receipts it already wrote, on which the unsound branch is shown not to
have run. The kernel listings before the closed-cover fix carry it: they accept an
uncovered zero-area row, and the later ones an uncovered one-point section, and neither
branch ran on W7, SW9 or N1.

Every path is repository-relative.

The checks. An entry is refused, and no count is reported at all, unless:

- its receipt exists;
- the receipt states a certified closure: `PASS_SAVED_CLOSED` or `PASS_CERTIFIED_CLOSED`
  from the kernel, on this cover's frame; `certified-infeasible` from the branch and
  bound, on this design, with no control flag and no soundness failure;
- the receipt's cells are the declared cells as a D4 class: their canonical masks agree;
- no D4 image of the pattern lies in the endpoint's state, which must survive;
- a declared certificate directory exists, and the data manifest lists, in it, the seed
  and node the kernel receipt names, or the manifest object the branch and bound's names;
- a listed object that is in place has the manifest's bytes;
- an admitted entry names evidence that exists (existence is all that is checked), and
  no class is declared twice;
- an admitted entry names a saved certificate and a verification receipt that exists,
  PASSes in full mode, ran under a listed verifier of the entry's kind whose listing
  admits the entry, checked the declared class, and checked the certificate's objects.

Objects are matched by content id: the `<id>` in `seed-<id>.json.gz` and
`node-<id>.json.gz`, or in the manifest's `<id>.json.gz` for the branch and bound, as the
producer and verification receipts name them. The ids are compared as names. The
directory the verification ran in is not compared, so a certificate directory can be
renamed without verifying it again, while a verification of other objects is refused.

The data. The certificate objects are bulk data, hosted outside Git under OR-18. The
count rests on the committed producer and verification receipts, so it does not need
the hosted objects. Re-running a verifier does: each entry's `certificate_data` says
whether its objects are in place, asking `sqpack.hosted_data.require` for each, which
holds a present file against the manifest's size and SHA-256 (the bytes were
downloaded, OR-16) and refuses one that differs. The report's `data` line says how many
certificates are not in place and the command, run from `packing/`, that fetches them:
`python -m devtools.hosted_data fetch --manifest` with the manifest's path, which checks
each download the same way and puts it at its path. Every verification command in the
record then runs as written. The census never downloads. development.md, Publishing
Hosted Data (`development.md#publishing-hosted-data`), is the procedure behind the
manifest and the release.

The report. The certified line counts admitted entries only. Pending entries with a
verified receipt are a separate projection, and pending entries still awaiting a receipt a
third. Each entry's exclusion is given alone, from the full census, and at the margin: for
an admitted entry, the survivors its removal from the ledger would restore; for a pending
one, what it would remove from the certified survivors. Last, every class the float
selector flagged in the given receipts and the ledger does not admit is listed with the
states and orbits it would remove from the certified survivors, and the survivors if all
of them were certified. Those are heuristic projections and never enter the certified
count. The report's `evidence_note` repeats that `evidence` is checked only to exist.

The flags come from selector receipts (`n17-sub-pattern-selector/v1`) or from a recheck
of earlier flags (`n17-sub-pattern-recheck/v1`), whose `flagged` list is the set still
flagged after the longer search. Receipts are read in the order given; a class a recheck
placed is withdrawn from the flags read before it. The default is the recheck of all 90
flags of the arity-7 and restricted arity-8 sweeps, `selector-recheck-90-seed1.json`,
which placed one arity-8 class and left 89 flagged.
"""

from __future__ import annotations

import argparse
import functools
import json
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from devtools import select_n17_sub_patterns as selector
from devtools.provenance import provenance
from sqpack import retained_json
from sqpack.hosted_data import (
    HostedDataError,
    HostedDataMissingError,
    HostedObject,
    fetch_command,
    load_manifest,
    require,
)
from sqpack.yamlio import load_yaml

SCHEMA = "n17-certified-census/v1"
LEDGER_SCHEMA = "n17-certified-sub-patterns/v3"
STATUS = (
    "exact census under admitted sub-pattern certificates; the pending and flagged lines "
    "are projections and never enter the certified count"
)
REPO = Path(__file__).resolve().parents[2]
PILOTS = "packing/campaign/explorations/X048-session-168-pilots"
DEFAULT_LEDGER = f"{PILOTS}/certified-sub-patterns.yaml"
DEFAULT_SELECTOR_RECEIPTS = (f"{PILOTS}/receipts/selector-recheck-90-seed1.json",)
FLAG_SCHEMAS = (selector.SCHEMA, selector.RECHECK_SCHEMA)
DESIGN = selector.DEFAULT_DESIGN
CENSUS = {"states": 346104, "orbits": 43593}
CERTIFIERS = ("kernel", "branch-and-bound")
STATUSES = ("admitted", "pending")
KERNEL_CLOSED = ("PASS_SAVED_CLOSED", "PASS_CERTIFIED_CLOSED")
KERNEL_FRAME = f"n17-{DESIGN}"
BB_SCHEMA = "n17-subpattern-bb-pilot/v1"
BB_CERTIFIED = "certified-infeasible"
VERIFICATION_SCHEMA = "n17-certificate-verification/v1"
FIELDS = ("name", "cells", "certifier", "receipt", "certificate", "status", "evidence")
VERIFIER_FIELDS = {"id", "certifier", "path", "version", "review"}
EVIDENCE_NOTE = (
    "each entry's evidence is a pointer for readers to the document that admits it; the "
    "census checks only that the file exists"
)
DATA_NOTE = (
    "the count rests on the committed producer and verification receipts; re-running a "
    "verifier needs the hosted certificate objects"
)
PROVENANCE = provenance(Path(__file__))

States = NDArray[np.int64]


class RefusedError(ValueError):
    """A ledger entry or its evidence fails a check; the census reports no count."""


@dataclass(frozen=True)
class Hosted:
    """The ledger's data manifest, if it declares one, and its objects by path."""

    manifest: Path | None
    objects: dict[str, HostedObject]


@dataclass(frozen=True)
class Cover:
    """The cover's cells and D4 group, the endpoint's state, and every state."""

    geometry: selector.Geometry
    endpoint_state: int
    states: States


@functools.cache
def cover_context() -> Cover:
    geometry = selector.cover_geometry(DESIGN)
    endpoint = selector.endpoint_pose(DESIGN)
    states = selector.all_states(len(geometry.names), selector.TARGET)
    return Cover(geometry, selector.mask_of(endpoint["cells"]), states)


@dataclass(frozen=True)
class Entry:
    """A ledger entry that passed every check."""

    name: str
    mask: int
    status: str
    certifier: str
    record: dict[str, Any]


def class_mask(cover: Cover, names: Any, where: str) -> int:
    """The canonical D4 mask of a list of cell names, refusing anything else."""
    known = cover.geometry.names
    if not isinstance(names, list) or not names:
        raise RefusedError(f"{where}: cells must be a non-empty list of cell names")
    cells: list[int] = []
    for name in names:
        if name not in known:
            raise RefusedError(f"{where}: {name!r} is not a cell of {DESIGN}")
        cells.append(known.index(name))
    if len(set(cells)) != len(cells):
        raise RefusedError(f"{where}: a cell is repeated")
    return selector.canonical(selector.mask_of(cells), cover.geometry.group)


def resolve(root: Path, declared: Any, where: str) -> Path:
    if not isinstance(declared, str) or not declared or Path(declared).is_absolute():
        raise RefusedError(f"{where}: {declared!r} is not a repository-relative path")
    path = root / declared
    if not path.exists():
        raise RefusedError(f"{where}: {declared} does not exist")
    return path


def receipt_cells(
    cover: Cover, entry: dict[str, Any], receipt: dict[str, Any], where: str
) -> Any:
    """The receipt's cells, once its status is checked to be a certified closure."""
    if entry["certifier"] == "kernel":
        status = receipt.get("status")
        if status not in KERNEL_CLOSED:
            raise RefusedError(f"{where}: kernel status {status!r} is not a closure")
        if receipt.get("frame", KERNEL_FRAME) != KERNEL_FRAME:
            raise RefusedError(f"{where}: kernel frame {receipt.get('frame')!r}")
        cells, mask = receipt.get("cells"), receipt.get("mask")
        names = cover.geometry.names
        indices = sorted(names.index(c) for c in cells if c in names) if cells else []
        if mask is not None and indices != sorted(mask):
            raise RefusedError(f"{where}: the receipt's cells and mask disagree")
        return cells
    if receipt.get("schema") != BB_SCHEMA or receipt.get("verdict") != BB_CERTIFIED:
        raise RefusedError(
            f"{where}: branch-and-bound verdict {receipt.get('verdict')!r} is not certified"
        )
    if receipt.get("design") != DESIGN:
        raise RefusedError(f"{where}: branch-and-bound design {receipt.get('design')!r}")
    if receipt.get("control") is not False or "soundness_failure" in receipt:
        raise RefusedError(f"{where}: a control run or a soundness failure certifies nothing")
    return receipt.get("pattern")


def object_names(certifier: str, ids: Any, manifest: str) -> list[str]:
    """The file names of a certificate's objects, from the content ids a receipt gives them:
    `seed-<id>.json.gz` and `node-<id>.json.gz` for the kernel, `<id>.json.gz` for the
    branch and bound's manifest, whose id the receipt holds under the key `manifest`.

    The ids are names here, and are matched as names; nothing is hashed (OR-16).
    """
    named: dict[str, Any] = ids if isinstance(ids, dict) else {}
    if certifier == "kernel":
        return [f"{kind}-{named.get(f'{kind}_sha256')}.json.gz" for kind in ("seed", "node")]
    return [f"{named.get(manifest)}.json.gz"]


def check_certificate(
    entry: dict[str, Any],
    receipt: dict[str, Any],
    context: tuple[Path, dict[str, HostedObject]],
    where: str,
) -> tuple[list[str], list[HostedObject]]:
    """The declared certificate directory, whose hosted files must include the objects the
    producer receipt names; those objects' file names, and every hosted file in it."""
    root, hosted = context
    directory = str(entry["certificate"]).rstrip("/")
    _ = resolve(root, directory, f"{where}: certificate")
    names = object_names(entry["certifier"], receipt, "certificate_manifest")
    for name in names:
        if f"{directory}/{name}" not in hosted:
            raise RefusedError(f"{where}: the data manifest lists no {name} in {directory}")
    records = [
        record for path, record in sorted(hosted.items()) if path.startswith(f"{directory}/")
    ]
    return names, records


def certificate_data(root: Path, hosted: Hosted, records: list[HostedObject]) -> dict[str, Any]:
    """Whether a certificate's hosted files are in place, each as `require` finds it: a
    present file must hold the manifest's bytes, and one that differs is refused."""
    present = 0
    for record in records:
        if hosted.manifest is None:
            raise RefusedError(f"{record.path}: the ledger declares no data manifest")
        try:
            _ = require(record.path, hosted.manifest, repo=root)
        except HostedDataMissingError:
            continue
        except HostedDataError as error:
            raise RefusedError(f"{error}, after moving the file aside") from None
        present += 1
    states = ["present"] * present + ["absent"] * (len(records) - present)
    local = "partial" if 0 < present < len(states) else "present" if present else "absent"
    return {
        "files": len(records),
        "bytes": sum(record.size for record in records),
        "local": local,
    }


def load_verifiers(root: Path, declared: Any, ledger: Path) -> dict[str, dict[str, Any]]:
    """The header's reviewed verifiers by id, each with a review that exists, and optionally
    `admits`, the only entries the listing may verify."""
    fields = "{id, certifier, path, version, review}"
    if not isinstance(declared, list) or not all(
        isinstance(item, dict) and VERIFIER_FIELDS <= set(item) <= {*VERIFIER_FIELDS, "admits"}
        for item in declared
    ):
        raise RefusedError(
            f"{ledger}: verifiers must be a list of {fields}, each optionally with admits"
        )
    listings: dict[str, dict[str, Any]] = {}
    for item in declared:
        where = f"verifier {item['id']!r}"
        if not isinstance(item["id"], str) or not item["id"] or item["id"] in listings:
            raise RefusedError(f"{where}: ids must be distinct non-empty names")
        if item["certifier"] not in CERTIFIERS:
            raise RefusedError(f"{where}: certifier {item['certifier']!r}")
        admits = item.get("admits", [])
        if not isinstance(admits, list) or not all(
            isinstance(name, str) and name for name in admits
        ):
            raise RefusedError(f"{where}: admits must be a list of entry names")
        _ = resolve(root, item["path"], f"{where}: path")
        _ = resolve(root, item["review"], f"{where}: review")
        listings[item["id"]] = item
    return listings


def listing_of(
    declared: dict[str, Any],
    verification: dict[str, Any],
    listings: dict[str, dict[str, Any]],
    entry: dict[str, Any],
    where: str,
) -> dict[str, Any]:
    """The listing the entry names for its verification: of the entry's kind, the file the
    receipt records as having run, and admitting the entry."""
    named = declared.get("verifier")
    if not isinstance(named, str) or named not in listings:
        raise RefusedError(f"{where}: the verification names no listed verifier ({named!r})")
    listing = listings[named]
    if listing["certifier"] != entry["certifier"]:
        raise RefusedError(
            f"{where}: verifier {named!r} checks {listing['certifier']} certificates"
        )
    recorded = verification.get("provenance")
    if recorded is not None:
        files = recorded.get("files") if isinstance(recorded, dict) else None
        if not isinstance(files, dict) or len(files) != 1:
            raise RefusedError(f"{where}: the receipt's provenance names no single verifier")
        ran = next(iter(files))
        if ran != listing["path"]:
            raise RefusedError(f"{where}: the receipt ran {ran}, not {listing['path']}")
        if recorded.get("dirty") is True:
            raise RefusedError(f"{where}: the verification ran on uncommitted verifier bytes")
    name = str(entry["name"])
    if "admits" in listing and name not in listing["admits"]:
        admitted = ", ".join(listing["admits"]) or "no entry"
        raise RefusedError(
            f"entry {name!r}: verifier {named!r} is reviewed only for other entries "
            f"(admits {admitted}); verify this entry under a listing without admits"
        )
    return listing


def check_verification(
    cover: Cover,
    entry: dict[str, Any],
    context: tuple[Path, dict[str, dict[str, Any]], int, list[str]],
    where: str,
) -> dict[str, Any]:
    """The standing verifier's receipt: full, passing, reviewed for this entry, and about
    this certificate's objects, named by their file names."""
    root, listings, mask, objects = context
    declared = entry.get("verification")
    if not isinstance(declared, dict) or set(declared) != {"receipt", "verifier"}:
        raise RefusedError(f"{where}: verification must name a receipt and a verifier")
    path = resolve(root, declared["receipt"], f"{where}: verification")
    verification = json.loads(path.read_text(encoding="utf-8"))
    certifier = entry["certifier"]
    if not isinstance(verification, dict) or (
        verification.get("schema") != VERIFICATION_SCHEMA
        or verification.get("verifier") != certifier
    ):
        raise RefusedError(f"{where}: not a {certifier} verification receipt")
    if verification.get("status") != "PASS":
        raise RefusedError(f"{where}: the verification did not pass")
    if verification.get("mode") != "full":
        raise RefusedError(f"{where}: the verification is a sample, not a full check")
    listing = listing_of(declared, verification, listings, entry, where)
    recorded = verification.get("provenance")
    checked = object_names(certifier, verification.get("certificate"), "manifest_sha256")
    if checked != objects:
        raise RefusedError(
            f"{where}: the verification checked other objects ({', '.join(checked)}) than "
            f"the certificate's ({', '.join(objects)})"
        )
    names = verification.get("cells" if certifier == "kernel" else "pattern")
    if class_mask(cover, names, f"{where}: verification") != mask:
        raise RefusedError(f"{where}: the verification checked another class")
    return {
        "receipt": declared["receipt"],
        "verifier": {key: listing[key] for key in ("id", "path", "version", "review")},
        "ran_at": recorded.get("revision") if isinstance(recorded, dict) else None,
        "mode": "full",
        "status": "PASS",
        "certificate": entry["certificate"],
    }


def check_entry(
    cover: Cover,
    entry: Any,
    context: tuple[Path, dict[str, dict[str, Any]], Hosted],
    index: int,
) -> Entry:
    """Every check on one ledger entry; refuses on the first that fails."""
    if not isinstance(entry, dict) or not set(FIELDS) <= set(entry) <= {
        *FIELDS,
        "verification",
    }:
        raise RefusedError(
            f"entry {index}: fields must be {', '.join(FIELDS)}, and optionally verification"
        )
    root, verifiers, hosted = context
    where = f"entry {entry['name']!r}"
    if entry["certifier"] not in CERTIFIERS:
        raise RefusedError(f"{where}: certifier {entry['certifier']!r}")
    if entry["status"] not in STATUSES:
        raise RefusedError(f"{where}: status {entry['status']!r}")
    mask = class_mask(cover, entry["cells"], where)
    group = cover.geometry.group
    if any(image & cover.endpoint_state == image for image in selector.orbit(mask, group)):
        raise RefusedError(f"{where}: the pattern lies in the endpoint's feasible state")
    if entry["status"] == "admitted" or entry["evidence"] is not None:
        _ = resolve(root, entry["evidence"], f"{where}: evidence")
    record: dict[str, Any] = {
        "name": entry["name"],
        "status": entry["status"],
        "certifier": entry["certifier"],
        "cells": list(entry["cells"]),
        "receipt": entry["receipt"],
        "evidence": entry["evidence"],
    }
    if entry["receipt"] is None:
        if entry["status"] == "admitted":
            raise RefusedError(f"{where}: only a pending entry may await its receipt")
        if entry.get("verification") is not None:
            raise RefusedError(f"{where}: a verification needs the producer receipt")
        record["verified"] = False
        return Entry(entry["name"], mask, entry["status"], entry["certifier"], record)
    path = resolve(root, entry["receipt"], f"{where}: receipt")
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(receipt, dict):
        raise RefusedError(f"{where}: the receipt is not a JSON object")
    certified = class_mask(
        cover, receipt_cells(cover, entry, receipt, where), f"{where}: receipt"
    )
    if certified != mask:
        raise RefusedError(f"{where}: the receipt certifies another class")
    admitted = entry["status"] == "admitted"
    if admitted and entry["certificate"] is None:
        raise RefusedError(f"{where}: an admitted entry names its saved certificate")
    if entry["certificate"] is not None:
        objects, records = check_certificate(entry, receipt, (root, hosted.objects), where)
        record["certificate_data"] = certificate_data(root, hosted, records)
        if admitted or entry.get("verification") is not None:
            checking = (root, verifiers, mask, objects)
            record["verification"] = check_verification(cover, entry, checking, where)
    elif entry.get("verification") is not None:
        raise RefusedError(f"{where}: a verification needs the saved certificate")
    kernel = entry["certifier"] == "kernel"
    record["verified"] = True
    record["receipt_status"] = receipt.get("status") if kernel else receipt.get("verdict")
    record["certifier_provenance"] = receipt.get("provenance") or {
        "sha256": receipt.get("tool_sha256" if kernel else "module_sha256")
    }
    return Entry(entry["name"], mask, entry["status"], entry["certifier"], record)


def read_ledger(ledger: Path) -> dict[str, Any]:
    if not ledger.is_file():
        raise RefusedError(f"{ledger} does not exist")
    document = load_yaml(ledger.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("schema") != LEDGER_SCHEMA:
        raise RefusedError(f"{ledger}: not a {LEDGER_SCHEMA} ledger")
    if document.get("design") != DESIGN:
        raise RefusedError(f"{ledger}: design {document.get('design')!r}, not {DESIGN}")
    if not isinstance(document.get("entries") or [], list):
        raise RefusedError(f"{ledger}: entries must be a list")
    return document


def hosted_files(root: Path, document: dict[str, Any]) -> Hosted:
    """The data manifest, read through `sqpack.hosted_data`, and its objects by path;
    none when the ledger declares no manifest."""
    declared = document.get("data_manifest")
    if declared is None:
        return Hosted(None, {})
    where = f"data_manifest {declared}"
    path = resolve(root, declared, where)
    try:
        manifest = load_manifest(path)
    except HostedDataError as error:
        raise RefusedError(f"{where}: {error}") from None
    objects = {item.path: item for item in manifest.objects}
    if len(objects) != len(manifest.objects):
        raise RefusedError(f"{where}: an object's path is listed twice")
    return Hosted(path, objects)


def load_ledger(cover: Cover, ledger: Path, root: Path) -> tuple[list[Entry], Hosted]:
    document = read_ledger(ledger)
    raw = document.get("entries") or []
    verifiers = load_verifiers(root, document.get("verifiers") or [], ledger)
    hosted = hosted_files(root, document)
    context = (root, verifiers, hosted)
    entries = [check_entry(cover, entry, context, index) for index, entry in enumerate(raw)]
    names = [entry.name for entry in entries]
    if len(set(names)) != len(names):
        raise RefusedError(f"{ledger}: entry names repeat")
    seen: dict[int, str] = {}
    for entry in entries:
        if entry.mask in seen:
            raise RefusedError(f"entries {seen[entry.mask]!r} and {entry.name!r} are one class")
        seen[entry.mask] = entry.name
    return entries, hosted


def count(cover: Cover, masks: list[int]) -> dict[str, Any]:
    record = selector.consume(
        len(cover.geometry.names),
        cover.geometry.group,
        masks,
        endpoint_state=cover.endpoint_state,
        states=cover.states,
    )
    return {key: record[key] for key in ("surviving_states", "orbits", "endpoint_survives")}


def removal(cover: Cover, alive: States, mask: int) -> dict[str, int]:
    """States and orbits of `alive` that hold some D4 image of the class."""
    hit = np.zeros(alive.size, dtype=np.bool_)
    for image in selector.orbit(mask, cover.geometry.group):
        hit |= (alive & image) == image
    removed = alive[hit]
    orbits = selector.count_orbits(removed, cover.geometry.group)["orbits"]
    return {"states": int(removed.size), "orbits": orbits}


def flagged_classes(
    cover: Cover, root: Path, receipts: Sequence[str]
) -> dict[int, dict[str, Any]]:
    """Every class the receipts leave flagged, with its latest record.

    A selector receipt's `flagged` list is what its sweep could not place; a recheck
    receipt's is what is still flagged after the longer search, and a class it placed is
    withdrawn from the flags of the receipts before it.
    """
    group = cover.geometry.group
    flags: dict[int, dict[str, Any]] = {}
    for declared in receipts:
        path = resolve(root, declared, "selector receipt")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if receipt.get("schema") not in FLAG_SCHEMAS or receipt.get("design") != DESIGN:
            raise RefusedError(f"{declared}: not a selector or recheck receipt on {DESIGN}")
        placed = [
            row["indices"]
            for row in receipt.get("rechecked", [])
            if receipt["schema"] == selector.RECHECK_SCHEMA and row["status"] == "placed"
        ]
        for indices in placed:
            _ = flags.pop(selector.canonical(selector.mask_of(indices), group), None)
        for flag in receipt["flagged"]:
            mask = selector.canonical(selector.mask_of(flag["indices"]), group)
            flags[mask] = {
                "cells": flag["cells"],
                "arity": flag["arity"],
                "best_penetration": flag["best_penetration"],
                "selector_receipt": declared,
            }
    return flags


def census(
    ledger: Path,
    *,
    root: Path = REPO,
    selector_receipts: Sequence[str] = DEFAULT_SELECTOR_RECEIPTS,
) -> dict[str, Any]:
    """The certified census, its projections, and every entry's exclusion."""
    clock = time.perf_counter()
    cover = cover_context()
    entries, hosted = load_ledger(cover, ledger, root)
    full = count(cover, [])
    if {"states": full["surviving_states"], "orbits": full["orbits"]} != CENSUS:
        raise RefusedError(f"the empty census is {full}, not H-266's {CENSUS}")
    admitted = [entry.mask for entry in entries if entry.status == "admitted"]
    verified = [e.mask for e in entries if e.status == "pending" and e.record["verified"]]
    pending = [entry.mask for entry in entries if entry.status == "pending"]
    certified = count(cover, admitted)
    if not certified["endpoint_survives"]:
        raise RefusedError("the admitted entries exclude the endpoint's state")
    alive = selector.survivors(
        cover.states,
        sorted({i for m in admitted for i in selector.orbit(m, cover.geometry.group)}),
    )
    rows: list[dict[str, Any]] = []
    for entry in entries:
        alone = removal(cover, cover.states, entry.mask)
        if entry.status == "admitted":
            without = count(cover, [m for m in admitted if m != entry.mask])
            margin = {
                "states": without["surviving_states"] - certified["surviving_states"],
                "orbits": without["orbits"] - certified["orbits"],
            }
        else:
            margin = removal(cover, alive, entry.mask)
        rows.append({**entry.record, "alone": alone, "marginal": margin})
    flags = flagged_classes(cover, root, selector_receipts)
    ledger_status = {entry.mask: entry.status for entry in entries}
    remaining = [
        {
            **flags[mask],
            "in_ledger": ledger_status.get(mask),
            "projected_gain": removal(cover, alive, mask),
        }
        for mask in sorted(flags)
        if ledger_status.get(mask) != "admitted"
    ]
    remaining.sort(key=lambda row: (-row["projected_gain"]["states"], row["cells"]))
    data = [row["certificate_data"] for row in rows if "certificate_data" in row]
    absent = [row for row in data if row["local"] != "present"]
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "design": DESIGN,
        "ledger": str(ledger.relative_to(root)) if ledger.is_relative_to(root) else str(ledger),
        "census": full,
        "entries": rows,
        "evidence_note": EVIDENCE_NOTE,
        "data": {
            "files": sum(row["files"] for row in data),
            "bytes": sum(row["bytes"] for row in data),
            "certificates_not_in_place": len(absent),
            "full_recheck": (
                f"run {fetch_command(hosted.manifest)} from packing/"
                if absent and hosted.manifest is not None
                else "the hosted files are in place"
            ),
            "note": DATA_NOTE,
        },
        "certified": {"admitted": len(admitted), **certified},
        "pending_verified_projection": {
            "entries": len(verified),
            **count(cover, admitted + verified),
        },
        "pending_all_projection": {"entries": len(pending), **count(cover, admitted + pending)},
        "flagged_uncertified": {
            "selector_receipts": list(selector_receipts),
            "classes": remaining,
            "all_certified_projection": count(cover, admitted + sorted(flags)),
        },
        "provenance": {**PROVENANCE, "ledger": provenance(ledger)},
        "seconds": round(time.perf_counter() - clock, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--ledger", default=DEFAULT_LEDGER, help="repository-relative")
    _ = parser.add_argument(
        "--selector-receipt",
        action="append",
        default=None,
        help=(
            "a selector or recheck receipt whose flags are projected (repeatable, read in "
            "order; default: the recheck of the 90 earlier flags)"
        ),
    )
    _ = parser.add_argument(
        "--root", type=Path, default=REPO, help="what the ledger's paths are relative to"
    )
    _ = parser.add_argument("--output", type=Path, help="write the census here")
    arguments = parser.parse_args(argv)
    root: Path = arguments.root
    receipts = arguments.selector_receipt or list(DEFAULT_SELECTOR_RECEIPTS)
    try:
        record = census(root / arguments.ledger, root=root, selector_receipts=receipts)
    except RefusedError as refusal:
        print(json.dumps({"refused": str(refusal)}))
        return 2
    text = retained_json.dumps(record, sort_keys=True)
    if arguments.output is not None:
        _ = arguments.output.write_text(text, encoding="utf-8")
    print(text, end="")
    if record["data"]["certificates_not_in_place"]:
        print(
            f"census: {record['data']['full_recheck']} to re-run the verifiers", file=sys.stderr
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
