#!/usr/bin/env python3
"""Write AGENTS.md's operating-rule summary from operating-rules.md.

`AGENTS.md` is the only file guaranteed to be in an agent's context before its first tool
call, so it carries a one-line summary of every operating rule. `operating-rules.md`
carries the rules themselves, with the evidence for each. Two hand-maintained copies of a
rule is exactly the arrangement that drifts, and the drift is silent: the summary an agent
reads keeps saying the old thing while the page nobody opened mid-session says the new one.

So the summary is generated rather than maintained. Add a rule to `operating-rules.md`,
run this, and the block between the markers in `AGENTS.md` is rewritten from the headings.
`--check` reports drift without writing, which is what the gate runs.

The block is compared on collapsed whitespace rather than bytes, because `AGENTS.md` is
ordinary prose that the Markdown formatter owns. A byte-exact generated block inside a
formatted file would fight flowmark forever -- the failure mode `.flowmarkignore` documents
for `ledger.md` and `defects.md`, which is why those files left the formatter entirely and
this one does not have to.

Usage:
    uv run --frozen python -m devtools.render_operating_rules
    uv run --frozen python -m devtools.render_operating_rules --check
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from collections.abc import Sequence

PACKING = pathlib.Path(__file__).resolve().parent.parent
REPO = PACKING.parent
RULES = REPO / "operating-rules.md"
AGENTS = REPO / "AGENTS.md"

BEGIN = "<!-- BEGIN OPERATING RULES SUMMARY -->"
END = "<!-- END OPERATING RULES SUMMARY -->"

# The id is the field; the punctuation after it, and the heading depth, are typography.
# Both patterns treat the separator as optional and the depth as a range, so an editorial
# pass over either file cannot break the parse. A delimiter that is also a display choice
# is a delimiter that will eventually move.
HEADING = re.compile(r"^#{2,3} (OR-\d+):?\s+(.+?)\s*$", re.MULTILINE)
BULLET = re.compile(r"^- \*\*(OR-\d+):?\*\*:?\s+(.+?)(?=\n- |\n*\Z)", re.MULTILINE | re.DOTALL)


def _statement(text: str) -> str:
    """One rule statement, insensitive to wrapping and to a closing period."""
    return " ".join(text.split()).rstrip(".")


def source_rules() -> list[tuple[str, str]]:
    """The rules as `operating-rules.md` declares them, in file order."""
    rules = [
        (rule_id, _statement(statement))
        for rule_id, statement in HEADING.findall(RULES.read_text(encoding="utf-8"))
    ]
    if not rules:
        raise ValueError(f"{RULES.name}: no `### OR-N` rule headings found")
    expected = [f"OR-{index}" for index in range(1, len(rules) + 1)]
    if [rule_id for rule_id, _ in rules] != expected:
        found = ", ".join(rule_id for rule_id, _ in rules)
        raise ValueError(f"{RULES.name}: rule ids are not contiguous from OR-1: {found}")
    return rules


def summary_rules(text: str) -> list[tuple[str, str]]:
    """Whatever the marked block in `AGENTS.md` currently claims."""
    if BEGIN not in text or END not in text:
        raise ValueError(f"AGENTS.md is missing the {BEGIN} / {END} markers")
    block = text.split(BEGIN, 1)[1].split(END, 1)[0]
    return [(rule_id, _statement(statement)) for rule_id, statement in BULLET.findall(block)]


def render(rules: list[tuple[str, str]]) -> str:
    """The block body, unwrapped; flowmark owns the line breaks once it lands."""
    return "\n".join(f"- **{rule_id}:** {statement}." for rule_id, statement in rules)


def apply(*, check: bool) -> int:
    rules = source_rules()
    text = AGENTS.read_text(encoding="utf-8")
    if summary_rules(text) == rules:
        print(f"  AGENTS.md mirrors all {len(rules)} rules in {RULES.name}")
        return 0
    if check:
        print(f"  AGENTS.md's summary has drifted from {RULES.name}", file=sys.stderr)
        print(
            "  run: uv run --frozen python -m devtools.render_operating_rules",
            file=sys.stderr,
        )
        return 1
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    AGENTS.write_text(f"{head}{BEGIN}\n{render(rules)}\n{END}{tail}", encoding="utf-8")
    print(f"  AGENTS.md: rewrote the summary from {RULES.name} ({len(rules)} rules)")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="report drift without writing AGENTS.md"
    )
    namespace = parser.parse_args(argv)
    try:
        return apply(check=namespace.check)
    except ValueError as error:
        print(f"  {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
