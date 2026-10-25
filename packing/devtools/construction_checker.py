"""Decide a recipe row exactly from its recipe and its replayed parent (D2, think-f2io).

The owner answered D2 on 23 October 2026: a construction an index or table states with no
certificate file of its own is a row once it is "decided exactly from the recipe by a
checker this project maintains". This is that checker (think-llit's plan, Recipe Rows).

A recipe in Couzo's indexes names a parent certificate (``source_n``, its path and its
SHA-256), ``tiles_per_side`` t, ``layers`` L and ``deleted_squares`` d, and states the
bound and, in ``construction.capacity``, how many squares the construction holds.

**The lemma.** Let P be a packing of n0 unit squares in the square [0, S]^2.

- *Tiling.* t^2 translated copies of P pack t^2 n0 squares in [0, tS]^2.
- *One L-border.* Around a container of side W, a layer adds floor(W + 1) unit squares
  along one side and floor(W) along the other, all inside [0, W + 1]^2 and outside
  [0, W]^2: 2 floor(W) + 1 squares.
- *The recipe* packs t^2 n0 + sum over j = 0 .. L - 1 of (2 floor(tS + j) + 1) squares at
  side tS + L (`capacity`), and deleting squares from a packing leaves a packing.

`decide` holds a recipe to the lemma in `Fraction`s: the parent must be the certificate
the index names (its path and SHA-256, at the count it names) and must have passed both
routes of the filtered replay with its six controls refused; the stated bound must be
tS + L exactly, the stated capacity the lemma's, and the count the capacity less the
stated deletions. It reads two kinds: ``square tiling and L-border`` and ``deletion`` (the
parent less its last d squares, t = 1 and L = 0). It refuses every other kind; a parent
that is a classical construction rather than a certificate the record replays, as
Friedman's off-centre family (think-zkxy); and a composite of Kevin Fang's, whatever its
table states, naming the parts the table leaves unstated, since no rule here reads a
composite (`COMPOSITE`). `controls` are the recipe's negative controls (`mutants`), each of
which `decide` must refuse. `write_out` builds the packing the lemma states, so a test can
decide it on both routes. A two-strip L-packing (#799) builds on no parent, and
`devtools.two_strip_checker` decides it from its parameters.

Exact throughout: the parent's side is its certificate's exact header side, and every
floor is taken of a `Fraction`.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Any

from devtools import evand_exact_certificates as legacy

TILING = "square tiling and L-border"
DELETION = "deletion"
#: Kevin Fang's composites (``composites/table.csv``): no rule here reads one, so each is
#: refused, naming whether his table states its parts (think-llit's plan).
COMPOSITE = "composite"
KINDS = (TILING, DELETION)
#: The lemma a decision rests on, as a receipt states it.
LEMMA = (
    "t^2 translated copies of a packing of n0 unit squares in [0, S]^2 pack t^2 n0 in "
    "[0, tS]^2; each L-border layer around a container of side W adds floor(W + 1) + "
    "floor(W) unit squares inside [0, W + 1]^2 and outside [0, W]^2; so the recipe packs "
    "t^2 n0 + sum_{j<L} (2 floor(tS + j) + 1) squares at side tS + L, and deleting squares "
    "leaves a packing"
)
#: The controls every recipe carries (`mutants`), in order.
CONTROLS = (
    "count above the capacity",
    "bound one unit below",
    "parent digest altered",
    "parent count wrong",
    "no tiles",
    "negative layers",
    "parent not replayed",
    "unknown kind",
    "deletes every square",
)
#: One unit in the 12th place, the print a side is compared at (`mutants`).
UNIT = Fraction(1, 10**12)
DECIDED = "decided"


class RecipeRefusedError(ValueError):
    """A recipe the checker does not decide, with the reason."""


def _refuse(condition: object, message: str) -> None:
    if not condition:
        raise RecipeRefusedError(message)


@dataclass(frozen=True, slots=True)
class Recipe:
    """A row an index states with no certificate file of its own: the count, the kind, the
    parent it names (count, path and SHA-256), the bound it states, and t, L and d; with
    the capacity the index states where it states one, and a composite's parts."""

    n: int
    kind: str
    source_n: int
    parent: str
    parent_sha256: str
    bound: Fraction
    tiles_per_side: int = 1
    layers: int = 0
    deleted: int = 0
    capacity: int | None = None
    parts: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Parent:
    """The certificate a recipe builds on: its count, exact header side, path and SHA-256,
    and the filtered replay's row that decided it (``replay``; None where it has not been
    replayed). ``classical`` names a classical construction standing in for a certificate,
    which the record does not replay."""

    n: int
    side: Fraction
    path: str
    sha256: str
    replay: Mapping[str, Any] | None = None
    classical: str = ""


def recipe_from_index(item: Mapping[str, Any]) -> Recipe:
    """A recipe as a claim map or an index entry states it: ``kind`` ``construction``
    (with its ``construction`` mapping) or ``deletion``, the parent's ``certificate`` and
    ``certificate_sha256``, the exact bound and ``deleted_squares``."""
    construction = item.get("construction") or {}
    kind = str(construction.get("kind", item["kind"]))
    return Recipe(
        n=int(item["n"]),
        kind=kind,
        source_n=int(construction.get("source_n", item.get("source_n", 0))),
        parent=str(item["certificate"]),
        parent_sha256=str(item["certificate_sha256"]),
        bound=Fraction(str(item["exact"])),
        tiles_per_side=int(construction.get("tiles_per_side", 1)),
        layers=int(construction.get("layers", 0)),
        deleted=int(item.get("deleted_squares") or 0),
        capacity=None if "capacity" not in construction else int(construction["capacity"]),
        parts=tuple(str(part) for part in item.get("parts") or ()),
    )


def parent_from_replay(row: Mapping[str, Any]) -> Parent:
    """A parent from the filtered receipt's row that decided it (`beyond_horizon_replay`'s
    ``decide_row`` or ``decide_parent``)."""
    return Parent(
        n=int(row["n"]),
        side=Fraction(str(row["exact_side"])),
        path=str(row["certificate"]),
        sha256=str(row["certificate_sha256"]),
        replay=row,
    )


def capacity(recipe: Recipe, side: Fraction) -> int:
    """How many squares the recipe's construction holds on a parent of side ``side``: t^2
    n0, and 2 floor(tS + j) + 1 for each layer j (the lemma)."""
    t = recipe.tiles_per_side
    return t * t * recipe.source_n + sum(
        2 * math.floor(t * side + j) + 1 for j in range(recipe.layers)
    )


def _replayed(parent: Parent) -> None:
    """Refuse a parent that has not passed both routes with its six controls refused."""
    row = parent.replay
    _refuse(row is not None, f"the parent n{parent.n} is not replayed")
    assert row is not None
    decision = row.get("decision") or {}
    _refuse(
        bool(row.get("verified"))
        and bool(decision.get("passed"))
        and Fraction(str(row.get("exact_side"))) == parent.side
        and row.get("certificate_sha256") == parent.sha256,
        f"the parent n{parent.n} did not pass both routes",
    )
    controls = row.get("controls") or []
    _refuse(
        len(controls) == 6
        and all(
            item["refused_by_sqpack"] and item["refused_by_independent"] for item in controls
        ),
        f"the parent n{parent.n}'s six controls are not all refused by both routes",
    )


def decide(recipe: Recipe, parent: Parent) -> dict[str, Any]:
    """The recipe decided exactly against its parent; `RecipeRefusedError` says why not."""
    if recipe.kind == COMPOSITE:
        _refuse(recipe.parts, "a composite whose parts its table does not state")
        raise RecipeRefusedError("a composite: no rule here reads one")
    _refuse(recipe.kind in KINDS, f"kind {recipe.kind!r}: not a recipe this checker reads")
    _refuse(
        not parent.classical,
        f"the parent is a classical construction ({parent.classical}), not a certificate "
        "the record replays (think-zkxy)",
    )
    _refuse(
        (parent.path, parent.sha256) == (recipe.parent, recipe.parent_sha256),
        "the parent is not the certificate the index names, by path and SHA-256",
    )
    _refuse(
        parent.n == recipe.source_n,
        f"the parent packs {parent.n}, the recipe names n{recipe.source_n}",
    )
    _replayed(parent)
    t, layers, deleted = recipe.tiles_per_side, recipe.layers, recipe.deleted
    _refuse(t >= 1 and layers >= 0 and deleted >= 0, f"t = {t}, L = {layers}: no recipe")
    if recipe.kind == DELETION:
        _refuse(t == 1 and layers == 0, "a deletion neither tiles nor adds a layer")
    held = capacity(recipe, parent.side)
    _refuse(deleted < held, f"deletes {deleted} of the {held} squares the construction holds")
    _refuse(
        recipe.capacity is None or recipe.capacity == held,
        f"the index states a capacity of {recipe.capacity}, the lemma gives {held}",
    )
    _refuse(recipe.n <= held, f"n = {recipe.n} is above the capacity {held}")
    _refuse(
        recipe.n + deleted == held,
        f"n = {recipe.n} is not the capacity {held} less the {deleted} stated deletions",
    )
    side = t * parent.side + layers
    _refuse(recipe.bound == side, f"the bound {recipe.bound} is not tS + L = {side}")
    return {
        "n": recipe.n,
        "kind": recipe.kind,
        "source_n": recipe.source_n,
        "parent": recipe.parent,
        "parent_sha256": recipe.parent_sha256,
        "tiles_per_side": t,
        "layers": layers,
        "deleted_squares": deleted,
        "capacity": held,
        "side": legacy.literal(side),
        "verdict": DECIDED,
    }


def mutants(recipe: Recipe, parent: Parent) -> list[tuple[str, Recipe, Parent]]:
    """A recipe's negative controls, each a change `decide` must refuse: a count one above
    the capacity, a bound one unit in the 12th place below tS + L, an altered parent digest
    or count, no tiles, a negative layer, an unreplayed parent, an unknown kind, and more
    deletions than the construction holds."""
    held = capacity(recipe, parent.side)
    altered = parent.sha256[:-1] + ("0" if parent.sha256[-1:] != "0" else "1")
    changed = [
        (replace(recipe, n=held + 1, deleted=0), parent),
        (replace(recipe, bound=recipe.bound - UNIT), parent),
        (recipe, replace(parent, sha256=altered)),
        (replace(recipe, source_n=recipe.source_n + 1), parent),
        (replace(recipe, tiles_per_side=0), parent),
        (replace(recipe, layers=-1), parent),
        (recipe, replace(parent, replay=None)),
        (replace(recipe, kind="spiral"), parent),
        (replace(recipe, deleted=held, n=0), parent),
    ]
    return [(name, *pair) for name, pair in zip(CONTROLS, changed, strict=True)]


def controls(recipe: Recipe, parent: Parent) -> list[dict[str, Any]]:
    """Each control (`mutants`) and the reason `decide` refused it; ``refused`` False marks
    one it accepted, which a check refuses."""
    found = []
    for name, changed, holder in mutants(recipe, parent):
        try:
            decide(changed, holder)
        except RecipeRefusedError as error:
            found.append({"control": name, "refused": True, "reason": str(error)})
        else:
            found.append({"control": name, "refused": False, "reason": ""})
    return found


def write_out(recipe: Recipe, parent: legacy.Certificate) -> legacy.Certificate:
    """The packing the lemma states for ``recipe`` on ``parent``: t^2 translated copies of
    the parent's poses, then each layer's axis-aligned unit squares along the top and the
    right of the container, less the last ``deleted`` squares. Every coordinate is exact."""
    t, side = recipe.tiles_per_side, parent.side
    poses = [
        legacy.Pose(pose.x + i * side, pose.y + j * side, pose.t)
        for i in range(t)
        for j in range(t)
        for pose in parent.poses
    ]
    half = Fraction(1, 2)
    for layer in range(recipe.layers):
        width = t * side + layer
        top = math.floor(width + 1)
        right = math.floor(width)
        # Along the top: unit squares centred at height width + 1/2, from the left.
        poses += [legacy.Pose(k + half, width + half, Fraction(0)) for k in range(top)]
        # Along the right: unit squares centred at width + 1/2, from the bottom.
        poses += [legacy.Pose(width + half, k + half, Fraction(0)) for k in range(right)]
    count = len(poses) - recipe.deleted
    return legacy.Certificate(count, t * side + recipe.layers, tuple(poses[:count]))
