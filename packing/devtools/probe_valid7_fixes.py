#!/usr/bin/env python3
"""Run the 2 October review's D-1, D-2 and D-3 demonstrations against each retained valid7 tree.

The method review of Hosono's independent Valid7 checker
(``docs/project/reviews/review-2026-10-02-valid7-independent-checker.md``, section 10)
found that ``tier_b2.nonneg_open`` accepts a polynomial that vanishes at its one sample
point (D-1), that the unused ``rf.nonneg_on`` misses negativity next to a root at an end
(D-2), and that ``tier_b2`` de-duplicates lines and caches masses by Python's 64-bit
``hash`` (D-3). The author's commit ``da469ec`` says it fixes all three. This tool asks
the code itself, at each retained revision:

- D-1: ``nonneg_open`` on ``-(u - 1/2)^2`` over ``(0, 1)``, which is negative at ``1/4``;
- D-2: ``nonneg_on`` on ``u (u - 1)`` over ``[0, 2]`` (the review's example) and on
  ``-u^2 (u - 1)^2`` over ``[0, 1]`` (the author's), both negative at ``1/2``;
- positive controls, which each version must still accept: ``(u - 1/2)^2`` over
  ``(0, 1)`` and ``u (2 - u)`` over ``[0, 2]``;
- D-3: whether ``tier_b2.py`` still calls ``hash(``, read from the source text.

The checker needs python-flint, which this project's environment does not carry, so the
demonstrations run in the interpreter the replay used (``--python``), on this file with
``--probe TREE``; that mode imports only the standard library and the tree's ``src/``.
The driver writes the receipt from both trees' answers. Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.probe_valid7_fixes \\
        --python VENV/bin/python
    uv run --frozen --all-extras --group dev python -m devtools.probe_valid7_fixes --check
"""

from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "resources/web"
#: The two retained revisions: the one the 2 October review read, and the author's fix.
TREES = {
    "38dd31b369991b0d96c917a4af0c7139b44a038d": WEB
    / "wand125-valid7-independent-check-2026-10-02/valid7-independent-check",
    "da469ecff5da0c71882e894b65d680ce57a0c87e": WEB
    / "wand125-valid7-independent-check-2026-10-03/valid7-independent-check",
}
RECEIPT = WEB / "wand125-valid7-independent-check-2026-10-03/receipts/valid7_fix_probe.json"
#: What each demonstration must answer at each revision: before the fix, then after it.
EXPECTED = {
    "d1_nonneg_open_neg_square_at_sample": (True, False),
    "d2_nonneg_on_review_example": (True, False),
    "d2_nonneg_on_author_example": (True, False),
    "control_nonneg_open_square": (True, True),
    "control_nonneg_on_cap": (True, True),
    "d3_tier_b2_calls_hash": (True, False),
}


def probe(tree: Path) -> dict[str, Any]:
    """Each demonstration's answer from the code under ``tree/src``; needs python-flint."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(tree / "src"))
    rf: Any = importlib.import_module("rf")
    tier_b: Any = importlib.import_module("tier_b")
    tier_b2: Any = importlib.import_module("tier_b2")
    poly, q, alg = rf.P, rf.Q, tier_b.Alg
    half = q(1, 2)
    u = poly([0, 1])
    zero, one, two = alg.rat(q(0)), alg.rat(q(1)), q(2)
    source = (tree / "src/tier_b2.py").read_text(encoding="utf-8")
    return {
        "d1_nonneg_open_neg_square_at_sample": bool(
            tier_b2.nonneg_open(-((u - half) ** 2), zero, one)
        ),
        "d2_nonneg_on_review_example": bool(rf.nonneg_on(u * (u - 1), q(0), two)),
        "d2_nonneg_on_author_example": bool(rf.nonneg_on(-(u**2) * (u - 1) ** 2, q(0), q(1))),
        "control_nonneg_open_square": bool(tier_b2.nonneg_open((u - half) ** 2, zero, one)),
        "control_nonneg_on_cap": bool(rf.nonneg_on(u * (two - u), q(0), two)),
        "d3_tier_b2_calls_hash": "hash(" in source,
    }


def run(python: str) -> dict[str, Any]:
    answers = {}
    for revision, tree in TREES.items():
        completed = subprocess.run(
            # -B: the retained trees must not gain a __pycache__ directory.
            [python, "-B", str(Path(__file__).resolve()), "--probe", str(tree)],
            check=True,
            capture_output=True,
            text=True,
        )
        answers[revision] = json.loads(completed.stdout)
    version = subprocess.run(
        [python, "-c", "import sys, flint; print(sys.version.split()[0], flint.__version__)"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split()
    return {
        "tool": "python -m devtools.probe_valid7_fixes",
        "interpreter": {"python": version[0], "python_flint": version[1]},
        "review": "docs/project/reviews/review-2026-10-02-valid7-independent-checker.md",
        "trees": {
            revision: tree.relative_to(ROOT).as_posix() for revision, tree in TREES.items()
        },
        "answers": answers,
    }


def problems(receipt: dict[str, Any]) -> list[str]:
    """Where a receipt's answers differ from what the fix should have changed."""
    found = []
    before, after = (receipt["answers"][revision] for revision in TREES)
    for name, (old, new) in EXPECTED.items():
        if before.get(name) != old:
            found.append(f"{name}: {before.get(name)} before the fix, expected {old}")
        if after.get(name) != new:
            found.append(f"{name}: {after.get(name)} after the fix, expected {new}")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--python", help="an interpreter with python-flint 0.9.0")
    group.add_argument("--probe", type=Path, help=argparse.SUPPRESS)
    group.add_argument("--check", action="store_true", help="check the retained receipt")
    args = parser.parse_args(argv)
    if args.probe is not None:
        print(json.dumps(probe(args.probe)))
        return 0
    if args.check:
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    else:
        receipt = run(args.python)
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    found = problems(receipt)
    for problem in found:
        print(f"FAIL {problem}", file=sys.stderr)
    if not found:
        print("valid7 fixes: D-1, D-2 and D-3 present at 38dd31b and gone at da469ec")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
