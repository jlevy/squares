#!/usr/bin/env python3
"""Each count's default picture: its regularized view where the view improves on the
house drawing, else the house drawing, recorded and held to the data.

Usage, from `packing/`, after
`uv run --frozen --all-extras --group dev python -m devtools.default_drawings`:

    --update [--workers K]
    --check [--workers K]

The owner decided on 13 October 2026 that the regularized drawing is the default picture,
with the house drawing kept as "as published", and that a regularization should be a
strict improvement (`docs/project/policies/regularization-policy.md`, section 12). For
every count the layer's index (`atlas/known-best/regularized/index.json`) draws, the
default picture is the view when all three hold:

1. **Exact.** Both maintained exact routes accept it, as its entry records.
2. **Side.** Its exact side is at most `U`, the case record's verified upper bound as
   `regularize_evand.verified_bound` holds it exactly, or the count is one of
   `ABOVE_U`, the views the policy's section 9, question 13 names above it.
3. **Improvement.** It improves on the house drawing under the policy's improvement rule
   (section 11), which `devtools.improvement_rule` reads from the policy and decides. Both
   drawings are measured as `devtools.regularize_select.today` measures a tree's drawing
   -- the house renderer's colouring by `census_drawing_regularity.regularity`, the house
   and stage totals by `regularize_evand.contact_partners` -- the two sides are compared
   exactly where the house witness is exact, and exactness is the view's gain where the
   house witness is only numerically checked.

Every other count is drawn from its house witness, including a view that ties its house
drawing on every goal: there the picture is the same, and the house is the record's.

`--update` writes `atlas/known-best/default-drawings.json`: one entry a drawn view, with
its default, the reason, both drawings' measures and the goals the view is better and
worse on. `--check` measures every view again and fails when the record is not what the
data gives, when a regularized default breaks the rule, or when the policy's goals or
their directions differ from the ones the code judges (`improvement_rule.problems`). It
lists, failing nothing, each count that keeps the house picture and why: "no gain",
"above U, not in the exceptions", a goal it is worse on, or an exact route's refusal.
It costs about 20 cpu-seconds for the 90 views of 13 October 2026: 5.5 seconds of wall
at four workers on a quiet host, and 24 to 34 seconds in the records tier on a host
other work was loading.

The site's drawings (`render_frontier_page`), the atlas tiles (`overview_sections`) and
the posters (`build_known_best_atlas`) read the record through `regularized_defaults`,
which refuses a record whose counts, views or generators are not the index's. Reading
it measures nothing: the measuring code is imported only to measure, so its readers stay
light.
"""

from __future__ import annotations

import argparse
import gzip
import json
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import improvement_rule
from devtools.improvement_rule import MEASURES
from devtools.regularize_axis_components import ABOVE_U
from sqpack import retained_json
from sqpack.workers import worker_count
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
INDEX = ROOT / "atlas/known-best/regularized/index.json"
RECORD = ROOT / "atlas/known-best/default-drawings.json"
RECORD_PATH = "packing/atlas/known-best/default-drawings.json"
CONTRACT = "packing.squares:DefaultDrawings/v1"
SCHEMA = "default-drawings.schema.yaml"
GENERATOR = "python -m devtools.default_drawings"
REGULARIZED = "regularized"
HOUSE = "house"
#: How a refused count's reason reads, beside the improvement rule's own words.
ROUTE_REFUSED = "an exact route refused it"
UNKNOWN_U = "U is unknown"
ABOVE_BOUND = "above U, not in the exceptions"


def drawn_views(index: Path = INDEX) -> dict[int, dict[str, Any]]:
    """The layer's entries that draw a view, by count."""
    document = json.loads(index.read_text(encoding="utf-8"))
    return {
        int(entry["n"]): entry
        for entry in document["entries"]
        if entry["status"] == REGULARIZED
    }


def _view_witness(entry: Mapping[str, Any]) -> dict[str, Any]:
    text = gzip.decompress((REPO / entry["view"]["path"]).read_bytes()).decode("utf-8")
    return load_yaml(text)["witness"]


def drawn_above_bound(index: Path = INDEX) -> dict[int, float]:
    """Every drawn view whose exact side lies above `U`, by how far: each view's side read
    from its view file, exactly as both routes decide it, and held to `U` as the
    selection reads it."""
    from devtools import regularize_evand as drive  # noqa: PLC0415

    above: dict[int, float] = {}
    for n, entry in drawn_views(index).items():
        side, _placements, _corners = drive.view_geometry(_view_witness(entry))
        upper = drive.verified_bound(drive.case_facts(n))
        if upper is None:
            raise ValueError(f"n={n}: U is unknown")
        order = upper.compare(side)
        if order is None:
            raise ValueError(f"n={n}: U is not read exactly: {upper.unread}")
        if order > 0:
            above[n] = upper.difference(side)
    return above


def _routes(entry: Mapping[str, Any]) -> bool:
    """Whether both maintained exact routes accepted the view, as its entry records."""
    verdict = entry.get("exact_verification") or {}
    return bool(
        verdict.get("repository_verifier")
        and verdict.get("independent_checker")
        and verdict.get("passed")
    )


def _against(view: Fraction, house: Fraction | None) -> str | None:
    if house is None:
        return None
    return "smaller" if view < house else "larger" if view > house else "same"


def decide(unit: tuple[Path, int, Mapping[int, Mapping[str, Any]]]) -> dict[str, Any]:
    """One count's view against its house drawing, and the picture the rule draws."""
    from devtools import regularize_evand as drive  # noqa: PLC0415
    from devtools import regularize_select as select  # noqa: PLC0415

    tree, n, entries = unit
    entry = entries[n]
    view = select.today((tree, n, entries))
    house = select.today((tree, n, {}))
    if view["drawing"]["kind"] != "regularized-view" or house["drawing"]["kind"] != "witness":
        raise ValueError(f"n={n}: the view and the house drawing were not both measured")
    side = Fraction(str(view["side"]))
    house_side = None if house["side"] is None else Fraction(str(house["side"]))
    upper = drive.verified_bound(drive.case_facts(n))
    order = None if upper is None else upper.compare(side)
    gains, worse = improvement_rule.compare(view, house)
    against = _against(side, house_side)
    judgement = improvement_rule.judge(
        gains,
        worse,
        smaller=against == "smaller",
        larger=against == "larger",
        # Exactness is the gain of an exactly verified view over a numerically checked
        # witness, so a view an exact route refused gains none (review B2 of #591).
        exact_gain=not house["verified"] and _routes(entry),
    )
    if not _routes(entry):
        default, reason = HOUSE, ROUTE_REFUSED
    elif order is None:
        default, reason = HOUSE, UNKNOWN_U
    elif order > 0 and n not in ABOVE_U:
        default, reason = HOUSE, ABOVE_BOUND
    elif not judgement.improves:
        default, reason = HOUSE, judgement.reason
    else:
        default, reason = REGULARIZED, f"better on {', '.join(judgement.better)}"
    return {
        "n": n,
        "default": default,
        "reason": reason,
        "generator": entry.get("generator"),
        "view": entry["view"]["path"],
        "exact_routes": _routes(entry),
        "side": {
            "view_minus_U": None
            if upper is None or order is None
            else f"{upper.difference(side):.3e}",
            "named_above_U": n in ABOVE_U,
            "against_house": against,
        },
        "house_exact": bool(house["verified"]),
        "better": list(judgement.better),
        "worse": list(judgement.worse),
        "measures": {key: {"view": view[key], "house": house[key]} for key in MEASURES},
    }


def document(*, workers: int = 1, tree: Path = REPO, index: Path = INDEX) -> dict[str, Any]:
    """The record the data gives: every drawn view's count, decided."""
    entries = drawn_views(index)
    units = [(tree, n, entries) for n in sorted(entries, reverse=True)]
    if workers > 1 and len(units) > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            decided = list(pool.map(decide, units))
    else:
        decided = [decide(unit) for unit in units]
    rows = sorted(decided, key=lambda row: row["n"])
    drawn = sum(1 for row in rows if row["default"] == REGULARIZED)
    return {
        "softschema": {"contract": CONTRACT, "schema": SCHEMA, "status": "enforced"},
        "contract": CONTRACT,
        "generated_by": f"{GENERATOR} --update",
        "policy_document": improvement_rule.POLICY_DOCUMENT,
        "rule": improvement_rule.SECTION,
        "measured_by": (
            "devtools.regularize_select.today on the view and on the house witness, "
            "judged by devtools.improvement_rule.judge"
        ),
        "measures": list(MEASURES),
        "totals": {"views": len(rows), REGULARIZED: drawn, HOUSE: len(rows) - drawn},
        "entries": rows,
    }


def text(record: Mapping[str, Any]) -> str:
    return retained_json.dumps(record, ensure_ascii=False) + "\n"


@cache
def decisions(record: Path = RECORD, index: Path = INDEX) -> dict[int, dict[str, Any]]:
    """Every drawn view's decision, by count, from the retained record, refused where the
    record's counts, views or generators are not the index's: a stale record is refused
    rather than drawn from. Nothing is measured here; the records tier's check measures."""
    stale = f"{RECORD_PATH} is stale; run `{GENERATOR} --update`"
    found = json.loads(record.read_text(encoding="utf-8"))
    if found.get("contract") != CONTRACT:
        raise SystemExit(f"{RECORD_PATH} is not a {CONTRACT} record")
    drawn = drawn_views(index)
    rows = {int(row["n"]): row for row in found["entries"]}
    if sorted(rows) != sorted(drawn):
        raise SystemExit(f"{stale}: it decides other counts than the index draws")
    for n, row in rows.items():
        if row["view"] != drawn[n]["view"]["path"] or row["generator"] != drawn[n].get(
            "generator"
        ):
            raise SystemExit(f"{stale}: n={n} names another view than the index")
    return rows


@cache
def regularized_defaults(
    record: Path = RECORD, index: Path = INDEX
) -> dict[int, dict[str, Any]]:
    """The counts whose default picture is their regularized view (`decisions`)."""
    rows = decisions(record, index)
    return {n: row for n, row in rows.items() if row["default"] == REGULARIZED}


def held_note(n: int) -> str:
    """For a count whose regularized view the layer holds but does not draw by default,
    the sentence its case page adds to the regularization note: the view does not
    improve on the packing as published, so the page draws the house drawing. Empty for
    every other count. Written from the record's reason (review A4 of #591)."""
    row = decisions().get(n)
    if row is None or row["default"] != HOUSE:
        return ""
    why = (
        "it ties the house drawing on every goal of the improvement rule"
        if row["reason"] == "no gain"
        else str(row["reason"])
    )
    return (
        "The layer holds this regularized view, but it does not improve on the packing as "
        f"published ({why}), so this page draws the house drawing (regularization policy, "
        "section 12)."
    )


@cache
def _generators(index: Path = INDEX) -> dict[str, Any]:
    return dict(json.loads(index.read_text(encoding="utf-8")).get("generators") or {})


def credit_line(n: int) -> str:
    """The credit line a drawing of count `n`'s regularized default carries: the
    generator's, as the policy's section 7 gives it (`regularized_drawings.
    generator_credit`)."""
    from devtools.regularized_drawings import generator_credit  # noqa: PLC0415

    row = regularized_defaults()[n]
    return generator_credit(str(row["generator"]), _generators())


def problems(expected: Mapping[str, Any], record: Path = RECORD) -> tuple[list[str], list[str]]:
    """What fails the check, and what it lists without failing: the counts that keep
    the house picture and why."""
    found = list(improvement_rule.problems())
    by_n = {int(row["n"]): row for row in expected["entries"]}
    if not record.is_file():
        found.append(f"{RECORD_PATH} is missing")
    else:
        retained = json.loads(record.read_text(encoding="utf-8"))
        for row in retained.get("entries", []):
            n = int(row["n"])
            if row.get("default") == REGULARIZED and by_n.get(n, {}).get("default") != (
                REGULARIZED
            ):
                why = by_n[n]["reason"] if n in by_n else "the index draws no view"
                found.append(
                    f"n={n} is drawn regularized by default, and the rule says not: {why}"
                )
        if record.read_text(encoding="utf-8") != text(expected):
            found.append(f"{RECORD_PATH} is not what the data gives")
    kept = [
        f"n={row['n']} keeps the house picture: {row['reason']}"
        for row in expected["entries"]
        if row["default"] == HOUSE
    ]
    return found, kept


def _summary(record: Mapping[str, Any]) -> str:
    totals = record["totals"]
    return (
        f"{totals[REGULARIZED]} of {totals['views']} drawn views are their counts' default "
        f"pictures, each improving on its house drawing; {totals[HOUSE]} keep the house"
    )


def update(*, workers: int = 1) -> int:
    expected = document(workers=workers)
    content = text(expected)
    if not RECORD.is_file() or RECORD.read_text(encoding="utf-8") != content:
        with atomic_output_file(RECORD) as temporary:
            temporary.write_text(content, encoding="utf-8")
    decisions.cache_clear()
    regularized_defaults.cache_clear()
    print(f"default drawings updated: {_summary(expected)}")
    return 0


def check(*, workers: int = 1) -> int:
    expected = document(workers=workers)
    found, kept = problems(expected)
    for line in kept:
        print(line)
    if found:
        for problem in found:
            print(f"default drawings drift: {problem}")
        print(f"run `{GENERATOR} --update`, or say why the rule has changed")
        return 1
    print(f"rule ({improvement_rule.SECTION}): {improvement_rule.statement()}")
    print(f"default drawings check passed: {_summary(expected)}")
    return 0


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true", help="write the record")
    mode.add_argument("--check", action="store_true", help="measure again and compare")
    command.add_argument(
        "--workers",
        type=int,
        default=None,
        help="processes to measure with (default: the gate's PACK_JOBS cap, or every core)",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    workers = args.workers if args.workers is not None else worker_count(len(drawn_views()))
    if args.update:
        return update(workers=workers)
    return check(workers=workers)


if __name__ == "__main__":
    raise SystemExit(main())
