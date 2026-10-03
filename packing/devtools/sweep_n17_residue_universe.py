"""Sweep of the n17 residue's arity-8-to-10 universe in float search (H-267). Not a certificate.

Lane F1's ranked plan, step 2 (cost-reduction review, sections 2.4, 2.6 and 3.1). The
residue is the states of the unique-state cover that survive every confirmed selector flag
(the selector's re-check receipt). Its *universe* at arity `k` is every connected class of
`k` cells that occurs in some residue state and lies in no D4 image of the endpoint's
state: a class in no residue state removes nothing whatever its verdict, and a class in an
endpoint image is placed by the endpoint's own pose, so both restrictions are exact for
the consumer. Every class is searched with the selector's `recheck_flag`, sub-pattern
witnesses first and then the class warm started from them, under a screen budget (12
starts, 24 hops, 48 and 48 deep attempts, the finish); a class the screen cannot place is
searched again under the selector's full budget, and is flagged only if that fails too.
Each verdict is the selector's, seeded by the run seed and the class's mask, so it does
not depend on the order or on the chunking.

Order. F1's locality-filtered queues come first: arity 8 at three to five missing pairs,
then arity 9 at most two, then arity 10 at most two; then the rest by arity and missing
pairs. Within a queue, classes go by residue coverage (the residue orbits holding an image
of the class), most first. Arity-8 classes with at most two missing pairs are not queued:
the arity-8 priority sweep searched them all and the residue holds only those it placed.

Resumable. `plan` writes the queue once (`plan.json`, with the flag masks it was planned
under, which a second `plan` must reproduce). `sweep` searches it in chunks of a fixed
size and writes each chunk's receipt atomically when it completes; rerun with the same
arguments after a restart and it skips every chunk already written. `summary` reads the
plan and the chunks, each of which must hold the plan's queue at its index: per queue, the
classes searched, placed and flagged and the hit rate; and the greedy cover of the
residue's orbits by the flags found so far, with the falsifier of F1's plan (a cover of
less than half).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections.abc import Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from devtools import select_n17_sub_patterns as selector
from devtools.provenance import provenance

PLAN_SCHEMA = "n17-residue-universe-plan/v1"
CHUNK_SCHEMA = "n17-residue-universe-chunk/v1"
SUMMARY_SCHEMA = "n17-residue-universe-summary/v1"
STATUS = (
    "float search, not a certificate: a flag is a class the selector's search with the "
    "finish could not place; the prover must certify it before it excludes anything"
)
PROVENANCE = provenance(Path(__file__))
SCREEN = selector.Budget(starts=12, hops=24, deep_starts=48, deep_hops=48)
FULL = selector.Budget()
# The random-first stage: a few random starts on a stream the old search never draws from,
# no hops, no deep stage, no finish. A placement there is a placement; a class it cannot
# place goes on to the old search, unchanged.
FIRST_STREAM = 1
FIRST_PLAIN = selector.Budget(starts=4, hops=0, deep_starts=0, deep_hops=0, finish=False)
FIRST = replace(FIRST_PLAIN, early_stop=True, fast_penalty=True)


@dataclass(frozen=True)
class Levers:
    """Cuts to the sweep's search time, each measurable on its own.

    `first` is the random-first stage; `cache` keeps every sub-pattern witness for the
    process, keyed by its exact mask and budget, so a verdict is the one the uncached search
    gives, byte for byte; `early_stop` and `fast_penalty` change the screen's and the full
    budget's descents, so they change poses at the level of rounding and are measured
    for verdict equivalence rather than assumed. `resume` lets the full budget continue
    from the screen's state after its deep starts instead of repeating the warm starts,
    random starts, hops and deep starts before it. The two budgets share the prefix
    (`selector.budget_prefix`), which decides the sub-pattern witnesses, the warm starts and
    every attempt up to that point, and the checkpoint carries the generator's state, so
    the verdict is the one the full budget gives from scratch, byte for byte; it applies
    only where the prefixes match, and `resume-check` measures it class by class.
    """

    first: selector.Budget | None = None
    cache: bool = False
    early_stop: bool = False
    fast_penalty: bool = False
    resume: bool = False

    def record(self) -> dict[str, Any]:
        return {
            "first": None if self.first is None else budget_record(self.first),
            "cache": self.cache,
            "early_stop": self.early_stop,
            "fast_penalty": self.fast_penalty,
            "resume": self.resume,
        }


LEVERS = {
    "baseline": Levers(),
    "first": Levers(first=FIRST_PLAIN),
    "cache": Levers(cache=True),
    "early-stop": Levers(early_stop=True),
    "fast-penalty": Levers(fast_penalty=True),
    "combined": Levers(first=FIRST, cache=True),
    "combined-fast": Levers(first=FIRST, cache=True, early_stop=True, fast_penalty=True),
    "combined-fast-resume": Levers(
        first=FIRST, cache=True, early_stop=True, fast_penalty=True, resume=True
    ),
}
ARITIES = (8, 9, 10)
PRIORITY_TESTED = (8, 2)  # the arity-8 priority sweep searched every class up to 2 missing
QUEUES: tuple[tuple[str, int, int, int | None], ...] = (
    ("arity 8, three to five missing pairs", 8, 3, 5),
    ("arity 9, at most two missing pairs", 9, 0, 2),
    ("arity 10, at most two missing pairs", 10, 0, 2),
    ("arity 8, six or more missing pairs", 8, 6, None),
    ("arity 9, three to five missing pairs", 9, 3, 5),
    ("arity 10, three to five missing pairs", 10, 3, 5),
    ("arity 9, six or more missing pairs", 9, 6, None),
    ("arity 10, six or more missing pairs", 10, 6, None),
)

States = NDArray[np.int64]


@dataclass(frozen=True)
class Residue:
    """The surviving states, their orbit index, and the endpoint's images."""

    alive: States
    orbit_of: NDArray[np.int64]
    orbits: int
    endpoint_images: tuple[int, ...]


def orbit_index(
    alive: States, group: tuple[tuple[int, ...], ...]
) -> tuple[NDArray[np.int64], int]:
    """Each state's orbit, numbered by its least image."""
    if not alive.size:
        return np.zeros(0, dtype=np.int64), 0
    least = np.min(np.stack([selector.apply_permutation(alive, p) for p in group]), axis=0)
    _, inverse = np.unique(least, return_inverse=True)
    return inverse.astype(np.int64), int(inverse.max()) + 1


def make_residue(
    geometry: selector.Geometry,
    flags: list[int],
    endpoint_state: int,
    *,
    size: int = selector.TARGET,
) -> Residue:
    states = selector.all_states(len(geometry.names), size)
    images = sorted({image for mask in flags for image in selector.orbit(mask, geometry.group)})
    alive = selector.survivors(states, images)
    orbit_of, orbits = orbit_index(alive, geometry.group)
    return Residue(
        alive, orbit_of, orbits, tuple(sorted(selector.orbit(endpoint_state, geometry.group)))
    )


def hit_orbits(
    residue: Residue, group: tuple[tuple[int, ...], ...], mask: int
) -> NDArray[np.int64]:
    """The residue orbits holding some image of the class."""
    hit = np.zeros(residue.alive.size, dtype=np.bool_)
    for image in selector.orbit(mask, group):
        hit |= (residue.alive & image) == image
    return np.unique(residue.orbit_of[hit])


def universe(
    geometry: selector.Geometry, residue: Residue, arities: Sequence[int]
) -> list[dict[str, Any]]:
    """Every connected class of the arities in some residue state and no endpoint image."""
    rows: list[dict[str, Any]] = []
    for arity in arities:
        classes = selector.pattern_classes(geometry, arity, None)
        free = [m for m in classes if not any(m & e == m for e in residue.endpoint_images)]
        rows.extend(
            {
                "mask": mask,
                "arity": arity,
                "missing": selector.missing_pairs(geometry, mask),
                "coverage": int(hit_orbits(residue, geometry.group, mask).size),
            }
            for mask in sorted(selector.occurring_classes(free, residue.alive))
        )
    return rows


def queue_of(row: dict[str, Any]) -> int | None:
    for index, (_, arity, low, high) in enumerate(QUEUES):
        if (
            row["arity"] == arity
            and low <= row["missing"]
            and (high is None or row["missing"] <= high)
        ):
            return index
    return None


def make_queue(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """The queue in F1's order, and the classes left out of it."""
    queued: list[dict[str, Any]] = []
    left: list[dict[str, Any]] = []
    for row in rows:
        index = queue_of(row)
        if index is None:
            left.append(row)
        else:
            queued.append({**row, "queue": index})
    queued.sort(key=lambda r: (r["queue"], -r["coverage"], r["mask"]))
    return queued, left


def load_flags(path: Path, geometry: selector.Geometry) -> list[int]:
    """The flags still standing: a re-check receipt's `flagged`, or any selector receipt's."""
    document = json.loads(path.read_text(encoding="utf-8"))
    return sorted(
        {
            selector.canonical(selector.mask_of(flag["indices"]), geometry.group)
            for flag in document["flagged"]
        }
    )


def digest_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_atomic(path: Path, document: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".partial")
    _ = temporary.write_text(
        json.dumps(document, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )
    _ = temporary.replace(path)


def plan(
    flags_path: Path, directory: Path, *, arities: Sequence[int] = ARITIES
) -> dict[str, Any]:
    """Compute and write the queue once; reuse it if it was planned under the same flags.

    The flags are compared as the sorted list of canonical masks; a plan written before it
    recorded them is compared by their count.
    """
    target = directory / "plan.json"
    geometry = selector.cover_geometry()
    flags = load_flags(flags_path, geometry)
    if target.exists():
        written = json.loads(target.read_text(encoding="utf-8"))
        same = (
            written["flag_masks"] == flags
            if "flag_masks" in written
            else written["flags"] == len(flags)
        )
        if not same:
            raise ValueError(f"{target} was planned under other flags; use a new directory")
        return written
    clock = time.perf_counter()
    endpoint = selector.mask_of(selector.endpoint_pose()["cells"])
    residue = make_residue(geometry, flags, endpoint)
    rows = universe(geometry, residue, arities)
    queued, left = make_queue(rows)
    by_arity: dict[str, Any] = {}
    for arity in arities:
        mine = [r for r in rows if r["arity"] == arity]
        counts = [r["missing"] for r in mine]
        coverages = sorted(r["coverage"] for r in mine)
        by_arity[str(arity)] = {
            "classes": len(mine),
            "by_missing_pairs": [counts.count(d) for d in range(max(counts, default=-1) + 1)],
            "coverage_max": coverages[-1] if coverages else 0,
            "coverage_median": coverages[len(coverages) // 2] if coverages else 0,
            "left_out": sum(1 for r in left if r["arity"] == arity),
        }
    document = {
        "schema": PLAN_SCHEMA,
        "status": STATUS,
        "design": selector.DEFAULT_DESIGN,
        "flags_source": {"path": str(flags_path)},
        "flags": len(flags),
        "flag_masks": flags,
        "residue": {
            "states": int(residue.alive.size),
            "orbits": residue.orbits,
            "endpoint_survives": endpoint in set(residue.alive.tolist()),
        },
        "universe": by_arity,
        "left_out_rule": "arity 8 at most two missing pairs: the priority sweep searched them",
        "queues": [
            {"name": name, "classes": sum(1 for r in queued if r["queue"] == index)}
            for index, (name, _, _, _) in enumerate(QUEUES)
        ],
        "queue": [
            [r["mask"], r["arity"], r["missing"], r["coverage"], r["queue"]] for r in queued
        ],
        "provenance": PROVENANCE,
        "seconds": round(time.perf_counter() - clock, 3),
    }
    directory.mkdir(parents=True, exist_ok=True)
    write_atomic(target, document)
    return document


Cache = dict[tuple[int, selector.Budget], selector.Verdict]


def first_stage(
    geometry: selector.Geometry, mask: int, *, seed: int, levers: Levers
) -> dict[str, Any] | None:
    """The random-first stage's row for a class it places; None if it is off or fails."""
    if levers.first is None:
        return None
    stream = np.random.default_rng(np.random.SeedSequence([seed, mask, FIRST_STREAM]))
    quick = selector.search(geometry, selector.cells_of(mask), stream, levers.first)
    if not quick.feasible:
        return None
    return {
        "screen": "placed",
        "screen_attempts": quick.attempts,
        "status": "placed",
        "best_penetration": quick.violation,
        "attempts": quick.attempts,
        "found_by": "random-first",
    }


def tuned_budgets(
    screen: selector.Budget, full: selector.Budget, levers: Levers
) -> tuple[selector.Budget, selector.Budget, bool]:
    """The screen and the full budget under the descent levers, and whether the full one
    passes through the screen's state after its deep starts, so that it may resume there."""
    tuned = {"early_stop": levers.early_stop, "fast_penalty": levers.fast_penalty}
    screen, full = replace(screen, **tuned), replace(full, **tuned)
    resumable = (
        selector.budget_prefix(screen) == selector.budget_prefix(full)
        and screen.deep_starts <= full.deep_starts
    )
    return screen, full, resumable


def class_row(screened: dict[str, Any], final: dict[str, Any]) -> dict[str, Any]:
    """A chunk's row for a class, from the screen's record and the final one."""
    row: dict[str, Any] = {
        "screen": screened["status"],
        "screen_attempts": screened["attempts"],
        "status": "placed" if final["status"] == "placed" else "flagged",
        "best_penetration": final["best_penetration"],
        "attempts": final["attempts"],
        "found_by": final["found_by"],
    }
    if row["status"] == "flagged":
        row.update(cells=final["cells"], pose=final["pose"], components=final["components"])
    return row


def search_class(
    geometry: selector.Geometry,
    mask: int,
    *,
    seed: int,
    screen: selector.Budget,
    full: selector.Budget,
    levers: Levers | None = None,
    cache: Cache | None = None,
) -> dict[str, Any]:
    """The screen, then the full budget for a class the screen cannot place.

    With the random-first lever, a few random starts on their own stream come first, and a
    class they place is placed; any other class gets the search below unchanged.
    """
    clock = time.perf_counter()
    levers = levers or Levers()
    quick = first_stage(geometry, mask, seed=seed, levers=levers)
    if quick is not None:
        return {**quick, "seconds": round(time.perf_counter() - clock, 3)}
    screen, full, resumable = tuned_budgets(screen, full, levers)
    kept = cache if levers.cache else None
    screened = selector.recheck_flag(
        geometry,
        mask,
        seed=seed,
        budget=screen,
        witness_cache=kept,
        checkpoint_at=screen.deep_starts if levers.resume and resumable else None,
    )
    final = screened
    if screened["status"] != "placed":
        final = selector.recheck_flag(
            geometry,
            mask,
            seed=seed,
            budget=full,
            witness_cache=kept,
            resume=screened.get("checkpoint"),
        )
    return {**class_row(screened, final), "seconds": round(time.perf_counter() - clock, 3)}


def resume_check(
    geometry: selector.Geometry,
    mask: int,
    *,
    seed: int,
    screen: selector.Budget,
    full: selector.Budget,
    levers: Levers,
    cache: Cache,
) -> dict[str, Any]:
    """The `resume` lever on one class: the full budget from scratch and resumed.

    The screen runs once. A class it or the random-first stage places never reaches the full
    budget, so the lever cannot change its row. For any other class the full budget runs
    from scratch and then from the screen's checkpoint, under `levers` otherwise, and the
    two records are compared field for field, all but `sub_pattern_attempts`, which the
    resumed search does not repeat. A verdict can survive a wrong trajectory when its best
    pose comes early, so each arm also keeps its state after the full budget's deep starts,
    and the two states must agree too (`deep_start_state`): generator, attempts and best
    pose. Each search is timed in wall and process seconds.
    """
    clocks: dict[str, dict[str, float]] = {}

    def timed(name: str, budget: selector.Budget, **options: Any) -> dict[str, Any]:
        wall, cpu = time.perf_counter(), time.process_time()
        record = selector.recheck_flag(
            geometry,
            mask,
            seed=seed,
            budget=budget,
            witness_cache=cache if levers.cache else None,
            **options,
        )
        clocks[name] = {
            "attempts": record["attempts"],
            "seconds": round(time.perf_counter() - wall, 3),
            "cpu_seconds": round(time.process_time() - cpu, 3),
        }
        return record

    line: dict[str, Any] = {"mask": mask, "arity": len(selector.cells_of(mask))}
    quick = first_stage(geometry, mask, seed=seed, levers=levers)
    if quick is not None:
        return {**line, "reached_full": False, "row": quick}
    screen, full, resumable = tuned_budgets(screen, full, levers)
    if not resumable:
        raise ValueError("the full budget does not pass through the screen's checkpoint")
    screened = timed("screen", screen, checkpoint_at=screen.deep_starts)
    checkpoint: selector.Checkpoint | None = screened.pop("checkpoint")
    if screened["status"] == "placed":
        return {**line, "reached_full": False, "row": class_row(screened, screened), **clocks}
    assert checkpoint is not None  # an unplaced screen always passes its last deep start
    scratch = timed("scratch", full, checkpoint_at=full.deep_starts)
    resumed = timed("resumed", full, checkpoint_at=full.deep_starts, resume=checkpoint)
    states = scratch.pop("checkpoint"), resumed.pop("checkpoint")
    differing = sorted(
        key
        for key in scratch.keys() | resumed.keys()
        if key != "sub_pattern_attempts" and scratch.get(key) != resumed.get(key)
    )
    if not same_state(*states):
        differing.append("deep_start_state")
    return {
        **line,
        "reached_full": True,
        "row": class_row(screened, scratch),
        "identical": not differing,
        "differing": differing,
        "skipped_attempts": checkpoint.attempts,
        **clocks,
    }


def same_state(first: selector.Checkpoint | None, second: selector.Checkpoint | None) -> bool:
    """Whether two searches stood in the same state at the same deep start, or both had
    placed the class by then."""
    if first is None or second is None:
        return first is second
    if first.best is None or second.best is None:
        same_best = first.best is second.best
    else:
        same_best = first.best[0] == second.best[0] and np.array_equal(
            first.best[1], second.best[1]
        )
    return (
        same_best
        and first.deep_starts_done == second.deep_starts_done
        and first.attempts == second.attempts
        and first.rng_state == second.rng_state
    )


def sweep_rows(directory: Path, masks: set[int]) -> dict[int, dict[str, Any]]:
    """The rows the sweep wrote for these classes, from the chunks under `directory`."""
    found: dict[int, dict[str, Any]] = {}
    for path in sorted(directory.glob("chunk-*.json")):
        for row in json.loads(path.read_text(encoding="utf-8"))["classes"]:
            if row["mask"] in masks:
                _ = found.setdefault(row["mask"], row)
    return found


def resume_bench(
    directory: Path,
    masks: Sequence[int],
    results: Path,
    *,
    levers: Levers,
    seed: int = 1,
    max_seconds: float = 540.0,
) -> dict[str, Any]:
    """`resume_check` on each class, a line each, resuming; then the tally of every line.

    Each line also says whether the from-scratch arm reproduces the row the sweep under
    `directory` wrote for the class, when there is one, so the comparison is anchored to the
    sweep's own verdicts and not only to a second run of the same code.
    """
    clock = time.perf_counter()
    done: set[int] = set()
    if results.exists():
        done = {
            json.loads(line)["mask"]
            for line in results.read_text(encoding="utf-8").splitlines()
        }
    old = sweep_rows(directory, set(masks))
    geometry = selector.cover_geometry()
    cache: Cache = {}
    with results.open("a", encoding="utf-8") as stream:
        for mask in masks:
            if mask in done:
                continue
            if time.perf_counter() - clock > max_seconds:
                break
            line = resume_check(
                geometry,
                mask,
                seed=seed,
                screen=SCREEN,
                full=FULL,
                levers=levers,
                cache=cache,
            )
            written = old.get(mask)
            line["reproduces_sweep"] = (
                None
                if written is None
                else all(written.get(key) == value for key, value in line["row"].items())
            )
            line["sweep_status"] = None if written is None else written["status"]
            _ = stream.write(json.dumps(line) + "\n")
            stream.flush()
    return resume_tally(results)


def resume_tally(results: Path) -> dict[str, Any]:
    """Identity and cost over every line: process seconds with the lever and without."""
    lines = [json.loads(t) for t in results.read_text(encoding="utf-8").splitlines()]
    full = [line for line in lines if line["reached_full"]]

    def cost(rows: list[dict[str, Any]], arm: str, unit: str) -> float:
        return round(sum(r["screen"][unit] + r[arm][unit] for r in rows), 1)

    by_status: dict[str, Any] = {}
    for status in ("flagged", "placed"):
        mine = [r for r in full if r["row"]["status"] == status]
        scratch, resumed = (
            cost(mine, "scratch", "cpu_seconds"),
            cost(mine, "resumed", "cpu_seconds"),
        )
        by_status[status] = {
            "classes": len(mine),
            "cpu_seconds_scratch": scratch,
            "cpu_seconds_resumed": resumed,
            "saved_share": round(1 - resumed / scratch, 4) if scratch else None,
            "seconds_scratch": cost(mine, "scratch", "seconds"),
            "seconds_resumed": cost(mine, "resumed", "seconds"),
            "attempts_scratch": sum(
                r["screen"]["attempts"] + r["scratch"]["attempts"] for r in mine
            ),
            "attempts_skipped": sum(r["skipped_attempts"] for r in mine),
        }
    return {
        "results": str(results),
        "classes": len(lines),
        "reached_full": len(full),
        "identical": sum(1 for r in full if r["identical"]),
        "differing": [r["mask"] for r in full if not r["identical"]],
        "reproduces_sweep": sum(1 for r in lines if r["reproduces_sweep"]),
        "does_not_reproduce_sweep": [
            r["mask"] for r in lines if r["reproduces_sweep"] is False
        ],
        "reached_full_by_status": by_status,
    }


def sweep(
    directory: Path,
    *,
    chunk: int,
    seed: int = 1,
    limit_chunks: int | None = None,
    geometry: selector.Geometry | None = None,
    screen: selector.Budget = SCREEN,
    full: selector.Budget = FULL,
    levers: Levers | None = None,
) -> list[int]:
    """Search the planned queue chunk by chunk, skipping chunks already written."""
    levers = levers or Levers()
    cache: dict[tuple[int, selector.Budget], selector.Verdict] = {}
    plan_path = directory / "plan.json"
    planned = json.loads(plan_path.read_text(encoding="utf-8"))
    geometry = geometry or selector.cover_geometry()
    queue = planned["queue"]
    written: list[int] = []
    chunks = (len(queue) + chunk - 1) // chunk
    for index in range(chunks):
        target = directory / f"chunk-{index:05d}.json"
        if target.exists():
            continue
        if limit_chunks is not None and len(written) >= limit_chunks:
            break
        clock = time.perf_counter()
        rows = []
        for mask, arity, missing, coverage, queue_index in queue[
            index * chunk : (index + 1) * chunk
        ]:
            found = search_class(
                geometry, mask, seed=seed, screen=screen, full=full, levers=levers, cache=cache
            )
            rows.append(
                {
                    "mask": mask,
                    "arity": arity,
                    "missing": missing,
                    "coverage": coverage,
                    "queue": queue_index,
                    **found,
                }
            )
        write_atomic(
            target,
            {
                "schema": CHUNK_SCHEMA,
                "status": STATUS,
                "chunk": index,
                "chunk_size": chunk,
                "seed": seed,
                "screen": budget_record(screen),
                "full": budget_record(full),
                **({} if levers == Levers() else {"levers": levers.record()}),
                "classes": rows,
                "provenance": PROVENANCE,
                "selector_provenance": selector.PROVENANCE,
                "seconds": round(time.perf_counter() - clock, 3),
            },
        )
        written.append(index)
        print(
            json.dumps(
                {
                    "chunk": index,
                    "of": chunks,
                    "flagged": sum(1 for r in rows if r["status"] == "flagged"),
                    "seconds": round(time.perf_counter() - clock, 1),
                }
            ),
            flush=True,
        )
    return written


def budget_record(budget: selector.Budget) -> dict[str, Any]:
    return {
        "starts": budget.starts,
        "hops": budget.hops,
        "deep_starts": budget.deep_starts,
        "deep_hops": budget.deep_hops,
        "margin": budget.margin,
        "finish": selector.FINISH if budget.finish else None,
    }


def greedy_cover(sets: dict[int, NDArray[np.int64]], orbits: int) -> list[dict[str, Any]]:
    """Flags in the order that removes the most residue orbits not yet removed."""
    left = np.ones(orbits, dtype=np.bool_)
    remaining = dict(sets)
    order: list[dict[str, Any]] = []
    while remaining:
        gains = {mask: int(np.count_nonzero(left[hit])) for mask, hit in remaining.items()}
        best = max(sorted(gains), key=lambda mask: gains[mask])
        if gains[best] == 0:
            break
        left[remaining.pop(best)] = False
        order.append({"mask": best, "removes": gains[best], "orbits_left": int(left.sum())})
    return order


def summary(directory: Path, flags_path: Path) -> dict[str, Any]:
    """Hit rates per queue and the greedy cover of the residue by the flags found so far."""
    planned = json.loads((directory / "plan.json").read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for path in sorted(directory.glob("chunk-*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        start = document["chunk"] * document["chunk_size"]
        queued = planned["queue"][start : start + document["chunk_size"]]
        if [row["mask"] for row in document["classes"]] != [row[0] for row in queued]:
            raise ValueError(f"{path} was written for another plan")
        rows.extend(document["classes"])
    queues = []
    for index, (name, _, _, _) in enumerate(QUEUES):
        mine = [r for r in rows if r["queue"] == index]
        flagged = [r for r in mine if r["status"] == "flagged"]
        queues.append(
            {
                "name": name,
                "planned": planned["queues"][index]["classes"],
                "searched": len(mine),
                "flagged": len(flagged),
                "hit_rate": len(flagged) / len(mine) if mine else None,
                "screen_unplaced": sum(1 for r in mine if r["screen"] != "placed"),
                "search_seconds": round(sum(r["seconds"] for r in mine), 1),
                "coverage_range": [
                    min(r["coverage"] for r in mine),
                    max(r["coverage"] for r in mine),
                ]
                if mine
                else None,
            }
        )
    geometry = selector.cover_geometry()
    endpoint = selector.mask_of(selector.endpoint_pose()["cells"])
    residue = make_residue(geometry, load_flags(flags_path, geometry), endpoint)
    flags = [r for r in rows if r["status"] == "flagged"]
    sets = {r["mask"]: hit_orbits(residue, geometry.group, r["mask"]) for r in flags}
    order = greedy_cover(sets, residue.orbits)
    removed = residue.orbits - (order[-1]["orbits_left"] if order else residue.orbits)
    named = {r["mask"]: r for r in flags}
    return {
        "schema": SUMMARY_SCHEMA,
        "status": STATUS,
        "plan": str(directory / "plan.json"),
        "residue_orbits": residue.orbits,
        "searched": len(rows),
        "planned": len(planned["queue"]),
        "flagged": len(flags),
        "queues": queues,
        "greedy_cover": [
            {
                **step,
                "cells": named[step["mask"]]["cells"],
                "best_penetration": named[step["mask"]]["best_penetration"],
            }
            for step in order
        ],
        "cover_removes": removed,
        "cover_share": removed / residue.orbits if residue.orbits else None,
        "falsifier": "the flags' greedy cover removes less than half of the residue",
        "falsified_so_far": removed < residue.orbits / 2,
        "provenance": PROVENANCE,
    }


def make_bench_set(directory: Path, flags_path: Path, *, chunks: int) -> dict[str, Any]:
    """A fixed test set with the old verdicts: the first chunks, every class the sweep has
    flagged so far, and every class of the re-check receipt."""
    classes: dict[int, dict[str, Any]] = {}
    for path in sorted(directory.glob("chunk-*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        for row in document["classes"]:
            if document["chunk"] < chunks or row["status"] == "flagged":
                classes.setdefault(
                    row["mask"],
                    {
                        "mask": row["mask"],
                        "arity": row["arity"],
                        "old": row["status"],
                        "old_seconds": row["seconds"],
                        "source": f"chunk {document['chunk']}",
                    },
                )
    geometry = selector.cover_geometry()
    rechecked = json.loads(flags_path.read_text(encoding="utf-8"))["rechecked"]
    for row in rechecked:
        mask = selector.canonical(selector.mask_of(row["indices"]), geometry.group)
        classes.setdefault(
            mask,
            {
                "mask": mask,
                "arity": row["arity"],
                "old": "flagged" if row["status"] == "still-flagged" else "placed",
                "old_seconds": None,
                "source": "re-check",
            },
        )
    return {
        "chunks": chunks,
        "flags_source": {"path": str(flags_path), "sha256": digest_of(flags_path)},
        "classes": list(classes.values()),
    }


def bench(
    set_path: Path,
    results: Path,
    *,
    levers: Levers,
    seed: int = 1,
    max_seconds: float = 540.0,
) -> int:
    """Search the test set under the levers, appending a line per class; resumes."""
    clock = time.perf_counter()
    test_set = json.loads(set_path.read_text(encoding="utf-8"))["classes"]
    done: set[int] = set()
    if results.exists():
        done = {
            json.loads(line)["mask"]
            for line in results.read_text(encoding="utf-8").splitlines()
        }
    geometry = selector.cover_geometry()
    cache: dict[tuple[int, selector.Budget], selector.Verdict] = {}
    written = 0
    with results.open("a", encoding="utf-8") as stream:
        for entry in test_set:
            if entry["mask"] in done:
                continue
            if time.perf_counter() - clock > max_seconds:
                break
            cpu = time.process_time()
            found = search_class(
                geometry,
                entry["mask"],
                seed=seed,
                screen=SCREEN,
                full=FULL,
                levers=levers,
                cache=cache,
            )
            line = {
                "mask": entry["mask"],
                "status": found["status"],
                "found_by": found["found_by"],
            }
            line.update(
                seconds=found["seconds"],
                cpu_seconds=round(time.process_time() - cpu, 3),
                penetration=found["best_penetration"],
            )
            _ = stream.write(json.dumps(line) + "\n")
            stream.flush()
            written += 1
    return written


def compare(set_path: Path, results: Path) -> dict[str, Any]:
    """The new verdicts against the old: every disagreement, class by class."""
    test_set = {
        e["mask"]: e for e in json.loads(set_path.read_text(encoding="utf-8"))["classes"]
    }
    new = {
        line["mask"]: line
        for line in (json.loads(t) for t in results.read_text(encoding="utf-8").splitlines())
    }
    wrongly_flagged = [
        m
        for m, row in new.items()
        if row["status"] == "flagged" and test_set[m]["old"] == "placed"
    ]
    newly_placed = [
        m
        for m, row in new.items()
        if row["status"] == "placed" and test_set[m]["old"] == "flagged"
    ]
    return {
        "set": str(set_path),
        "results": str(results),
        "searched": len(new),
        "of": len(test_set),
        "old_placed_new_flagged": [{**test_set[m], **new[m]} for m in sorted(wrongly_flagged)],
        "old_flagged_new_placed": [{**test_set[m], **new[m]} for m in sorted(newly_placed)],
        "agree": len(new) - len(wrongly_flagged) - len(newly_placed),
        "seconds_by_old_verdict": {
            verdict: round(
                sum(r["seconds"] for m, r in new.items() if test_set[m]["old"] == verdict), 1
            )
            for verdict in ("placed", "flagged")
        },
        "count_by_old_verdict": {
            verdict: sum(1 for m in new if test_set[m]["old"] == verdict)
            for verdict in ("placed", "flagged")
        },
    }


def measure(arguments: argparse.Namespace) -> int:
    """The lever-measurement commands: `bench-set`, `bench`, `compare`, `resume-check`."""
    record: dict[str, Any]
    if arguments.command == "bench-set":
        record = make_bench_set(
            arguments.directory, arguments.flags, chunks=arguments.bench_chunks
        )
        write_atomic(arguments.set, record)
        old = [c["old"] for c in record["classes"]]
        print(json.dumps({"classes": len(old), "flagged": old.count("flagged")}))
        return 0
    if arguments.command == "bench":
        written = bench(
            arguments.set,
            arguments.results,
            levers=LEVERS[arguments.levers],
            seed=arguments.seed,
            max_seconds=arguments.max_seconds,
        )
        print(json.dumps({"levers": arguments.levers, "classes": written}))
        return 0
    if arguments.command == "compare":
        record = compare(arguments.set, arguments.results)
    else:
        record = resume_bench(
            arguments.directory,
            arguments.masks,
            arguments.results,
            levers=LEVERS[arguments.levers],
            seed=arguments.seed,
            max_seconds=arguments.max_seconds,
        )
    if arguments.output is not None:
        write_atomic(arguments.output, record)
    print(json.dumps(record, indent=1, sort_keys=True))
    return 1 if record.get("differing") else 0


MEASURE = ("bench-set", "bench", "compare", "resume-check")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "command",
        choices=("plan", "sweep", "summary", *MEASURE),
    )
    _ = parser.add_argument("--flags", type=Path, required=True, help="the re-check receipt")
    _ = parser.add_argument("--directory", type=Path, required=True, help="plan and chunks")
    _ = parser.add_argument("--levers", choices=sorted(LEVERS), default="baseline")
    _ = parser.add_argument("--set", type=Path, help="bench: the fixed test set")
    _ = parser.add_argument(
        "--results", type=Path, help="bench, resume-check: one line per class"
    )
    _ = parser.add_argument(
        "--masks", type=int, nargs="*", default=[], help="resume-check: the classes"
    )
    _ = parser.add_argument("--bench-chunks", type=int, default=3)
    _ = parser.add_argument("--max-seconds", type=float, default=540.0)
    _ = parser.add_argument("--chunk", type=int, default=500)
    _ = parser.add_argument("--seed", type=int, default=1)
    _ = parser.add_argument("--limit-chunks", type=int, default=None)
    _ = parser.add_argument("--output", type=Path, help="the summary's receipt")
    arguments = parser.parse_args(argv)
    if arguments.command in MEASURE:
        return measure(arguments)
    planned = plan(arguments.flags, arguments.directory)
    if arguments.command == "plan":
        print(json.dumps({k: planned[k] for k in ("residue", "universe", "queues", "seconds")}))
        return 0
    if arguments.command == "sweep":
        _ = sweep(
            arguments.directory,
            chunk=arguments.chunk,
            seed=arguments.seed,
            limit_chunks=arguments.limit_chunks,
            levers=LEVERS[arguments.levers],
        )
        return 0
    record = summary(arguments.directory, arguments.flags)
    text = json.dumps(record, indent=1, sort_keys=True)
    if arguments.output is not None:
        write_atomic(arguments.output, record)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
