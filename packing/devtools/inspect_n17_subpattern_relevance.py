"""SciPy-free potential named-D4 coverage; never verify or admit a certificate."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import math
import time
import zlib
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_n11_envelope_windows as old
from devtools.provenance import provenance
from sqpack import retained_json

finite, require, tick = old.finite, old.require, old.tick
SCHEMA = "n17-subpattern-relevance/v1"
CONTEXT_SCHEMA = "n17-subpattern-relevance-context/v1"
MANIFEST_LIMIT, DECODED_LIMIT, OUTPUT_LIMIT = 1 << 20, 10 << 20, 64 << 20
CANDIDATE_LIMIT, COMPARISON_LIMIT = 16, 1000000


def path(value: Any) -> Path:
    require(type(value) is str, "declared path required")
    p = Path(value)
    return p if p.is_absolute() else old.REPO / p


def hold(held: dict[Path, bytes], p: Path, raw: bytes, expected: Any) -> None:
    require(
        type(expected) is str and hashlib.sha256(raw).hexdigest() == expected,
        "artifact bytes differ",
    )
    require(p not in held or held[p] == raw, "conflicting artifact alias")
    held[p] = raw


def manifest(p: Path, record: dict[str, Any], held: dict[Path, bytes]) -> dict[str, Any]:
    with p.open("rb") as stream:
        raw = stream.read(MANIFEST_LIMIT + 1)
    if len(raw) > MANIFEST_LIMIT:
        raise finite.IncompleteError("compact manifest compressed ceiling")
    hold(held, p, raw, record["compressed_sha256"])
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
        decoded = stream.read(DECODED_LIMIT + 1)
    if len(decoded) > DECODED_LIMIT:
        raise finite.IncompleteError("compact manifest decoded ceiling")
    data = finite.decode(decoded)
    require(
        finite.identity(data) == record["manifest_id"], "canonical generated manifest differs"
    )
    return data


def candidate(data: Any, record: dict[str, Any], names: list[str]) -> dict[str, Any]:
    require(
        type(data) is dict
        and data.get("schema")
        in ("n17-subpattern-bb-certificate/v1", "n17-subpattern-bb-certificate/v2"),
        "branch-and-bound manifest required",
    )
    header = data.get("header")
    require(
        type(header) is dict and header.get("cap") == str(old.U), "original cap header required"
    )
    header = cast(dict[str, Any], header)
    cells = header.get("pattern")
    require(
        type(cells) is list
        and 1 <= len(cells) <= 24
        and all(type(c) is str and c in names for c in cells)
        and len(set(cells)) == len(cells),
        "unique original named cells required",
    )
    cells = cast(list[str], cells)
    return {
        "id": record["id"],
        "source_mask": sum(1 << names.index(c) for c in cells),
        "source_cells": copy.deepcopy(cells),
        "manifest_id": record["manifest_id"],
        "schema": data["schema"],
        "cap": header["cap"],
        "explicit_B": copy.deepcopy(header.get("B")),
        "explicit_frame": copy.deepcopy(header.get("frame")),
        "root_boxes": copy.deepcopy(header.get("root_boxes")),
        "root_angles": copy.deepcopy(header.get("root_angles")),
        "settings": copy.deepcopy(header.get("settings")),
        "complete_pair_roster_present": header.get("pairs")
        == [[i, j] for i in range(len(cells)) for j in range(i + 1, len(cells))],
        "complete_cell_enclosure_checked": False,
        "unit_side_and_frame_join_checked": False,
        "full_shifted_closed_angle_cover_checked": False,
        "hidden_conditioning_absence_checked": False,
        "full_tree_verification_performed": False,
        "future_full_replay_can_join_default_unit_frame_convention": True,
    }


def project(
    names: list[str],
    actions: dict[str, list[int]],
    rows: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    deadline: float,
) -> dict[str, Any]:
    require(len(names) == 24 and len(set(names)) == 24, "complete cell names")
    require(
        bool(actions)
        and all(
            type(p) is list and sorted(p) == list(range(24)) and all(type(i) is int for i in p)
            for p in actions.values()
        ),
        "typed action permutations",
    )
    require(
        1 <= len(candidates) <= CANDIDATE_LIMIT
        and len({c["id"] for c in candidates}) == len(candidates),
        "unique bounded candidates",
    )
    coverage: dict[str, set[int]] = {}
    reports = []
    comparisons = 0
    sizes = {row["mask"]: row["orbit_size"] for row in rows}
    require(len(sizes) == len(rows), "distinct current orbit representatives")
    distance_two = {r["mask"] for r in rows if r["distance"] == 2}
    for source in candidates:
        mask = source["source_mask"]
        require(type(mask) is int and 0 < mask < 1 << 24, "candidate mask")
        images = [
            (action, sum(1 << p[i] for i in range(24) if mask & (1 << i)))
            for action, p in sorted(actions.items())
        ]
        matches = []
        hits: set[int] = set()
        for row in rows:
            tick(deadline)
            successful = None
            for action, image in images:
                comparisons += 1
                if comparisons > COMPARISON_LIMIT:
                    raise finite.IncompleteError("D4 subset comparison ceiling")
                if row["mask"] & image == image and successful is None:
                    successful = (action, image)
            if successful is not None:
                action, image = successful
                hits.add(row["mask"])
                matches.append(
                    {
                        "current_mask": row["mask"],
                        "orbit_size": row["orbit_size"],
                        "distance": row["distance"],
                        "action": action,
                        "image_mask": image,
                        "image_cells": [names[i] for i in range(24) if image & (1 << i)],
                    }
                )
        coverage[source["id"]] = hits
        reports.append(
            source
            | {
                "canonical_D4_mask": min(image for _, image in images),
                "potential_current_residue": counts(hits, sizes),
                "potential_distance_two": counts(hits & distance_two, sizes),
                "matched_orbits": matches,
            }
        )
    union = set().union(*coverage.values())
    overlaps = [
        {
            "candidates": [a, b],
            "current_residue": counts(coverage[a] & coverage[b], sizes),
            "distance_two": counts(coverage[a] & coverage[b] & distance_two, sizes),
        }
        for index, a in enumerate(coverage)
        for b in list(coverage)[index + 1 :]
    ]
    return {
        "candidates": reports,
        "union_potential_current_residue": counts(union, sizes),
        "union_potential_distance_two": counts(union & distance_two, sizes),
        "pairwise_overlap": overlaps,
        "D4_subset_comparisons": comparisons,
        "current_orbits_accounted": len(rows),
        "distance_two_orbits_accounted": len(distance_two),
        "potential_counts_marginal_only_after_inherited60_partition": True,
    }


def counts(masks: set[int], sizes: dict[int, int]) -> dict[str, int]:
    return {"orbits": len(masks), "states": sum(sizes[m] for m in masks)}


def generate(document: Any, deadline: float) -> dict[str, Any]:
    require(
        type(document) is dict
        and set(document)
        == {"schema", "accepted_descriptor", "accepted_descriptor_sha256", "candidates"}
        and document["schema"] == CONTEXT_SCHEMA,
        "typed relevance descriptor",
    )
    document = cast(dict[str, Any], document)
    frozen = finite.canonical(document)
    descriptor_path = path(document["accepted_descriptor"])
    raw, accepted = finite.read_json(descriptor_path, old.INPUT_LIMIT)
    held: dict[Path, bytes] = {}
    hold(held, descriptor_path, raw, document["accepted_descriptor_sha256"])
    _, names, _, transitive = old.intake(accepted, deadline)
    for p, data in transitive.items():
        require(p not in held or held[p] == data, "conflicting inherited alias")
        held[p] = data
    partition = finite.decode(held[path(accepted["partition"])])
    records = document["candidates"]
    require(
        type(records) is list and 1 <= len(records) <= CANDIDATE_LIMIT,
        "bounded candidates required",
    )
    candidates = []
    for record in records:
        tick(deadline)
        require(
            type(record) is dict
            and set(record) == {"id", "manifest", "compressed_sha256", "manifest_id"}
            and type(record["id"]) is str,
            "typed compact manifest record",
        )
        record = cast(dict[str, Any], record)
        candidates.append(
            candidate(manifest(path(record["manifest"]), record, held), record, names)
        )
    result = project(names, accepted["d4"], partition["orbits"], candidates, deadline)
    for p, data in held.items():
        tick(deadline)
        with p.open("rb") as stream:
            require(stream.read(len(data) + 1) == data, "held artifact changed")
    require(finite.canonical(document) == frozen, "descriptor mutated")
    tick(deadline)
    return {
        "schema": SCHEMA,
        "status": "potential_metadata_relevance",
        "accepted_inputs": copy.deepcopy(document),
        **result,
        "verification_passed": False,
        "certificate_admission_performed": False,
        "ordinary_assignment_exclusion_proved": False,
        "census_admission_proved": False,
        "global_bound_proved": False,
        "global_optimality_proved": False,
        "physical_packing_proved": False,
        "parent_geometry_replayed": False,
        "proof_tree_replayed": False,
        "scope": "Replay priority only; named D4 subset matches are not proof exclusions.",
        "limits": {
            "compact_manifest_compressed_bytes": MANIFEST_LIMIT,
            "compact_manifest_decoded_bytes": DECODED_LIMIT,
            "candidate_count": CANDIDATE_LIMIT,
            "D4_subset_comparisons": COMPARISON_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
        },
    }


def serialize(result: dict[str, Any]) -> str:
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT:
        raise finite.IncompleteError("metadata output ceiling")
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", required=True, type=Path)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-seconds", type=float, default=30)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("finite positive max-seconds required")
    deadline = time.monotonic() + args.max_seconds
    try:
        raw, document = finite.read_json(args.descriptor, old.INPUT_LIMIT)
        result = generate(document, deadline)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            require(
                old.payload(result) == old.payload(certificate),
                "fresh metadata payload differs",
            )
            require(
                saved == finite.read_json(args.certificate, OUTPUT_LIMIT)[0],
                "saved metadata changed",
            )
            result["verification_passed"] = True
        require(
            raw == finite.read_json(args.descriptor, old.INPUT_LIMIT)[0],
            "descriptor bytes changed",
        )
        result.update(
            provenance=provenance(Path(__file__), Path(old.__file__)), invocation={"argv": argv}
        )
        text = serialize(result)
        tick(deadline)
    except (
        finite.IncompleteError,
        ValueError,
        KeyError,
        TypeError,
        OSError,
        EOFError,
        zlib.error,
    ) as exc:
        result = {
            "schema": SCHEMA,
            "status": "incomplete" if isinstance(exc, finite.IncompleteError) else "refused",
            "error": str(exc),
            "verification_passed": False,
            "certificate_admission_performed": False,
            "ordinary_assignment_exclusion_proved": False,
            "census_admission_proved": False,
            "global_bound_proved": False,
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(text)
    return int(result["status"] in ("incomplete", "refused"))


if __name__ == "__main__":
    raise SystemExit(main())
