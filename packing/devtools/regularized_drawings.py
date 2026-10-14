#!/usr/bin/env python3
"""Record the regularized drawings in the register, generated from the layer's index.

Usage, from `packing/`, after `uv run --frozen --all-extras --group dev python -m
devtools.regularized_drawings`:

    [--check]

The atlas's regularized layer (`atlas/known-best/regularized/index.json`) draws a view of
a count's credited packing that this project regularized: by `regularize_axis_components/2`,
by Evan Daniel's regularizer through `devtools.regularize_evand`, or by the grid-slack
generator (`docs/project/policies/regularization-policy.md`). Each entry that draws a view
carries its regularization in the register's terms, `results.schema.yaml`'s
`regularizations` item, with `of_witness`, the source witness, standing in for `of`. The
owner asked that the regularizations the project makes be tracked with the provenance of
the packings they redraw (11 October 2026), and that every regularized version be captured
in the frontier records (12 October 2026). So `results.yaml` carries them too, as its
`regularized_drawings`: one item a drawn count, the layer's record with `of` resolved to the
registered result that holds the packing, and the view it is drawn from.

**Which result holds the packing.** A view at the witness's own side (`same`) redraws the
packing the witness retains: `of` is the registered result whose `attribution` names the
witness's source and whose scope holds the count. A view at the verified upper bound
(`bound`, written `solved` in the register's terms) redraws the packing solved to that
bound: `of` is the result the case's verified upper bound rests on
(`build_bound_citations.results_carrying` on the bound's own evidence), and only while the
view's side is exactly that bound: a later result that lowers `U` leaves the view at a
side no result holds, and the count is listed unregistered rather than credited to the
new holder (#548 review B1). A `same` view whose side is also exactly the verified upper
bound, where no registered result attributes the witness's source, redraws the packing
at that bound in the same way: the result the bound rests on holds it (T-155 certified
26 witnesses' own sides exactly from views that are drawn here). Where the bound rests on
several results, the one whose `regularizations` registered a view of the count at that
bound answers: at 33 counts T-155's view lies exactly at the side of Evan Daniel's
earlier certificate, and the case cites both (T-101, T-155). An axis view is `same` where
its regularization is, and a view at neither side is not a drawing frame (row 4).
Exactly one result must answer; where none does, or more than one, the count is listed
under `unregistered` with the reason, and its record stays in the layer's index alone.
The register holds a
result by others only when the record acts on it (`epistemics.md`, Results by Others), so a
packing from before this project began that no replay here ever registered has no result to
name, and inventing one is not this tool's to do.

**What is not a result.** A pure regularization, one that proves no new bound, is never
a result. A drawing changes no side, frontier value, evidence tier or credit (the policy,
section 1), so these items are not a register result and carry no rung: they are this
project's regularizations of results the register already holds. A view whose side lies
below the verified upper bound is a result first (row 3) and is registered by its own
entry's `regularizations`, as T-155 registered 59 exact sides; where such a view is also
drawn, at fifteen counts, its case note says that its exact side is registered as that
result (`registering_result`). It proves a new bound unless an earlier certificate
already stated that side, which the item then names (`first_certified_in`): T-155's side
is new at 26 counts, and at the other 33 it is the side of Evan Daniel's certificate
(T-101), which the record had carried rounded up, so there the note says that the side
is registered in T-155, that his certificate first certified it, naming T-101, and that
it proves no new bound. `first_certified_problems` holds the field to the case records,
whose verified upper bound rests on both results exactly where an item names one. Nor is
the bound new where a larger count's verified upper bound already proved it when the
side was registered, which the result's registration receipt records at the count
(`implied_by`, read by `implied_bounds`): T-156's side at n = 290 is that of T-155's
certificate at n = 291, and `s(290) ≤ s(291)`, so its note says that the side is
registered in T-156, that the certificate registered at n = 291 (T-155) already proved
the bound by monotonicity, and that it proves no new bound (the policy's section 9,
question 16).

**Whose regularization, and whether it was modified.** The owner asked on 13 October 2026
that the frontier records say which counts have been regularized and whether the
regularization is this project's, that a pure regularization never count as a result
while staying a credited part of the record, and that where this project's own
modifications to Evan Daniel's regularizer were used, the record say so as well. So each
item names its `modifications` where his regularizer or the grid-slack port of his
placement made the view, read from the index entry alone (`project_modifications`): the
retry rungs the kept solve climbed (`run.rungs`, or before the retry ladder
`run.retried_with`), the replica patches its `method` names, the same-side exact re-solve a
view at the witness's side was brought to it by, and for a grid-slack view the port
itself, which is this project's code and not his. An empty list says his regularizer ran
unmodified; a view of this project's axis tool has no such field. A registered result's
own regularization (`by: project`, as T-155's 59 are) names them in its item too, read
from its `method` and `side` the same way (`registered_modifications`) and written in
place after its `method`; an item records no solve, so where his regularizer made the view
it also says that whether the solve climbed a retry rung is not recorded
(`modifications_unrecorded`), rather than reading as unmodified. Where the layer draws
that very solve, the item reads its rungs from the drawn entry instead, as the drawing
does (`recorded_solves`): the result registers the drawing itself, and its registration
receipt names, at the count, a run whose receipt the entry's run block records, the
entry's output and its exact side. T-155's certificates are the full run's views at
fourteen drawn counts, which the index records; at 87 the layer draws a later run's
view at the same side, which records nothing of T-155's solve.

**The case records.** Each case record whose count the layer draws, whose count a
registered result holds this project's own regularization of (as T-155's 59 are), or
whose house is itself a regularization its source published (a register result's
`regularizations` item whose `by` is the bibliography key of the source the witness
names, as `T-146`'s are), carries a generated `regularization` field in its front
matter: a one-paragraph `note` the site's case page prints, then its `items`, the
source's regularization first in the register's own terms and this project's after it,
with the generator, the credit
line, the modifications, the side relation (`same` or `bound`), the registered result
that holds the packing (`of`, or null where none does), the result that registers the
drawn regularization itself where one does (`registered_in`), the earlier result whose
certificate first stated that side where its item names one (`first_certified_in`) and
the view's path. Last comes this project's regularization a result registers where the
layer does not draw it (`registered_case_items`), in the register's terms like a
source's, with its generator, credit line and modifications: T-155's at 43 undrawn
counts, and at 227, where the grid-slack view is drawn instead. A record the layer does
not draw, whose count no result holds a regularization of by this project, and whose
house no source regularized carries no such field.

The register's list is a block at the end of `results.yaml`, from `MARKER` on, which this
tool writes whole, and each case record's field is written in place, at the end of its
front matter; `--check` compares both with what the index gives and writes nothing.
`devtools.check_results` holds the same comparison (`problems`), so neither the register
nor a case record can drift from the layer.
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from devtools.build_bound_citations import (
    Register,
    in_scope,
    load_case,
    load_register,
    own_evidence,
    results_carrying,
)
from sqpack.yamlio import load_yaml, safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RESULTS = ROOT / "frontier/results.yaml"
INDEX = ROOT / "atlas/known-best/regularized/index.json"
FRONTIER = ROOT / "frontier"
VENDORED = REPO / "vendor/evand-regularize/vendored.yaml"
KEY = "regularized_drawings"
#: The case record's front-matter field this tool writes.
CASE_FIELD = "regularization"
MARKER = (
    "# Generated by python -m devtools.regularized_drawings from the regularized layer's\n"
    "# index (packing/atlas/known-best/regularized/index.json); do not edit by hand.\n"
)
GENERATOR = "python -m devtools.regularized_drawings"
#: A regularization's `by` for this project's own runs (`results.schema.yaml`).
PROJECT_REGULARIZER = "project"
#: The fields of a layer record the register's item keeps, in its order.
ITEM_FIELDS = ("n", "of", "by", "method", "modifications", "side", "changes", "identity")
#: The layer's generators, as its index names them.
AXIS_GENERATOR = "regularize_axis_components/2"
EVAND_GENERATOR = "evand-regularize"
#: Whose code made each generator's view: this project's axis tool (`axis`), Evan Daniel's
#: regularizer through the vendored driver (`evand`), or the grid-slack port of his
#: placement (`grid`). A generator not named here is refused, not credited by a guess.
GENERATOR_KINDS = {
    AXIS_GENERATOR: "axis",
    EVAND_GENERATOR: "evand",
    "regularize_grid_slack/0": "grid",
    "regularize_grid_slack/1": "grid",
}
#: The credit line of a view this project's axis tool made (policy section 7); the other
#: generators' lines are their index blocks' `credit`.
AXIS_CREDIT = (
    "Regularized by the Squares Project with its own axis tool (regularize_axis_components/2)"
)
#: The kind of result whose exact side a registered regularization proves, which the
#: notes say it is.
UPPER_BOUND = "upper-bound"
#: How an item names each of this project's modifications to Evan Daniel's regularizer.
SAME_SIDE_RESOLVE = "same-side exact re-solve (devtools.regularize_same_side)"
BOUND_RESOLVE = "exact re-solve at the verified upper bound (devtools.regularize_same_side)"
#: The retry rungs, by the name the driver records (`devtools.regularize_evand`). The
#: stall-stop rung's one change is its replica patch, which the view's `method` names, so
#: it has no words of its own (`SILENT_RUNGS`); any other rung is refused.
RUNG_WORDS = {
    "dps-100": "retry rung dps-100",
    "force-kkt": "retry rung force-kkt",
    "first-pass": "retry rung first-pass (devtools.regularize_evand_first_pass)",
}
SILENT_RUNGS = frozenset({"stall-stop"})
#: What a registered result's item cannot establish of the modifications: it records no
#: solve, so whether the solve that made the view climbed a retry rung, unless the layer
#: draws that very solve (`recorded_solves`).
UNRECORDED_RUNGS = "retry rungs"
#: What the grid-slack tool appends to its generator block's method when it writes a
#: view's or a registered item's `method`: the module that ran it. Written only by
#: `grid_written_method`, which both writers and `method_forms` use.
GRID_THROUGH = ", through devtools.regularize_grid_slack"
#: A registered regularization's field naming the earlier registered result whose
#: certificate first stated its exact side (`results.schema.yaml`): there the item
#: registers that side exactly and proves no new bound, as T-155's do at the 33 counts
#: where its side is that of Evan Daniel's certificate (T-101).
FIRST_CERTIFIED = "first_certified_in"
#: The format of the receipt a registration of regularized views keeps among its
#: result's artifacts, naming the run and output each certificate came from
#: (`devtools.register_regularized_bounds`, `FORMAT`).
REGISTRATION_RECEIPT = "regularized-bounds-receipt-v1"
#: The cost fields a run's index block keeps as its receipt recorded them, which
#: `regularize_evand reclassify` leaves as they were.
RECEIPT_COST = ("cpu_seconds", "wall_seconds", "workers")
#: The patches a vendored view's `method` names after the pin, `@675a5ea+name`.
_METHOD_PATCHES = re.compile(r"evand/square-packing@[0-9a-f]+((?:\+[^,+\s]+)*)")
#: What a drawing is when no result registers it (the owner, 13 October 2026: "Pure
#: regularization should not be considered a new result").
PURE = "a pure regularization, which proves no new bound"
#: How a note reads a project item's side relation and a source item's.
SIDE_WORDS = {
    "same": "at the witness's own side",
    "bound": "at the verified upper bound",
    "solved": "solved to its side",
}
IDENTITY_FIELDS = ("basis", "measured_in", "one_to_one", "moved", "max_move", "max_turn_deg")


class RegularizedDrawingsError(ValueError):
    """The index or the register names something this tool has no words for: a generator,
    a retry rung or retry argument, or a registering result that is not an upper bound."""


def generator_kind(generator: str) -> str:
    """Whose code made a generator's view (`GENERATOR_KINDS`); refused where unknown."""
    try:
        return GENERATOR_KINDS[generator]
    except KeyError:
        raise RegularizedDrawingsError(
            f"generator {generator!r} is not one this tool knows; name it in GENERATOR_KINDS"
        ) from None


def generator_credit(generator: str, generators: Mapping[str, Any]) -> str:
    """A generator's credit line: the axis tool's own, or its index block's `credit`."""
    if generator_kind(generator) == "axis":
        return AXIS_CREDIT
    credit = (generators.get(generator) or {}).get("credit")
    if not credit:
        raise RegularizedDrawingsError(f"the index's {generator} block names no credit")
    return str(credit)


def upper_bound_result(result: Mapping[str, Any]) -> str:
    """A registering result's id, refused unless it is an upper bound, which is what the
    notes say its regularization's exact side proves."""
    if result.get("kind") != UPPER_BOUND:
        raise RegularizedDrawingsError(
            f"{result['id']} registers a regularization but is a {result.get('kind')} result, "
            f"not an {UPPER_BOUND}"
        )
    return str(result["id"])


@dataclass(frozen=True)
class Resolved:
    """Which registered result holds a drawn count's packing, or why none answers."""

    of: str | None
    reason: str


def relation(entry: Mapping[str, Any]) -> str:
    """A drawn entry's side relation: the index's, or, for an axis view, which records
    none, `same` where its regularization is at the witness's side and `solved` else."""
    side = entry.get("side") or {}
    if side.get("relation"):
        return str(side["relation"])
    return "same" if (entry.get("regularization") or {}).get("side") == "same" else "solved"


def bound_side(bound: Mapping[str, Any]) -> Fraction | None:
    """A verified upper bound as a rational where it is one: its exact form, or its decimal
    where it states none; `None` for a closed form, which no rational side equals."""
    exact = bound.get("exact_form")
    text = str(exact if exact is not None else bound.get("value") or "")
    try:
        return Fraction(text)
    except ValueError:
        return None


def at_bound(entry: Mapping[str, Any], bound: Mapping[str, Any]) -> bool:
    """Whether a drawn entry's exact side is the case's verified upper bound."""
    view = (entry.get("side") or {}).get("view")
    upper = bound_side(bound)
    return view is not None and upper is not None and Fraction(str(view)) == upper


def witness_source_key(entry: Mapping[str, Any], repo: Path = REPO) -> str | None:
    """The bibliography key the drawn entry's source witness names."""
    document = load_yaml((repo / entry["source"]["witness"]).read_text(encoding="utf-8"))
    return (document["witness"].get("source") or {}).get("key")


def registering_holders(
    n: int, holders: Sequence[str], results: Sequence[Mapping[str, Any]], *, side: str
) -> list[str]:
    """The results a verified upper bound rests on, narrowed, where several prove it, to
    those that registered a regularized view of `n` at that bound (a `regularizations` item
    for `n` on `side`). At 33 counts the side of Evan Daniel's certificate (T-101) is also
    the side of a registered regularized view (T-155), and the case cites both: the view
    drawn there is the registering result's. Where none or several register one, the
    holders stand as they were, and the count is listed unregistered."""
    if len(holders) < 2:
        return list(holders)
    registering = [
        str(result["id"])
        for result in results
        if str(result["id"]) in holders
        and any(
            int(item["n"]) == n and item.get("side") == side
            for item in result.get("regularizations") or []
        )
    ]
    return registering if len(registering) == 1 else list(holders)


def _bound_result(
    n: int,
    bound_holders: Sequence[str],
    results: Sequence[Mapping[str, Any]],
    *,
    side_at_bound: bool,
) -> Resolved:
    """A `bound` view's result: the one its bound rests on, narrowed to the one that
    registered a view of `n` there, and only while the view's side is that bound."""
    holders = registering_holders(n, bound_holders, results, side="solved")
    if side_at_bound and len(holders) == 1:
        return Resolved(holders[0], "holds the verified upper bound the view is at")
    return Resolved(
        None,
        f"the verified upper bound rests on {list(holders)}"
        if side_at_bound
        else "the view's side is no longer the verified upper bound",
    )


def packing_result(
    entry: Mapping[str, Any],
    results: Sequence[Mapping[str, Any]],
    *,
    source_key: str | None,
    bound_holders: Sequence[str],
    side_at_bound: bool = False,
) -> Resolved:
    """The registered result whose packing the drawn entry redraws (see the module).
    `side_at_bound` says the view's side is exactly the case's verified upper bound."""
    n = int(entry["n"])
    if relation(entry) == "solved":
        return Resolved(None, "the view is at neither the witness's side nor the bound (row 4)")
    if relation(entry) == "bound":
        return _bound_result(n, bound_holders, results, side_at_bound=side_at_bound)
    if side_at_bound:
        bound_holders = registering_holders(n, bound_holders, results, side="same")
    holders = [
        str(result["id"])
        for result in results
        if in_scope(result["scope"], n)
        and source_key in ((result.get("attribution") or {}).get("source_keys") or [])
    ]
    if len(holders) == 1:
        return Resolved(holders[0], "attributes the witness's source")
    if not holders and side_at_bound and len(bound_holders) == 1:
        return Resolved(
            bound_holders[0], "holds the verified upper bound the witness's side is exactly"
        )
    if not holders:
        return Resolved(
            None, f"no registered result attributes the witness's source {source_key}"
        )
    return Resolved(None, f"several results attribute the witness's source: {holders}")


def rungs(entry: Mapping[str, Any]) -> list[str]:
    """The retry rungs a drawn view's solve climbed, as its index entry records them:
    `run.rungs`, or before the retry ladder the one retry's arguments, `retried_with`
    (`--dps N` and `--force-kkt`; any other argument is refused)."""
    run = entry.get("run") or {}
    if "rungs" in run:
        return [str(rung) for rung in run["rungs"]]
    arguments = [str(argument) for argument in run.get("retried_with") or []]
    found = []
    at = 0
    while at < len(arguments):
        if arguments[at] == "--dps" and at + 1 < len(arguments):
            found.append(f"dps-{arguments[at + 1]}")
            at += 2
        elif arguments[at] == "--force-kkt":
            found.append("force-kkt")
            at += 1
        else:
            raise RegularizedDrawingsError(
                f"n={entry.get('n')}: retry argument {arguments[at]!r} is not one this tool "
                "knows"
            )
    return found


def rung_words(found: Sequence[str], n: object = None) -> list[str]:
    """How an item names each rung a solve climbed (`RUNG_WORDS`), the stall-stop rung
    by its patch alone; a rung with no words is refused rather than dropped."""
    words = []
    for rung in found:
        if rung in SILENT_RUNGS:
            continue
        if rung not in RUNG_WORDS:
            raise RegularizedDrawingsError(
                f"n={n}: retry rung {rung!r} is not one this tool knows; name it in RUNG_WORDS"
            )
        words.append(RUNG_WORDS[rung])
    return words


@cache
def patch_kinds(path: Path = VENDORED) -> dict[str, str]:
    """The vendored copy's recorded local changes by the name a `method` gives them: a
    replica patch by its patch file's stem, any other change by its path. Read only where
    a view's `method` names one, so a tree without `vendor/` (a negative control's
    snapshot) reads none."""
    document = load_yaml(path.read_text(encoding="utf-8")) or {}
    kinds: dict[str, str] = {}
    for change in document.get("local_changes") or []:
        name = Path(str(change["patch"])).stem if change.get("patch") else str(change["path"])
        kinds[name] = str(change.get("kind") or "modified")
    return kinds


def project_modifications(
    entry: Mapping[str, Any], kinds: Mapping[str, str] | None = None
) -> list[str] | None:
    """This project's modifications to Evan Daniel's regularizer that made a drawn view,
    read from its index entry: the retry rungs its solve climbed, the vendored copy's
    patches its `method` names, and the exact re-solve that brought it to the witness's
    side; for a grid-slack view, the port of his placement, which is this project's code,
    and its re-solve. An empty list: his regularizer ran unmodified. None: the view is
    this project's axis tool's, which is not his regularizer."""
    generator = str(entry.get("generator"))
    kind = generator_kind(generator)
    if kind == "grid":
        return grid_modifications(generator, same=relation(entry) == "same")
    if kind == "axis":
        return None
    found = rung_words(rungs(entry), entry.get("n"))
    found.extend(
        patch_words(str((entry.get("regularization") or {}).get("method") or ""), kinds)
    )
    if relation(entry) == "same":
        found.append(SAME_SIDE_RESOLVE)
    return found


def grid_modifications(generator: str, *, same: bool) -> list[str]:
    """A grid-slack view's modifications: the port of his placement, which is this
    project's code, and the exact re-solve that brought it to its side."""
    return [
        f"port of his coincidence placement ({generator}) rather than his code",
        SAME_SIDE_RESOLVE if same else BOUND_RESOLVE,
    ]


def patch_words(method: str, kinds: Mapping[str, str] | None = None) -> list[str]:
    """The vendored copy's patches a `method` names after the pin, `@675a5ea+name`, each as
    a replica patch or another local change (`patch_kinds`)."""
    match = _METHOD_PATCHES.search(method)
    named = [name for name in (match.group(1) if match else "").split("+") if name]
    if kinds is None:
        kinds = patch_kinds() if named else {}
    return [
        f"replica patch {name}" if kinds.get(name) == "replica" else f"local change {name}"
        for name in named
    ]


# ------------------------------------------------- the registered results' own items


def grid_written_method(method: str) -> str:
    """A grid-slack generator's `method` as its writers write it, into a view's layer
    record (`devtools.regularize_grid_slack`) and into a registered item
    (`devtools.register_regularized_bounds`): with the module that ran it. The one place
    the form is made, so the writers and `method_forms` cannot drift apart."""
    return method + GRID_THROUGH


def method_forms(generator: str, generators: Mapping[str, Any]) -> tuple[str, ...]:
    """The `method` strings that name a generator: its index block's `method`, and for a
    grid-slack generator that method as its writers write it (`grid_written_method`)."""
    block = str((generators.get(generator) or {}).get("method") or "")
    if not block:
        return ()
    if GENERATOR_KINDS[generator] == "grid":
        return (block, grid_written_method(block))
    return (block,)


def method_generator(method: str, generators: Mapping[str, Any]) -> str:
    """The layer generator a registered regularization's `method` names: the one whose
    index block's `method` it is, less any patches after the pin; refused where no
    generator, or more than one, answers."""
    base = _METHOD_PATCHES.sub(
        lambda match: match.group(0)[: match.start(1) - match.start()], method
    )
    found = [
        generator
        for generator in GENERATOR_KINDS
        if base in method_forms(generator, generators)
    ]
    if len(found) != 1:
        raise RegularizedDrawingsError(
            f"method {method!r} names {found or 'no generator'} among the layer's generators"
        )
    return found[0]


def registered_modifications(
    record: Mapping[str, Any],
    generators: Mapping[str, Any],
    kinds: Mapping[str, str] | None = None,
    solve: Mapping[str, Any] | None = None,
) -> tuple[list[str] | None, list[str]]:
    """This project's modifications to Evan Daniel's regularizer that made a registered
    result's own regularization (`by: project`), as far as its item establishes them, read
    as a drawing's are (`project_modifications`): the patches its `method` names and the
    same-side re-solve of a view at the witness's side; for a grid-slack view the port and
    its re-solve. Then what the item cannot establish: it records no solve, so where his
    regularizer made the view, whether the solve climbed a retry rung (`UNRECORDED_RUNGS`).
    None, with nothing unrecorded: the axis tool's, which is not his regularizer.

    `solve` is the layer's index entry that draws the very solve the item registered,
    where one does (`recorded_solves`): the entry records that solve's rungs, so the item
    reads them from it, as the drawing does, and nothing is left unrecorded."""
    method = str(record["method"])
    generator = method_generator(method, generators)
    kind = generator_kind(generator)
    same = str(record["side"]) == "same"
    if kind == "axis":
        return None, []
    if kind == "grid":
        return grid_modifications(generator, same=same), []
    if solve is not None:
        return project_modifications(solve, kinds), []
    found = patch_words(method, kinds)
    if same:
        found.append(SAME_SIDE_RESOLVE)
    return found, [UNRECORDED_RUNGS]


def registration_receipt(
    result: Mapping[str, Any], repo: Path = REPO
) -> tuple[dict[int, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    """The receipt among a result's `artifacts` that names the run and output each of its
    registered certificates came from (`REGISTRATION_RECEIPT`, T-155's `selection.json`):
    its rows by count and its runs by name; both empty where the result keeps none."""
    for artifact in result.get("artifacts") or []:
        path = repo / str(artifact)
        if path.suffix != ".json" or not path.is_file():
            continue
        document = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict) or document.get("format") != REGISTRATION_RECEIPT:
            continue
        rows = {int(row["n"]): row for row in document.get("rows") or []}
        runs = {str(run["run"]): run for run in document.get("runs") or []}
        return rows, runs
    return {}, {}


def same_receipt(
    block: Mapping[str, Any],
    run: Mapping[str, Any],
    blocks: Mapping[str, Mapping[str, Any]] | None = None,
) -> bool:
    """Whether a run block of the layer's index records the receipt of a registration
    receipt's run: the same generator, the same parameters and the same cost, each as the
    run's own receipt recorded it. `regularize_evand reclassify` leaves a run's
    parameters as they were, so a copy of the run decided again answers too: its views are
    that run's solves. The index records the copy's cost once, on the run it was
    reclassified from (`reclassified_from`, #548 review B5), so the copy's cost is read
    from that run's block in `blocks`."""
    parameters = block.get("parameters") or {}
    theirs = run.get("parameters") or {}
    source = block.get("reclassified_from")
    costed = (blocks or {}).get(str(source)) if source else block
    cost = (costed or {}).get("cost") or {}
    spent = run.get("cost") or {}
    return (
        str(block.get("generator")) == str((run.get("generator") or {}).get("name"))
        and bool(parameters)
        and all(key in theirs and theirs[key] == value for key, value in parameters.items())
        and all(key in cost and cost[key] == spent.get(key) for key in RECEIPT_COST)
    )


def recorded_solves(
    drawn: Sequence[Drawn],
    results: Sequence[Mapping[str, Any]],
    runs: Sequence[Mapping[str, Any]],
    repo: Path = REPO,
) -> dict[tuple[str, int], Mapping[str, Any]]:
    """The registered regularizations whose very solve the layer draws, by (result, count),
    each with the index entry that draws it. A drawn entry draws the solve a result
    registered where the result registers the drawing itself (`registered_record`), and
    the result's registration receipt names, at that count, a run whose receipt the
    entry's run block records (`same_receipt`), the entry's output and the entry's exact
    side. T-155's certificates are the full run's views at fourteen drawn counts, and the
    index records those solves; at 87 the layer draws a later run's view at the same side,
    which says nothing of the solve T-155 registered."""
    blocks = {str(block["id"]): block for block in runs}
    receipts: dict[str, tuple[dict[int, Mapping[str, Any]], dict[str, Mapping[str, Any]]]] = {}
    found: dict[tuple[str, int], Mapping[str, Any]] = {}
    by_id = {str(result["id"]): result for result in results}
    for count in drawn:
        registered = registered_record(count, results)
        if registered is None:
            continue
        rid = registered[0]
        if rid not in receipts:
            receipts[rid] = registration_receipt(by_id[rid], repo)
        rows, receipt_runs = receipts[rid]
        entry = count.entry
        n = int(entry["n"])
        row = rows.get(n)
        run = entry.get("run") or {}
        view = (entry.get("side") or {}).get("view")
        if row is None or view is None:
            continue
        block = blocks.get(str(run.get("id")))
        receipt_run = receipt_runs.get(str(row.get("run")))
        if (
            block is not None
            and receipt_run is not None
            and same_receipt(block, receipt_run, blocks)
            and str(run.get("output")) == str(row.get("output"))
            and Fraction(str(view)) == Fraction(str(row.get("side")))
        ):
            found[(rid, n)] = entry
    return found


def registered_lines(found: list[str] | None, unrecorded: Sequence[str]) -> list[str]:
    """The `modifications` lines of a registered item, as the register writes them."""
    lines = []
    if found is not None:
        inner = ", ".join(json.dumps(word, ensure_ascii=False) for word in found)
        lines.append(f"        modifications: [{inner}]")
    if unrecorded:
        inner = ", ".join(json.dumps(word, ensure_ascii=False) for word in unrecorded)
        lines.append(f"        modifications_unrecorded: [{inner}]")
    return lines


_RESULT_HEAD = re.compile(r"^  - id: (T-[0-9]{3})$")
_ITEM_HEAD = re.compile(r"^      - n: ([0-9]+)$")
_MODIFICATION_LINE = re.compile(r"^        modifications(?:_unrecorded)?: ")


def with_registered_modifications(
    text: str,
    results: Sequence[Mapping[str, Any]],
    generators: Mapping[str, Any],
    solves: Mapping[tuple[str, int], Mapping[str, Any]] | None = None,
) -> str:
    """`results.yaml`'s hand-written register with each result's `by: project`
    regularization carrying the `modifications` its `method` and `side` give, or the
    drawn entry of its very solve where the layer draws it (`recorded_solves`), written
    after its `method`; every other line left as it was."""
    solves = solves or {}
    wanted = {
        (str(result["id"]), int(record["n"])): registered_lines(
            *registered_modifications(
                record,
                generators,
                solve=solves.get((str(result["id"]), int(record["n"]))),
            )
        )
        for result in results
        for record in result.get("regularizations") or []
        if record["by"] == PROJECT_REGULARIZER
    }
    if not wanted:
        return text
    out: list[str] = []
    rid: str | None = None
    current: tuple[str, int] | None = None
    # The lines owed after the `method` just read, written once its folded lines end.
    pending: list[str] | None = None
    for line in text.split("\n"):
        if pending is not None and not line.startswith("          "):
            out.extend(pending)
            pending = None
        if head := _RESULT_HEAD.match(line):
            rid, current = head.group(1), None
        elif not line.startswith("      ") and line.strip():
            current = None
        elif (item_head := _ITEM_HEAD.match(line)) and rid is not None:
            current = (rid, int(item_head.group(1)))
        if current in wanted and _MODIFICATION_LINE.match(line):
            continue
        out.append(line)
        if current in wanted and line.startswith("        method:"):
            pending = wanted[current]
    return "\n".join(out)


def item(
    entry: Mapping[str, Any], of: str, modifications: Sequence[str] | None = None
) -> dict[str, Any]:
    """The register's item for a drawn entry: its regularization with `of` resolved, and
    this project's modifications to Evan Daniel's regularizer where his method made it."""
    record = entry["regularization"]
    found = {**record, "of": of}
    if modifications is not None:
        found["modifications"] = list(modifications)
    kept = {key: found[key] for key in ITEM_FIELDS if key in found}
    kept["identity"] = {
        key: record["identity"][key] for key in IDENTITY_FIELDS if key in record["identity"]
    }
    kept["view"] = entry["view"]["path"]
    return kept


@dataclass(frozen=True)
class Drawn:
    """A count the layer draws, the result that holds its packing, and the modifications
    to Evan Daniel's regularizer that made it."""

    entry: Mapping[str, Any]
    resolved: Resolved
    modifications: list[str] | None


def drawn_counts(index: Mapping[str, Any], repo: Path = REPO) -> list[Drawn]:
    """Every count the layer draws regularized, with `of` resolved (see the module)."""
    register = load_register()
    results = register.results
    found: list[Drawn] = []
    for entry in sorted(index["entries"], key=lambda record: int(record["n"])):
        if entry.get("status") != "regularized":
            continue
        n = int(entry["n"])
        holders: list[str] = []
        exact = False
        if relation(entry) in {"bound", "same"}:
            bound = load_case(n).get("verified_upper_bound") or {}
            exact = at_bound(entry, bound)
            if relation(entry) == "bound" or exact:
                own = own_evidence(bound.get("evidence") or [], register)
                holders = results_carrying(n, own, results)
        resolved = packing_result(
            entry,
            results,
            source_key=witness_source_key(entry, repo),
            bound_holders=holders,
            side_at_bound=exact,
        )
        found.append(Drawn(entry, resolved, project_modifications(entry)))
    return found


def expected(
    index: Mapping[str, Any], repo: Path = REPO, drawn: Sequence[Drawn] | None = None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """What the register's `regularized_drawings` should hold for this index: the items
    whose packing a registered result holds, and the drawn counts with none, each with
    its reason."""
    items: list[dict[str, Any]] = []
    unregistered: list[dict[str, Any]] = []
    for count in drawn_counts(index, repo) if drawn is None else drawn:
        if count.resolved.of is None:
            unregistered.append({"n": int(count.entry["n"]), "reason": count.resolved.reason})
        else:
            items.append(item(count.entry, count.resolved.of, count.modifications))
    return items, unregistered


# ---------------------------------------------------------------- the case records


def source_regularizations(
    results: Sequence[Mapping[str, Any]],
    sources: Mapping[str, Any],
    repo: Path = REPO,
) -> dict[int, dict[str, Any]]:
    """The counts whose house is itself a regularization its source published: a
    register result's `regularizations` item by a source (`by` a bibliography key) whose
    key the count's known-best witness names, in the register's own terms, with the
    result that registered it (`registered_in`) and the source's credit line."""
    found: dict[int, dict[str, Any]] = {}
    for result in results:
        for record in result.get("regularizations") or []:
            by = str(record["by"])
            n = int(record["n"])
            if by == PROJECT_REGULARIZER:
                continue
            witness = {"source": {"witness": f"packing/witnesses/known-best/n-{n:03d}.yaml"}}
            if witness_source_key(witness, repo) != by:
                continue
            source = sources.get(by)
            credit = getattr(source, "credit", None) or ", ".join(
                getattr(source, "authors", ()) or (by,)
            )
            found[n] = {
                "by": by,
                "credit": credit,
                "of": str(record["of"]),
                "registered_in": upper_bound_result(result),
                "method": str(record["method"]),
                "side": str(record["side"]),
            }
    return found


#: A drawn view's side relation in the register's terms (`results.schema.yaml`).
REGISTER_SIDES = {"same": "same", "bound": "solved"}


def registered_record(
    count: Drawn, results: Sequence[Mapping[str, Any]]
) -> tuple[str, Mapping[str, Any]] | None:
    """The result that registers the drawn regularization itself as an upper bound, with
    its item: the drawn packing's own result (`of`), where its `regularizations` hold a
    `by: project` item at the count by the drawn view's method and at its side relation.
    T-155 does so at fifteen drawn counts, whose exact sides it registered (at eight of
    them the side Evan Daniel's certificate, T-101, first stated); elsewhere a drawing is
    a pure regularization, proving no new bound."""
    of = count.resolved.of
    if of is None:
        return None
    entry = count.entry
    n = int(entry["n"])
    method = str(entry["regularization"]["method"])
    side = REGISTER_SIDES[relation(entry)]
    for result in results:
        if str(result["id"]) != of:
            continue
        for record in result.get("regularizations") or []:
            if (
                int(record["n"]) == n
                and record["by"] == PROJECT_REGULARIZER
                and str(record["method"]) == method
                and record["side"] == side
            ):
                return upper_bound_result(result), record
    return None


def registering_result(count: Drawn, results: Sequence[Mapping[str, Any]]) -> str | None:
    """The id of the result that registers the drawn regularization itself
    (`registered_record`), or None where none does."""
    found = registered_record(count, results)
    return None if found is None else found[0]


def project_case_item(
    count: Drawn,
    generators: Mapping[str, Any],
    registered_in: str | None = None,
    first_certified_in: str | None = None,
) -> dict[str, Any]:
    """This project's regularization of a drawn count, as its case record keeps it, with
    the result that registers it where one does (`registering_result`), and where that
    result's item names one, the earlier result whose certificate first stated its exact
    side (`FIRST_CERTIFIED`)."""
    entry = count.entry
    generator = str(entry["generator"])
    found: dict[str, Any] = {
        "by": PROJECT_REGULARIZER,
        "credit": generator_credit(generator, generators),
        "generator": generator,
    }
    if count.modifications is not None:
        found["modifications"] = list(count.modifications)
    found["side"] = relation(entry)
    found["of"] = count.resolved.of
    if registered_in is not None:
        found["registered_in"] = registered_in
        if first_certified_in is not None:
            found[FIRST_CERTIFIED] = first_certified_in
    found["view"] = str(entry["view"]["path"])
    return found


def registered_case_items(
    results: Sequence[Mapping[str, Any]],
    generators: Mapping[str, Any],
    drawn: Collection[tuple[str, int]] = (),
) -> dict[int, dict[str, Any]]:
    """The counts at which a registered result holds this project's own regularization
    (`by: project`) that the layer does not draw, each as its case record keeps it: in
    the register's terms, like a source's (`method`, `side`, `of`, `registered_in`),
    with the generator its method names, its credit line and its modifications, and the
    earlier result whose certificate first stated its exact side where the item names one
    (`FIRST_CERTIFIED`). T-155 holds 59; at the fifteen in `drawn`, (result, count) pairs
    whose drawing is that regularization itself, the drawn item names the result
    instead."""
    found: dict[int, dict[str, Any]] = {}
    for result in results:
        for record in result.get("regularizations") or []:
            n = int(record["n"])
            if record["by"] != PROJECT_REGULARIZER or (str(result["id"]), n) in drawn:
                continue
            method = str(record["method"])
            generator = method_generator(method, generators)
            modifications, unrecorded = registered_modifications(record, generators)
            item: dict[str, Any] = {
                "by": PROJECT_REGULARIZER,
                "credit": generator_credit(generator, generators),
                "generator": generator,
                "method": method,
            }
            if modifications is not None:
                item["modifications"] = modifications
            if unrecorded:
                item["modifications_unrecorded"] = list(unrecorded)
            item["side"] = str(record["side"])
            item["of"] = str(record["of"])
            item["registered_in"] = upper_bound_result(result)
            if record.get(FIRST_CERTIFIED):
                item[FIRST_CERTIFIED] = str(record[FIRST_CERTIFIED])
            if n in found:
                raise RegularizedDrawingsError(
                    f"n={n}: two registered results hold this project's regularization"
                )
            found[n] = item
    return found


#: How a note says what a registered item cannot establish (`modifications_unrecorded`).
UNRECORDED_WORDS = {UNRECORDED_RUNGS: "whether its solve climbed a retry rung"}


def credit_sentence(found: Mapping[str, Any], *, also: bool = False) -> str:
    """Who made a project regularization, with which of this project's modifications to
    Evan Daniel's regularizer, and what of them is not recorded."""
    head = str(found["credit"])
    if also:
        head = f"Also {head[:1].lower()}{head[1:]}"
    modifications = found.get("modifications")
    unrecorded = [str(word) for word in found.get("modifications_unrecorded") or []]
    if modifications:
        head += f", with the project's modifications: {', '.join(modifications)}"
    elif modifications is not None:
        head += (
            ", with none of the project's modifications established"
            if unrecorded
            else ", unmodified"
        )
    for word in unrecorded:
        if word not in UNRECORDED_WORDS:
            raise RegularizedDrawingsError(f"no words for what is unrecorded: {word!r}")
        head += f"; {UNRECORDED_WORDS[word]} is not recorded"
    return head + "."


def registered_words(
    found: Mapping[str, Any],
    certificates: Mapping[str, str],
    implied: Mapping[str, Any] | None = None,
) -> str:
    """What a note says of a registered regularization's exact side: that its result
    registers it as the upper bound it proves, or, where an earlier result's certificate
    first stated that side (`FIRST_CERTIFIED`), that its result registers it and that
    certificate first certified it, naming that result, so it proves no new bound; or,
    where a larger count's verified upper bound already proved the bound when the side
    was registered (`implied`, from `implied_bounds`), that its result registers it and
    that the certificate registered at that count proved it by monotonicity, naming its
    results, so it proves no new bound. `certificates` gives whose certificate each
    result is (`certificate_words`)."""
    registered_in = found["registered_in"]
    first = found.get(FIRST_CERTIFIED)
    if not first and implied:
        return (
            f"its exact side is registered in {registered_in}, and the certificate "
            f"registered at n = {implied['n']} ({', '.join(implied['results'])}) already "
            "proved the bound by monotonicity, so it proves no new bound"
        )
    if not first:
        return f"its exact side is registered as {registered_in}, the upper bound it proves"
    whose = certificates.get(str(first)) or f"{first}'s certificate"
    return (
        f"its exact side is registered in {registered_in}, and the same side was first "
        f"certified by {whose} ({first}), so it proves no new bound"
    )


def certificate_words(rid: str, register: Register) -> str:
    """Whose certificate a registered result is, as a note names it: its sources' authors
    by their full credited names (`Evan Daniel's certificate`), or this project's for a
    result of its own."""
    result = next((found for found in register.results if str(found["id"]) == rid), None)
    keys = ((result or {}).get("attribution") or {}).get("source_keys") or []
    if result is None:
        return f"{rid}'s certificate"
    if not keys:
        return "this project's certificate"
    full = {surname: name for name, surname in register.names.items()}
    authors: list[str] = [
        full.get(str(author), str(author))
        for key in keys
        for author in getattr(register.sources.get(str(key)), "authors", ()) or ()
    ]
    names: list[str] = list(dict.fromkeys(authors)) or [rid]
    who = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
    return f"{who}'s certificate"


def implied_bounds(
    results: Sequence[Mapping[str, Any]], repo: Path = REPO
) -> dict[tuple[str, int], Mapping[str, Any]]:
    """The registered regularizations whose bound a larger count's verified upper bound
    already proved when they were registered, by (result, count), each with that ceiling
    as the result's registration receipt records it at the count (`implied_by`, which
    `register_regularized_bounds.implied_by` writes): T-156's at n = 290, T-155's
    certificate at n = 291. Such a result says that its bound follows by monotonicity
    (the policy's section 9, question 16), and so does the case note
    (`registered_words`)."""
    found: dict[tuple[str, int], Mapping[str, Any]] = {}
    for result in results:
        counts = {
            int(record["n"])
            for record in result.get("regularizations") or []
            if record["by"] == PROJECT_REGULARIZER
        }
        if not counts:
            continue
        rows, _runs = registration_receipt(result, repo)
        for n in sorted(counts & set(rows)):
            if rows[n].get("implied_by"):
                found[(str(result["id"]), n)] = rows[n]["implied_by"]
    return found


def case_note(
    items: Sequence[Mapping[str, Any]],
    certificates: Mapping[str, str] | None = None,
    implied: Mapping[str, Mapping[str, Any]] | None = None,
) -> str:
    """The record's one paragraph: who regularized the drawing, with which modifications,
    and either that it is a pure regularization, proving no new bound, so no result, or
    that its exact side is registered as the result that proves it, or where an earlier
    certificate first stated that side, that it is registered there and whose certificate
    first certified it, or where a larger count's ceiling already proved the bound, that
    it is registered there and which certificate proved it by monotonicity
    (`registered_words`, `implied` by the registering result's id); then this project's
    registered regularization of the count where the layer does not draw it, naming the
    result; then who regularized the house, where its source did."""
    certificates = certificates or {}
    implied = implied or {}
    sentences: list[str] = []
    for found in items:
        if found["by"] != PROJECT_REGULARIZER or "view" not in found:
            continue
        sentences.append(credit_sentence(found))
        where = SIDE_WORDS[str(found["side"])]
        if found.get("registered_in"):
            words = registered_words(
                found, certificates, implied.get(str(found["registered_in"]))
            )
            sentences.append(
                f"A drawing of {found['of']}'s packing {where}. {words[:1].upper()}"
                f"{words[1:]}; the drawing itself is no further result."
            )
        elif found.get("of"):
            sentences.append(
                f"A drawing of {found['of']}'s packing {where}: {PURE}, so not a result."
            )
        else:
            sentences.append(
                f"A drawing {where}: {PURE}, so not a result; no registered result holds the "
                "packing."
            )
    for found in items:
        if found["by"] != PROJECT_REGULARIZER or "view" in found:
            continue
        sentences.append(credit_sentence(found, also=bool(sentences)))
        words = registered_words(found, certificates, implied.get(str(found["registered_in"])))
        sentences.append(
            f"A regularization of {found['of']}'s packing {SIDE_WORDS[str(found['side'])]}, "
            f"not drawn here; {words}."
        )
    for found in items:
        if found["by"] == PROJECT_REGULARIZER:
            continue
        sentences.append(
            f"The house is itself its source's regularization of {found['of']}'s packing "
            f"({found['credit']}), registered as {found['registered_in']} for the upper "
            "bound its exact side proves."
        )
    return " ".join(sentences)


def case_fields(
    index: Mapping[str, Any], repo: Path = REPO, drawn: Sequence[Drawn] | None = None
) -> dict[int, dict[str, Any]]:
    """Each case record's `regularization` field, by count, for the records that carry
    one: the source's regularization of the house first, then this project's drawing,
    then this project's regularization a result registers where the layer does not draw
    it (`registered_case_items`)."""
    register = load_register()
    by_source = source_regularizations(register.results, register.sources, repo)
    generators = index.get("generators") or {}
    projects: dict[int, dict[str, Any]] = {}
    for count in drawn_counts(index, repo) if drawn is None else drawn:
        registered_by = registered_record(count, register.results)
        projects[int(count.entry["n"])] = project_case_item(
            count,
            generators,
            None if registered_by is None else registered_by[0],
            None
            if registered_by is None or not registered_by[1].get(FIRST_CERTIFIED)
            else str(registered_by[1][FIRST_CERTIFIED]),
        )
    registered = registered_case_items(
        register.results,
        generators,
        {
            (str(found["registered_in"]), n)
            for n, found in projects.items()
            if found.get("registered_in")
        },
    )
    certificates = {
        first: certificate_words(first, register)
        for first in {
            str(found[FIRST_CERTIFIED])
            for found in [*projects.values(), *registered.values()]
            if found.get(FIRST_CERTIFIED)
        }
    }
    implied = implied_bounds(register.results, repo)
    fields: dict[int, dict[str, Any]] = {}
    for n in sorted(set(by_source) | set(projects) | set(registered)):
        items = [
            found for found in (by_source.get(n), projects.get(n), registered.get(n)) if found
        ]
        here = {rid: ceiling for (rid, count), ceiling in implied.items() if count == n}
        fields[n] = {"note": case_note(items, certificates, here), "items": items}
    return fields


def case_block(field: Mapping[str, Any]) -> str:
    """The field as the front matter writes it, under `packing:`."""
    dumped = yaml.safe_dump(
        {CASE_FIELD: dict(field)}, sort_keys=False, allow_unicode=True, width=96
    )
    return "".join(f"  {line}\n" for line in dumped.splitlines())


_CASE_BLOCK = re.compile(rf"^  {CASE_FIELD}:.*\n(?:    .*\n)*", re.MULTILINE)


def with_case_field(text: str, field: Mapping[str, Any] | None) -> str:
    """A case record's text with its `regularization` field set to `field`, at the end
    of its front matter, or removed where `field` is None; the rest left as it was."""
    if not text.startswith("---\n"):
        raise ValueError("a case record opens with its front matter")
    end = text.index("\n---\n", 4) + 1
    front, rest = text[:end], text[end:]
    block = case_block(field) if field is not None else ""
    if _CASE_BLOCK.search(front):
        front = _CASE_BLOCK.sub(lambda _match: block, front, count=1)
    else:
        front += block
    return front + rest


def case_problems(
    index: Mapping[str, Any], fields: Mapping[int, Mapping[str, Any]] | None = None
) -> list[str]:
    """The case records whose `regularization` field differs from what the index gives."""
    wanted = case_fields(index) if fields is None else fields
    problems = []
    for path in sorted(FRONTIER.glob("n-[0-9][0-9][0-9].md")):
        n = int(path.stem.split("-")[1])
        text = path.read_text(encoding="utf-8")
        if with_case_field(text, wanted.get(n)) != text:
            problems.append(
                f"{path.name}'s {CASE_FIELD} differs from the regularized layer's index; "
                f"run {GENERATOR}"
            )
    return problems


def update_cases(fields: Mapping[int, Mapping[str, Any]]) -> int:
    """Write each case record's `regularization` field; return how many records changed."""
    changed = 0
    for path in sorted(FRONTIER.glob("n-[0-9][0-9][0-9].md")):
        n = int(path.stem.split("-")[1])
        text = path.read_text(encoding="utf-8")
        updated = with_case_field(text, fields.get(n))
        if updated != text:
            with atomic_output_file(path) as temporary:
                temporary.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


_PLAIN = re.compile(r"^[A-Za-z0-9_./-]+$")
_NUMERIC = re.compile(r"^[0-9.eE+-]+$")
#: Plain words YAML would read as something other than a string.
_WORDS = frozenset({"null", "true", "false", "yes", "no", "on", "off", "y", "n"})


def scalar(value: Any) -> str:
    """One scalar as the block writes it: JSON's double-quoted string where YAML would read
    the plain text differently, which YAML reads back as the same string."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        # YAML 1.1, which the register's loader reads, takes `1e-15` for a string: its
        # float needs a point in the mantissa, so JSON's exponent form gains one.
        text = json.dumps(value)
        mantissa, exponent, power = text.partition("e")
        return f"{mantissa}.0e{power}" if exponent and "." not in mantissa else text
    if isinstance(value, int):
        return json.dumps(value)
    text = str(value)
    if _PLAIN.match(text) and not _NUMERIC.match(text) and text.lower() not in _WORDS:
        return text
    return json.dumps(text, ensure_ascii=False)


def block_text(
    items: Sequence[Mapping[str, Any]], unregistered: Sequence[Mapping[str, Any]]
) -> str:
    """The generated block: `MARKER`, then `regularized_drawings` in the register's style."""
    lines = [
        MARKER.rstrip("\n"),
        f"{KEY}:",
        "  index: packing/atlas/known-best/regularized/index.json",
    ]
    if unregistered:
        lines.append("  unregistered:")
        for row in unregistered:
            lines.append(f"    - n: {row['n']}")
            lines.append(f"      reason: {scalar(row['reason'])}")
    else:
        lines.append("  unregistered: []")
    lines.append("  items:" if items else "  items: []")
    for row in items:
        lines.append(f"    - n: {row['n']}")
        for key in ITEM_FIELDS[1:]:
            if key not in row:
                continue
            value = row[key]
            if key == "changes":
                inner = ", ".join(f"{name}: {scalar(number)}" for name, number in value.items())
                lines.append(f"      changes: {{{inner}}}")
            elif key == "modifications":
                inner = ", ".join(json.dumps(str(found), ensure_ascii=False) for found in value)
                lines.append(f"      modifications: [{inner}]")
            elif key == "identity":
                lines.append("      identity:")
                lines.extend(
                    f"        {name}: {scalar(found)}" for name, found in value.items()
                )
            else:
                lines.append(f"      {key}: {scalar(value)}")
        lines.append(f"      view: {scalar(row['view'])}")
    return "\n".join(lines) + "\n"


def split(text: str) -> tuple[str, str]:
    """`results.yaml` as the hand-written register and the generated block after it."""
    at = text.find(MARKER)
    if at < 0:
        return text, ""
    return text[:at], text[at:]


def index_document(path: Path = INDEX) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def problems(
    register_text: str | None = None, index: Mapping[str, Any] | None = None
) -> list[str]:
    """Where `results.yaml`'s generated block, a registered result's own regularization's
    `modifications` or `first_certified_in`, or a case record's `regularization` field
    differs from what the layer's index and the register give."""
    text = RESULTS.read_text(encoding="utf-8") if register_text is None else register_text
    head, block = split(text)
    document = index_document() if index is None else index
    drawn = drawn_counts(document)
    items, unregistered = expected(document, drawn=drawn)
    wanted = block_text(items, unregistered)
    results = (safe_load(head) or {}).get("results") or []
    solves = recorded_solves(drawn, results, document.get("runs") or [])
    found_problems = registered_problems(head, document.get("generators") or {}, solves)
    found_problems += first_certified_problems(load_register())
    found_problems += case_problems(document, case_fields(document, drawn=drawn))
    if block == wanted:
        return found_problems
    found = (safe_load(block) or {}).get(KEY) or {} if block else {}
    named = {row["n"] for row in found.get("items") or []}
    owed = {row["n"] for row in items}
    detail = []
    if named != owed:
        detail.append(f"items for {sorted(owed - named)} missing, {sorted(named - owed)} extra")
    return [
        f"results.yaml's {KEY} differs from the regularized layer's index"
        + (f" ({'; '.join(detail)})" if detail else "")
        + f"; run {GENERATOR}",
        *found_problems,
    ]


def registered_problems(
    head: str,
    generators: Mapping[str, Any],
    solves: Mapping[tuple[str, int], Mapping[str, Any]] | None = None,
) -> list[str]:
    """Whether each registered result's own regularization (`by: project`) carries the
    `modifications` its `method` and `side` give, or the drawn entry of its very solve
    where the layer draws it (`registered_modifications`, `recorded_solves`)."""
    results = (safe_load(head) or {}).get("results") or []
    solves = solves or {}
    if with_registered_modifications(head, results, generators, solves) == head:
        return []
    owed = sorted(
        {
            str(result["id"])
            for result in results
            for record in result.get("regularizations") or []
            if record["by"] == PROJECT_REGULARIZER
            and (record.get("modifications"), record.get("modifications_unrecorded") or [])
            != registered_modifications(
                record,
                generators,
                solve=solves.get((str(result["id"]), int(record["n"]))),
            )
        }
    )
    return [
        (
            f"results.yaml's `by: project` regularizations of {owed or 'some result'} do "
            f"not carry the modifications their methods and sides give; run {GENERATOR}"
        )
    ]


def bound_holders(n: int, register: Register) -> list[str]:
    """The registered results a case's verified upper bound rests on, by the results that
    carry its own evidence (`build_bound_citations.results_carrying`)."""
    bound = load_case(n).get("verified_upper_bound") or {}
    own = own_evidence(bound.get("evidence") or [], register)
    return results_carrying(n, own, register.results)


def first_certified_problems(register: Register) -> list[str]:
    """Whether each registered result's own regularization (`by: project`) names the
    earlier result whose certificate first stated its exact side exactly where the case
    record shows one (`FIRST_CERTIFIED`). Where the item is the case's verified upper
    bound, the bound rests on the registering result; where an earlier registered result
    proves the same bound beside it, its certificate stated that side first, and the item
    must name it, as T-155's do at the 33 counts whose bound T-101's replay of Evan
    Daniel's certificates also proves. An item that names a result the case's bound does
    not rest on beside the registering one, or names one where the bound rests on the
    registering result alone, is listed.

    A count a later house adoption holds is history for the item: the case's bound rests
    on the adopted house alone, below the item's side, and the item still names who first
    stated that side, as T-155's does at n = 264, where issue 528's packing (T-158) was
    adopted (`register_regularized_bounds.readopted`)."""
    from devtools import register_regularized_bounds as registration  # noqa: PLC0415
    from devtools.check_results import result_date  # noqa: PLC0415

    dated = {str(result["id"]): result_date(result) for result in register.results}

    def no_later(other: str, than: str) -> bool:
        # At the precision both dates give, as `check_results` compares them.
        shared = min(len(dated[other]), len(dated[than]))
        return dated[other][:shared] <= dated[than][:shared]

    found: list[str] = []
    for result in register.results:
        rid = str(result["id"])
        for record in result.get("regularizations") or []:
            if record["by"] != PROJECT_REGULARIZER:
                continue
            n = int(record["n"])
            holders = bound_holders(n, register)
            named = record.get(FIRST_CERTIFIED)
            earlier = [other for other in holders if other != rid and no_later(other, rid)]
            name = f"{rid}'s regularization at n = {n}"
            if rid not in holders and registration.readopted_by(n, rid):
                continue
            if named is not None and (rid not in holders or str(named) not in earlier):
                found.append(
                    f"{name} names {named} as {FIRST_CERTIFIED}, but the case's verified "
                    f"upper bound rests on {holders}"
                )
            elif named is None and rid in holders and earlier:
                found.append(
                    f"{name}: the case's verified upper bound rests on {earlier} as well, "
                    f"whose certificate stated the side first; name it as {FIRST_CERTIFIED}"
                )
    return found


def update() -> tuple[int, int, int]:
    """Write the generated block and the case records' fields; return the items, the
    unregistered counts and the case records changed."""
    text = RESULTS.read_text(encoding="utf-8")
    head, _block = split(text)
    document = index_document()
    drawn = drawn_counts(document)
    results = (safe_load(head) or {}).get("results") or []
    head = with_registered_modifications(
        head,
        results,
        document.get("generators") or {},
        recorded_solves(drawn, results, document.get("runs") or []),
    )
    items, unregistered = expected(document, drawn=drawn)
    with atomic_output_file(RESULTS) as temporary:
        temporary.write_text(
            head.rstrip("\n") + "\n\n" + block_text(items, unregistered), "utf-8"
        )
    changed = update_cases(case_fields(document, drawn=drawn))
    return len(items), len(unregistered), changed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--check", action="store_true", help="compare, writing nothing")
    args = parser.parse_args(argv)
    if args.check:
        found = problems()
        for problem in found:
            print(problem)
        if found:
            return 1
        print(
            f"{KEY} in results.yaml and the case records' {CASE_FIELD} agree with the "
            "regularized layer's index"
        )
        return 0
    recorded, missing, changed = update()
    print(
        f"{KEY}: {recorded} items, {missing} drawn counts no registered result holds; "
        f"{changed} case records changed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
