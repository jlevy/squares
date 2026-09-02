#!/usr/bin/env python3
"""Refuse a declared parser or recursion bound that no test ever reaches.

`cases/unitsquare_precision/production/adapter.py` declares seven `MAX_` constants. They
are the difference between a bounded parser and an attacker-shaped stack overflow, and
they are also the easiest kind of guard to get silently wrong: raise the number while
debugging, or delete the branch that reads it, and every test still passes, because a
bound that is never exceeded is indistinguishable from a bound that is not there.

So this asks the one question that separates the two. For every module-level `MAX_`
integer under `cases/`, is there a test that reaches the guard the constant controls? A
bound with a named test is doing work. A bound without one is a number in a file.

Reaching a guard is recognized two ways, because tests legitimately do it two ways.

**By name.** A test that imports the constant and asserts against it names it directly.

**By refusal message.** `test_selected_path_scan_enforces_depth_before_python_recursion`
never writes `MAX_XML_DEPTH`; it builds a scene deeper than the recursion limit and
matches `"bounded parser limits"`, which is the message the `MAX_XML_DEPTH` branch
raises. That is a stronger test than an equality assertion -- it exercises the guard
rather than restating the constant -- and a check that only accepted the literal name
would refuse the best control in the repository. So the tool reads each constant's guard
messages out of the `raise` statements its `if` branches guard, and accepts a test whose
own string literals match one.

A bound with no guard message and no naming test is not automatically a defect; several
`MAX_` constants here are search widths rather than refusals. Those go in `ALLOWLIST`
with a reason, which is a registration, not an exemption: the entry is visible, dated to
the block that added it, and has to be removed on purpose.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.check_declared_bounds
    uv run --frozen --all-extras --group dev python -m devtools.check_declared_bounds --json
"""

from __future__ import annotations

import argparse
import ast
import json
import pathlib
import re
import sys
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from typing import TypedDict

ROOT = pathlib.Path(__file__).resolve().parent.parent

BOUND_PATTERN = re.compile(r"\AMAX_[A-Z0-9_]+\Z")

#: The shortest string literal a test may use to match a guard message. Below this a
#: coincidental word ("depth") would count as evidence, which is worse than no check.
MIN_MESSAGE_MATCH = 12

#: This tool's own controls quote constant names as data. Counting them would let the
#: check satisfy itself: the positive control mentions `MAX_XML_DEPTH` to assert that a
#: real test reaches it, and without this the mention would be the evidence.
EXCLUDED_REFERENCES = ("tests/test_check_declared_bounds.py",)

#: Bounds registered without a naming test, each with the reason it has none. Keyed by
#: `<packing-relative module>::<constant>`.
ALLOWLIST: dict[str, str] = {
    "cases/lifted_q2/packing.py::MAX_DENOMINATOR": (
        "pre-existing; registered by BC-140. A search width for the lift sweep, not a"
        " refusal: exceeding it returns no lift rather than raising, so there is no guard"
        " branch for a test to reach."
    ),
    "cases/lifted_q7/packing.py::MAX_DENOMINATOR": (
        "pre-existing; registered by BC-140. Same search width as the lifted_q2 sweep,"
        " over sqrt(7) instead of sqrt(2)."
    ),
    "cases/n5/rotating_release_paths.py::MAX_BERNSTEIN_DEPTH": (
        "pre-existing; registered by BC-140. The subdivision-limit refusal exists but no"
        " test drives a numerator to it; reaching it needs an uncertifiable Bernstein"
        " form, which the n = 5 fixtures do not carry."
    ),
    "cases/unitsquare_precision/production/adapter.py::MAX_PARENT_BYTES": (
        "pre-existing; registered by BC-140. Passed as the default byte cap to the"
        " bounded opener rather than compared in a branch, so it declares no guard"
        " message of its own."
    ),
    "cases/unitsquare_precision/production/adapter.py::MAX_COVER_NODES": (
        "pre-existing; registered by BC-140. The wall-cover node budget refuses, but no"
        " test builds a cover large enough to exhaust it."
    ),
    "cases/unitsquare_precision/production/adapter.py::MAX_COVER_DEPTH": (
        "pre-existing; registered by BC-140. Shares the wall-cover refusal with"
        " MAX_COVER_NODES and is unreached for the same reason."
    ),
    "cases/unitsquare_precision/production/adapter.py::MAX_NUMBER_TOKEN_BYTES": (
        "pre-existing; registered by BC-140. The numeric-token refusal is unreached; no"
        " fixture carries a 128-byte number token."
    ),
    "cases/unitsquare_precision/production/adapter.py::MAX_STABLE_ID_BYTES": (
        "pre-existing; registered by BC-140. The retained-id refusal is unreached; no"
        " fixture carries a 512-byte polygon id."
    ),
}


@dataclass(frozen=True, slots=True)
class Bound:
    """One module-level `MAX_` integer and the refusal messages its branches raise."""

    module: str
    name: str
    value: int
    line: int
    guard_messages: tuple[str, ...] = ()

    @property
    def key(self) -> str:
        return f"{self.module}::{self.name}"


class NameEvidence(TypedDict):
    """One function that names one bound, and how it names it."""

    kind: str
    path: str
    function: str
    detail: str


class BoundEntry(TypedDict):
    """One classified bound, as it appears in the report."""

    module: str
    name: str
    value: int
    line: int
    guard_messages: list[str]
    status: str
    named_by: list[NameEvidence]
    allowlist_reason: str | None


class BoundsReport(TypedDict):
    """The whole receipt, which `--json` prints verbatim."""

    root: str
    declared_bounds: int
    allowlist: dict[str, str]
    bounds: list[BoundEntry]
    violations: list[BoundEntry]
    ok: bool


@dataclass(frozen=True, slots=True)
class Reference:
    """One test or selftest function, reduced to what it could name a bound with."""

    path: str
    function: str
    identifiers: frozenset[str] = field(default_factory=frozenset)
    literals: tuple[str, ...] = ()


def _literal_parts(node: ast.AST) -> Iterator[str]:
    """Every string literal inside an expression, f-string fragments included."""
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            yield child.value


def _guard_messages(tree: ast.Module, name: str) -> tuple[str, ...]:
    """Messages raised by `if` branches whose condition reads the named constant."""
    messages: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        reads = any(
            isinstance(inner, ast.Name) and inner.id == name for inner in ast.walk(node.test)
        )
        if not reads:
            continue
        for statement in ast.walk(node):
            if isinstance(statement, ast.Raise) and statement.exc is not None:
                messages.extend(_literal_parts(statement.exc))
    return tuple(dict.fromkeys(message for message in messages if message.strip()))


def declared_bounds(root: pathlib.Path) -> list[Bound]:
    """Every module-level `MAX_` integer declared under `cases/`."""
    found: list[Bound] = []
    for path in sorted((root / "cases").rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except OSError, SyntaxError:
            continue
        module = path.relative_to(root).as_posix()
        for node in tree.body:
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name) or not BOUND_PATTERN.match(target.id):
                continue
            if not (isinstance(node.value, ast.Constant) and isinstance(node.value.value, int)):
                continue
            found.append(
                Bound(
                    module=module,
                    name=target.id,
                    value=node.value.value,
                    line=node.lineno,
                    guard_messages=_guard_messages(tree, target.id),
                )
            )
    return found


def _functions(
    path: pathlib.Path, relative: str, *, selftest_only: bool
) -> Iterator[Reference]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except OSError, SyntaxError:
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        lowered = node.name.lower()
        if selftest_only and "selftest" not in lowered and "self_test" not in lowered:
            continue
        identifiers = {inner.id for inner in ast.walk(node) if isinstance(inner, ast.Name)} | {
            inner.attr for inner in ast.walk(node) if isinstance(inner, ast.Attribute)
        }
        yield Reference(
            path=relative,
            function=node.name,
            identifiers=frozenset(identifiers),
            literals=tuple(_literal_parts(node)),
        )


def references(root: pathlib.Path) -> list[Reference]:
    """Every test function under `tests/` and every selftest inside `cases/`."""
    found: list[Reference] = []
    for path in sorted((root / "tests").rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        if relative in EXCLUDED_REFERENCES:
            continue
        found.extend(_functions(path, relative, selftest_only=False))
    for path in sorted((root / "cases").rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        found.extend(_functions(path, path.relative_to(root).as_posix(), selftest_only=True))
    return found


def _names(bound: Bound, reference: Reference) -> NameEvidence | None:
    """How, if at all, one function names one bound."""
    if bound.name in reference.identifiers or any(
        bound.name in literal for literal in reference.literals
    ):
        return NameEvidence(
            kind="constant-name",
            path=reference.path,
            function=reference.function,
            detail=bound.name,
        )
    for message in bound.guard_messages:
        for literal in reference.literals:
            if len(literal) < MIN_MESSAGE_MATCH:
                continue
            if literal in message or message in literal:
                return NameEvidence(
                    kind="guard-message",
                    path=reference.path,
                    function=reference.function,
                    detail=literal,
                )
    return None


def report(root: pathlib.Path = ROOT, allowlist: dict[str, str] | None = None) -> BoundsReport:
    """Classify every declared bound as named, allowlisted, or unnamed."""
    registered = ALLOWLIST if allowlist is None else allowlist
    known = references(root)
    entries: list[BoundEntry] = []
    for bound in declared_bounds(root):
        evidence = [
            found for reference in known if (found := _names(bound, reference)) is not None
        ]
        reason = registered.get(bound.key)
        if evidence:
            status = "named"
        elif reason is not None:
            status = "allowlisted"
        else:
            status = "unnamed"
        entries.append(
            BoundEntry(
                module=bound.module,
                name=bound.name,
                value=bound.value,
                line=bound.line,
                guard_messages=list(bound.guard_messages),
                status=status,
                named_by=evidence,
                allowlist_reason=reason,
            )
        )
    violations = [entry for entry in entries if entry["status"] == "unnamed"]
    return BoundsReport(
        root=str(root),
        declared_bounds=len(entries),
        allowlist=dict(sorted(registered.items())),
        bounds=entries,
        violations=violations,
        ok=not violations,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=ROOT, help="tree to check")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)

    receipt = report(args.root.resolve())
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(f"declared bounds under {receipt['root']}/cases: {receipt['declared_bounds']}")
        for entry in receipt["bounds"]:
            named_by = entry["named_by"]
            where = named_by[0]["function"] if named_by else (entry["allowlist_reason"] or "")
            print(f"  {entry['status']:>12}  {entry['module']}::{entry['name']}  {where}")
        if receipt["ok"]:
            print("every declared bound is named by a test or registered with a reason")
    for entry in receipt["violations"]:
        print(
            f"declared bound has no naming test and no allowlist entry: "
            f"{entry['module']}::{entry['name']} (line {entry['line']})",
            file=sys.stderr,
        )
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
