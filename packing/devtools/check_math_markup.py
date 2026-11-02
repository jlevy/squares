#!/usr/bin/env python3
"""The math-markup ratchet: a migrated Markdown file keeps its mathematics as LaTeX.

`devtools.migrate_math` moves a file's mathematics from code spans to `$…$`. Without a
check, the next edit writes `` `s(11) ≥ 3.82` `` again and the file drifts back one span
at a time. This is that check, for the pull-request surface: every file listed under
`migrated` in `devtools/math-markup.yaml` is planned exactly as `migrate_math` plans it,
and a code span it would convert fails the gate, with the LaTeX to write instead. A span
that must stay code despite reading as math is recorded under `keep` with its reason, and
a `keep` entry whose span has gone fails too, so the list only shrinks.
A file that must never move -- its exact bytes are pinned by a replay, or it quotes an
external source whose spans would be retyped -- is recorded under `exempt` with its
reason, and leaves the backlog.

The reverse fails as well: a formula written as `$…$` where GitHub shows the dollars
instead -- after a hyphen or a slash, inside a link's text or italics -- with the code
span to write back, since GitHub is where most of these files are read
(`migrate_math.github_unsafe_math`, whose rules the GitHub probe measured).

A file that is not listed is never read. The check counts them instead -- every tracked
hand-written Markdown file not yet migrated -- so the backlog stays visible without
being enforced, and `--backlog` lists it. Generated views are counted apart, since they
move at their renderers; the literature archive, vendored trees, tool-owned files under
dot directories, renderer templates and the preserved sources `.flowmarkignore` protects
are excluded, each with the reason the document map or `.flowmarkignore` records.

It is fast by construction, since it runs in the edit tier: a migrated file whose spans
contain no math by their text alone (`has_math_spans`) needs no block parse, and that is
every migrated file with nothing wrong in it. The run prints its own wall time.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.check_math_markup
    uv run --frozen --all-extras --group dev python -m devtools.check_math_markup --backlog

Exits 1 on a finding, and 2 if the register cannot be read.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from collections import Counter
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from devtools.migrate_math import (
    UnsafeMath,
    github_unsafe_math,
    has_math_spans,
    open_math_spans,
    plan,
)
from devtools.repo_scope import (
    excluded_by,
    flowmark_exclusions,
    tracked_markdown,
    vendored_directories,
)
from sqpack.yamlio import load_yaml, safe_load

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
REGISTER = Path(__file__).resolve().parent / "math-markup.yaml"
DOCUMENT_MAP = PurePosixPath("docs/project/document-map.yaml")


class RegisterError(ValueError):
    """The register is not the shape this check reads."""


@dataclass(frozen=True)
class Keep:
    """One code span that reads as math but stays code, and why."""

    path: str
    span: str
    reason: str


@dataclass(frozen=True)
class Exempt:
    """One file that stays as it is, and why: its bytes are pinned, or it quotes a source."""

    path: str
    reason: str


@dataclass(frozen=True)
class Register:
    """The migrated files, the spans they keep as code, and the files that never move."""

    migrated: tuple[str, ...]
    keep: tuple[Keep, ...]
    exempt: tuple[Exempt, ...] = ()


def load_register(path: Path = REGISTER) -> Register:
    """Read and shape-check the register; a malformed one raises `RegisterError`."""
    data = load_yaml(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) - {"exempt"} != {"migrated", "keep"}:
        raise RegisterError(
            f"{path.name}: expected the keys `migrated` and `keep`, and optionally `exempt`"
        )
    migrated, keep = data["migrated"], data["keep"]
    if not isinstance(migrated, list) or not all(isinstance(item, str) for item in migrated):
        raise RegisterError(f"{path.name}: `migrated` must be a list of paths")
    if not isinstance(keep, list):
        raise RegisterError(f"{path.name}: `keep` must be a list")
    entries: list[Keep] = []
    for item in keep:
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "span", "reason"}
            or not all(isinstance(value, str) and value.strip() for value in item.values())
        ):
            raise RegisterError(
                f"{path.name}: a `keep` entry is {{path, span, reason}}, none empty: {item!r}"
            )
        entries.append(Keep(item["path"], item["span"], item["reason"]))
    exempt: list[Exempt] = []
    for item in data.get("exempt") or []:
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "reason"}
            or not all(isinstance(value, str) and value.strip() for value in item.values())
        ):
            raise RegisterError(
                f"{path.name}: an `exempt` entry is {{path, reason}}, neither empty: {item!r}"
            )
        exempt.append(Exempt(item["path"], item["reason"]))
    return Register(tuple(migrated), tuple(entries), tuple(exempt))


@dataclass(frozen=True)
class Scope:
    """Every tracked Markdown file, sorted by what the ratchet may do with it."""

    eligible: frozenset[str]
    generated: frozenset[str]
    excluded: dict[str, str] = field(default_factory=dict)


def _document_map(repo: Path) -> tuple[frozenset[str], list[str]]:
    """The document map's generated views and its exclusion patterns, if it has one."""
    source = repo / DOCUMENT_MAP
    if not source.is_file():
        return frozenset(), []
    document = safe_load(source.read_text(encoding="utf-8"))
    generated = frozenset(
        entry["path"]
        for entry in document.get("documents", [])
        if entry.get("role") == "generated-view" or entry.get("authority") == "generated"
    )
    return generated, [entry["pattern"] for entry in document.get("exclusions", [])]


def _why_excluded(
    path: str, repo: Path, map_patterns: Sequence[str], ignored: Sequence[str]
) -> str | None:
    """Why the ratchet may never list `path`, or `None` if it may."""
    parts = PurePosixPath(path).parts
    prefixes = {"/".join(parts[:length]) for length in range(1, len(parts))}
    if prefixes & vendored_directories(repo):
        return "vendored"
    if any(part.startswith(".") for part in parts[:-1]):
        return "tool-owned"
    if excluded_by(path, map_patterns):
        return "document-map exclusion"
    if excluded_by(path, ignored):
        return "flowmark exclusion"
    return None


def scope(repo: Path = REPO) -> Scope:
    """Sort the tracked Markdown into eligible, generated and excluded files."""
    generated_views, map_patterns = _document_map(repo)
    ignored = flowmark_exclusions(repo)
    eligible: set[str] = set()
    generated: set[str] = set()
    excluded: dict[str, str] = {}
    for path in tracked_markdown(repo):
        if path in generated_views:
            generated.add(path)
        elif (reason := _why_excluded(path, repo, map_patterns, ignored)) is not None:
            excluded[path] = reason
        else:
            eligible.add(path)
    return Scope(frozenset(eligible), frozenset(generated), excluded)


@dataclass
class Outcome:
    """What one run found: the problems, and the counts it reports."""

    problems: list[str] = field(default_factory=list)
    kept: int = 0


def _normalized(content: str) -> str:
    return " ".join(content.split())


def _check_file(path: str, text: str, keeps: set[str], outcome: Outcome) -> None:
    """Fail every math code span in one migrated file that `keep` does not name."""
    found: set[str] = set()
    # A `keep` needs the full plan to tell a live span from a stale one; otherwise a file
    # with no span `$` could replace has nothing the plan would convert.
    if has_math_spans(text) and (keeps or open_math_spans(text)):
        for decision in plan(text).decisions:
            if decision.verdict.kind != "math":
                continue
            span = _normalized(decision.span.content)
            found.add(span)
            if span in keeps:
                outcome.kept += 1
                continue
            outcome.problems.append(
                f"{path}:{decision.span.line}: `{span}` is mathematics written as code "
                f"({decision.verdict.rule}); write ${decision.verdict.latex}$, or run "
                f"`python -m devtools.migrate_math --apply {path}`"
            )
    outcome.problems.extend(
        f"{path}: `keep` names `{span}`, which is no longer a math code span here; remove it"
        for span in sorted(keeps - found)
    )
    if "$" in text:
        outcome.problems.extend(
            f"{path}:{item.line}: ${item.tex}$ is not drawn as written on GitHub -- "
            f"{item.reason}; {_remedy(path, item)}"
            for item in github_unsafe_math(text)
        )


def _remedy(path: str, item: UnsafeMath) -> str:
    apply = f"`python -m devtools.migrate_math --apply --github {path}`"
    if item.code is not None:
        return f"write {item.code}, or run {apply}"
    if item.replacement is not None:
        return f"run {apply}, which writes the TeX GitHub keeps"
    return "move it where GitHub draws math, or rephrase it"


def check(register: Register, repo: Path = REPO, files: Scope | None = None) -> Outcome:
    """Check every migrated file and the register's own consistency."""
    files = files if files is not None else scope(repo)
    outcome = Outcome()
    if list(register.migrated) != sorted(set(register.migrated)):
        outcome.problems.append("math-markup.yaml: `migrated` must be sorted and unique")
    for keep in register.keep:
        if keep.path not in register.migrated:
            outcome.problems.append(f"math-markup.yaml: `keep` names {keep.path}, not migrated")
    exempt = [item.path for item in register.exempt]
    if exempt != sorted(set(exempt)):
        outcome.problems.append("math-markup.yaml: `exempt` must be sorted and unique")
    for path in exempt:
        if path in register.migrated:
            outcome.problems.append(f"math-markup.yaml: {path} is both migrated and exempt")
        elif path not in files.eligible:
            outcome.problems.append(
                f"math-markup.yaml: `exempt` names {path}, which is not a hand-written "
                "Markdown file the ratchet could read"
            )
    jobs: list[tuple[str, str, frozenset[str]]] = []
    for path in register.migrated:
        if path not in files.eligible:
            why = (
                "a generated view, migrated at its renderer"
                if path in files.generated
                else files.excluded.get(path, "not a tracked Markdown file")
            )
            outcome.problems.append(f"math-markup.yaml: {path} cannot be listed: {why}")
            continue
        keeps = frozenset(keep.span for keep in register.keep if keep.path == path)
        jobs.append((path, (repo / path).read_text(encoding="utf-8"), keeps))
    if len(jobs) < PARALLEL_FROM:
        results = [_checked(job) for job in jobs]
    else:
        # Each file is independent, and with every Markdown file migrated the serial walk
        # was seven seconds of the edit tier; the cores take a share each.
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
            results = list(pool.map(_checked, jobs, chunksize=32))
    for problems, kept in results:
        outcome.problems.extend(problems)
        outcome.kept += kept
    return outcome


#: The register size from which the files are checked in parallel; a handful is faster
#: checked where it is than spread across fresh processes.
PARALLEL_FROM = 64


def _checked(job: tuple[str, str, frozenset[str]]) -> tuple[list[str], int]:
    """One migrated file's problems and kept-span count, in a form a worker can return."""
    path, text, keeps = job
    outcome = Outcome()
    _check_file(path, text, set(keeps), outcome)
    return outcome.problems, outcome.kept


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_math_markup",
        description="Fail a math code span in a migrated file; report the unmigrated backlog.",
    )
    parser.add_argument("--register", type=Path, default=REGISTER, help=argparse.SUPPRESS)
    parser.add_argument("--repo", type=Path, default=REPO, help=argparse.SUPPRESS)
    parser.add_argument("--backlog", action="store_true", help="list the unmigrated files")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    started = time.perf_counter()
    try:
        register = load_register(arguments.register)
    except (OSError, RegisterError) as error:
        print(f"  cannot read the math-markup register: {error}", file=sys.stderr)
        return 2
    files = scope(arguments.repo)
    outcome = check(register, arguments.repo, files)
    exempt = {item.path for item in register.exempt}
    backlog = sorted(files.eligible - set(register.migrated) - exempt)
    for problem in outcome.problems:
        print(f"  {problem}", file=sys.stderr)
    excluded = Counter(files.excluded.values())
    kept = f", {outcome.kept} spans kept as code" if outcome.kept else ""
    print(f"  math markup: {len(register.migrated)} migrated files checked{kept}")
    reasons = ", ".join(f"{reason} {count}" for reason, count in sorted(excluded.items()))
    print(
        f"  backlog: {len(backlog)} of {len(files.eligible)} hand-written Markdown files "
        f"not yet migrated, {len(exempt)} exempt; "
        f"{len(files.generated)} generated views move at their renderers; "
        f"{excluded.total()} excluded" + (f" ({reasons})" if reasons else "")
    )
    if arguments.backlog:
        for path in backlog:
            print(f"    {path}")
    print(f"  ({time.perf_counter() - started:.2f}s)")
    return 1 if outcome.problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
