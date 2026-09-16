#!/usr/bin/env python3
"""Decide which of the two published pages a pull request has to build and check.

The Pages workflow publishes two pages from one artifact: the explainer at `/` and the
workbench at `/workbench/`. Until 2026-09-15 every pull request that touched either
page's paths paid for both. #178 changed ten workbench probe files and ran about 330 s
of explainer Chromium checks on a page whose bytes it could not change; an explainer-only
change paid for the workbench build the same way.

This tool is what lets each half run only on its own inputs. For each half it takes:

* the builder's own declaration of what a render reads -- `RENDER_INPUTS` in
  `devtools/render_explainer.py` for the explainer and in `workbench_tools/build_site.py`
  for the workbench. Read live from those modules rather than copied here, because a copy
  is a second list that drifts, and the builders' lists already have tests that keep
  them honest (`test_the_pages_filter_covers_every_render_input`, `test_build_site_inputs`);
* every developer tool and test the workflow's jobs for that half run, read out of
  `pages.yml` itself, with the modules those tools import from this repository. A checker
  is an input of the verdict even though it is not an input of the page: editing
  `check_print_layout.py` has to run the print-layout check;
* the workflow file and this module, because either can change what runs.

A pull request's changed files are the difference between its merge commit and that
commit's first parent, which is the base branch as GitHub merged it: exactly what the PR
would change on its base, and the same set GitHub's own `paths:` filter considers. A half
none of those files touches is skipped, and the workflow says so in a job of its own
rather than leaving the reader to infer it from grey checks. A push to `main` and a manual
dispatch build everything; this tool is only ever asked to narrow a pull request.

The failure direction is the safe one. A declared input that is missing from a half makes
that half run less often, so the tests compare the scope against the builders'
declarations and against the workflow's commands. An error here -- a revision git cannot
diff, a workflow it cannot read -- fails the job, and every page check waiting on it is
then skipped as a dependency failure, which the required aggregate reports as a failure,
not as a justified skip.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.pages_scope --diff HEAD^1 HEAD
    uv run --frozen --all-extras --group dev python -m devtools.pages_scope --all "a push"

Both write `<half>=true|false` and `<half>_reason=...` to `$GITHUB_OUTPUT` and a summary
table to `$GITHUB_STEP_SUMMARY` when those are set, and print the same to stdout.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import os
import re
import subprocess
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
WORKFLOW = REPO / ".github" / "workflows" / "pages.yml"

#: The first-party packages whose modules the workflow runs and whose imports are
#: followed. `sqpack` is not here: both builders declare the parts of it they read.
LOCAL_PACKAGES = ("devtools", "workbench_tools", "tests")

_RUN_MODULE = re.compile(r"\bpython\s+-m\s+((?:devtools|workbench_tools)(?:\.\w+)+)")
_PYTEST_FILE = re.compile(r"\bpytest\b[^\n]*?\s(tests/[\w/.-]+\.py)")
_HALF_GATE = re.compile(r"needs\.scope\.outputs\.(\w+)\s*==\s*'true'")
#: The two ways a job in this workflow says it never runs on a pull request: the deploy
#: path's `github.event_name != 'pull_request'` and a dispatch-only experiment's
#: `github.event_name == 'workflow_dispatch'`.
_NOT_ON_PULL_REQUESTS = re.compile(
    r"github\.event_name\s*(?:!=\s*'pull_request'|==\s*'workflow_dispatch')"
)


def _explainer_inputs() -> tuple[Path, ...]:
    from devtools import render_explainer  # noqa: PLC0415

    return tuple(render_explainer.RENDER_INPUTS)


def _workbench_inputs() -> tuple[Path, ...]:
    from workbench_tools import build_site  # noqa: PLC0415

    return tuple(build_site.RENDER_INPUTS)


#: Each half, and the builder declaration it starts from, in the order the workflow's
#: outputs and summary use.
BUILDER_INPUTS: Mapping[str, Callable[[], tuple[Path, ...]]] = {
    "explainer": _explainer_inputs,
    "workbench": _workbench_inputs,
}


def load_workflow(path: Path = WORKFLOW) -> dict[str, Any]:
    """The Pages workflow as data."""
    document = safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("jobs"), dict):
        raise SystemExit(f"{path}: not a workflow with jobs")
    return document


def needs_of(job: Mapping[str, Any]) -> list[str]:
    """A job's `needs:`, which YAML allows as one name or a list."""
    needs = job.get("needs", [])
    return [needs] if isinstance(needs, str) else list(needs)


def pull_request_jobs(workflow: Mapping[str, Any]) -> set[str]:
    """The jobs a pull request can run: all but the deploy path and dispatch-only jobs.

    Only these contribute tools to a half's inputs. `verify-deployment` runs
    `check_published_site`, which imports the PDF exporter; counting it would put every
    explainer tool into the workbench's scope for a job no pull request ever starts.
    """
    jobs: Mapping[str, Mapping[str, Any]] = workflow["jobs"]
    excluded = {
        name
        for name, job in jobs.items()
        if _NOT_ON_PULL_REQUESTS.search(str(job.get("if", "")))
    }
    grew = True
    while grew:
        grew = False
        for name, job in jobs.items():
            if name not in excluded and any(need in excluded for need in needs_of(job)):
                excluded.add(name)
                grew = True
    return set(jobs) - excluded


def half_jobs(workflow: Mapping[str, Any]) -> dict[str, set[str]]:
    """The jobs each half gates, directly or by needing a job it gates.

    A job belongs to a half when its `if:` requires `needs.scope.outputs.<half> ==
    'true'`, or when it needs a job that does -- GitHub skips a job whose need was
    skipped, so a check downstream of `prepare` is gated by `prepare`'s condition whether
    or not it repeats it. A job downstream of both halves (the aggregate, the deploy
    path) belongs to both, which only ever widens what a half counts as its input.
    """
    jobs: Mapping[str, Mapping[str, Any]] = workflow["jobs"]
    members: dict[str, set[str]] = {half: set() for half in BUILDER_INPUTS}
    for name, job in jobs.items():
        for half in _HALF_GATE.findall(str(job.get("if", ""))):
            if half not in members:
                raise SystemExit(
                    f"{WORKFLOW.name}: job {name!r} gates on unknown half {half!r}"
                )
            members[half].add(name)
    grew = True
    while grew:
        grew = False
        for name, job in jobs.items():
            for gated in members.values():
                if name not in gated and any(need in gated for need in needs_of(job)):
                    gated.add(name)
                    grew = True
    return members


def _module_file(module: str) -> Path:
    spec = importlib.util.find_spec(module)
    if spec is None or spec.origin is None:
        raise SystemExit(f"{WORKFLOW.name} runs {module}, which does not resolve to a file")
    return Path(spec.origin).resolve()


def _conftests(test: Path) -> set[Path]:
    """Every `conftest.py` pytest loads for a test file under `packing/`."""
    found: set[Path] = set()
    directory = test.parent
    while directory.is_relative_to(PACKING):
        conftest = directory / "conftest.py"
        if conftest.is_file():
            found.add(conftest)
        if directory == PACKING:
            break
        directory = directory.parent
    return found


def commands_run(jobs: Iterable[Mapping[str, Any]]) -> set[Path]:
    """The first-party modules and test files the given jobs execute."""
    files: set[Path] = set()
    for job in jobs:
        for step in job.get("steps", []):
            command = str(step.get("run", ""))
            files.update(_module_file(module) for module in _RUN_MODULE.findall(command))
            for test in _PYTEST_FILE.findall(command):
                path = (PACKING / test).resolve()
                if not path.is_file():
                    raise SystemExit(f"{WORKFLOW.name} runs pytest on {test}, which is gone")
                files.add(path)
                files.update(_conftests(path))
    return files


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
            # `from devtools import render_explainer_pdf as pdf` imports a module too.
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return {name for name in names if name.split(".")[0] in LOCAL_PACKAGES}


def _source_of(module: str) -> Path | None:
    try:
        spec = importlib.util.find_spec(module)
    except ModuleNotFoundError:
        return None  # `from devtools.x import NAME`: NAME is not a module
    if spec is None or spec.origin is None or not spec.origin.endswith(".py"):
        return None
    return Path(spec.origin).resolve()


def import_closure(files: Iterable[Path]) -> set[Path]:
    """The files, and every first-party module they import, transitively."""
    seen = set(files)
    pending = [path for path in seen if path.suffix == ".py"]
    while pending:
        for module in _imported_modules(pending.pop()):
            origin = _source_of(module)
            if origin is not None and origin not in seen:
                seen.add(origin)
                pending.append(origin)
    return seen


def declared_inputs(workflow: Mapping[str, Any] | None = None) -> dict[str, tuple[Path, ...]]:
    """Every repository path whose change puts each half in scope on a pull request."""
    workflow = load_workflow() if workflow is None else workflow
    members = half_jobs(workflow)
    runnable = pull_request_jobs(workflow)
    declared: dict[str, tuple[Path, ...]] = {}
    for half, builder in BUILDER_INPUTS.items():
        jobs = (workflow["jobs"][name] for name in sorted(members[half] & runnable))
        tools = import_closure(commands_run(jobs))
        paths = {*builder(), *tools, WORKFLOW, Path(__file__)}
        declared[half] = tuple(sorted({path.resolve() for path in paths}))
    return declared


def matches(changed: str, declared: Path) -> bool:
    """Whether a repository-relative changed path is, or is inside, a declared input."""
    relative = declared.relative_to(REPO).as_posix()
    return changed == relative or changed.startswith(f"{relative}/")


@dataclass(frozen=True)
class Decision:
    """One half's verdict, and the sentence the workflow shows for it."""

    half: str
    in_scope: bool
    reason: str
    touched: tuple[str, ...]


def decide(changed: Sequence[str], declared: Mapping[str, tuple[Path, ...]]) -> list[Decision]:
    """For each half, the changed files among its inputs and a sentence saying so."""
    decisions: list[Decision] = []
    for half, inputs in declared.items():
        touched = [path for path in changed if any(matches(path, i) for i in inputs)]
        if touched:
            more = f" and {len(touched) - 1} more" if len(touched) > 1 else ""
            reason = f"{touched[0]}{more} changed, among the {half}'s {len(inputs)} inputs"
        else:
            files = f"{len(changed)} changed file" + ("s" if len(changed) != 1 else "")
            reason = f"none of the {files} is among the {half}'s {len(inputs)} declared inputs"
        decisions.append(Decision(half, bool(touched), reason, tuple(touched)))
    return decisions


def changed_paths(base: str, head: str) -> list[str]:
    """Repository-relative paths that differ between two revisions, renames split.

    `--no-renames` lists a renamed file under both names, so moving an input away counts
    as a change to it. A submodule appears as its gitlink path, `vendor/kpress`.
    """
    result = subprocess.run(
        ("git", "diff", "--name-only", "--no-renames", "-z", base, head, "--"),
        cwd=REPO,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = result.stderr.decode(errors="replace").strip()
        raise SystemExit(f"git diff {base} {head} failed: {detail}")
    return [path for path in result.stdout.decode("utf-8").split("\0") if path]


def _append(variable: str, text: str) -> None:
    target = os.environ.get(variable)
    if target:
        with Path(target).open("a", encoding="utf-8") as handle:
            handle.write(text)


def report(decisions: Sequence[Decision], *, changed: int | None) -> None:
    """Write the decision where the workflow and its reader will look for it."""
    _append(
        "GITHUB_OUTPUT",
        "".join(
            f"{d.half}={'true' if d.in_scope else 'false'}\n{d.half}_reason={d.reason}\n"
            for d in decisions
        ),
    )
    heading = "every page" if changed is None else f"{changed} changed files"
    rows = "".join(
        f"| {d.half} | {'builds and checks' if d.in_scope else '**skipped**'} | {d.reason} |\n"
        for d in decisions
    )
    _append(
        "GITHUB_STEP_SUMMARY",
        f"### Which pages this run builds ({heading})\n\n"
        f"| Page | This run | Why |\n| --- | --- | --- |\n{rows}",
    )
    for d in decisions:
        print(f"{d.half}: {'in scope' if d.in_scope else 'skipped'} -- {d.reason}")
        for path in d.touched[:20]:
            print(f"  {path}")
        if len(d.touched) > 20:
            print(f"  ... and {len(d.touched) - 20} more")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--diff",
        nargs=2,
        metavar=("BASE", "HEAD"),
        help="scope each half to the files that differ between two revisions",
    )
    mode.add_argument(
        "--all",
        metavar="WHY",
        help="put every half in scope, saying why (a push to main, a dispatch)",
    )
    parser.add_argument(
        "--list", action="store_true", help="also print every declared input of each half"
    )
    args = parser.parse_args(argv)
    declared = declared_inputs()
    if args.list:
        for half, inputs in declared.items():
            print(f"{half}: {len(inputs)} declared inputs")
            for path in inputs:
                print(f"  {path.relative_to(REPO).as_posix()}")
    if args.all is not None:
        decisions = [
            Decision(
                half, in_scope=True, reason=f"every page is built on {args.all}", touched=()
            )
            for half in declared
        ]
        report(decisions, changed=None)
        return 0
    base, head = args.diff
    changed = changed_paths(base, head)
    report(decide(changed, declared), changed=len(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
