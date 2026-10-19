"""Inventory conservative dependencies of an accepted full standing certificate.

This stage does not project or rewrite a certificate, run a producer, admit a
smaller mask, or establish geometric exclusion/minimality. A later typed projection
requires its own registration and a complete standing smaller-arity replay.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
import time
from collections import Counter
from collections.abc import Iterable
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_capacity_one_cover as cover
from devtools import check_n17_subpattern as saved
from devtools import verify_n17_kernel_certificate as standing
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-certificate-dependency-inventory/v1"
CHANNELS = ("geometric_dependencies", "validation_dependencies")
RULES = {
    "implicit_hulls": "every nonempty foreign prior owned hull for every new row",
    "predecessor": "current accepted predecessor and owner presence, including dead rows",
    "geometric_partners": "every current row of each collision-cited partner",
    "validation_partners": "every current row of every supplied complete partner cover",
    "compression": "old owner hull plus every new row, including replace mode",
    "closure": "named owner's final rows or both named final hulls",
    "empty_hull": "no foreign forbidden edge; presence retained for its own facts",
}
FALSE_FLAGS = {
    "geometry_proved": False,
    "exclusion_proved": False,
    "smaller_mask_admitted": False,
    "core_minimality_proved": False,
    "census_admission_proved": False,
    "global_coverage_proved": False,
    "certificate_rewritten": False,
    "producer_run": False,
}


class IncompleteError(ValueError):
    """A resource ceiling prevented complete inventory."""


def require(value: bool, message: str) -> None:  # noqa: FBT001
    exact.require(value, message)


def ref_key(value: Any) -> str:
    require(type(value) is dict, "untyped row reference")
    if value.get("kind") == "wall_seed":
        require(set(value) == {"kind", "owner", "row"}, "unknown seed reference fields")
        integers = (value["owner"], value["row"])
    elif value.get("kind") == "phase3":
        require(
            set(value) == {"kind", "node", "step", "row"}
            and type(value["node"]) is str
            and 0 < len(value["node"]) <= 256,
            "unknown phase3 reference fields",
        )
        integers = (value["step"], value["row"])
    else:
        raise exact.AuditError("unknown typed row reference grammar")
    require(
        all(type(number) is int and number >= 0 for number in integers),
        "row reference integer type differs",
    )
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def polygon(value: Any) -> list[standing.Point]:
    require(type(value) is list, "polygon is not a list")
    result = []
    for point in value:
        require(type(point) is list and len(point) == 2, "polygon point shape")
        result.append((exact.rational(point[0]), exact.rational(point[1])))
    return standing.hull(result)


def same_polygon(first: Any, second: Any) -> bool:
    return standing.same_set(polygon(first), polygon(second))


class Inventory:
    """Typed acyclic facts; both transitive owner sets are retained independently."""

    def __init__(self, deadline: float, max_facts: int, max_edges: int) -> None:
        self.deadline, self.max_facts, self.max_edges = deadline, max_facts, max_edges
        self.facts: dict[str, dict[str, Any]] = {}
        self.edge_count = 0

    def tick(self) -> None:
        if time.monotonic() >= self.deadline:
            raise IncompleteError("dependency inventory wall ceiling")

    def add(
        self,
        name: str,
        kind: str,
        owner: int | None,
        edges: dict[str, dict[str, str]],
        **metadata: Any,
    ) -> str:
        self.tick()
        require(name not in self.facts, "duplicate fact or row reference")
        require(set(edges) == set(CHANNELS), "dependency channels differ")
        self.edge_count += sum(len(items) for items in edges.values())
        if len(self.facts) >= self.max_facts or self.edge_count > self.max_edges:
            raise IncompleteError("dependency fact/edge ceiling")
        fact: dict[str, Any] = {
            "id": name,
            "kind": kind,
            "owner": owner,
            **copy.deepcopy(metadata),
        }
        for channel in CHANNELS:
            owners = set() if owner is None else {owner}
            for parent in edges[channel]:
                require(parent in self.facts, "missing/future/foreign dependency fact")
                owners.update(self.facts[parent][channel]["owners"])
            fact[channel] = {
                "edges": [
                    {"fact": p, "reason": reason}
                    for p, reason in sorted(edges[channel].items())
                ],
                "owners": sorted(owners),
            }
        self.facts[name] = fact
        return name


def channels(edges: dict[str, str]) -> dict[str, dict[str, str]]:
    return {name: dict(edges) for name in CHANNELS}


def inventory(
    seed: dict[str, Any],
    node: dict[str, Any],
    steps: Iterable[dict[str, Any]],
    receipt: dict[str, Any],
    cells: standing.Cells,
    *,
    deadline: float,
    max_facts: int = 25000,
    max_edges: int = 500000,
) -> dict[str, Any]:
    require(
        receipt["schema"] == standing.SCHEMA
        and receipt["verifier"] == standing.KIND
        and receipt["status"] == "PASS"
        and receipt["mode"] == "full"
        and receipt["sample_rows_per_step"] is None
        and receipt["sample_seed"] is None
        and receipt["closed"] is True
        and receipt["failure"] is None,
        "standing receipt is not a complete full PASS",
    )
    graph = Inventory(deadline, max_facts, max_edges)
    for document in (seed, node):
        exact.rational(document["U"])
        exact.rational(document["B"])
    for world_cell in seed["world"]:
        polygon(world_cell)
    mask = list(standing.check_frame(seed, node, cells))
    require(
        mask == sorted(mask) and all(type(owner) is int for owner in mask),
        "noncanonical owner mask",
    )
    seed_id = saved.content_sha256(seed)
    require(
        node["source"]["sha256"] == seed_id == receipt["certificate"]["seed_sha256"]
        and receipt["mask"] == mask
        and receipt["cells"] == [cells.names[i] for i in mask]
        and receipt["bins"] == seed["bins"]
        and exact.exact_structure(receipt["cells_source"], cells.source),
        "standing seed/mask/cell/frame custody differs",
    )
    require(type(seed["bins"]) is int and seed["bins"] > 0, "invalid seed bins")
    keyset = set(map(str, mask))
    require(set(seed["cells"]) == set(seed["groups"]) == keyset, "seed owner inventory differs")
    require(
        set(node["initial"]["groups"]) == set(node["initial"]["cell_references"]) == keyset,
        "initial owner inventory differs",
    )
    premise = graph.add(
        "premise:frame-root-wall-seed",
        "frame_root_wall_premises",
        None,
        channels({}),
        frame=cells.source,
        cap=str(cells.cap),
        unit_scale="1",
        root_node=node["node_id"],
    )
    presence, hulls, rows, groups, nonempty = {}, {}, {}, {}, {}
    seen_refs: set[str] = set()
    for owner in mask:
        graph.tick()
        presence[owner] = graph.add(
            f"presence:{owner}",
            "owner_presence",
            owner,
            channels({premise: "frame_cell_wall_root"}),
            cell=cells.names[owner],
        )
        groups[owner] = seed["groups"][str(owner)]
        nonempty[owner] = bool(polygon(groups[owner]))
        require(
            same_polygon(groups[owner], node["initial"]["groups"][str(owner)]),
            "initial owned hull differs",
        )
        hulls[owner] = graph.add(
            f"seed-hull:{owner}",
            "seed_owned_hull",
            owner,
            channels({presence[owner]: "owner_presence"}),
            empty=not nonempty[owner],
        )
        rows[owner] = []
        require(len(seed["cells"][str(owner)]) == seed["bins"], "seed row count differs")
        for index, row in enumerate(seed["cells"][str(owner)]):
            interval = exact.read_interval(row["interval"])
            require(
                interval == (Q(index, seed["bins"]), Q(index + 1, seed["bins"])),
                "seed closed row cover differs",
            )
            require(
                row["reference"] == {"kind": "wall_seed", "owner": owner, "row": index},
                "seed reference differs",
            )
            key = ref_key(row["reference"])
            require(key not in seen_refs, "duplicate seed reference")
            seen_refs.add(key)
            fact = graph.add(
                "row:" + key,
                "seed_row",
                owner,
                channels({presence[owner]: "seed_owner_wall_row"}),
                reference=copy.deepcopy(row["reference"]),
                closed_interval=row["interval"],
            )
            rows[owner].append((row, fact))
        require(
            node["initial"]["cell_references"][str(owner)]
            == [row["reference"] for row, _ in rows[owner]],
            "initial row identity differs",
        )
    count, last_updated_owner = 0, None
    for index, step in enumerate(steps):
        graph.tick()
        require(
            type(step["index"]) is int
            and step["index"] == index
            and type(step["owner"]) is int
            and step["owner"] in mask
            and step["complete"] is True
            and step["allowed_half_angle"] == ["0", "1"],
            "unknown/incomplete step grammar",
        )
        owner = step["owner"]
        last_updated_owner = owner
        require(
            set(step["prior_owned_hulls"]) == keyset
            and all(same_polygon(step["prior_owned_hulls"][str(i)], groups[i]) for i in mask),
            "prior hull custody differs",
        )
        covers = step["prior_partner_pose_covers"]
        require(type(covers) is dict, "partner cover grammar")
        partner_facts: dict[int, str] = {}
        for key, pieces in covers.items():
            partner = int(key)
            require(
                str(partner) == key and partner in mask and partner != owner,
                "foreign partner cover",
            )
            accepted = rows[partner]
            require(
                type(pieces) is list and len(pieces) == len(accepted),
                "incomplete partner row roster",
            )
            for item, (prior, _) in zip(pieces, accepted, strict=True):
                require(
                    ref_key(item["reference"]) == ref_key(prior["reference"])
                    and item["interval"] == prior["interval"],
                    "partner reference is stale/future/foreign",
                )
            partner_facts[partner] = graph.add(
                f"partner-cover:{index}:{partner}",
                "partner_pose_cover",
                partner,
                channels({fact: "complete_current_partner_row" for _, fact in accepted}),
                closed_rows=[
                    {"reference": copy.deepcopy(row["reference"]), "interval": row["interval"]}
                    for row, _ in accepted
                ],
            )
        validation_roster = graph.add(
            f"validation-roster:{index}",
            "validation_partner_roster",
            None,
            channels(dict.fromkeys(partner_facts.values(), "supplied_full_partner_cover")),
        )
        by_ref = {ref_key(row["reference"]): (row, fact) for row, fact in rows[owner]}
        cursor, new_rows = Q(0), []
        for row_index, row in enumerate(step["rows"]):
            graph.tick()
            lo, hi = exact.read_interval(row["interval"])
            require(cursor == lo < hi <= 1, "open/incomplete closed row cover")
            cursor = hi
            prior = by_ref.get(ref_key(row["prior_reference"]))
            require(prior is not None, "missing/future/foreign predecessor")
            assert prior is not None
            old_lo, old_hi = exact.read_interval(prior[0]["interval"])
            require(old_lo <= lo < hi <= old_hi, "predecessor closed interval escaped")
            reference = {
                "kind": "phase3",
                "node": node["node_id"],
                "step": index,
                "row": row_index,
            }
            require(
                row["reference"] == reference and row.get("self_hull_cuts", []) == [],
                "unknown row reference/cut grammar",
            )
            key = ref_key(reference)
            require(key not in seen_refs, "duplicate row reference")
            seen_refs.add(key)
            base = {presence[owner]: "owner_presence", prior[1]: "predecessor"}
            for other in mask:
                if other != owner and nonempty[other]:
                    base[hulls[other]] = "implicit_nonempty_foreign_hull"
            geometric, validation = dict(base), dict(base)
            validation[validation_roster] = "supplied_full_partner_roster"
            cited = set()
            for collision in row["collision_regions"]:
                partner = collision["partner"]
                require(
                    type(partner) is int and partner in partner_facts,
                    "collision partner lacks full cover",
                )
                cited.add(partner)
            for partner in cited:
                geometric[partner_facts[partner]] = "explicit_collision_full_partner_cover"
            fact = graph.add(
                "row:" + key,
                "updated_row",
                owner,
                dict(zip(CHANNELS, (geometric, validation), strict=True)),
                reference=reference,
                closed_interval=row["interval"],
                predecessor_outer_empty=not polygon(prior[0]["outer_domain"]),
                collision_partners=sorted(cited),
            )
            new_rows.append((row, fact))
        require(cursor == 1 and bool(new_rows), "incomplete owner cover")
        rows[owner] = new_rows
        hull_edges = {
            hulls[owner]: "compression_old_hull_including_replace",
            presence[owner]: "owner_presence",
            **{fact: "all_new_rows_common_kernel" for _, fact in new_rows},
        }
        hulls[owner] = graph.add(
            f"hull:{owner}:{index}",
            "updated_owned_hull",
            owner,
            channels(hull_edges),
            mode=step.get("inner_grid_compression", {}).get("mode", "accumulate"),
        )
        kernel = polygon(step["common_owned_kernel"])
        compression = step.get("inner_grid_compression")
        if compression is not None:
            require(
                compression.get("mode", "accumulate") in {"replace", "accumulate"},
                "unsupported compression grammar",
            )
            promoted = polygon(compression["vertices"])
            points = (
                promoted
                if compression.get("mode") == "replace"
                else standing.hull(polygon(groups[owner]) + promoted)
            )
            groups[owner] = [[str(x), str(y)] for x, y in points]
            nonempty[owner] = bool(points)
        else:
            require(
                not kernel or not any(row["residual_polygons"] for row, _ in new_rows),
                "missing accepted compression output",
            )
        count += 1
    require(
        count > 0 and receipt["counts"]["steps"] == count,
        "incomplete stream/standing step count",
    )
    stream_digest = getattr(steps, "content_sha256", None)
    if type(steps) is list:
        require(steps is node["steps"], "synthetic full-node step custody differs")
        stream_digest = saved.content_sha256(node)
    require(
        stream_digest is not None and stream_digest == receipt["certificate"]["node_sha256"],
        "complete streamed node identity differs",
    )
    closure = node["contradiction"]
    require(
        exact.exact_structure(closure, receipt["closure"])
        and type(closure["step"]) is int
        and closure["step"] == count - 1,
        "closure receipt/step differs",
    )
    if closure["kind"] == "all_parent_poses_forbidden":
        owner = closure["owner"]
        require(
            type(owner) is int
            and owner == last_updated_owner
            and owner in rows
            and all(not row["residual_polygons"] for row, _ in rows[owner]),
            "unsupported empty-row closure",
        )
        roots = {fact: "closure_all_final_rows" for _, fact in rows[owner]}
    elif closure["kind"] == "owned_hulls_intersect":
        owners = closure["owners"]
        require(
            type(owners) is list
            and len(owners) == 2
            and owners == sorted(set(owners))
            and all(type(owner) is int and owner in hulls for owner in owners),
            "unsupported two-hull closure",
        )
        last_owner = last_updated_owner
        require(last_owner in owners, "declared two-hull closure omits last updated owner")
        other = next(value for value in owners if value != last_owner)
        first_group, second_group = polygon(groups[last_owner]), polygon(groups[other])
        require(
            bool(first_group)
            and len(second_group) >= 3
            and bool(standing.intersect_convex(first_group, second_group)),
            "declared closure pair does not satisfy standing intersection predicate",
        )
        roots = {hulls[owner]: "closure_final_owned_hulls" for owner in owners}
    else:
        raise exact.AuditError("unsupported closure grammar")
    final = node["final_state"]
    require(
        set(final["groups"]) == set(final["cells"]) == keyset
        and all(
            same_polygon(final["groups"][str(i)], groups[i])
            and [r["reference"] for r in final["cells"][str(i)]]
            == [r["reference"] for r, _ in rows[i]]
            for i in mask
        ),
        "final state custody differs",
    )
    closure_fact = graph.add(
        "closure", "closure", None, channels(roots), closure=copy.deepcopy(closure)
    )
    geometric = graph.facts[closure_fact][CHANNELS[0]]["owners"]
    validation = graph.facts[closure_fact][CHANNELS[1]]["owners"]
    first_use: dict[str, dict[str, dict[str, Any]]] = {}
    for channel in CHANNELS:
        reachable, pending = set(), [closure_fact]
        while pending:
            graph.tick()
            current = pending.pop()
            if current in reachable:
                continue
            reachable.add(current)
            pending.extend(edge["fact"] for edge in graph.facts[current][channel]["edges"])
        reasons: dict[str, dict[str, Any]] = {}
        for fact in graph.facts.values():
            if fact["id"] not in reachable:
                continue
            for edge in fact[channel]["edges"]:
                if edge["reason"] in {
                    "frame_cell_wall_root",
                    "owner_presence",
                    "seed_owner_wall_row",
                }:
                    continue
                for dependency_owner in graph.facts[edge["fact"]][channel]["owners"]:
                    owner_reasons = reasons.setdefault(str(dependency_owner), {})
                    owner_reasons.setdefault(
                        edge["reason"], {"fact": fact["id"], "dependency": edge["fact"]}
                    )
        first_use[channel] = reasons
    return {
        "schema": SCHEMA,
        "status": "inventory_complete",
        "inventory_complete": True,
        "rules": dict(RULES),
        "original_mask": mask,
        "original_named_cells": [cells.names[i] for i in mask],
        "frame": {
            "cap": str(cells.cap),
            "unit_scale": "1",
            "world_cell_names": list(cells.names),
            "world_unchanged": True,
        },
        "closure_roots": sorted(roots),
        "closure_fact": closure_fact,
        "geometric_owner_set": geometric,
        "validation_owner_set": validation,
        "strict_subset_proposal": set(geometric) < set(mask),
        "proposal_named_cells": [cells.names[i] for i in geometric],
        "typed_fact_counts": dict(Counter(f["kind"] for f in graph.facts.values())),
        "typed_edge_count": graph.edge_count,
        "first_use_reasons": first_use,
        "dag": list(graph.facts.values()),
        "standing_custody": copy.deepcopy(receipt),
        "future_acceptance": (
            "separate registered typed projection and FULL standing smaller-arity replay only"
        ),
        **FALSE_FLAGS,
    }


def load_inventory(
    directory: Path,
    receipt_path: Path,
    *,
    seconds: float,
    max_facts: int,
    max_edges: int,
    max_node_bytes: int = 512 << 20,
    max_decoded_node_bytes: int = 2 << 30,
) -> dict[str, Any]:
    require(
        math.isfinite(seconds)
        and seconds > 0
        and 0 < max_facts <= 25000
        and 0 < max_edges <= 500000
        and type(max_node_bytes) is int
        and 0 < max_node_bytes <= 512 << 20,
        "invalid inventory ceiling",
    )
    require(
        type(max_decoded_node_bytes) is int and 0 < max_decoded_node_bytes <= 2 << 30,
        "invalid decoded node ceiling",
    )
    deadline = time.monotonic() + seconds
    # Bounded preflight before the existing streaming parser; retain one step at a time.
    from devtools import check_n17_capture_leaf as consumer  # noqa: PLC0415

    seed_path, node_path = saved.saved_files(directory)
    require(
        seed_path.resolve().parent == node_path.resolve().parent == directory.resolve(),
        "saved objects escape directory",
    )
    if seed_path.stat().st_size > 10 << 20 or node_path.stat().st_size > max_node_bytes:
        raise IncompleteError("compressed object byte ceiling")
    frozen = [consumer.file_digest(path) for path in (seed_path, node_path)]
    try:
        seed = exact.decode(
            consumer.bounded_gzip(seed_path, 10 << 20, deadline=deadline, retain=True)
        )
        consumer.bounded_gzip(node_path, max_decoded_node_bytes, deadline=deadline)
    except consumer.IncompleteError as error:
        raise IncompleteError(str(error)) from error
    except exact.AuditError as error:
        if str(error) == "saved gzip decoded byte ceiling":
            raise IncompleteError(str(error)) from error
        raise
    receipt_bytes = exact.read_bytes(receipt_path)
    receipt_digest = hashlib.sha256(receipt_bytes).hexdigest()
    receipt = exact.decode(receipt_bytes)
    require(
        receipt["directory"] == str(directory.resolve().relative_to(exact.REPO)),
        "standing receipt directory differs",
    )
    packet, steps = saved.stream_node(node_path)
    result = inventory(
        seed,
        packet,
        steps,
        receipt,
        standing.cover_cells(),
        deadline=deadline,
        max_facts=max_facts,
        max_edges=max_edges,
    )
    require(
        steps.content_sha256 == receipt["certificate"]["node_sha256"],
        "complete streamed node identity differs",
    )
    require(
        frozen == [consumer.file_digest(path) for path in (seed_path, node_path)],
        "saved objects changed during inventory",
    )
    require(
        hashlib.sha256(exact.read_bytes(receipt_path)).hexdigest() == receipt_digest,
        "standing receipt changed during inventory",
    )
    result["inputs"] = {
        "directory": receipt["directory"],
        "standing_receipt": str(receipt_path.resolve().relative_to(exact.REPO)),
        "standing_receipt_sha256": receipt_digest,
        "seed_sha256": saved.content_sha256(seed),
        "node_sha256": steps.content_sha256,
    }
    return result


def output_ceiling(result: dict[str, Any], limit: int) -> None:
    if len(retained_json.dumps(result).encode()) > limit:
        raise IncompleteError("dependency output byte ceiling")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saved", type=Path, required=True)
    parser.add_argument("--standing-receipt", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=90)
    parser.add_argument("--max-facts", type=int, default=25000)
    parser.add_argument("--max-edges", type=int, default=500000)
    parser.add_argument("--max-node-bytes", type=int, default=512 << 20)
    parser.add_argument("--max-decoded-node-bytes", type=int, default=2 << 30)
    parser.add_argument("--max-output-bytes", type=int, default=64 << 20)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        require(
            type(args.max_output_bytes) is int and 0 < args.max_output_bytes <= 64 << 20,
            "invalid output byte ceiling",
        )
        result = load_inventory(
            args.saved,
            args.standing_receipt,
            seconds=args.max_seconds,
            max_facts=args.max_facts,
            max_edges=args.max_edges,
            max_node_bytes=args.max_node_bytes,
            max_decoded_node_bytes=args.max_decoded_node_bytes,
        )
        result["deterministic_inventory_sha256"] = saved.content_sha256(result)
        output_ceiling(result, args.max_output_bytes)
    except (IncompleteError, TimeoutError) as error:
        result = {
            "schema": SCHEMA,
            "status": "incomplete",
            "inventory_complete": False,
            "error": str(error),
            **FALSE_FLAGS,
        }
    except (
        ValueError,
        OSError,
        EOFError,
        KeyError,
        TypeError,
        IndexError,
        standing.VerificationError,
    ) as error:
        result = {
            "schema": SCHEMA,
            "status": "refused",
            "inventory_complete": False,
            "error": str(error),
            **FALSE_FLAGS,
        }
    result["execution"] = {
        "argv": list(argv) if argv is not None else sys.argv[1:],
        "python": sys.version,
        "limits": {
            "inventory_seconds": str(args.max_seconds),
            "seed_compressed_and_decoded_bytes": 10 << 20,
            "node_compressed_bytes": args.max_node_bytes,
            "node_decoded_bytes": args.max_decoded_node_bytes,
            "facts": args.max_facts,
            "total_channel_edges": args.max_edges,
            "retained_output_bytes": args.max_output_bytes,
        },
    }
    result["provenance"] = provenance(
        Path(__file__),
        Path(saved.__file__),
        Path(standing.__file__),
        Path(exact.__file__),
        Path(cover.__file__),
        Path(__file__).with_name("check_n17_capture_leaf.py"),
    )
    if result["inventory_complete"]:
        try:
            output_ceiling(result, args.max_output_bytes)
        except IncompleteError as error:
            result = {
                "schema": SCHEMA,
                "status": "incomplete",
                "inventory_complete": False,
                "error": str(error),
                "execution": result["execution"],
                "provenance": result["provenance"],
                **FALSE_FLAGS,
            }
    args.output.write_text(retained_json.dumps(result))
    print(
        json.dumps(
            {
                key: value
                for key, value in result.items()
                if key not in {"dag", "standing_custody", "provenance"}
            }
        )
    )
    return 0 if result["inventory_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
