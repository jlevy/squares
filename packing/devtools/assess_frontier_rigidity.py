#!/usr/bin/env python3
"""Record this repository's own finding on rigidity, for every n it can settle.

`rigidity: null` means "not assessed", and it sat on 99 of 100 records while the
material to settle 94 of them was already generated and committed. Two sound
arguments are available and neither needs a source:

  A hit in the translation escape screen exhibits a square, a direction and a
  distance, so the configuration admits a non-trivial feasible motion. That is a
  certificate of NOT rigid, and it is the strong direction of that screen -- a
  miss is weak and is never read as rigidity here.

  n a perfect square whose side is *verified* to be exactly k means k*k unit
  squares exactly tile a k by k container. Total area equals container area, so
  no square has slack and no motion of any kind is feasible. That is rigid, and
  it is elementary -- but it rests on the side, not on n. The first draft of this
  tool inferred the tiling from `math.isqrt(n)` alone and never opened the record
  it wrote into, which would have stamped `verified` rigidity on a perfect-square
  record whose retained side had regressed above k. The claims were true; nothing
  checked them. The tiling branch now reads the record's own verified bounds and
  refuses when they do not pin the side at exactly k.

What the screen cannot do is establish rigidity, because rotation and
coordinated multi-square motion are outside it. So the packings the catalogue
annotates "Rigid." are left `undetermined` here rather than promoted: the
catalogue's word for them lives in reported_upper_bound.catalogue_rigid, and
restating it as a first-party finding is exactly the conflation the split fixed.

Two records carry a first-party argument and this tool never overwrites either:
n=11 from the tangent-cone work, and n=5 from `X-007` and its successor `X-012`,
which settle the first-order cone exactly, refuse its one free direction at
second order, and then close local isolation by curve selection and an order-2m
coefficient induction. n=5 read `undetermined` while only the second-order half
existed -- second-order rigidity is not local rigidity -- and reads
`locally-rigid` since 2026-09-03, when that closing was independently reviewed
and registered as T-014. Either way this tool leaves it alone: leaving a record
alone is about who owns the argument, not about which verdict it reached.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

import yaml
from strif import atomic_output_file

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
SCREEN = ROOT / "atlas/known-best/translation-escape-screen.json"
GENERATOR = "python -m devtools.assess_frontier_rigidity"


class RigidityAssessmentError(ValueError):
    """The corpus did not support a claim this tool was about to write."""


ESCAPE_EVIDENCE = "E-translation-escape-not-rigid"
TILING_EVIDENCE = "E-perfect-square-tiling-rigid"
# Blocks this tool owns. A rigidity block resting on any other evidence was
# written by a stronger argument than this one and is never overwritten.
OWNED_EVIDENCE = {ESCAPE_EVIDENCE, TILING_EVIDENCE}

SCREEN_REPLAY = (
    "uv run --frozen --all-extras --group dev python -m "
    "devtools.screen_translation_escape --check"
)


def screen_cases() -> tuple[dict[int, dict], list[int]]:
    screen = json.loads(SCREEN.read_text(encoding="utf-8"))["screen"]
    return (
        {case["n"]: case for case in screen["cases"]},
        [item["n"] for item in screen["excluded"]],
    )


def _decimals(value: str, places: int = 6) -> str:
    text = f"{float(value):.{places}f}".rstrip("0").rstrip(".")
    return text or "0"


def _exact_side(record: dict, field: str) -> Decimal | None:
    """The record's bound as an exact decimal, or None when it is absent."""
    bound = record.get(field)
    if not isinstance(bound, dict):
        return None
    value = bound.get("value")
    if not isinstance(value, str):
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def rigidity_for(
    n: int, cases: dict[int, dict], excluded: list[int], record: dict
) -> dict | None:
    """The block this tool would write for `n`, or None to leave the record alone."""
    root = math.isqrt(n)
    if root * root == n:
        # The tiling argument rests on the side being exactly k, which is a property of
        # this record and not of n. Read it rather than assume it.
        upper = _exact_side(record, "verified_upper_bound")
        lower = _exact_side(record, "verified_lower_bound")
        if upper != Decimal(root) or lower != Decimal(root):
            raise RigidityAssessmentError(
                f"n={n} is a perfect square but its verified bounds do not pin the side "
                f"at exactly {root} (upper={upper}, lower={lower}), so the tiling "
                "argument does not apply and no rigidity claim is written"
            )
        return {
            "property": "locally-rigid",
            "assurance": "verified",
            "method": "exact-algebraic",
            "scope": (
                f"This record's side is verified above and below at exactly {root}, so its "
                f"{n} unit square{'' if n == 1 else 's'} of total area {n} "
                f"{'sits' if n == 1 else 'sit'} in a {root} by {root} container "
                f"of area {n}. The packing is a tiling with no slack anywhere, so no "
                f"square admits any feasible motion. This is global rather than local, "
                f"and holds for the exact configuration rather than for a materialized "
                f"approximation of it. It says nothing about s(n) beyond what the tiling "
                f"itself shows."
            ),
            "certificate": None,
            "replay": None,
            "evidence": [TILING_EVIDENCE],
        }

    if n in excluded:
        return {
            "property": "undetermined",
            "assurance": "numerically-checked",
            "method": "numerical-multiprecision",
            "scope": (
                "Assessed and not settled. The translation escape screen excludes this "
                "record because the retained witness's own squares are not unit squares "
                "to the residual the screen requires, so no contact claim it would make "
                "is trustworthy. This is a statement about the witness, not about the "
                "packing."
            ),
            "certificate": str(SCREEN.relative_to(ROOT)),
            "replay": SCREEN_REPLAY,
            "evidence": [ESCAPE_EVIDENCE],
        }

    case = cases[n]
    if case["movable_square_count"] == 0:
        return {
            "property": "undetermined",
            "assurance": "numerically-checked",
            "method": "numerical-multiprecision",
            "scope": (
                "Assessed and not settled. No square of the retained witness can be "
                "translated at any tolerance screened, which is consistent with rigidity "
                "but does not establish it: rotation and coordinated multi-square motion "
                "are outside the screen. What a source says about this packing's "
                "rigidity is carried by reported_upper_bound.catalogue_rigid and is "
                "deliberately not restated here as a finding of ours."
            ),
            "certificate": str(SCREEN.relative_to(ROOT)),
            "replay": SCREEN_REPLAY,
            "evidence": [ESCAPE_EVIDENCE],
        }

    first = case["movable_squares"][0]
    distance = _decimals(first["slide_distance"])
    return {
        "property": "not-rigid",
        "assurance": "numerically-checked",
        "method": "numerical-multiprecision",
        "scope": (
            f"Square {first['square_index']} of the retained witness "
            f"(witness id {first['witness_square_id']}) translates {distance} along "
            f"({_decimals(first['direction']['x'])}, {_decimals(first['direction']['y'])}) "
            f"with the packing still valid, so the configuration admits a non-trivial "
            f"feasible motion; {case['movable_square_count']} of its {case['square_count']} "
            f"squares do. Every constraint is exactly affine in the slide parameter, so "
            f"the arithmetic carries no linearization error, but the coordinates are the "
            f"witness's own finite-precision transcription: this settles the retained "
            f"configuration, not the true optimum. Rigidity and optimality are "
            f"independent, and this bears only on the former."
        ),
        "certificate": str(SCREEN.relative_to(ROOT)),
        "replay": SCREEN_REPLAY,
        "evidence": [ESCAPE_EVIDENCE],
    }


def _render(block: dict) -> str:
    """The block as frontmatter lines, at the indentation `packing.rigidity` sits at."""
    body = yaml.safe_dump(
        {key: value for key, value in block.items() if value is not None},
        sort_keys=False,
        width=96,
        allow_unicode=True,
        default_flow_style=False,
    )
    lines = ["  rigidity:"]
    lines += [f"    {line}" if line.strip() else line for line in body.rstrip("\n").split("\n")]
    return "\n".join(lines) + "\n"


def _record(text: str) -> dict:
    """The record's parsed `packing` frontmatter."""
    return safe_load(text.split("---", 2)[1])["packing"]


def _existing_evidence(record: dict) -> set[str] | None:
    """Evidence ids on the record's current rigidity block, or None if it is null."""
    current = record.get("rigidity")
    return None if current is None else set(current.get("evidence", []))


def plan() -> list[tuple[int, Path, str, str]]:
    """(n, path, current text, desired text) for every record this tool would touch."""
    cases, excluded = screen_cases()
    entries: list[tuple[int, Path, str, str]] = []
    for n in range(1, 101):
        path = FRONTIER / f"n-{n:03d}.md"
        text = path.read_text(encoding="utf-8")
        record = _record(text)
        held = _existing_evidence(record)
        if held is not None and not held <= OWNED_EVIDENCE:
            continue  # A stronger argument owns this record.
        block = rigidity_for(n, cases, excluded, record)
        if block is None:
            continue
        if held is None:
            marker = "  rigidity: null\n"
            if marker not in text:
                raise ValueError(f"n={n}: expected `rigidity: null` and did not find it")
            desired = text.replace(marker, _render(block), 1)
        else:
            desired = _replace_block(text, _render(block), n)
        entries.append((n, path, text, desired))
    return entries


def _replace_block(text: str, rendered: str, n: int) -> str:
    """Swap an existing block this tool owns for the freshly derived one."""
    start = text.find("  rigidity:\n")
    if start < 0:
        raise ValueError(f"n={n}: expected an existing rigidity block and did not find it")
    rest = text[start + len("  rigidity:\n") :]
    consumed = 0
    for line in rest.split("\n"):
        if line.strip() and not line.startswith("    "):
            break
        consumed += len(line) + 1
    return text[:start] + rendered + rest[consumed:]


def update() -> None:
    changed = 0
    for _n, path, text, desired in plan():
        if text == desired:
            continue
        with atomic_output_file(path) as temporary:
            temporary.write_text(desired, encoding="utf-8")
        changed += 1
    print(f"frontier rigidity assessed: {changed} record(s) rewritten")


def check() -> None:
    stale = [n for n, _p, text, desired in plan() if text != desired]
    if stale:
        raise ValueError(f"stale rigidity blocks for n = {stale}; re-run with --update")
    print("frontier rigidity check passed: every block matches the derivation")


def review() -> None:
    cases, excluded = screen_cases()
    buckets: dict[str, list[int]] = {}
    skipped: list[int] = []
    for n in range(1, 101):
        text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
        record = _record(text)
        held = _existing_evidence(record)
        if held is not None and not held <= OWNED_EVIDENCE:
            skipped.append(n)
            continue
        block = rigidity_for(n, cases, excluded, record)
        assert block is not None
        buckets.setdefault(block["property"], []).append(n)
    summary = ", ".join(f"{len(values)} {name}" for name, values in sorted(buckets.items()))
    print(f"assessed: {summary}, {len(skipped)} left to a stronger argument")
    for name, values in sorted(buckets.items()):
        print(f"  {name:16s} {len(values):3d}")
        if len(values) <= 16:
            print(f"    n = {values}")
    print(f"  left to a stronger argument: n = {skipped}")
    print(f"  screen excluded: n = {excluded}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="write the blocks")
    group.add_argument("--check", action="store_true", help="fail if any block is stale")
    group.add_argument("--review", action="store_true", help="report what would be written")
    arguments = parser.parse_args(argv)
    try:
        if arguments.update:
            update()
        elif arguments.check:
            check()
        else:
            review()
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
