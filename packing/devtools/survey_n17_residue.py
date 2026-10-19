"""Survey of the n17 residue: how hard is each orbit the selector's flags leave (H-267).

Not a certificate. Every number here comes from the float search of the sub-pattern
selector (`select_n17_sub_patterns`), whose search, consumer and geometry this tool
imports rather than copies.

What it surveys. On the cover `ring-3-voronoi-8-tabbed-unique` at cap U = 1169/250, an
occupancy state is a 17-subset of the 24 cells. The selector flags forbidden
sub-patterns; the states with no flagged pattern in any D4 image survive. With the
arity-8 receipt's 90 flags, 2,256 D4 orbits survive; with the arity-7 receipt's 44,
5,084. The tool enumerates them as canonical representatives (the least mask of the
orbit), checks those counts against the selector's own Burnside count, and draws a
seeded stratified sample.

Strata. Each orbit is placed by how many corner, side and interior cells it uses (bands
of corners and of interior cells; sides are the rest) and by its Hamming distance to the
nearest D4 image of the endpoint's state (2, 4, 6, 8 or more; distance 2 is one cell
moved). Allocation is one per non-empty stratum, then the rest by the Sainte-Laguë rule
on stratum size, weighted toward the endpoint (`NEIGHBOURHOOD_WEIGHT`); within a stratum
the draw is uniform without replacement, and the extrapolation weights each stratum by
its size, so the oversampling biases nothing. The endpoint's own orbit is a certainty
stratum of one, the positive control. States run control first, then in a seeded random
order, so a wall ceiling leaves a random subsample.

The frame (`--distance`, `--sample`). By default the sample is drawn from every surviving
orbit. `--distance D` restricts the frame to the orbits at Hamming distance exactly D
from the endpoint's orbit; the endpoint's own orbit stays as the control, and the strata,
the allocation and every extrapolation are then over that frame alone, while a found
class is still measured against all survivors. `--sample 0` takes every orbit in the
frame, so the survey is a census of it and each estimate is exact. `--flag-set arity8
--distance 2 --sample 0` is every one-cell move from the endpoint that the arity-8 flags
leave. `--shard K/N` keeps the K-th of N interleaved parts of the draw in mask order, so N
runs survey a frame once between them, each under its own wall ceiling; a shard's
estimates cover its part only, and the parts are combined afterwards.

The measurements, per sampled state:

- Full-state placement at U. The selector's `search` runs on all 17 cells under a stated
  budget, for a stated number of rounds on independent streams. Each round that ends
  unplaced is finished by one long L-BFGS-B descent of the selector's own penalty from
  its best pose (`FINISH`), and a placement is finished once more. The finish is what
  makes the control pass: the selector's descent stops at 600 iterations, and on the
  endpoint's own state its best attempt at the default budget sits at 1.7e-3 to 2.1e-3 in
  the right arrangement, which one long descent takes to a penalty of exactly zero
  (measured). The best penetration over every attempt and finish is reported, with the
  per-round trace. The endpoint's orbit must place; any other state that does is a
  packing of side at most U in that state, reported with its pose under `placed_states`.
- The smallest failing sub-pattern, on a seeded share of the sample. From an unplaced
  state, cells are removed one at a time while the rest still fails at U: a deletion
  filter, so the result is irreducible (every one-cell removal was placed). The cell tried
  first is the one whose removal leaves the current best pose most violated, so the
  conflict's core is kept. A removal is decided without search where that is exact or is
  the selector's own verdict: the current pose restricted to the rest is within the
  margin; or every interaction component of the rest is a class the selector's receipts
  placed; or the rest holds a flagged class. Otherwise each component is screened under
  a modest budget, warm started from the current pose and, as the selector does, from
  each witness of the rest less one necessary cell with that cell redrawn; a failed
  screen escalates to the full-state budget before the removal counts. The pilot without
  escalation reached ten-cell patterns that a second search then placed. The minimal
  pattern is searched once more on fresh streams (`confirm`), and classed as an existing
  flag, a class the selector placed, or a new class the selector never tested.
- Wall time per state, and per stage.

Calibration (`--calibrate`). Blind runs on the endpoint's state at the full-state budget,
over seeds and rounds, give its placement rate by round under fresh and carried rounds;
seeded runs start from its exact pose and from perturbed copies, reported apart; and a
seeded draw of distance-2 states is searched at the same budget.

The receipt records the module's provenance at import (`devtools.provenance`), the
parameters, the population and
strata, each state's results, the distributions (penetration bands, by Hamming distance,
minimal arity, the share of new classes), each distinct minimal class with the survivors
it would remove if certified, and a stratified extrapolation to all surviving orbits:
per stratum the sample mean, weighted by stratum size, with the variance of a stratified
mean under a finite-population correction (a singleton stratum borrows the pooled sample
variance).
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import math
import time
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from devtools import select_n17_sub_patterns as selector
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-residue-survey/v1"
STATUS = (
    "heuristic survey, not a certificate: placements are float witnesses within the "
    "margin, failures are searches that found none, and minimal sub-patterns are "
    "candidates the prover would have to certify"
)
PROVENANCE = provenance(Path(__file__))
REPO = Path(__file__).resolve().parents[2]
RECEIPTS = "packing/campaign/explorations/X048-session-168-pilots/receipts"
ARITY7 = f"{RECEIPTS}/selector-arity7-seed1.json"
ARITY8 = f"{RECEIPTS}/selector-arity8-seed1-restricted.json"
FLAG_SETS = {"arity7": (ARITY7,), "arity8": (ARITY8,)}
EXPECTED_ORBITS = {"arity7": 5084, "arity8": 2256}
KNOWLEDGE_RECEIPTS = (ARITY7, ARITY8)
MARGIN = selector.MARGIN
# One long descent of the selector's penalty, which now lives in the selector. Measured on
# the endpoint's state: from the selector's best attempt at 1.7e-3, 1,605 iterations reach
# a penalty of exactly zero.
FINISH = selector.FINISH
BANDS = (
    ("<1e-6", 0.0, 1e-6),
    ("1e-6..1e-4", 1e-6, 1e-4),
    ("1e-4..1e-3", 1e-4, 1e-3),
    ("1e-3..1e-2", 1e-3, 1e-2),
    (">1e-2", 1e-2, math.inf),
)
KINDS = ("corner", "side", "interior")
NEIGHBOURHOOD_WEIGHT = {"d2": 4.0, "d4": 2.0}
ENDPOINT_STRATUM = "endpoint"
Z95 = 1.959963984540054

Floats = NDArray[np.float64]


# ---------------------------------------------------------------------------
# Population: surviving orbits, their features and strata
# ---------------------------------------------------------------------------


def surviving_orbits(
    cells: int, group: tuple[tuple[int, ...], ...], flags: list[int], size: int
) -> tuple[NDArray[np.int64], list[int]]:
    """The surviving states and the canonical representative of each surviving orbit.

    The representatives are the distinct least images, and their number must equal the
    selector's own Burnside count, which `count_orbits` checks against the same forms.
    """
    states = selector.all_states(cells, size)
    forbidden = sorted({image for mask in flags for image in selector.orbit(mask, group)})
    alive = selector.survivors(states, forbidden)
    if not alive.size:
        return alive, []
    images = np.stack([selector.apply_permutation(alive, permutation) for permutation in group])
    representatives = [int(mask) for mask in np.unique(images.min(axis=0))]
    orbits = selector.count_orbits(alive, group)["orbits"]
    if orbits != len(representatives):
        raise ValueError(f"{len(representatives)} representatives for {orbits} orbits")
    return alive, representatives


def kind_of(name: str) -> str:
    prefix = name.split("-", maxsplit=1)[0]
    return prefix if prefix in KINDS else "other"


def composition(names: tuple[str, ...], mask: int) -> dict[str, int]:
    counts = Counter(kind_of(names[cell]) for cell in selector.cells_of(mask))
    return {kind: counts.get(kind, 0) for kind in (*KINDS, "other")}


def contact(mask: int, endpoint_images: list[int]) -> int:
    """The most cells the state shares with any D4 image of the endpoint's state."""
    return max(((mask & image).bit_count() for image in endpoint_images), default=0)


def distance(mask: int, endpoint_images: list[int]) -> int:
    """The Hamming distance to the nearest D4 image of the endpoint's state."""
    return min(((mask ^ image).bit_count() for image in endpoint_images), default=-1)


def distance_band(apart: int) -> str:
    return f"d{apart}" if apart <= 6 else "d>=8"


def stratum_of(counts: dict[str, int], apart: int) -> str:
    corners, interior = counts["corner"], counts["interior"]
    c = "c<=2" if corners <= 2 else f"c{corners}"
    i = "i<=3" if interior <= 3 else ("i4" if interior == 4 else "i>=5")
    return f"{c}/{i}/{distance_band(apart)}"


def weight_of(key: str) -> float:
    """Oversampling toward the endpoint: its distance-2 and distance-4 neighbours."""
    return NEIGHBOURHOOD_WEIGHT.get(key.rsplit("/", maxsplit=1)[-1], 1.0)


def allocate(
    sizes: dict[str, int], n: int, weights: dict[str, float] | None = None
) -> dict[str, int]:
    """One per non-empty stratum when `n` allows, the rest by Sainte-Laguë on weighted size."""
    keys = sorted(key for key, size in sizes.items() if size > 0)
    if n >= sum(sizes[key] for key in keys):
        return {key: sizes[key] for key in keys}
    weight = {key: (weights or {}).get(key, 1.0) for key in keys}
    taken = dict.fromkeys(keys, 1 if n >= len(keys) else 0)
    while sum(taken.values()) < n:
        open_keys = [key for key in keys if taken[key] < sizes[key]]
        best = max(
            open_keys, key=lambda key: (weight[key] * sizes[key] / (2 * taken[key] + 1), key)
        )
        taken[best] += 1
    return taken


def draw_sample(
    strata: dict[str, list[int]], n: int, seed: int, *, weighted: bool = False
) -> tuple[dict[str, int], list[tuple[str, int]]]:
    """A seeded stratified draw: the allocation and the drawn `(stratum, mask)` pairs."""
    sizes = {key: len(masks) for key, masks in strata.items()}
    weights = {key: weight_of(key) for key in sizes} if weighted else None
    allocation = allocate(sizes, n, weights)
    rng = np.random.default_rng(np.random.SeedSequence([seed, 0x5A4D]))
    drawn: list[tuple[str, int]] = []
    for key in sorted(allocation):
        masks = sorted(strata[key])
        picks = sorted(int(i) for i in rng.choice(len(masks), allocation[key], replace=False))
        drawn.extend((key, masks[i]) for i in picks)
    return allocation, drawn


# ---------------------------------------------------------------------------
# What the selector's receipts settle without searching
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Rule:
    """One complete selector sweep: which classes it tested, and the flags it raised."""

    max_arity: int
    restrict_from: int | None
    max_missing: int | None
    flags: tuple[int, ...]


@dataclass
class Knowledge:
    """Selector verdicts by class: flagged, holding a flag, placed, or never tested."""

    geometry: selector.Geometry
    size: int
    rules: tuple[Rule, ...]
    penetration: dict[int, float]
    _alive: dict[tuple[int, int], NDArray[np.int64]] = field(default_factory=dict)

    @functools.cached_property
    def flags(self) -> set[int]:
        return {mask for rule in self.rules for mask in rule.flags}

    @functools.cached_property
    def flag_images(self) -> list[int]:
        group = self.geometry.group
        return sorted({image for mask in self.flags for image in selector.orbit(mask, group)})

    def survivors_below(self, rule_index: int, arity: int) -> NDArray[np.int64]:
        key = (rule_index, arity)
        if key not in self._alive:
            rule, group = self.rules[rule_index], self.geometry.group
            lower = [mask for mask in rule.flags if mask.bit_count() < arity]
            images = sorted({image for mask in lower for image in selector.orbit(mask, group)})
            states = selector.all_states(len(self.geometry.names), self.size)
            self._alive[key] = selector.survivors(states, images)
        return self._alive[key]

    def status(self, mask: int) -> str:
        """`flagged`, `holds-flag`, `placed` or `unknown` for a connected class."""
        group = self.geometry.group
        canonical = selector.canonical(mask, group)
        if canonical in self.flags:
            return "flagged"
        if any(image & mask == image for image in self.flag_images):
            return "holds-flag"
        cells = selector.cells_of(mask)
        if not selector.connected(self.geometry, cells):
            return "unknown"
        arity = len(cells)
        for index, rule in enumerate(self.rules):
            if arity > rule.max_arity:
                continue
            if rule.restrict_from is None or arity < rule.restrict_from:
                return "placed"
            if (
                rule.max_missing is not None
                and selector.missing_pairs(self.geometry, mask) > rule.max_missing
            ):
                continue
            alive = self.survivors_below(index, arity)
            if bool(np.any((alive & canonical) == canonical)):
                return "placed"
        return "unknown"

    def untested_reason(self, mask: int) -> str:
        """Why no selector sweep tested the class, for a class whose status is unknown."""
        arity = mask.bit_count()
        if all(arity > rule.max_arity for rule in self.rules):
            return f"arity {arity} above every sweep"
        missing = selector.missing_pairs(self.geometry, mask)
        return f"arity {arity} with {missing} missing pairs, deferred by the priority subset"


def load_knowledge(
    geometry: selector.Geometry, design: str, paths: tuple[str, ...], root: Path, size: int
) -> Knowledge:
    rules: list[Rule] = []
    penetration: dict[int, float] = {}
    for declared in paths:
        path = root / declared
        receipt = json.loads(path.read_text(encoding="utf-8"))
        parameters = receipt["parameters"]
        if parameters.get("window") is not None or not receipt["sweep"]["complete"]:
            raise ValueError(f"{declared}: a windowed or incomplete sweep settles nothing")
        flags = selector.receipt_flags(path, geometry, design)
        for flag in receipt["flagged"]:
            mask = selector.canonical(selector.mask_of(flag["indices"]), geometry.group)
            penetration[mask] = float(flag["best_penetration"])
        rules.append(
            Rule(
                max_arity=int(parameters["max_arity"]),
                restrict_from=parameters.get("restrict_to_survivors_from"),
                max_missing=parameters.get("max_missing_pairs"),
                flags=tuple(flags),
            )
        )
    return Knowledge(geometry, size, tuple(rules), penetration)


# ---------------------------------------------------------------------------
# Placement: the selector's search, rounds, and the long finish
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Effort:
    """A stated search effort: the selector's budget, rounds of it, and the finish."""

    budget: selector.Budget
    rounds: int
    finish: bool = True
    carry: bool = False

    def record(self) -> dict[str, Any]:
        b = self.budget
        return {
            "starts": b.starts,
            "hops": b.hops,
            "deep_starts": b.deep_starts,
            "deep_hops": b.deep_hops,
            "hop_centre": b.hop_centre,
            "hop_angle": b.hop_angle,
            "wide_centre": b.wide_centre,
            "wide_angle": b.wide_angle,
            "margin": b.margin,
            "rounds": self.rounds,
            "finish": FINISH if self.finish else None,
            "carry_best_into_next_round": self.carry,
        }


@dataclass
class Placement:
    """The outcome for one pattern; on failure, `cells` is the failing component."""

    cells: tuple[int, ...]
    feasible: bool
    violation: float
    pose: Floats
    attempts: int = 0
    searches: int = 0
    found_by: str = "none"
    decided_by: str = "search"
    components: dict[str, float] = field(default_factory=dict[str, float])
    trace: list[dict[str, Any]] = field(default_factory=list[dict[str, Any]])


def signed_margins(problem: selector.Problem, pose: Floats) -> dict[str, float]:
    """Float clearances of a witness, positive when strict: separating axis, walls, cells.

    For each interacting pair, the best of the four edge normals' gaps; the least over the
    pairs is the separating-axis margin, zero for touching squares and negative for any
    overlap. The selector's `violations` reports the same quantities clipped at zero.
    """
    x, y, angle = pose[:, 0], pose[:, 1], pose[:, 2]
    support = (np.abs(np.cos(angle)) + np.abs(np.sin(angle))) / 2
    walls = np.min(
        [x - support, problem.cap - support - x, y - support, problem.cap - support - y]
    )
    cell = np.min(problem.plane_c - problem.plane_a * x[:, None] - problem.plane_b * y[:, None])
    pair = math.inf
    for first, second in zip(problem.first, problem.second, strict=True):
        offset = pose[second, :2] - pose[first, :2]
        best = -math.inf
        for axis in (
            angle[first],
            angle[first] + np.pi / 2,
            angle[second],
            angle[second] + np.pi / 2,
        ):
            reach = abs(math.cos(axis) * offset[0] + math.sin(axis) * offset[1])
            half = sum(
                (abs(math.cos(angle[row] - axis)) + abs(math.sin(angle[row] - axis))) / 2
                for row in (first, second)
            )
            best = max(best, reach - half)
        pair = min(pair, best)
    return {"pair": float(pair), "container": float(walls), "cell": float(cell)}


def stream(seed: int, mask: int, role: int, round_index: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([seed, mask, role, round_index]))


def search_component(
    geometry: selector.Geometry,
    cells: tuple[int, ...],
    *,
    seed: int,
    role: int,
    effort: Effort,
    warm: list[Floats] | None,
) -> Placement:
    """Rounds of the selector's search on one connected pattern, each finished if unplaced.

    Every round starts from the given warm poses on its own stream; with `carry`, a later
    round also starts from the best pose so far, so its hops continue around it. A
    placement is finished once more, which takes a pose within the margin to a penalty of
    zero where it can. The trace
    holds the best violation after each round, with cumulative attempts and wall.
    """
    clock = time.perf_counter()
    problem = selector.Problem(geometry, cells)
    mask = selector.mask_of(cells)
    best: Placement | None = None
    attempts = 0
    trace: list[dict[str, Any]] = []
    templates = [(0, pose) for pose in warm or []]
    for round_index in range(effort.rounds):
        rng = stream(seed, mask, role, round_index)
        carried = best is not None and effort.carry
        starts = [*templates, (0, best.pose)] if best is not None and carried else templates
        verdict = selector.search(geometry, cells, rng, effort.budget, starts or None)
        attempts += verdict.attempts
        value, pose, how = verdict.violation, verdict.pose, verdict.found_by
        if not verdict.feasible and effort.finish:
            finished = selector.finish(problem, pose)
            finished_value = problem.violation(finished)
            if finished_value < value:
                value, pose, how = finished_value, finished, "finish"
        if best is None or value < best.violation:
            best = Placement(
                cells,
                feasible=value <= effort.budget.margin,
                violation=value,
                pose=pose,
                found_by=f"{how}-round-{round_index}",
            )
        trace.append(
            {
                "round": round_index,
                "best": best.violation,
                "attempts": attempts,
                "seconds": round(time.perf_counter() - clock, 3),
            }
        )
        if best.feasible:
            break
    assert best is not None
    if best.feasible and effort.finish and best.violation > 0.0:
        finished = selector.finish(problem, best.pose)
        if problem.violation(finished) < best.violation:
            best.pose, best.violation = finished, problem.violation(finished)
    best.attempts, best.searches, best.trace = attempts, 1, trace
    best.components = problem.violations(best.pose)
    return best


def components_of(geometry: selector.Geometry, cells: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Interaction components, smallest first: squares in different ones never meet."""
    left, parts = set(cells), []
    while left:
        start = min(left)
        seen, stack = {start}, [start]
        while stack:
            current = stack.pop()
            for other in left - seen:
                if geometry.interact[current, other]:
                    seen.add(other)
                    stack.append(other)
        parts.append(tuple(sorted(seen)))
        left -= seen
    return sorted(parts, key=lambda part: (len(part), part))


@dataclass(frozen=True)
class Efforts:
    """The screening search of a removal, and the search a failed screen escalates to."""

    screen: Effort
    escalate: Effort | None


def place(
    geometry: selector.Geometry,
    knowledge: Knowledge | None,
    cells: tuple[int, ...],
    *,
    seed: int,
    efforts: Efforts,
    warm: Floats,
    templates: list[Floats] | None = None,
) -> Placement:
    """Place a pattern component by component; a failing component is returned as such.

    A component the screen cannot place is searched again under the escalation effort,
    from the screen's best pose as well, before it counts as failing.
    """
    margin = efforts.screen.budget.margin
    restricted = selector.Problem(geometry, cells).violation(warm)
    if restricted <= margin:
        return Placement(
            cells, feasible=True, violation=restricted, pose=warm, decided_by="restriction"
        )
    attempts = searches = 0
    worst = 0.0
    pose = warm.copy()
    escalated = False
    for part in components_of(geometry, cells):
        rows = [cells.index(cell) for cell in part]
        verdict = None if knowledge is None else knowledge.status(selector.mask_of(part))
        if verdict == "placed" or len(part) == 1:
            continue
        if verdict in {"flagged", "holds-flag"}:
            assert knowledge is not None
            canonical = selector.canonical(selector.mask_of(part), geometry.group)
            return Placement(
                part,
                feasible=False,
                violation=knowledge.penetration.get(canonical, math.nan),
                pose=warm[rows],
                attempts=attempts,
                searches=searches,
                decided_by=verdict,
            )
        starts = [warm[rows], *(template[rows] for template in templates or [])]
        outcome = search_component(
            geometry, part, seed=seed, role=ROLE_REDUCE, effort=efforts.screen, warm=starts
        )
        attempts += outcome.attempts
        searches += 1
        if not outcome.feasible and efforts.escalate is not None:
            escalated = True
            again = search_component(
                geometry,
                part,
                seed=seed,
                role=ROLE_ESCALATE,
                effort=efforts.escalate,
                warm=[*starts, outcome.pose],
            )
            attempts += again.attempts
            searches += 1
            if again.violation < outcome.violation:
                outcome = again
        if not outcome.feasible:
            outcome.attempts, outcome.searches = attempts, searches
            outcome.decided_by = "escalated-search" if escalated else "search"
            return outcome
        pose[rows] = outcome.pose
        worst = max(worst, outcome.violation)
    decided = ("escalated-search" if escalated else "search") if searches else "selector-placed"
    return Placement(
        cells,
        feasible=True,
        violation=worst,
        pose=pose,
        attempts=attempts,
        searches=searches,
        decided_by=decided,
    )


# ---------------------------------------------------------------------------
# One state: full placement, then the deletion filter
# ---------------------------------------------------------------------------

ROLE_FULL, ROLE_REDUCE, ROLE_CONFIRM, ROLE_ESCALATE, ROLE_TEMPLATE = 1, 2, 3, 4, 5
MAX_TEMPLATES = 6


def deletion_order(
    geometry: selector.Geometry, cells: tuple[int, ...], pose: Floats, candidates: list[int]
) -> list[int]:
    """Candidates whose removal leaves the pose most violated first: the least involved."""
    keys: list[tuple[float, float, int]] = []
    for cell in candidates:
        rows = [row for row, other in enumerate(cells) if other != cell]
        rest = tuple(cells[row] for row in rows)
        problem = selector.Problem(geometry, rest)
        value = problem.violation(pose[rows])
        penalty = problem.penalty(problem.pack(pose[rows]))[0]
        keys.append((-value, -penalty, cell))
    return [cell for _, _, cell in sorted(keys)]


def witness_templates(
    geometry: selector.Geometry,
    rest: tuple[int, ...],
    witnesses: dict[int, tuple[tuple[int, ...], Floats]],
    seed: int,
) -> list[Floats]:
    """The selector's warm start, here: a placement of `rest` less one cell, that cell redrawn.

    A witness for a necessary cell `d` places a superset of `rest` without `d`.
    """
    templates: list[Floats] = []
    problem = selector.Problem(geometry, rest)
    for missing in sorted(witnesses, reverse=True)[:MAX_TEMPLATES]:
        if missing not in rest:
            continue
        placed, pose = witnesses[missing]
        rng = stream(seed, selector.mask_of(rest), ROLE_TEMPLATE, missing)
        start = np.empty((len(rest), 3))
        for row, cell in enumerate(rest):
            if cell == missing:
                start[row, :2] = problem.random_centre(row, rng)
                start[row, 2] = rng.uniform(0.0, np.pi / 2)
            else:
                start[row] = pose[placed.index(cell)]
        templates.append(start)
    return templates


def reduce_state(
    geometry: selector.Geometry,
    knowledge: Knowledge | None,
    start: Placement,
    *,
    seed: int,
    efforts: Efforts,
    max_steps: int,
) -> dict[str, Any]:
    """Deletion filter from a failing pattern to a minimal failing one."""
    current, pose, value = start.cells, start.pose, start.violation
    necessary: set[int] = set()
    witnesses: dict[int, tuple[tuple[int, ...], Floats]] = {}
    steps: list[dict[str, Any]] = []
    decided: Counter[str] = Counter()
    while len(steps) < max_steps:
        candidates = [cell for cell in current if cell not in necessary]
        if not candidates:
            break
        cell = deletion_order(geometry, current, pose, candidates)[0]
        rows = [row for row, other in enumerate(current) if other != cell]
        rest = tuple(current[row] for row in rows)
        clock = time.perf_counter()
        outcome = place(
            geometry,
            knowledge,
            rest,
            seed=seed,
            efforts=efforts,
            warm=pose[rows],
            templates=witness_templates(geometry, rest, witnesses, seed),
        )
        decided[outcome.decided_by] += 1
        steps.append(
            {
                "remove": geometry.names[cell],
                "from_arity": len(current),
                "rest_placed": outcome.feasible,
                "violation": outcome.violation,
                "decided_by": outcome.decided_by,
                "attempts": outcome.attempts,
                "seconds": round(time.perf_counter() - clock, 3),
            }
        )
        if outcome.feasible:
            necessary.add(cell)
            witnesses[cell] = (rest, outcome.pose)
            continue
        current, pose, value = outcome.cells, outcome.pose, outcome.violation
        necessary &= set(current)
        witnesses = {d: w for d, w in witnesses.items() if d in necessary}
    return {
        "cells": current,
        "pose": pose,
        "violation": value,
        "minimal": not [cell for cell in current if cell not in necessary],
        "steps": steps,
        "decided_by": dict(sorted(decided.items())),
    }


@dataclass(frozen=True)
class Plan:
    """Everything a worker needs: the cover, the selector's verdicts and the efforts."""

    geometry: selector.Geometry
    knowledge: Knowledge | None
    seed: int
    full: Effort
    reduce: Efforts
    confirm: Effort | None
    max_steps: int


def pose_rows(geometry: selector.Geometry, cells: tuple[int, ...], pose: Floats) -> list[Any]:
    return [
        [geometry.names[cell], float(row[0]), float(row[1]), float(row[2])]
        for cell, row in zip(cells, pose, strict=True)
    ]


def classify(plan: Plan, mask: int) -> dict[str, Any]:
    knowledge, group = plan.knowledge, plan.geometry.group
    canonical = selector.canonical(mask, group)
    if knowledge is None:
        return {"class": "untested", "canonical_mask": canonical}
    status = knowledge.status(mask)
    label = {"flagged": "existing-flag", "placed": "selector-placed"}.get(status, "new")
    record: dict[str, Any] = {"class": label, "selector_status": status}
    if label == "new":
        record["why_untested"] = knowledge.untested_reason(mask)
    return {**record, "canonical_mask": canonical}


def survey_state(plan: Plan, mask: int, *, reduce: bool = True) -> dict[str, Any]:
    """Full placement at U, the minimal failing sub-pattern, and the wall of each."""
    clock = time.perf_counter()
    geometry = plan.geometry
    cells = selector.cells_of(mask)
    full = search_component(
        geometry, cells, seed=plan.seed, role=ROLE_FULL, effort=plan.full, warm=None
    )
    full_seconds = time.perf_counter() - clock
    record: dict[str, Any] = {
        "mask": mask,
        "cells": [geometry.names[cell] for cell in cells],
        "full": {
            "placed": full.feasible,
            "best_penetration": full.violation,
            "components": full.components,
            "attempts": full.attempts,
            "found_by": full.found_by,
            "signed_margins": signed_margins(selector.Problem(geometry, cells), full.pose)
            if full.feasible
            else None,
            "trace": full.trace,
            "pose": pose_rows(geometry, cells, full.pose),
            "seconds": round(full_seconds, 3),
        },
        "minimal": None,
        "reduce_selected": reduce,
    }
    if not full.feasible and reduce:
        reduce_clock = time.perf_counter()
        reduced = reduce_state(
            geometry,
            plan.knowledge,
            full,
            seed=plan.seed,
            efforts=plan.reduce,
            max_steps=plan.max_steps,
        )
        sub = reduced["cells"]
        sub_mask = selector.mask_of(sub)
        minimal: dict[str, Any] = {
            "cells": [geometry.names[cell] for cell in sub],
            "indices": list(sub),
            "arity": len(sub),
            "best_penetration": reduced["violation"],
            "irreducible": reduced["minimal"],
            "connected": selector.connected(geometry, sub),
            "missing_pairs": selector.missing_pairs(geometry, sub_mask),
            **classify(plan, sub_mask),
            "steps": reduced["steps"],
            "decided_by": reduced["decided_by"],
            "pose": pose_rows(geometry, sub, reduced["pose"]),
            "seconds": round(time.perf_counter() - reduce_clock, 3),
        }
        if plan.confirm is not None and minimal["class"] != "existing-flag":
            confirm_clock = time.perf_counter()
            again = search_component(
                geometry,
                sub,
                seed=plan.seed,
                role=ROLE_CONFIRM,
                effort=plan.confirm,
                warm=[reduced["pose"]],
            )
            minimal["confirm"] = {
                "placed": again.feasible,
                "best_penetration": again.violation,
                "attempts": again.attempts,
                "seconds": round(time.perf_counter() - confirm_clock, 3),
            }
            minimal["best_penetration"] = min(reduced["violation"], again.violation)
        record["minimal"] = minimal
    record["seconds"] = round(time.perf_counter() - clock, 3)
    return record


_WORKER: dict[str, Any] = {}


def _initialise(plan: Plan) -> None:
    _WORKER["plan"] = plan


def _survey(task: tuple[int, bool]) -> dict[str, Any]:
    mask, reduce = task
    return survey_state(_WORKER["plan"], mask, reduce=reduce)


# ---------------------------------------------------------------------------
# Distributions and the extrapolation
# ---------------------------------------------------------------------------


def band_of(value: float) -> str:
    for label, low, high in BANDS:
        if low <= value < high:
            return label
    return BANDS[-1][0]


def stratified_estimate(
    sizes: dict[str, int], values: dict[str, list[float]]
) -> dict[str, float | None]:
    """The population total of a per-orbit value from a stratified sample, with its SE.

    `values` holds each stratum's sampled values. A singleton stratum's variance is the
    pooled within-sample variance, an assumption stated in the receipt.
    """
    sampled = {key: v for key, v in values.items() if v}
    if not sampled:
        return {"total": None, "se": None, "low": None, "high": None}
    pooled_all = [x for v in sampled.values() for x in v]
    pooled = float(np.var(pooled_all, ddof=1)) if len(pooled_all) > 1 else 0.0
    total = variance = 0.0
    covered = 0
    for key, v in sampled.items():
        size, n = sizes[key], len(v)
        covered += size
        total += size * float(np.mean(v))
        spread = float(np.var(v, ddof=1)) if n > 1 else pooled
        variance += size * size * (1 - n / size) * spread / n
    population = sum(sizes.values())
    if covered < population:
        total *= population / covered
    se = math.sqrt(variance) * (population / covered)
    return {
        "total": total,
        "se": se,
        "low": max(total - Z95 * se, 0.0),
        "high": total + Z95 * se,
    }


def zero_upper(n: int, population: int) -> float:
    """A 95% upper bound on a count never seen in `n` draws (exact binomial)."""
    return population * (1 - 0.05 ** (1 / n)) if n else float(population)


def by_distance(sample: list[dict[str, Any]]) -> dict[str, Any]:
    """Per Hamming distance to the endpoint: bands, placements, minimal arities, wall."""
    table: dict[str, Any] = {}
    for apart in sorted({r["distance"] for r in sample}):
        rows = [r for r in sample if r["distance"] == apart]
        reduced = [r["minimal"] for r in rows if r["minimal"] is not None]
        table[str(apart)] = {
            "states": len(rows),
            "placed": sum(1 for r in rows if r["full"]["placed"]),
            "bands": dict(Counter(band_of(r["full"]["best_penetration"]) for r in rows)),
            "least_penetration": min(r["full"]["best_penetration"] for r in rows),
            "minimal_arity": dict(sorted(Counter(str(m["arity"]) for m in reduced).items())),
            "mean_seconds": float(np.mean([r["seconds"] for r in rows])),
        }
    return table


def distributions(
    records: list[dict[str, Any]], sizes: dict[str, int], population: int
) -> dict[str, Any]:
    """Sample counts and stratified estimates over all surviving orbits."""
    sample = [r for r in records if r["stratum"] != ENDPOINT_STRATUM]
    control = [r for r in records if r["stratum"] == ENDPOINT_STRATUM]
    random_sizes = {key: size for key, size in sizes.items() if key != ENDPOINT_STRATUM}

    selected = [r for r in sample if r.get("reduce_selected", True)]

    def by_stratum(
        indicator: Any, rows: list[dict[str, Any]] | None = None
    ) -> dict[str, list[float]]:
        grouped: dict[str, list[float]] = {key: [] for key in random_sizes}
        for record in sample if rows is None else rows:
            grouped[record["stratum"]].append(float(indicator(record)))
        return grouped

    bands = {label: 0 for label, _, _ in BANDS}
    for record in sample:
        bands[band_of(record["full"]["best_penetration"])] += 1
    band_estimates = {
        label: stratified_estimate(
            random_sizes,
            by_stratum(lambda r, b=label: band_of(r["full"]["best_penetration"]) == b),
        )
        for label, _, _ in BANDS
    }
    reduced = [r for r in sample if r["minimal"] is not None]
    arity = Counter(r["minimal"]["arity"] for r in reduced)
    classes = Counter(r["minimal"]["class"] for r in reduced)
    confirmed = [r for r in reduced if not r["minimal"].get("confirm", {}).get("placed", False)]
    placed_other = [r for r in sample if r["full"]["placed"]]
    new_share = classes.get("new", 0) / len(reduced) if reduced else None
    return {
        "sample_states": len(sample),
        "control_states": len(control),
        "by_distance": by_distance(sample),
        "full_penetration_bands": {"sample": bands, "estimate_over_survivors": band_estimates},
        "placed_at_cap": {
            "sample": len(placed_other),
            "estimate": stratified_estimate(
                random_sizes, by_stratum(lambda r: r["full"]["placed"])
            ),
            "upper95_if_none_seen": zero_upper(len(sample), population - len(control))
            if not placed_other
            else None,
        },
        "minimal_arity": {
            "sample": {str(k): v for k, v in sorted(arity.items())},
            "estimate_over_survivors": {
                str(k): stratified_estimate(
                    random_sizes,
                    by_stratum(
                        lambda r, a=k: r["minimal"] is not None and r["minimal"]["arity"] == a,
                        selected,
                    ),
                )
                for k in sorted(arity)
            },
            "mean": float(np.mean([r["minimal"]["arity"] for r in reduced]))
            if reduced
            else None,
        },
        "minimal_class": {
            "sample": dict(sorted(classes.items())),
            "new_share": new_share,
            "new_estimate_over_survivors": stratified_estimate(
                random_sizes,
                by_stratum(
                    lambda r: r["minimal"] is not None and r["minimal"]["class"] == "new",
                    selected,
                ),
            ),
            "confirmed_by_second_search": len(confirmed),
        },
        "wall": {
            "mean_seconds_per_state": float(np.mean([r["seconds"] for r in sample]))
            if sample
            else None,
            "full_state_over_survivors_seconds": stratified_estimate(
                random_sizes, by_stratum(lambda r: r["full"]["seconds"])
            ),
            "reduction_over_survivors_seconds": stratified_estimate(
                random_sizes,
                by_stratum(lambda r: r["seconds"] - r["full"]["seconds"], selected),
            ),
        },
    }


def found_classes(
    plan: Plan,
    records: list[dict[str, Any]],
    alive: NDArray[np.int64],
    flags: list[int],
    size: int,
) -> dict[str, Any]:
    """Each distinct minimal class found, and what certifying it would remove."""
    group = plan.geometry.group
    found: dict[int, dict[str, Any]] = {}
    for record in records:
        minimal = record["minimal"]
        if minimal is None:
            continue
        mask = minimal["canonical_mask"]
        entry = found.setdefault(
            mask,
            {
                "cells": minimal["cells"],
                "arity": minimal["arity"],
                "class": minimal["class"],
                "best_penetration": minimal["best_penetration"],
                "sampled_states": 0,
            },
        )
        entry["sampled_states"] += 1
        entry["best_penetration"] = min(entry["best_penetration"], minimal["best_penetration"])
    rows = []
    for mask, entry in sorted(found.items()):
        hit = np.zeros(alive.size, dtype=np.bool_)
        for image in selector.orbit(mask, group):
            hit |= (alive & image) == image
        removed = alive[hit]
        orbits = selector.count_orbits(removed, group)["orbits"] if removed.size else 0
        rows.append(
            {
                **entry,
                "mask": mask,
                "removes_states": int(removed.size),
                "removes_orbits": orbits,
            }
        )
    rows.sort(key=lambda row: (-row["removes_orbits"], row["mask"]))
    new = [row["mask"] for row in rows if row["class"] == "new"]
    after = selector.consume(len(plan.geometry.names), group, flags + new, size=size)
    return {
        "classes": rows,
        "distinct": len(rows),
        "survivors_if_new_classes_certified": {
            "states": after["surviving_states"],
            "orbits": after["orbits"],
        },
    }


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------


def budget_of(text: str, margin: float) -> selector.Budget:
    starts, hops, deep_starts, deep_hops = (int(part) for part in text.split(","))
    # The survey finishes its own rounds, so the selector's in-search finish stays off.
    return selector.Budget(
        starts=starts,
        hops=hops,
        deep_starts=deep_starts,
        deep_hops=deep_hops,
        margin=margin,
        finish=False,
    )


@dataclass(frozen=True)
class Population:
    """The surviving orbits under a flag set, with features and strata."""

    flags: list[int]
    alive: NDArray[np.int64]
    representatives: list[int]
    features: dict[int, dict[str, Any]]
    strata: dict[str, list[int]]


def population(
    geometry: selector.Geometry,
    flags: list[int],
    size: int,
    endpoint_state: int | None,
) -> Population:
    """Reuse the complete combinatorial census while returning detached mutable values."""
    snapshot = _population_cached(
        tuple(geometry.names),
        tuple(tuple(permutation) for permutation in geometry.group),
        tuple(sorted(set(flags))),
        size,
        endpoint_state,
    )
    return Population(
        list(flags),
        snapshot.alive.copy(),
        snapshot.representatives.copy(),
        deepcopy(snapshot.features),
        deepcopy(snapshot.strata),
    )


def clear_population_cache() -> None:
    """Discard retained censuses so a caller can measure a complete cold calculation."""
    _population_cached.cache_clear()


@functools.lru_cache(maxsize=4)
def _population_cached(
    names: tuple[str, ...],
    group: tuple[tuple[int, ...], ...],
    flags: tuple[int, ...],
    size: int,
    endpoint_state: int | None,
) -> Population:
    alive, representatives = surviving_orbits(len(names), group, list(flags), size)
    images = [] if endpoint_state is None else sorted(selector.orbit(endpoint_state, group))
    endpoint_rep = None if endpoint_state is None else selector.canonical(endpoint_state, group)
    features: dict[int, dict[str, Any]] = {}
    strata: dict[str, list[int]] = {}
    for mask in representatives:
        counts = composition(names, mask)
        apart = distance(mask, images)
        key = ENDPOINT_STRATUM if mask == endpoint_rep else stratum_of(counts, apart)
        features[mask] = {
            "composition": counts,
            "contact": contact(mask, images),
            "distance": apart,
            "orbit_size": len(selector.orbit(mask, group)),
            "stratum": key,
        }
        strata.setdefault(key, []).append(mask)
    return Population(list(flags), alive, representatives, features, strata)


def frame_of(pop: Population, apart: int | None) -> Population:
    """The orbits at Hamming distance `apart` from the endpoint's orbit, and the endpoint's
    own orbit as the control; the whole population when `apart` is None. The surviving
    states and the flags stay whole, since a found class is measured against them all."""
    if apart is None:
        return pop
    kept = [
        mask
        for mask in pop.representatives
        if pop.features[mask]["distance"] == apart
        or pop.features[mask]["stratum"] == ENDPOINT_STRATUM
    ]
    strata: dict[str, list[int]] = {}
    for mask in kept:
        strata.setdefault(pop.features[mask]["stratum"], []).append(mask)
    features = {mask: pop.features[mask] for mask in kept}
    return Population(pop.flags, pop.alive, kept, features, strata)


def shard_of(drawn: list[tuple[str, int]], shard: str | None) -> list[tuple[str, int]]:
    """The K-th of N interleaved parts of a draw, in mask order, for `shard` = "K/N", or
    the whole draw for None. The N parts partition the draw, so N runs of a `--sample 0`
    frame survey every orbit in it exactly once, each run short enough for its own wall
    ceiling; each run still places the endpoint's control first."""
    if shard is None:
        return drawn
    part, slash, parts = shard.partition("/")
    if not slash or not part.isdigit() or not parts.isdigit():
        raise ValueError(f"shard {shard!r}: write K/N")
    k, n = int(part), int(parts)
    if not 0 <= k < n:
        raise ValueError(f"shard {shard!r}: need 0 <= K < N")
    ordered = sorted(drawn, key=lambda item: item[1])
    return [item for index, item in enumerate(ordered) if index % n == k]


def draw_frame(
    frame: Population, sample: int, seed: int
) -> tuple[dict[str, int], list[tuple[str, int]]]:
    """The seeded weighted draw from the frame's random strata: `sample` orbits, or every
    orbit in the frame when `sample` is 0. The endpoint's control is not part of it."""
    if sample < 0:
        raise ValueError(f"sample {sample}: 0 takes every orbit in the frame")
    strata = {key: masks for key, masks in frame.strata.items() if key != ENDPOINT_STRATUM}
    if not strata:
        raise ValueError("the frame holds no surviving orbit besides the endpoint's")
    size = sum(len(masks) for masks in strata.values())
    return draw_sample(strata, sample or size, seed, weighted=True)


def write(path: Path | None, receipt: dict[str, Any]) -> None:
    if path is not None:
        text = retained_json.dumps(receipt, sort_keys=True, default=float)
        _ = path.write_text(text, encoding="utf-8")


def run_survey(
    plan: Plan,
    pop: Population,
    drawn: list[tuple[str, int]],
    *,
    workers: int,
    timeout: float | None,
    header: dict[str, Any],
    output: Path | None,
    size: int,
    reduce: set[int] | None = None,
    seed: int = 0,
) -> dict[str, Any]:
    """Survey every drawn state, writing the receipt as each finishes.

    The endpoint's control runs first, then the rest in a seeded random order, so a wall
    ceiling leaves a random subsample of every stratum rather than whole strata. Only the
    states in `reduce` (all, when it is None) get the deletion filter.
    """
    clock = time.perf_counter()
    records: dict[int, dict[str, Any]] = {}
    sizes = {key: len(masks) for key, masks in pop.strata.items()}
    total = len(pop.representatives)
    order = {mask: index for index, (_, mask) in enumerate(drawn)}

    def receipt(*, complete: bool) -> dict[str, Any]:
        done = [records[mask] for _, mask in drawn if mask in records]
        placed = [
            {k: r[k] for k in ("mask", "cells", "stratum", "distance")} | {"full": r["full"]}
            for r in done
            if r["full"]["placed"] and r["stratum"] != ENDPOINT_STRATUM
        ]
        body: dict[str, Any] = {
            **header,
            "complete": complete,
            "states_done": len(done),
            "states_drawn": len(drawn),
            "placed_states": placed,
            "controls": [r for r in done if r["stratum"] == ENDPOINT_STRATUM],
            "states": done,
            "seconds": round(time.perf_counter() - clock, 3),
        }
        if done:
            body["distributions"] = distributions(done, sizes, total)
            body["found_classes"] = found_classes(plan, done, pop.alive, pop.flags, size)
        return body

    def accept(mask: int, record: dict[str, Any]) -> None:
        feature = pop.features[mask]
        records[mask] = {
            "index": order[mask],
            "stratum": feature["stratum"],
            "composition": feature["composition"],
            "contact": feature["contact"],
            "distance": feature["distance"],
            "orbit_size": feature["orbit_size"],
            **record,
        }
        minimal = record["minimal"]
        line = {
            "done": len(records),
            "of": len(drawn),
            "stratum": feature["stratum"],
            "distance": feature["distance"],
            "full": f"{record['full']['best_penetration']:.2e}",
            "placed": record["full"]["placed"],
            "minimal_arity": None if minimal is None else minimal["arity"],
            "class": None if minimal is None else minimal["class"],
            "seconds": record["seconds"],
        }
        print(json.dumps(line), flush=True)
        write(output, receipt(complete=False))

    first = [mask for key, mask in drawn if key == ENDPOINT_STRATUM]
    rest = [mask for key, mask in drawn if key != ENDPOINT_STRATUM]
    shuffled = np.random.default_rng(np.random.SeedSequence([seed, 0x0D])).permutation(
        len(rest)
    )
    masks = first + [rest[int(i)] for i in shuffled]
    tasks = [(mask, reduce is None or mask in reduce) for mask in masks]
    complete = True
    if workers <= 1:
        _initialise(plan)
        for task in tasks:
            if timeout is not None and time.perf_counter() - clock > timeout:
                complete = False
                break
            accept(task[0], _survey(task))
    else:
        # The ceiling stops new states from starting; a state already running finishes.
        with ProcessPoolExecutor(workers, initializer=_initialise, initargs=(plan,)) as pool:
            pending: dict[Future[dict[str, Any]], int] = {
                pool.submit(_survey, task): task[0] for task in tasks
            }
            while pending:
                left = None if timeout is None else timeout - (time.perf_counter() - clock)
                if left is not None and left <= 0 and complete:
                    complete = False
                    pending = {f: m for f, m in pending.items() if not f.cancel()}
                    left = None
                finished, _ = wait(pending, timeout=left, return_when=FIRST_COMPLETED)
                for future in finished:
                    accept(pending.pop(future), future.result())
    final = receipt(complete=complete and len(records) == len(drawn))
    write(output, final)
    return final


def _calibration_job(job: dict[str, Any]) -> dict[str, Any]:
    plan: Plan = _WORKER["plan"]
    cells = selector.cells_of(job["mask"])
    clock = time.perf_counter()
    outcome = search_component(
        plan.geometry,
        cells,
        seed=job["seed"],
        role=ROLE_FULL,
        effort=job["effort"],
        warm=job["warm"],
    )
    record = {
        "kind": job["kind"],
        "mask": job["mask"],
        "cells": [plan.geometry.names[cell] for cell in cells],
        "distance": job["distance"],
        "seed": job["seed"],
        "placed": outcome.feasible,
        "best_penetration": outcome.violation,
        "components": outcome.components,
        "found_by": outcome.found_by,
        "attempts": outcome.attempts,
        "trace": outcome.trace,
        "seconds": round(time.perf_counter() - clock, 3),
    }
    if outcome.feasible:
        record["pose"] = pose_rows(plan.geometry, cells, outcome.pose)
        problem = selector.Problem(plan.geometry, cells)
        record["signed_margins"] = signed_margins(problem, outcome.pose)
    return record


def calibration_jobs(
    plan: Plan,
    pop: Population,
    endpoint_rep: int,
    carried: Floats,
    *,
    seeds: int,
    rounds: int,
    neighbours: int,
    seed: int,
) -> list[dict[str, Any]]:
    """Blind endpoint runs under both round policies, seeded controls, and neighbours."""
    budget, done = plan.full.budget, plan.full.finish
    jobs: list[dict[str, Any]] = []
    for kind, carry in (("blind-fresh", False), ("blind-carry", True)):
        effort = Effort(budget, rounds, done, carry)
        jobs.extend(
            {"kind": kind, "mask": endpoint_rep, "seed": s, "effort": effort, "warm": None}
            for s in range(1, seeds + 1)
        )
    rng = np.random.default_rng(np.random.SeedSequence([seed, 0xCA1]))
    jobs.append(
        {
            "kind": "seeded-exact",
            "mask": endpoint_rep,
            "seed": 1,
            "effort": Effort(budget, 1, done),
            "warm": [carried],
        }
    )
    for sigma in (0.02, 0.05):
        for s in (1, 2):
            start = carried.copy()
            start[:, :2] += rng.normal(0.0, sigma, (len(start), 2))
            start[:, 2] += rng.normal(0.0, 5 * sigma, len(start))
            jobs.append(
                {
                    "kind": f"seeded-perturbed-{sigma}",
                    "mask": endpoint_rep,
                    "seed": s,
                    "effort": Effort(budget, 1, done),
                    "warm": [start],
                }
            )
    near = sorted(m for m in pop.representatives if pop.features[m]["distance"] == 2)
    picks = sorted(
        int(i) for i in rng.choice(len(near), min(neighbours, len(near)), replace=False)
    )
    fresh = Effort(budget, rounds, done)
    jobs.extend(
        {"kind": "distance-2", "mask": near[i], "seed": 1, "effort": fresh, "warm": None}
        for i in picks
    )
    for job in jobs:
        job["distance"] = pop.features[job["mask"]]["distance"]
    return jobs


def calibration_summary(records: list[dict[str, Any]], rounds: int) -> dict[str, Any]:
    """Blind success by round under each policy, and every other job's outcome."""
    summary: dict[str, Any] = {}
    for kind in ("blind-fresh", "blind-carry"):
        runs = [r for r in records if r["kind"] == kind]
        by_round = []
        for limit in range(1, rounds + 1):
            placed = [
                r for r in runs if r["placed"] and r["trace"] and len(r["trace"]) <= limit
            ]
            by_round.append(
                {
                    "rounds": limit,
                    "placed": len(placed),
                    "of": len(runs),
                    "mean_seconds_to_place": float(np.mean([r["seconds"] for r in placed]))
                    if placed
                    else None,
                }
            )
        summary[kind] = {
            "by_round": by_round,
            "best_unplaced": sorted(r["best_penetration"] for r in runs if not r["placed"]),
            "seconds_per_round": float(
                np.mean([r["seconds"] / len(r["trace"]) for r in runs if r["trace"]])
            )
            if runs
            else None,
        }
    summary["others"] = [
        {k: r[k] for k in ("kind", "seed", "distance", "placed", "best_penetration", "seconds")}
        for r in records
        if not r["kind"].startswith("blind")
    ]
    return summary


def run_calibration(
    plan: Plan,
    jobs: list[dict[str, Any]],
    *,
    workers: int,
    header: dict[str, Any],
    output: Path | None,
    rounds: int,
) -> dict[str, Any]:
    clock = time.perf_counter()
    records: list[dict[str, Any]] = []

    def body(*, complete: bool) -> dict[str, Any]:
        ordered = sorted(records, key=lambda r: (r["kind"], r["seed"], r["mask"]))
        return {
            **header,
            "mode": "calibration",
            "complete": complete,
            "jobs_done": len(records),
            "jobs": len(jobs),
            "summary": calibration_summary(ordered, rounds),
            "runs": ordered,
            "seconds": round(time.perf_counter() - clock, 3),
        }

    with ProcessPoolExecutor(
        max(workers, 1), initializer=_initialise, initargs=(plan,)
    ) as pool:
        for record in pool.map(_calibration_job, jobs):
            records.append(record)
            line = {k: record[k] for k in ("kind", "seed", "distance", "placed", "seconds")}
            print(json.dumps({**line, "best": f"{record['best_penetration']:.2e}"}), flush=True)
            write(output, body(complete=False))
    final = body(complete=True)
    write(output, final)
    return final


def endpoint_check(
    geometry: selector.Geometry, endpoint: dict[str, Any]
) -> tuple[int, dict[str, Any], Floats]:
    """The endpoint's orbit representative, and its pose carried there by the group."""
    state = selector.mask_of(endpoint["cells"])
    representative = selector.canonical(state, geometry.group)
    for element, permutation in enumerate(geometry.group):
        if selector.image_mask(state, permutation) == representative:
            cells, pose = selector.transform_pose(
                geometry, endpoint["cells"], endpoint["pose"], element
            )
            value = selector.Problem(geometry, cells).violation(pose)
            record = {
                "state": [geometry.names[cell] for cell in endpoint["cells"]],
                "representative": representative,
                "image_by": geometry.actions[element],
                "violation_of_carried_pose": value,
            }
            return representative, record, pose
    raise ValueError("the endpoint's state has no least image")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--flag-set", choices=sorted(FLAG_SETS), default="arity8")
    _ = parser.add_argument(
        "--sample", type=int, default=60, help="random states drawn; 0 takes the whole frame"
    )
    _ = parser.add_argument(
        "--distance",
        type=int,
        default=None,
        help="restrict the frame to the orbits at this Hamming distance from the endpoint's",
    )
    _ = parser.add_argument(
        "--shard",
        default=None,
        help="K/N: survey the K-th of N interleaved parts of the draw, in mask order",
    )
    _ = parser.add_argument("--seed", type=int, default=1)
    _ = parser.add_argument("--workers", type=int, default=1)
    _ = parser.add_argument("--timeout", type=float, default=None, help="wall ceiling, s")
    _ = parser.add_argument("--output", type=Path, default=None)
    _ = parser.add_argument("--margin", type=float, default=MARGIN)
    _ = parser.add_argument(
        "--full-budget", default="8,16,16,40", help="starts,hops,deep_starts,deep_hops"
    )
    _ = parser.add_argument("--full-rounds", type=int, default=3)
    _ = parser.add_argument("--reduce-budget", default="4,8,8,16")
    _ = parser.add_argument("--reduce-rounds", type=int, default=1)
    _ = parser.add_argument(
        "--escalate-rounds",
        type=int,
        default=1,
        help="rounds of the full budget a failed removal screen escalates to; 0 skips",
    )
    _ = parser.add_argument(
        "--confirm-rounds", type=int, default=1, help="0 skips the confirmation search"
    )
    _ = parser.add_argument("--max-steps", type=int, default=40)
    _ = parser.add_argument(
        "--reduce-fraction",
        type=float,
        default=1.0,
        help="a seeded random share of the drawn states gets the deletion filter",
    )
    _ = parser.add_argument("--no-finish", action="store_true", help="ablation: no finish")
    _ = parser.add_argument(
        "--no-knowledge", action="store_true", help="ablation: search every removal"
    )
    _ = parser.add_argument(
        "--strata-only", action="store_true", help="enumerate and draw; search nothing"
    )
    _ = parser.add_argument(
        "--calibrate",
        action="store_true",
        help="blind and seeded endpoint runs and distance-2 states instead of the sample",
    )
    _ = parser.add_argument("--calibrate-seeds", type=int, default=6)
    _ = parser.add_argument("--calibrate-rounds", type=int, default=8)
    _ = parser.add_argument("--calibrate-neighbours", type=int, default=2)
    _ = parser.add_argument(
        "--carry", action="store_true", help="later full-state rounds start from the best pose"
    )
    arguments = parser.parse_args(argv)
    clock = time.perf_counter()
    design = selector.DEFAULT_DESIGN
    geometry = selector.cover_geometry(design)
    size = selector.TARGET
    endpoint = selector.endpoint_pose(design)
    endpoint_state = selector.mask_of(endpoint["cells"])
    endpoint_rep, endpoint_record, carried_pose = endpoint_check(geometry, endpoint)
    flag_paths = FLAG_SETS[arguments.flag_set]
    flags = sorted(
        {m for p in flag_paths for m in selector.receipt_flags(REPO / p, geometry, design)}
    )
    pop = population(geometry, flags, size, endpoint_state)
    expected = EXPECTED_ORBITS[arguments.flag_set]
    if len(pop.representatives) != expected:
        raise ValueError(f"{len(pop.representatives)} surviving orbits, expected {expected}")
    frame = frame_of(pop, arguments.distance)
    try:
        allocation, drawn = draw_frame(frame, arguments.sample, arguments.seed)
    except ValueError as error:
        parser.error(f"--distance {arguments.distance} --sample {arguments.sample}: {error}")
    if arguments.shard is not None:
        try:
            drawn = shard_of(drawn, arguments.shard)
        except ValueError as error:
            parser.error(f"--shard: {error}")
        allocation = {}
        for key, _ in drawn:
            allocation[key] = allocation.get(key, 0) + 1
    drawn = [(ENDPOINT_STRATUM, endpoint_rep), *drawn]
    margin = arguments.margin
    finish_on = not arguments.no_finish
    full = Effort(
        budget_of(arguments.full_budget, margin),
        arguments.full_rounds,
        finish_on,
        arguments.carry,
    )
    plan = Plan(
        geometry=geometry,
        knowledge=None
        if arguments.no_knowledge
        else load_knowledge(geometry, design, KNOWLEDGE_RECEIPTS, REPO, size),
        seed=arguments.seed,
        full=full,
        reduce=Efforts(
            screen=Effort(
                budget_of(arguments.reduce_budget, margin), arguments.reduce_rounds, finish_on
            ),
            escalate=Effort(full.budget, arguments.escalate_rounds, finish_on)
            if arguments.escalate_rounds
            else None,
        ),
        confirm=Effort(full.budget, arguments.confirm_rounds, finish_on)
        if arguments.confirm_rounds
        else None,
        max_steps=arguments.max_steps,
    )
    header: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "design": design,
        "cap": str(selector.cover.U),
        "cells": list(geometry.names),
        "provenance": PROVENANCE,
        "selector_provenance": selector.PROVENANCE,
        "parameters": {
            "flag_set": arguments.flag_set,
            "flag_receipts": {
                p: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for p in flag_paths
            },
            "knowledge_receipts": None
            if arguments.no_knowledge
            else {
                p: hashlib.sha256((REPO / p).read_bytes()).hexdigest()
                for p in KNOWLEDGE_RECEIPTS
            },
            "sample": arguments.sample,
            "distance": arguments.distance,
            "shard": arguments.shard,
            "seed": arguments.seed,
            "workers": arguments.workers,
            "timeout": arguments.timeout,
            "full": plan.full.record(),
            "reduce_screen": plan.reduce.screen.record(),
            "reduce_escalate": None
            if plan.reduce.escalate is None
            else plan.reduce.escalate.record(),
            "confirm": None if plan.confirm is None else plan.confirm.record(),
            "max_steps": arguments.max_steps,
            "bands": [label for label, _, _ in BANDS],
            "strata": "corners {<=2,3,4} x interior {<=3,4,>=5} x Hamming distance to "
            "the endpoint's orbit {2,4,6,>=8}; one per stratum, then Sainte-Lague on size "
            f"weighted {NEIGHBOURHOOD_WEIGHT}; the endpoint's orbit is a certainty stratum",
            "variance": "stratified proportion with finite-population correction; a "
            "singleton stratum takes the pooled sample variance",
        },
        "population": {
            "flagged_classes": len(flags),
            "surviving_states": int(pop.alive.size),
            "surviving_orbits": len(pop.representatives),
            "expected_orbits": expected,
            "endpoint_survives": endpoint_rep in pop.features,
            "endpoint": endpoint_record,
            "strata": {
                key: {"orbits": len(pop.strata[key]), "drawn": allocation.get(key, 0)}
                for key in sorted(pop.strata)
            },
            "frame": {
                "distance": arguments.distance,
                "orbits": sum(len(v) for k, v in frame.strata.items() if k != ENDPOINT_STRATUM),
                "drawn": len(drawn) - 1,
            },
        },
    }
    header["population"]["strata"][ENDPOINT_STRATUM]["drawn"] = 1
    if arguments.calibrate:
        jobs = calibration_jobs(
            plan,
            pop,
            endpoint_rep,
            carried_pose,
            seeds=arguments.calibrate_seeds,
            rounds=arguments.calibrate_rounds,
            neighbours=arguments.calibrate_neighbours,
            seed=arguments.seed,
        )
        result = run_calibration(
            plan,
            jobs,
            workers=arguments.workers,
            header=header,
            output=arguments.output,
            rounds=arguments.calibrate_rounds,
        )
        print(json.dumps(result["summary"], indent=1, sort_keys=True, default=float))
        return 0
    if arguments.strata_only:
        header["drawn"] = [{"stratum": key, "mask": mask} for key, mask in drawn]
        header["seconds"] = round(time.perf_counter() - clock, 3)
        write(arguments.output, header)
        print(json.dumps(header["population"], indent=1, sort_keys=True))
        return 0
    chooser = np.random.default_rng(np.random.SeedSequence([arguments.seed, 0x7ED]))
    reduce = {
        mask
        for key, mask in drawn
        if key == ENDPOINT_STRATUM or chooser.random() < arguments.reduce_fraction
    }
    header["parameters"]["reduce_fraction"] = arguments.reduce_fraction
    receipt = run_survey(
        plan,
        frame,
        drawn,
        reduce=reduce,
        seed=arguments.seed,
        workers=arguments.workers,
        timeout=arguments.timeout,
        header=header,
        output=arguments.output,
        size=size,
    )
    summary = {
        "complete": receipt["complete"],
        "states_done": receipt["states_done"],
        "placed_states": len(receipt["placed_states"]),
        "controls": [
            {"placed": c["full"]["placed"], "best": c["full"]["best_penetration"]}
            for c in receipt["controls"]
        ],
        "distributions": receipt.get("distributions"),
        "seconds": receipt["seconds"],
    }
    print(json.dumps(summary, indent=1, sort_keys=True, default=float))
    controls_ok = all(c["full"]["placed"] for c in receipt["controls"])
    return 0 if receipt["complete"] and controls_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
