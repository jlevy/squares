"""Replay n11's case 2095 (mode A) through `sqpack.hull_kernel` on the n11 frame.

The method control for the induction path of the hull-kernel adaptation (BC-418, slice
1b). Every input is loaded under the frozen fresh-wall checker's own pins
(`check_n11_generic_fresh`, SHA-256 `e8fcfd02...`) and then held to a canonical-JSON
content digest, so the library sees exactly what that checker admitted. Then:

1. the library proves the seed (77 owned points, 352 wall rows), replays the five
   sequential owner updates (160 rows), promotes each kernel by its convex-combination
   witnesses, checks every published state (each step's prior hulls and the final state)
   and the terminal contradiction, and transfers the exclusion by containment and the
   half-turn;
2. the frozen checker's own `_seed` and `_full` run on the same inputs (in a second
   process with `--workers 2`) with its ownership proofs, row results and compressions
   recorded as they are returned;
3. the two are compared object for object, and both against the retained receipt
   `receipts/generic-mask2095-intake/full-result.json`, pinned by its SHA-256.

Any difference refuses and names the first differing path. `--sample` checks owner 6's
seed, step 0's first row and step 0's compression against the frozen functions and the
receipt; it is a partial check and claims nothing.
"""

# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections.abc import Callable, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import check_hull_kernel_mask0 as mask0_tool
from devtools import check_n11_generic_fresh as frozen
from devtools import check_n11_optimality_field_mask0 as frozen_geometry
from sqpack.hull_kernel import n11, node
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.induction import hull
from sqpack.hull_kernel.rational import as_fraction

RECEIPT_DIR = frozen.PACKET / "receipts/generic-mask2095-intake"
RECEIPT = RECEIPT_DIR / "full-result.json"
RECEIPT_SHA = "2aa9c3819e4f39d9f4f489a25d1885b2a1c5a6f6c21099f42821d1165d608f88"
FROZEN_SHA = "e8fcfd02560d09e7a2a5b2622976ab021ef15a4456a2824b37abae926f6ab7d3"
# SHA-256 of the canonical JSON (sorted keys, no spaces) of each admitted object.
CONTENT_SHA = {
    "cover": "883f21ed4b666724dfdfa85eefdab4252db6be0a74b95e3b6e958a7c37a1171b",
    "source": "264898d158141da55d5ec7fa6b85ca6ae3abb218c47e4d0805c51ce28bbd9b99",
    "seed": "2b8bc9ce2d5e54f596fb80e7c817c5f0350cdb61ba2c0064497d030be8b71043",
    "audit": "1536b51ab58950cf195f516560ee9d1d9c4dc242f59252bed7ae1f6d20e7ddf9",
}
MASK_INDEX = 2095
BINS = 32
MAX_EVENTS = 50_000
SEED_POINTS = 77
SEED_ROWS = 352
STEP_OWNERS = (6, 10, 7, 14, 11)
STEP_ROWS = 160
CONTRADICTION = {"kind": "all_parent_poses_forbidden", "owner": 11, "step": 4}
FROZEN_PASS = "PASS_ONE_GENERIC_EXCLUSION"


@dataclass(frozen=True)
class Sources:
    cover: dict[str, Any]
    source: dict[str, Any]
    seed: dict[str, Any]
    audit: dict[str, Any]
    a1: dict[str, Any]

    def named(self) -> dict[str, dict[str, Any]]:
        return {
            "cover": self.cover,
            "source": self.source,
            "seed": self.seed,
            "audit": self.audit,
        }


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_sources() -> Sources:
    """Every input under the frozen checker's pins, with its bindings admitted."""
    frozen_geometry.admit_d4_receipt()
    cover = frozen._load_pin(
        frozen.COVER,
        (frozen_geometry.COVER_SHA, 773_471, frozen_geometry.COVER_LFS_SHA, 25_016),
    )
    source = frozen._load_pin(frozen.OBJECTS / f"{frozen.SOURCE_PIN[0]}.gz", frozen.SOURCE_PIN)
    seed = frozen._load_pin(frozen.OBJECTS / f"{frozen.SEED_PIN[0]}.gz", frozen.SEED_PIN)
    audit = frozen._load_pin(frozen.OBJECTS / f"{frozen.AUDIT_PIN[0]}.gz", frozen.AUDIT_PIN)
    a1 = frozen._load_pin(frozen.A1_OBJECT, frozen.A1_PIN)
    return Sources(cover, source, seed, audit, a1)


def admit_content(sources: Sources) -> None:
    for name, value in sources.named().items():
        if mask0_tool.content_digest(value) != CONTENT_SHA[name]:
            raise RefusalError(f"{name} content differs from the pinned object")


def admit_bindings(sources: Sources) -> None:
    """The n11-specific identities the frozen `run` and `_full` check before any geometry."""
    audit, seed = sources.audit, sources.seed
    if not (
        audit["source_sha256"] == frozen.SOURCE_PIN[0]
        and audit["root_sha256"] == frozen.SEED_PIN[0]
        and audit["cover_sha256"] == frozen_geometry.COVER_SHA
        and audit["mask_index"] == MASK_INDEX
        and audit["mask"] == list(frozen.MASK)
        and audit["required_antecedent_mask"] == list(frozen.MASK)
        and audit["transferred_canonical_mask_indices"] == [MASK_INDEX]
    ):
        raise RefusalError("audit identity changed")
    if seed["cover_source"]["sha256"] != frozen_geometry.COVER_SHA:
        raise RefusalError("seed cover binding")
    assignments = [cert for cert in sources.a1["certificates"] if MASK_INDEX in cert["cases"]]
    if not (
        len(assignments) == 1
        and assignments[0]["family"] == "generic"
        and assignments[0]["source_sha256"] == frozen.SOURCE_PIN[0]
        and assignments[0]["fresh_audit_sha256"] == frozen.AUDIT_PIN[0]
        and assignments[0]["cases"] == [MASK_INDEX]
    ):
        raise RefusalError("A1 does not assign exactly this generic case to the pinned source")


def load_receipt() -> dict[str, Any]:
    raw = RECEIPT.read_bytes()
    if sha(raw) != RECEIPT_SHA:
        raise RefusalError("retained case-2095 receipt changed")
    receipt = frozen_geometry.strict_json(raw)
    if (
        receipt.get("status") != FROZEN_PASS
        or receipt["source_sha256"]["checker"] != FROZEN_SHA
    ):
        raise RefusalError("retained case-2095 receipt identity changed")
    return receipt


def admit_frozen_source() -> None:
    if sha(Path(frozen.__file__).read_bytes()) != FROZEN_SHA:
        raise RefusalError("the frozen case-2095 checker changed")


def library_frame(sources: Sources) -> Frame:
    admit_content(sources)
    admit_bindings(sources)
    return n11.frame_from_cover(
        sources.cover, provenance=f"n11 cover {frozen_geometry.COVER_SHA}"
    )


def library_replay(sources: Sources, *, max_seconds: float) -> dict[str, Any]:
    """The library's whole replay, as plain data for comparison."""
    frame = library_frame(sources)
    budget = Budget(time.monotonic() + max_seconds, MAX_EVENTS)
    seed = node.admit_seed(frame, sources.seed, mask_index=MASK_INDEX, bins=BINS, budget=budget)
    if len(seed.proofs) != SEED_POINTS or sum(map(len, seed.rows.values())) != SEED_ROWS:
        raise RefusalError("seed census changed")
    node.admit_header(
        frame, sources.source, seed, mask_index=MASK_INDEX, seed_sha256=frozen.SEED_PIN[0]
    )
    trace = node.replay_node(
        frame, sources.source, seed, mask_index=MASK_INDEX, bins=BINS, budget=budget
    )
    if tuple(step.owner for step in trace.steps) != STEP_OWNERS:
        raise RefusalError("step owner order changed")
    if trace.contradiction != CONTRADICTION:
        raise RefusalError("terminal contradiction changed")
    excluded = frame.states_containing(frame.representatives[MASK_INDEX])
    if excluded != sources.audit["transferred_canonical_mask_indices"]:
        raise RefusalError("library transfer differs from the audit's")
    return {
        "seed_groups": seed.groups,
        "seed_rows": seed.rows,
        "proofs": [
            {key: value for key, value in proof.items() if key not in ("owner", "point_index")}
            for proof in seed.proofs
        ],
        "rows": [result for step in trace.steps for result in step.rows],
        "compressions": [step.group for step in trace.steps if any(r[1] for r in step.rows)],
        "excluded_case_ids": excluded,
    }


def _recording[**P, R](function: Callable[P, R], sink: list[R]) -> Callable[P, R]:
    def recorded(*args: P.args, **kwargs: P.kwargs) -> R:
        value = function(*args, **kwargs)
        sink.append(value)
        return value

    return recorded


def frozen_replay(max_seconds: float) -> dict[str, Any]:
    """The frozen checker's own seed and `_full`, with what it accepts recorded.

    The frozen module's functions are wrapped, never edited, and only for this call; a
    worker process runs it so that the wrapping touches nothing else.
    """
    admit_frozen_source()
    sources = load_sources()
    proofs: list[dict[str, Any]] = []
    rows: list[Any] = []
    compressions: list[Any] = []
    originals = (frozen_geometry.ownership, frozen._check_row, frozen._compressed)
    frozen_geometry.ownership = _recording(originals[0], proofs)
    frozen._check_row = _recording(originals[1], rows)
    frozen._compressed = _recording(originals[2], compressions)
    try:
        started = time.monotonic()
        budget = frozen_geometry.Budget(started + max_seconds, MAX_EVENTS)
        groups, seed_rows, world = frozen._seed(sources.seed, sources.cover, budget=budget)
        result: dict[str, Any] = {}
        frozen._full(
            sources.source,
            sources.audit,
            sources.a1,
            groups,
            seed_rows,
            world=world,
            result=result,
            budget=budget,
            workers=1,
        )
        result["wall_seconds"] = time.monotonic() - started
    finally:
        frozen_geometry.ownership, frozen._check_row, frozen._compressed = originals
    return {
        "seed_groups": groups,
        "seed_rows": seed_rows,
        "proofs": proofs,
        "rows": rows,
        "compressions": compressions,
        "result": result,
    }


def receipt_projection(result: dict[str, Any]) -> dict[str, Any]:
    """The receipt fields a replay must reproduce: counts, owners, per-row events and probes."""
    return {
        "rows_checked": result["rows_checked"],
        "steps_completed": result["steps_completed"],
        "steps": [
            {
                "owner": step["owner"],
                "rows": step["rows"],
                "row_events": step["row_events"],
                "row_probes": step["row_probes"],
                "row_cover": [[row["events"], row["probes"]] for row in step["row_timings"]],
            }
            for step in result["step_timings"]
        ],
    }


def library_projection(library: dict[str, Any]) -> dict[str, Any]:
    rows = library["rows"]
    steps = []
    for number, owner in enumerate(STEP_OWNERS):
        block = rows[number * BINS : (number + 1) * BINS]
        steps.append(
            {
                "owner": owner,
                "rows": len(block),
                "row_events": sum(row[0]["events"] for row in block),
                "row_probes": sum(row[0]["probes"] for row in block),
                "row_cover": [[row[0]["events"], row[0]["probes"]] for row in block],
            }
        )
    return {"rows_checked": len(rows), "steps_completed": len(STEP_OWNERS), "steps": steps}


def as_fractions(polygon: Sequence[tuple[Any, Any]]) -> list[tuple[Fraction, Fraction]]:
    """The kernel's polygon as the frozen checker's `Fraction` points; the values are equal."""
    return [(as_fraction(x), as_fraction(y)) for x, y in polygon]


def require_same(left: Any, right: Any, what: str) -> None:
    """Exact equality; on a difference, the first differing path of the JSON forms."""
    if left == right:
        return
    found = mask0_tool.first_difference(_plain(left), _plain(right))
    raise RefusalError(f"{what} differ at {found or 'the root (types)'}")


def _plain(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str, sort_keys=True))


def full_replay(sources: Sources, *, max_seconds: float, workers: int = 2) -> dict[str, Any]:
    admit_frozen_source()
    receipt = load_receipt()
    if workers > 1:
        with ProcessPoolExecutor(max_workers=1) as pool:
            pending = pool.submit(frozen_replay, max_seconds)
            started = time.monotonic()
            library = library_replay(sources, max_seconds=max_seconds)
            library_seconds = time.monotonic() - started
            reference = pending.result()
    else:
        started = time.monotonic()
        library = library_replay(sources, max_seconds=max_seconds)
        library_seconds = time.monotonic() - started
        reference = frozen_replay(max_seconds)
    for key in ("seed_groups", "seed_rows", "proofs", "rows", "compressions"):
        require_same(library[key], reference[key], f"library and frozen {key}")
    projection = library_projection(library)
    require_same(
        projection, receipt_projection(reference["result"]), "library and frozen counts"
    )
    require_same(projection, receipt_projection(receipt), "library and receipt counts")
    if not (
        receipt["owned_seed_points_checked"] == len(library["proofs"]) == SEED_POINTS
        and receipt["seed_rows_checked"] == SEED_ROWS
        and receipt["excluded_case_ids"] == library["excluded_case_ids"] == [MASK_INDEX]
        and receipt["geometry_verified"] is True
    ):
        raise RefusalError("library and receipt seed or exclusion differ")
    return {
        "status": "PASS_LIBRARY_REPRODUCES_CASE2095",
        "seed_points": len(library["proofs"]),
        "seed_rows": SEED_ROWS,
        "steps": len(STEP_OWNERS),
        "step_owners": list(STEP_OWNERS),
        "step_rows": len(library["rows"]),
        "row_events": [step["row_events"] for step in projection["steps"]],
        "row_probes": [step["row_probes"] for step in projection["steps"]],
        "compressions": len(library["compressions"]),
        "published_states_matched": len(STEP_OWNERS),
        "contradiction": CONTRADICTION,
        "excluded_case_ids": library["excluded_case_ids"],
        "compared": [
            "ownership proofs",
            "seed hulls and rows",
            "every row's cover, residual vertices, planes and accepted row",
            "every compressed hull",
            "per-row events and probes against the receipt",
        ],
        "library_wall_seconds": library_seconds,
        "frozen_wall_seconds": reference["result"]["wall_seconds"],
        "geometry_verified": True,
    }


def sample_replay(sources: Sources, *, max_seconds: float) -> dict[str, Any]:
    """Owner 6's seed, step 0's first row and step 0's compression, against the frozen."""
    admit_frozen_source()
    receipt = load_receipt()
    frame = library_frame(sources)
    budget = Budget(time.monotonic() + max_seconds, MAX_EVENTS)
    frozen_budget = frozen_geometry.Budget(time.monotonic() + max_seconds, MAX_EVENTS)
    seed = node.admit_seed(
        frame, sources.seed, mask_index=MASK_INDEX, bins=BINS, budget=budget, owners=[6]
    )
    group = frozen.points(sources.seed["groups"]["6"])
    require_same(
        [
            {key: value for key, value in proof.items() if key not in ("owner", "point_index")}
            for proof in seed.proofs
        ],
        [
            frozen_geometry.ownership(
                frozen_geometry.cell_vertices(sources.cover, 6), point, budget=frozen_budget
            )
            for point in group
        ],
        "library and frozen owner-6 proofs",
    )
    prior = {
        owner: hull(node.points(sources.seed["groups"][str(owner)])) for owner in frozen.MASK
    }
    step = sources.source["steps"][0]
    row = node.check_row(
        frame,
        sources.source,
        step,
        step["rows"][0],
        row_index=0,
        owner=6,
        bins=BINS,
        prior=prior,
        predecessor=seed.rows[6][0],
        budget=budget,
    )
    world = [frozen.points(polygon) for polygon in sources.seed["world"]]
    reference = frozen._check_row(
        sources.source,
        step,
        step["rows"][0],
        0,
        6,
        prior={owner: as_fractions(polygon) for owner, polygon in prior.items()},
        predecessor=seed.rows[6][0],
        world=world,
        budget=frozen_budget,
    )
    require_same(row, reference, "library and frozen step-0 row 0")
    first = receipt["step_timings"][0]["row_timings"][0]
    require_same(
        [row[0]["events"], row[0]["probes"]],
        [first["events"], first["probes"]],
        "library and receipt step-0 row 0",
    )
    kernel = node.points(step["common_owned_kernel"])
    require_same(
        node.compressed(step, prior[6], kernel),
        frozen._compressed(step, as_fractions(prior[6]), as_fractions(kernel)),
        "library and frozen step-0 compression",
    )
    return {
        "status": "PASS_PARTIAL_SAMPLE",
        "seed_points_checked": len(seed.proofs),
        "seed_rows_checked": len(seed.rows[6]),
        "rows_checked": 1,
        "row_cover": row[0],
        "geometry_verified": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sample", action="store_true", help="a partial replay; claims nothing"
    )
    parser.add_argument("--workers", type=int, choices=(1, 2), default=2)
    parser.add_argument("--max-seconds", type=float, default=300.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("the wall ceiling must be positive and finite")
    start, cpu = time.monotonic(), time.process_time()
    try:
        sources = load_sources()
        if args.sample:
            result = sample_replay(sources, max_seconds=args.max_seconds)
        else:
            result = full_replay(sources, max_seconds=args.max_seconds, workers=args.workers)
    except (IncompleteError, frozen_geometry.IncompleteError) as error:
        result = {"status": "INCOMPLETE", "reason": str(error), "geometry_verified": False}
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result = {"status": "REFUSED", "reason": str(error), "geometry_verified": False}
    result.update(
        kernel_sha256=mask0_tool.kernel_digests(),
        frozen_checker_sha256=FROZEN_SHA,
        receipt_sha256=RECEIPT_SHA,
        tool_sha256=sha(Path(__file__).read_bytes()),
        wall_seconds=time.monotonic() - start,
        process_cpu_seconds=time.process_time() - cpu,
        wall_ceiling_seconds=args.max_seconds,
    )
    encoded = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if str(result["status"]).startswith("PASS") else 2


if __name__ == "__main__":
    sys.exit(main())
