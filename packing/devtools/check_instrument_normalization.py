#!/usr/bin/env python3
"""Refuse a bound instrument file that a later formatting pass would silently sever.

An immutable result binds the exact bytes of the files that produced it: `exp-055` records
`instrument_bindings`, `exp-050` records `bindings`, `exp-052`'s checkpoint records
`binding.source_sha256`. Every one of those is a SHA-256 of a file still sitting in the
working tree, and the guarantee is only worth what the bytes are worth. Run
`ruff format` over a bound Python file and the digest changes; the result is then bound to
bytes that no longer exist anywhere, and nothing in the repository notices.

The repository already knows this, which is why `[tool.ruff.format] exclude` in
`pyproject.toml` carries five instrument files with that exact reason written above them.
What it does not have is a check that the list is complete. A new round that binds a
sixth file gets no warning at freeze time, and the failure surfaces later as an
unreproducible hash with no record of when it moved.

So this runs before the freeze, not after it. For every bound Python file in every
immutable result it asks one question: is this file `ruff format --check` clean, or is it
excluded from formatting? Either answer is safe. A file that is neither is one
`make format` away from breaking its own result, and the tool exits 1 naming it.

Exclusion is read from the configuration and confirmed against the formatter, because
the two can disagree and the formatter is the one that edits files. `[tool.ruff.format]
exclude` is the per-file list; `[tool.ruff] exclude` and `extend-exclude` are directory
scopes, and `resources` is one of them -- the bound `n = 17` verifier script lives there
and is unformatted, which is safe for exactly that reason and would be a false refusal if
only the per-file list were consulted. Anything the configuration does not settle is
handed to `ruff format --check --force-exclude`, so a file counts as clean only when
ruff itself, under this repository's own settings, says it would not rewrite it.

Deliberately not checked here: whether the recorded digest still matches the file. That
is a different failure -- drift that has already happened -- and it belongs to the
replay path, which can say what the correct bytes were. This check is about the drift
that has not happened yet.

Usage:
    uv run --frozen --all-extras --group dev \
        python -m devtools.check_instrument_normalization
    uv run --frozen --all-extras --group dev \
        python -m devtools.check_instrument_normalization --json
"""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tomllib
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import TypedDict

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: Result fields that carry instrument bindings. Named rather than inferred, so a new
#: binding shape is a deliberate edit here and not a silently unscanned result.
BINDING_FIELDS = ("instrument_bindings", "bindings", "binding")

_HEX = set("0123456789abcdef")


@dataclass(frozen=True, slots=True)
class Binding:
    """One packing-relative path bound by one immutable result."""

    result: str
    field: str
    path: str


class BindingEntry(TypedDict):
    """One classified binding, as it appears in the report."""

    result: str
    field: str
    path: str
    status: str
    detail: str


class NormalizationReport(TypedDict):
    """The whole receipt, which `--json` prints verbatim."""

    root: str
    results_scanned: int
    bound_python_files: int
    format_exclusions: dict[str, list[str]]
    bindings: list[BindingEntry]
    violations: list[BindingEntry]
    ok: bool


def _is_digest(value: object) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value) <= _HEX


def _bound_paths(node: object) -> Iterator[str]:
    """Every packing-relative path a binding structure associates with a digest."""
    if isinstance(node, dict):
        path = node.get("path")
        if isinstance(path, str) and _is_digest(node.get("sha256")):
            yield path
        for key, value in node.items():
            if isinstance(key, str) and _is_digest(value):
                yield key
            else:
                yield from _bound_paths(value)
        return
    if isinstance(node, list):
        if len(node) == 2 and isinstance(node[0], str) and _is_digest(node[1]):
            yield node[0]
            return
        for item in node:
            yield from _bound_paths(item)


def result_files(root: pathlib.Path) -> list[pathlib.Path]:
    """Every immutable result JSON under the campaign series."""
    return sorted((root / "campaign" / "series").glob("*/results/*.json"))


def bindings(root: pathlib.Path) -> list[Binding]:
    """Every Python file bound by an immutable result, in a stable order."""
    found: list[Binding] = []
    seen: set[tuple[str, str]] = set()
    for result in result_files(root):
        try:
            record = json.loads(result.read_text(encoding="utf-8"))
        except OSError, json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        name = result.relative_to(root).as_posix()
        for field in BINDING_FIELDS:
            if field not in record:
                continue
            for path in _bound_paths(record[field]):
                if not path.endswith(".py"):
                    continue
                key = (name, path)
                if key in seen:
                    continue
                seen.add(key)
                found.append(Binding(result=name, field=field, path=path))
    return found


def _string_list(section: object, key: str) -> list[str]:
    if not isinstance(section, dict):
        return []
    values = section.get(key, [])
    if not isinstance(values, list):
        return []
    return [entry for entry in values if isinstance(entry, str)]


def format_exclusions(root: pathlib.Path) -> dict[str, list[str]]:
    """The configured exclusions, split into the per-file list and the directory scopes."""
    config = root / "pyproject.toml"
    if not config.exists():
        return {"format_exclude": [], "scope_exclude": []}
    data = tomllib.loads(config.read_text(encoding="utf-8"))
    tool = data.get("tool", {})
    ruff = tool.get("ruff", {}) if isinstance(tool, dict) else {}
    section = ruff.get("format", {}) if isinstance(ruff, dict) else {}
    scope = _string_list(ruff, "exclude") + _string_list(ruff, "extend-exclude")
    return {
        "format_exclude": sorted(_string_list(section, "exclude")),
        "scope_exclude": sorted(scope),
    }


def _excluded_by(path: str, exclusions: dict[str, list[str]]) -> str | None:
    """Which configured exclusion, if any, keeps the formatter away from `path`."""
    if path in exclusions["format_exclude"]:
        return "tool.ruff.format exclude"
    segments = path.split("/")
    for entry in exclusions["scope_exclude"]:
        parts = entry.strip("/").split("/")
        if path == entry or segments[: len(parts)] == parts:
            return f"tool.ruff exclude scope {entry}"
    return None


def _ruff() -> str:
    candidate = pathlib.Path(sys.executable).parent / "ruff"
    if candidate.exists():
        return str(candidate)
    found = shutil.which("ruff")
    if found is None:
        raise RuntimeError("ruff is not available; run under the project environment")
    return found


def _is_format_clean(root: pathlib.Path, path: str) -> bool:
    """Whether ruff, under this tree's own settings, would leave the file alone."""
    completed = subprocess.run(
        [_ruff(), "format", "--check", "--force-exclude", "--quiet", path],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


SAFE = ("excluded", "formatter-clean")


def report(root: pathlib.Path = ROOT) -> NormalizationReport:
    """Classify every bound Python file as excluded, clean, missing, or unformatted."""
    exclusions = format_exclusions(root)
    entries: list[BindingEntry] = []
    for binding in bindings(root):
        reason = _excluded_by(binding.path, exclusions)
        if reason is not None:
            status, detail = "excluded", reason
        elif not (root / binding.path).exists():
            status, detail = "missing", "bound path is absent from the tree"
        elif _is_format_clean(root, binding.path):
            status, detail = "formatter-clean", "ruff format --check leaves it unchanged"
        else:
            status, detail = "unformatted-and-not-excluded", "ruff format would rewrite it"
        entries.append(
            BindingEntry(
                result=binding.result,
                field=binding.field,
                path=binding.path,
                status=status,
                detail=detail,
            )
        )
    violations = [entry for entry in entries if entry["status"] not in SAFE]
    return NormalizationReport(
        root=str(root),
        results_scanned=len(result_files(root)),
        bound_python_files=len(entries),
        format_exclusions=exclusions,
        bindings=entries,
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
        print(f"scanned {receipt['results_scanned']} immutable results under {receipt['root']}")
        print(f"bound Python files: {receipt['bound_python_files']}")
        for entry in receipt["bindings"]:
            print(f"  {entry['status']:>28}  {entry['path']}  <- {entry['result']}")
        if receipt["ok"]:
            print("every bound instrument file is formatter-clean or explicitly excluded")
    for entry in receipt["violations"]:
        print(
            f"bound instrument file is neither formatter-clean nor excluded: {entry['path']}"
            f" ({entry['status']}, bound by {entry['result']})",
            file=sys.stderr,
        )
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
