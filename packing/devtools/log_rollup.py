#!/usr/bin/env python3
"""Write an efficiency rollup for one coding-agent session log.

The harness is detected from the log's content, so the same command serves every reader
in `devtools.logrollup.REGISTRY`.

The rollup is the retained artifact rather than a pointer to one: the raw JSONL is large,
harness-private, and full of prose this repository has no reason to keep, so it will not
always be archived. Everything a reader emits excludes prose by construction, and each
record states what it dropped.

Usage:
    uv run --frozen python -m devtools.log_rollup LOG.jsonl
    uv run --frozen python -m devtools.log_rollup LOG.jsonl --out campaign/resource-usage
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from devtools.logrollup import REGISTRY


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", type=Path, nargs="+", help="agent session logs")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="directory to write <log-stem>.yaml into; default prints to stdout",
    )
    namespace = parser.parse_args(argv)
    failed = 0
    for log in namespace.logs:
        failed += _one(log, namespace.out)
    return 1 if failed else 0


def _one(log: Path, out: Path | None) -> int:
    """Roll up one log, returning 1 on failure so a batch can carry on."""
    if not log.is_file():
        print(f"  no such log: {log}", file=sys.stderr)
        return 1
    try:
        reader = REGISTRY.for_path(log)
    except LookupError as error:
        print(f"  {error}", file=sys.stderr)
        return 1

    rollup = reader.read(log)
    text = yaml.safe_dump(rollup.payload(), sort_keys=False, allow_unicode=True, width=88)
    if out is None:
        print(text)
        return 0

    out.mkdir(parents=True, exist_ok=True)
    # Named by the log's own stem, never by `session_id`. A subagent transcript carries
    # its parent's session id, so keying on that silently overwrote the parent's record
    # with the last subagent's.
    destination = out / f"{log.stem}.yaml"
    destination.write_text(text, encoding="utf-8")
    calls = rollup.extra.get("tool_calls", {})
    turns = rollup.extra.get("turns", {})
    print(
        f"  {destination.name}: {rollup.source.records} records, "
        f"{turns.get('assistant', 0)} turns, {calls.get('total', 0)} tool calls, "
        f"{rollup.span.hours:.2f} h"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
