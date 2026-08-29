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
    parser.add_argument("log", type=Path, help="an agent session log")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="directory to write <session-id>.yaml into; default prints to stdout",
    )
    namespace = parser.parse_args(argv)
    if not namespace.log.is_file():
        print(f"  no such log: {namespace.log}", file=sys.stderr)
        return 1

    try:
        reader = REGISTRY.for_path(namespace.log)
    except LookupError as error:
        print(f"  {error}", file=sys.stderr)
        return 1

    rollup = reader.read(namespace.log)
    text = yaml.safe_dump(rollup.payload(), sort_keys=False, allow_unicode=True, width=88)
    if namespace.out is None:
        print(text)
        return 0

    namespace.out.mkdir(parents=True, exist_ok=True)
    name = rollup.source.session_id or namespace.log.stem
    destination = namespace.out / f"{name}.yaml"
    destination.write_text(text, encoding="utf-8")
    calls = rollup.extra.get("tool_calls", {})
    turns = rollup.extra.get("turns", {})
    print(f"  wrote {destination} ({reader.harness})")
    print(
        f"  {rollup.source.records} records, {turns.get('assistant', 0)} turns, "
        f"{calls.get('total', 0)} tool calls, {rollup.span.hours:.2f} h wall"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
