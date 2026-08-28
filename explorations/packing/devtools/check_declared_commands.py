#!/usr/bin/env python3
"""Reject a session phase whose declared validation command could never run.

A phase's `validation_command` is its declared falsifier. Nothing checked that the
command exists, so on 2026-08-27 two phases carried
`packing-validate --list-steps` -- a flag that exits 2, because the flag is `--list`.
That contract was never executable, and it was only found when a later session tried
to run it. See think-ldy8.

This parses the arguments of every declared `packing-validate` and `packing-ledger`
invocation against those tools' own argument parsers. It deliberately does not run
anything: the question is whether the command is well formed, not whether it passes.
Commands naming other tools are left alone, because their parsers are not ours to
import and a guard that guesses is worse than none.
"""

# Importing each CLI's own `_parser` is the point: a guard that reimplemented the flag
# set would drift from the tools it checks, which is the failure it exists to prevent.
# `tests/test_validation_cli.py` takes the same exemption for the same reason.
# pyright: reportPrivateUsage=false
from __future__ import annotations

import argparse
import contextlib
import io
import shlex
import sys
from pathlib import Path

import yaml

from sqpack.campaign.ledger import _parser as _ledger_parser
from sqpack.cli.validate import UsageError
from sqpack.cli.validate import _parser as _validate_parser

ROOT = Path(__file__).resolve().parents[1]
SESSIONS = ROOT / "campaign" / "agent-sessions"
# Shell operators that end one invocation's argument list.
SEPARATORS = {"&&", "||", "|", ";"}


def _parsers() -> dict[str, argparse.ArgumentParser]:
    """The real parsers, so this guard cannot drift from the CLIs it checks."""
    return {"packing-validate": _validate_parser(), "packing-ledger": _ledger_parser()}


def _invocations(command: str, tools: set[str]) -> list[tuple[str, list[str]]]:
    """Every (tool, args) pair in one command line, split on shell operators."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        # An unbalanced quote is a shell problem, not a flag problem; leave it.
        return []
    found: list[tuple[str, list[str]]] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in tools:
            args: list[str] = []
            index += 1
            while index < len(tokens) and tokens[index] not in SEPARATORS:
                args.append(tokens[index])
                index += 1
            found.append((token, args))
        else:
            index += 1
    return found


def _declared_commands() -> list[tuple[str, int, str]]:
    """Every (session, phase number, command) declared across the session records."""
    declared: list[tuple[str, int, str]] = []
    for path in sorted(SESSIONS.glob("session-[0-9][0-9][0-9]-*.md")):
        # Deliberately one exception type per clause. Negative controls invoke ambient
        # `python3`, which is 3.13 here, while the project targets 3.14 -- and ruff
        # formats multi-type `except` clauses to the unparenthesized 3.14-only form that
        # 3.13 cannot parse. See think-y4nk.
        parts = path.read_text(encoding="utf-8").split("---\n", 2)
        if len(parts) < 2:
            continue
        try:
            document = yaml.safe_load(parts[1])
        except yaml.YAMLError:
            continue
        session = (document or {}).get("session")
        if not isinstance(session, dict):
            continue
        for number, phase in enumerate(session.get("workflow_phases") or [], start=1):
            command = phase.get("validation_command")
            if isinstance(command, str) and command.strip():
                declared.append((path.name, number, " ".join(command.split())))
    return declared


def check() -> list[str]:
    parsers = _parsers()
    problems: list[str] = []
    checked = 0
    for name, number, command in _declared_commands():
        for tool, args in _invocations(command, set(parsers)):
            checked += 1
            stderr = io.StringIO()
            try:
                with contextlib.redirect_stderr(stderr):
                    parsers[tool].parse_args(args)
            # packing-validate's parser overrides error() to raise UsageError instead of
            # exiting, so catching only SystemExit lets exactly the tool that carried the
            # original defect escape as a traceback. Both are caught deliberately.
            except (SystemExit, UsageError) as refusal:
                # argparse writes its reason to stderr before exiting; UsageError carries
                # it on the exception instead. Prefer whichever is actually populated.
                captured = stderr.getvalue().strip().splitlines()
                reason = str(refusal).strip() or (
                    captured[-1] if captured else "rejected by its own parser"
                )
                problems.append(
                    f"{name} phase {number}: `{tool} {' '.join(args)}` is not runnable: "
                    f"{reason}"
                )
    if not problems:
        print(f"  {checked} declared packing-CLI invocations parse against their own CLIs")
    return problems


def main() -> int:
    problems = check()
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
