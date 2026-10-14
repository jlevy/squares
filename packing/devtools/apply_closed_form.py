#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes case-record prose, whose typography uses curly
# apostrophes.
"""Carry wand125's closed-form lower bound into the case records' reported lane.

Hiroaki Hosono's (wand125's) closed form (T-180, `[wand125 closed form 2026-10-14]`)
states `s(N) >= a(N)` for every non-square `N >= 49`. The packet's own exact evaluation
(`resources/web/wand125-closed-form-2026-10-14/evaluation/outputs/bounds.json`) gives
`a(n)` rounded down at 30 places at every count from 49 to 324 and compares it with each
bound the case records held when it ran. This tool writes the comparison's consequence:

- **The reported lane** at every count where `a(n)`, rounded down at 30 places, is above
  the case's reported lower bound, decided here exactly, and below its verified upper
  bound, except where a registered report that is still pending adoption is stronger
  (`STRONGER`): wand125's `563/50` at 122 to 126 (T-144) and `306/25` at 145 to 149
  (T-179), which by the per-count ledger's rule keep 125 and 148. The block takes `a(n)`
  rounded down at 12 places as its `value` and at 30 as its `exact_form`, both implied by
  the theorem, and cites `E-wand125-closed-form-report`. At the 33 counts `m^2 - j`,
  where `a(n)` meets the proved value, no record changes: T-064, T-084 and T-086 name the
  route, and the generator that drafts those records owns them.

Each written case also takes the closed form's resource, `source_reviewed` no earlier
than the intake, and one paragraph under its title, found again by its opening words, so
a second run rewrites nothing. A case whose reported lower bound is no longer the one
the evaluation compared with, and is not the closed form's, is refused rather than
overwritten, as is one whose verified upper bound is not above `a(n)`. The verified lane
is untouched until a replay.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.apply_closed_form --plan
    uv run --frozen --all-extras --group dev python -m devtools.apply_closed_form
    uv run --frozen --all-extras --group dev python -m devtools.apply_closed_form --check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import ROUND_FLOOR, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
PACKET = ROOT / "resources" / "web" / "wand125-closed-form-2026-10-14"
BOUNDS = PACKET / "evaluation" / "outputs" / "bounds.json"

SOURCE_KEY = "[wand125 closed form 2026-10-14]"
REPORT = "E-wand125-closed-form-report"
INTAKE = "2026-10-14"
RESOURCE = {
    "key": SOURCE_KEY,
    "role": "lower-bound-proof",
    "local": "web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form",
    "url": (
        "https://github.com/wand125/square-packing/tree/"
        "9a28a84bd55dc124bfa2919bb6c4fb504dda3149/problems/closed-form"
    ),
    "retrieved": True,
}
SCOPE = "Unrestricted unit-square packing with independent rotations and disjoint interiors."
#: Registered reports pending adoption that are stronger than `a(n)` somewhere: the
#: entry, its bound and the counts it reaches.
STRONGER: tuple[tuple[str, Fraction, range], ...] = (
    ("T-144", Fraction(563, 50), range(122, 127)),
    ("T-179", Fraction(306, 25), range(145, 150)),
)
#: How the paragraph opens; a second run finds its own paragraph by these words, or by
#: the opening it had before the source's credit was carried (review A4 of #602).
OPENING = "**Hiroaki Hosono’s closed form, 14 October 2026.**"
OPENINGS = (OPENING, "**wand125’s closed form, 14 October 2026.**")
#: How the source states its AI assistance (issue 600).
ASSISTANCE = (
    "The source states that its search, certificates, checkers and text were produced with "
    "AI assistance (Claude and Codex), under the direction of and reviewed by Hiroaki "
    "Hosono."
)
#: The dated paragraphs another writer keeps directly under the title, which this one
#: follows: `register_regularized_bounds` writes its own first on every application.
LEADS = ("**Exact regularized certificate,",)
#: The previous holder of the reported lane, as the paragraph names it.
HOLDERS = {
    "nagamochi": "Nagamochi’s closed form",
    "monotonicity": "a smaller count’s bound by monotonicity",
    "unavoidable-points": "the unavoidable-points bound",
    "counting": "a counting bound",
}


@dataclass(frozen=True, slots=True)
class Plan:
    """One count's raised reported lane: where `a(n)` comes from, and what it replaces."""

    n: int
    k: int
    interval: int
    a30: Decimal
    held: Mapping[str, Any]


def _a12(a30: Decimal) -> str:
    """`a(n)` rounded down at 12 places, as the case writes a value."""
    with localcontext(prec=80):
        return str(a30.quantize(Decimal("1e-12"), rounding=ROUND_FLOOR))


def _exact30(a30: Decimal) -> str:
    """`a(n)` rounded down at 30 places, as a fraction over `10^30`."""
    with localcontext(prec=80):
        places = a30.quantize(Decimal("1e-30"), rounding=ROUND_FLOOR)
        return f"{int(places.scaleb(30))}/1{'0' * 30}"


def raises(a30: Decimal, held: Mapping[str, Any]) -> bool:
    """`a(n)` rounded down at 30 places is above the bound held, exactly."""
    return Fraction(_exact30(a30)) > Fraction(Decimal(str(held["value"])))


def _upper(payload: Mapping[str, Any]) -> Fraction | None:
    """The case's verified upper bound, exactly where its exact form is a rational."""
    field: Mapping[str, Any] = payload.get("verified_upper_bound") or {}
    if not field:
        return None
    try:
        return Fraction(str(field.get("exact_form")).replace(" ", ""))
    except ValueError:
        return Fraction(Decimal(str(field["value"])))


def stronger(n: int, a30: Decimal) -> str | None:
    for entry, bound, counts in STRONGER:
        if n in counts and Fraction(a30) < bound:
            return entry
    return None


def _ours(field: Mapping[str, Any] | None) -> bool:
    return bool(field) and REPORT in (field.get("evidence") or [])


def plans(frontier: Path = FRONTIER) -> list[Plan]:
    """Every count whose reported lane the closed form raises.

    The evaluation gives `a(n)` and the bound each case held when it ran; whether `a(n)` is
    above that bound is decided here, exactly, not read from the evaluation's relation.
    """
    rows = json.loads(BOUNDS.read_text(encoding="utf-8"))["rows"]
    found: list[Plan] = []
    for row in rows:
        n = int(row["n"])
        held = row.get("reported_lower_bound") or {}
        if not held or not (frontier / f"n-{n:03d}.md").exists():
            continue
        a30 = Decimal(row["a_floor_30"])
        if not raises(a30, held) or stronger(n, a30) is not None:
            continue
        found.append(Plan(n, int(row["k"]), int(row["interval"]), a30, held))
    return found


def reported_field(plan: Plan) -> dict[str, Any]:
    return {
        "value": _a12(plan.a30),
        "exact_form": _exact30(plan.a30),
        "kind": "counting",
        "proved_by": ["wand125"],
        "proved_year": 2026,
        "source_key": SOURCE_KEY,
        "note": (
            "Hiroaki Hosono's closed form (wand125, 13 October 2026, T-180): s(N) >= a(N) for "
            "every non-square N >= 49, from a measure of line segments on 34 intervals of the "
            f"fractional part. At n = {plan.n}, k = {plan.k} and interval {plan.interval} "
            f"give a({plan.n}) = {plan.a30}..., here rounded down at 12 and 30 places. The "
            "source replayed its certificate with its own checker; no replay has run here."
        ),
        "scope": SCOPE,
        "evidence": [REPORT],
    }


def paragraph(plan: Plan) -> str:
    held = plan.held
    holder = HOLDERS.get(str(held.get("kind")), "the earlier report")
    what = (
        f"At $n = {plan.n}$, $k = {plan.k}$ and interval {plan.interval} give "
        f"$a({plan.n}) = {plan.a30}\\ldots$, so the reported lower bound here is now "
        f"$s({plan.n}) \\ge {_a12(plan.a30)}$, rounded down, above {holder}, "
        f"${held.get('value')}$. The source replayed its certificate with its own "
        "checker; no record of it has been replayed here, so the verified lower bound "
        "is unchanged."
    )
    return (
        f"{OPENING} Hiroaki Hosono’s closed form (wand125, 13 October 2026, T-180) "
        "states $s(N) \\ge a(N)$ for every non-square $N \\ge 49$, from a measure of line "
        f"segments on 34 intervals of the fractional part. {what} {ASSISTANCE}"
    )


#: The line width the case records' writers dump their front matter at
#: (`register_refinement_reports.dump`), so that a writer that re-renders a record this
#: tool wrote leaves its block as it is.
WIDTH = 96


def _block(name: str, value: Mapping[str, Any]) -> str:
    """The block as a whole front matter's dump writes it, under `packing:`."""
    dumped = yaml.safe_dump(
        {"packing": {name: dict(value)}}, allow_unicode=True, sort_keys=False, width=WIDTH
    )
    return "".join(line + "\n" for line in dumped.splitlines()[1:])


def _replace_block(front: str, name: str, block: str) -> str:
    pattern = re.compile(rf"^  {name}:\n(?:^    .*\n)*", re.MULTILINE)
    if not pattern.search(front):
        raise ValueError(f"no {name} block")
    return pattern.sub(lambda _match: block, front, count=1)


def _append_list(front: str, name: str, items: Sequence[str]) -> str:
    """Append raw items to the end of a top-level `packing` list."""
    match = re.search(rf"^  {name}:\n((?:^  - .*\n(?:^    .*\n)*)*)", front, re.MULTILINE)
    if not match:
        raise ValueError(f"no {name} list")
    return front[: match.end(1)] + "".join(items) + front[match.end(1) :]


def apply_case(plan: Plan, frontier: Path = FRONTIER) -> str:
    """The case record with this plan written into it."""
    return apply_text(plan, (frontier / f"n-{plan.n:03d}.md").read_text(encoding="utf-8"))


def replay(n: int, text: str) -> str:
    """A record as this tool leaves it, for a writer's replay that runs before it: the
    record unchanged where the closed form has no plan at `n`."""
    plan = next((plan for plan in plans() if plan.n == n), None)
    return text if plan is None else apply_text(plan, text)


def carried(text: str) -> bool:
    """Whether a record's text already carries the closed form's reported lane."""
    payload: Mapping[str, Any] = safe_load(text.split("---\n", 2)[1])["packing"]
    return _ours(payload.get("reported_lower_bound"))


def apply_text(plan: Plan, text: str) -> str:
    """The record `text` with this plan written into it."""
    _, front, body = text.split("---\n", 2)
    payload: dict[str, Any] = safe_load(front)["packing"]
    current: Mapping[str, Any] = payload.get("reported_lower_bound") or {}
    if not _ours(current):
        if str(current.get("value")) != str(plan.held["value"]):
            raise ValueError(
                f"n = {plan.n}: the reported lower bound is {current.get('value')!r}, "
                f"not the {plan.held['value']!r} the evaluation compared with"
            )
        if not raises(plan.a30, current):
            raise ValueError(
                f"n = {plan.n}: a(n) rounded down is not above the reported lower bound "
                f"{current.get('value')!r}"
            )
    upper = _upper(payload)
    if upper is not None and Fraction(plan.a30) >= upper:
        raise ValueError(f"n = {plan.n}: a(n) is not below the verified upper bound")
    front = _replace_block(
        front, "reported_lower_bound", _block("reported_lower_bound", reported_field(plan))
    )
    if REPORT not in (payload.get("evidence") or []):
        front = _append_list(front, "evidence", [f"  - {REPORT}\n"])
    keys = {resource.get("key") for resource in payload.get("resources") or []}
    if SOURCE_KEY not in keys:
        dumped = yaml.safe_dump(
            {"packing": {"resources": [RESOURCE]}},
            allow_unicode=True,
            sort_keys=False,
            width=WIDTH,
        )
        front = _append_list(
            front, "resources", ["".join(line + "\n" for line in dumped.splitlines()[2:])]
        )
    reviewed = max(str(payload.get("source_reviewed") or ""), INTAKE)
    front = re.sub(
        r"^  source_reviewed: .*$",
        f"  source_reviewed: '{reviewed}'",
        front,
        count=1,
        flags=re.MULTILINE,
    )
    title, _, rest = body.partition("\n\n")
    parts = rest.split("\n\n")
    mine = [index for index, part in enumerate(parts) if part.startswith(OPENINGS)]
    if len(mine) > 1:
        raise ValueError(f"n = {plan.n} holds {len(mine)} closed-form paragraphs")
    written = paragraph(plan)
    # The Markdown formatter rewraps the paragraph; the same words are the same paragraph.
    if mine and " ".join(parts[mine[0]].split()) == written:
        written = parts[mine[0]]
    else:
        written = _formatted(written)
    # The prose the generator writes for the lane this replaces (Green's DS7 value at 173,
    # 261 and 294) describes a bound the lane no longer holds; the generator drops it with
    # the lane, so the record does too (review C2 of #602).
    replaced = f"The reported lower-bound expression for $s({plan.n})$ is"
    parts = [
        part
        for index, part in enumerate(parts)
        if index not in mine and not part.startswith(replaced)
    ]
    place = 0
    while place < len(parts) and parts[place].startswith(LEADS):
        place += 1
    parts.insert(place, written)
    return f"---\n{front}---\n{title}\n\n" + "\n\n".join(parts)


def _formatted(text: str) -> str:
    """A new paragraph wrapped as the register's Markdown formatter wraps it, in process,
    as `generate_frontier_case` formats a record, so a generated record carries it as the
    committed one does (review C2 of #602)."""
    from flowmark import reformat_text  # noqa: PLC0415

    return reformat_text(text, semantic=True, cleanups=True, smartquotes=True).rstrip("\n")


def stale(frontier: Path = FRONTIER) -> list[str]:
    """The counts whose record differs from what this tool writes."""
    return [
        f"n = {plan.n}"
        for plan in plans(frontier)
        if apply_case(plan, frontier)
        != (frontier / f"n-{plan.n:03d}.md").read_text(encoding="utf-8")
    ]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--plan", action="store_true", help="print the per-count plan")
    mode.add_argument("--check", action="store_true", help="fail if a record is not written")
    parser.add_argument("--frontier", type=Path, default=FRONTIER)
    args = parser.parse_args(argv)
    found = plans(args.frontier)
    if args.plan:
        for plan in found:
            print(f"{plan.n}\t{_a12(plan.a30)}\t{plan.held.get('value')}")
        print(f"{len(found)} reported lanes raised")
        return 0
    if args.check:
        problems = stale(args.frontier)
        for problem in problems:
            print(f"not written: {problem}", file=sys.stderr)
        return 1 if problems else 0
    for plan in found:
        path = args.frontier / f"n-{plan.n:03d}.md"
        text = apply_case(plan, args.frontier)
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8")
    print(f"wrote {len(found)} case records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
