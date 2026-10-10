#!/usr/bin/env python3
"""Select the test files a change can reach, erring toward running too many.

`BC-086`. Three red pushes on 2026-08-30 shared one shape: the change was to gate or
tooling code, the break was in a test pinned to that code, and the pre-push floor
(`--edit`, 43s) runs no tests at all while the tier that does (`--fast`) is priced at the
cost of its 499-second test step. The gap between 44s and 568s is where all three
failures lived. This module is the instrument that closes it: given the paths a push
changes, it names the test files that change can reach, so `packing-validate --push` can
run them without paying for the whole suite.

Reachability is computed from evidence, not convention, and every rule errs toward
inclusion:

- **Import closure.** A static import graph over `src/sqpack`, `devtools`, `cases`,
  `benchmarks`, the top-level workbench package and both Python test roots (AST,
  relative imports resolved); a test reaches a changed module if it imports it
  transitively. `benchmarks` joined the map in agenda-015 `BC-142`, after the agenda-014
  push tier selected all 1,302 tests for a change whose only Python lived there.
- **Text mention.** A test that names a changed module's dotted path, or a changed
  file's basename, is selected even without an import edge. This is what catches the
  `D-381` class: a test pinning a literal string emitted by code it exercises through a
  subprocess rather than an import.
- **Walkers always run.** A test that enumerates the repository (`rglob`, `iterdir`,
  `glob`, `listdir`) or imports dynamically (`importlib`, `__import__`) has the whole
  path space as its input, so it is selected for every change, exactly as unattributed
  steps are.
- **Whole-suite fallbacks.** An empty change set, a changed suite configuration file,
  a Python file outside the mapped roots, or a parse failure selects everything.
  "Nothing was determined" is not "nothing changed".

The same honesty proviso as `Step.touches` applies and is worth restating: this is a
static over-approximation, not a proof. Pull-request CI runs the complete fast surface;
full checkpoints also run deferred checks and exhaustive tests. This selector narrows
pre-push feedback only and does not establish reusable coverage for omitted tests.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.reachable_tests
"""

from __future__ import annotations

import argparse
import ast
import gc
import os
import re
import shlex
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from yaml import YAMLError

from devtools.retained_data import DATA_SUFFIXES, compressed_path
from sqpack.cli.validate import BEHAVIORAL_TEST_ROOTS, changed_paths
from sqpack.release import DATA_PATHS as RELEASE_DATA_PATHS

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
TEST_ROOTS = tuple((ROOT / path).resolve() for path in BEHAVIORAL_TEST_ROOTS)

#: Package roots the import graph maps, as (top-level package name, directory).
#: `sqpack` is installed from `src/`, the rest resolve via pytest's `pythonpath = ["."]`.
PACKAGE_ROOTS: tuple[tuple[str, Path], ...] = (
    ("sqpack", ROOT / "src" / "sqpack"),
    ("devtools", ROOT / "devtools"),
    ("cases", ROOT / "cases"),
    ("benchmarks", ROOT / "benchmarks"),
    ("tests", ROOT / "tests"),
    (
        "workbench_tools",
        REPO / "packages" / "workbench" / "tools" / "workbench_tools",
    ),
    ("workbench_tests", REPO / "packages" / "workbench" / "tests"),
)

#: A changed path equal to or under any of these selects the whole suite: they configure
#: how every test runs rather than what any one test checks.
SUITE_WIDE = (
    "packing/pyproject.toml",
    "packing/uv.lock",
    "packing/tests/conftest.py",
    "packing/.python-version",
    "packages/workbench/pyproject.toml",
    # Keep root-level configuration conservative if it is added to this checkout.
    "pyproject.toml",
    "uv.lock",
    "tests/conftest.py",
    ".python-version",
)

PAGES_WORKFLOW = ".github/workflows/pages.yml"

#: These exact inputs determine the current finite refinement identities and the
#: retained earlier-bound controls. They reach the builder's tests through the same
#: import closure as its Python source; this does not add a production step to --push.
REFINEMENT_REGISTER_INPUTS = frozenset(
    {
        "packing/resources/web/rehwaldt-n68-refinement-2026-10-07/facts/n-068.json.gz",
        "packing/resources/web/rehwaldt-couzo-refinements-2026-10-07/facts/n-105.json.gz",
        "packing/resources/web/rehwaldt-couzo-refinements-2026-10-07/facts/n-292.json.gz",
        "packing/resources/web/rehwaldt-couzo-refinements-2026-10-07/receipts/admission.json.xz",
        "packing/resources/web/rehwaldt-couzo-refinements-2026-10-07/receipts/house-metadata.json.xz",
        "packing/resources/web/rehwaldt-n68-refinement-2026-10-07/acquisition/prior-state.json",
        "packing/resources/web/rehwaldt-couzo-refinements-2026-10-07/acquisition/prior-state.json",
        "packing/witnesses/known-best/n-068.yaml",
        "packing/witnesses/known-best/n-105.yaml",
        "packing/witnesses/known-best/n-292.yaml",
    }
)

#: Latest native arrangements and source-only root candidates use the same closure.
LATEST_EXACT_SOURCE_INPUTS = frozenset(
    {
        "packing/resources/web/evand-new-arrangements-2026-10-07/facts/complete-certificates.json.xz",
        "packing/resources/web/evand-new-arrangements-2026-10-07/receipts/exact-certification.json.xz",
        "packing/resources/web/evand-new-arrangements-2026-10-07/acquisition/prior-state.json.xz",
        "packing/resources/web/evand-new-arrangements-2026-10-07/acquisition/declaration.json",
        "packing/resources/web/evand-new-arrangements-2026-10-07/acquisition/sources.json",
        "packing/resources/web/evand-new-arrangements-2026-10-07/acquisition/upstream-subtree.sha256",
        "packing/witnesses/known-best/n-266.yaml",
        "packing/witnesses/known-best/n-270.yaml",
        "packing/witnesses/known-best/n-272.yaml",
        "packing/resources/web/evand-exact-and-local-reports-2026-10-07/source/s12/search/exact/exact_forms.json.gz",
        "packing/resources/web/evand-exact-and-local-reports-2026-10-07/reported-catalogue.json",
        "packing/resources/web/evand-exact-and-local-reports-2026-10-07/acquisition/declaration.json",
        "packing/resources/web/evand-exact-and-local-reports-2026-10-07/acquisition/sources.json",
        "packing/resources/web/evand-exact-and-local-reports-2026-10-07/acquisition/upstream-subtree.sha256",
    }
)

#: This collector checks README and the packet-wide closed gzip inventory.
REPORTED_ROOT_PACKET = "packing/resources/web/evand-exact-and-local-reports-2026-10-07/"

#: Newly retained finite certificate identities and their complete source custody.
CERTIFICATE_REGISTER_PACKETS = (
    "packing/resources/web/ry-xu-new-packings-2026-10-08/",
    "packing/resources/web/gupta-square-packing-refinements-2026-10-08/",
    "packing/resources/web/couzo-exact-refinements-2026-10-08/",
    "packing/resources/web/couzo-followup-refinements-2026-10-08/",
    "packing/resources/web/evand-batch-105-130-2026-10-07/",
    "packing/resources/web/evand-batch-292-2026-10-07/",
)

WALKER_MARKERS = ("rglob(", "iterdir(", ".glob(", "listdir(", "importlib", "__import__")


class _WithoutBenignMetadataVersion(ast.NodeTransformer):
    """Remove only the metadata lookup that cannot import repository code."""

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom | None:
        if (
            node.level == 0
            and node.module == "importlib.metadata"
            and len(node.names) == 1
            and node.names[0].name == "version"
            and node.names[0].asname is None
        ):
            return None
        return node


@dataclass(frozen=True)
class TestSelection:
    """The outcome of one reachability question."""

    everything: bool
    reason: str
    """Why `everything` is set, or a summary of the narrow selection."""

    tests: tuple[str, ...] = ()
    """Repo-relative test paths, empty when `everything` is true."""


def _module_name(path: Path) -> str | None:
    """Dotted module name for a file under a mapped package root, else None."""
    for package, directory in PACKAGE_ROOTS:
        try:
            relative = path.relative_to(directory)
        except ValueError:
            continue
        parts = (package, *relative.with_suffix("").parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
        return ".".join(parts)
    return None


def _is_test_file(path: Path) -> bool:
    return path.parent in TEST_ROOTS and path.name.startswith("test_")


def _walker_markers_in(source: str, tree: ast.Module) -> bool:
    """`_walker_evidence` on a source already parsed into `tree`, which is not modified."""
    try:
        if "importlib" in source:
            # The transformer edits the tree it visits, so it gets a parse of its own.
            tree = _WithoutBenignMetadataVersion().visit(ast.parse(source))
        unparsed = ast.unparse(tree)
    except SyntaxError, RecursionError, ValueError:
        return True
    return any(marker in unparsed for marker in WALKER_MARKERS)


_WALKER_FROM_IMPORT_SCAN: dict[Path, bool] = {}
"""Walker evidence for test files, taken by `_imports_of` from the tree it parsed, so a
test file is parsed once per process. `_walker_evidence` reads it first."""


@cache
def _imports_of(path: Path) -> set[str] | None:
    """Top-level dotted names this file imports, or None when it cannot be parsed.

    Memoized on the path for the life of the process, which is exactly one selection in
    production: `main` calls `select_tests` once, and `packing-validate --push` reaches
    this module as a subprocess (twice, `--summary` then `--run`, each a fresh process).
    So no consumer can observe a tree that moved under the memo. The repeat caller is
    `tests/test_reachable_tests.py`, which puts ten questions to one static tree; the
    five that get past the everything-shortcuts each re-parsed every mapped file, at
    1.25s to 1.52s a call and 6.97s of the quick lane between them.

    The returned set is shared between callers now. `select_tests` only reads it; a
    future caller that wants to mutate one has to copy it first.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except OSError, SyntaxError, UnicodeDecodeError:
        return None
    if _is_test_file(path):
        _WALKER_FROM_IMPORT_SCAN[path] = _walker_markers_in(source, tree)
    found: set[str] = set()
    pending: list[ast.AST] = [tree]
    while pending:
        node = pending.pop()
        # Import statements can occur in compound-statement suites, but never
        # inside expressions. Skip large literal/geometry expressions while
        # retaining every suite, including exception handlers and match cases.
        pending.extend(
            child for child in ast.iter_child_nodes(node) if not isinstance(child, ast.expr)
        )
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = _module_name(path)
                if base is None:
                    continue
                parts = base.split(".")
                # A module of depth d can climb at most d-1 levels; deeper is a parse-time
                # error left to pytest, treated here as reaching the package root.
                anchor = parts[: max(len(parts) - node.level, 1)]
                prefix = ".".join(anchor)
                found.add(f"{prefix}.{node.module}" if node.module else prefix)
            elif node.module:
                found.add(node.module)
                # `from a.b import c` may bind the submodule a.b.c; include both readings.
                found.update(f"{node.module}.{alias.name}" for alias in node.names)
    return found


@cache
def _mapped_files() -> dict[str, Path]:
    """Every mapped module name to its file, packages included via __init__.

    Memoized for the same reason and under the same guarantee as `_imports_of`, and read
    rather than mutated by its one caller.
    """
    files: dict[str, Path] = {}
    for _package, directory in PACKAGE_ROOTS:
        for path in sorted(directory.rglob("*.py")):
            name = _module_name(path)
            if name is not None:
                files[name] = path
    return files


def _reaches(imported: set[str], targets: set[str]) -> bool:
    """Does any imported name land on a target module or inside a target package?"""
    for name in imported:
        parts = name.split(".")
        prefixes = {".".join(parts[: index + 1]) for index in range(len(parts))}
        if prefixes & targets:
            return True
    return False


@cache
def _walker_evidence(path: Path) -> bool:
    """Apply the old conservative marker scan, ignoring comments and one benign import.

    Unparsing preserves calls, aliases, module names, and string or bytes literals.
    It also handles indirect execution without guessing its dataflow. If parsing or
    unparsing fails, select the test rather than risk dropping a repository walker.
    """
    if path in _WALKER_FROM_IMPORT_SCAN:
        return _WALKER_FROM_IMPORT_SCAN[path]
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except OSError, SyntaxError, UnicodeDecodeError, RecursionError, ValueError:
        return True
    return _walker_markers_in(source, tree)


def _pages_workflow_inputs() -> set[Path]:
    """Publication invocation inputs, without pretending unchanged libraries were edited.

    Reuse the site's live declarations and command resolver. Every literal pytest
    target is included: the scope resolver recognizes only the first per command line.
    Directory declarations retain their builder/tool contracts rather than marking
    every descendant as changed. Actual changed Python/config paths are checked first.
    """
    from devtools import pages_scope  # noqa: PLC0415

    workflow = pages_scope.load_workflow()
    jobs = tuple(workflow["jobs"].values())
    files = pages_scope.import_closure(pages_scope.commands_run(jobs))
    for builder in pages_scope.BUILDER_INPUTS.values():
        declared = frozenset(builder())
        for path in declared:
            resolved = path
            if not path.exists():
                logical = path.with_suffix("") if path.suffix == ".gz" else path
                alternate = logical if path.suffix == ".gz" else compressed_path(path)
                if (
                    logical.suffix not in DATA_SUFFIXES
                    or alternate not in declared
                    or not alternate.is_file()
                ):
                    raise FileNotFoundError(f"declared Pages input is missing: {path}")
                resolved = alternate
            if resolved.is_file():
                files.add(resolved.resolve())
    for job in jobs:
        for step in job.get("steps", []):
            command = str(step.get("run", ""))
            for module in re.findall(r"\bpython\s+-m\s+(\S+)", command):
                if module in {"playwright", "pytest"}:
                    continue
                if re.fullmatch(r"(?:devtools|workbench_tools)(?:\.\w+)+", module) is None:
                    raise ValueError(f"unknown Pages Python entrypoint: {module}")
            targets = re.findall(r"\btests/[\w/.-]+\.py\b", command)
            for line in command.replace("\\\n", " ").splitlines():
                if re.search(r"\bpytest\b", line) is None:
                    continue
                words = shlex.split(line, comments=True)
                if "pytest" not in words:
                    continue
                arguments = words[words.index("pytest") + 1 :]
                if not arguments or not any(word != "-q" for word in arguments):
                    raise ValueError("Pages pytest invocation has no explicit test files")
                if any(
                    word != "-q" and re.fullmatch(r"tests/[\w/.-]+\.py(?:::.+)?", word) is None
                    for word in arguments
                ):
                    raise ValueError("Pages pytest invocation contains an unknown selection")
            for target in targets:
                path = (ROOT / target).resolve()
                if not path.is_file():
                    raise FileNotFoundError(f"Pages test target is missing: {target}")
                files.add(path)
    files.update(
        ROOT / "tests" / name for name in ("test_pages_workflow.py", "test_pages_scope.py")
    )
    files.add(Path(pages_scope.__file__).resolve())
    if any(not path.is_relative_to(REPO) for path in files):
        raise ValueError("a Pages input is outside the repository")
    return files


def _suite_configuration_reason(changed: list[str]) -> str | None:
    if not changed:
        return "no changed paths were determined"

    for path in changed:
        if path in SUITE_WIDE or (path.startswith(".github/") and path != PAGES_WORKFLOW):
            return f"{path} configures the suite"
        resolved = (REPO / path).resolve()
        if path.endswith(".py") and _module_name(resolved) is None:
            return f"{path} is Python outside the mapped roots"

    return None


def select_tests(changed: list[str]) -> TestSelection:
    """The test files a change to `changed` (repo-relative paths) can reach."""
    configuration = _suite_configuration_reason(changed)
    if configuration is not None:
        return TestSelection(everything=True, reason=configuration)

    publication_inputs: set[Path] = set()
    if PAGES_WORKFLOW in changed:
        try:
            publication_inputs = _pages_workflow_inputs()
        except (
            OSError,
            ValueError,
            SyntaxError,
            ImportError,
            TypeError,
            KeyError,
            AttributeError,
            SystemExit,
            YAMLError,
        ) as exc:
            return TestSelection(
                everything=True, reason=f"Pages invocation inputs could not be resolved: {exc}"
            )

    modules = _mapped_files()
    imports: dict[str, set[str]] = {}
    # The scan allocates millions of short-lived AST nodes and frees them itself; the
    # cyclic collector's passes over them cost about a sixth of the scan and free nothing.
    collecting = gc.isenabled()
    gc.disable()
    try:
        for name, file in modules.items():
            found = _imports_of(file)
            if found is None:
                return TestSelection(everything=True, reason=f"{file.name} did not parse")
            imports[name] = found
    finally:
        if collecting:
            gc.enable()

    changed_modules: set[str] = set()
    changed_basenames: set[str] = set()
    changed_dotted: set[str] = set()
    for path in changed:
        resolved = (REPO / path).resolve()
        name = _module_name(resolved) if path.endswith(".py") else None
        if name is not None:
            changed_modules.add(name)
            changed_dotted.add(name)
        else:
            changed_basenames.add(Path(path).name)

    for path in publication_inputs:
        # Workflow discovery includes these to resolve imports, but the workflow
        # has not edited package initializers or changed the pytest environment.
        if path.name in {"__init__.py", "conftest.py"}:
            continue
        name = _module_name(path) if path.suffix == ".py" else None
        if name is not None:
            changed_modules.add(name)
            changed_dotted.add(name)
        else:
            changed_basenames.add(path.name)

    # `release.data_revision` reads these Git paths rather than their file contents.
    # Give that declared non-Python input the same import-closure treatment as an edit
    # to `sqpack.release`; otherwise a new frontier record can stale the publication
    # pin while the push tier omits the test that enforces it.
    if any(
        changed_path == data_path or changed_path.startswith(f"{data_path}/")
        for changed_path in changed
        for data_path in RELEASE_DATA_PATHS
    ):
        changed_modules.add("sqpack.release")
        changed_dotted.add("sqpack.release")

    if any(
        path in REFINEMENT_REGISTER_INPUTS | LATEST_EXACT_SOURCE_INPUTS
        or path.startswith((REPORTED_ROOT_PACKET, *CERTIFICATE_REGISTER_PACKETS))
        for path in changed
    ):
        changed_modules.add("devtools.build_exact_values")
        changed_dotted.add("devtools.build_exact_values")

    # Transitive closure: grow the changed-module set by everything that imports it.
    grew = True
    while grew:
        grew = False
        for name, found in imports.items():
            if name not in changed_modules and _reaches(found, changed_modules):
                changed_modules.add(name)
                grew = True

    selected: dict[str, str] = {}
    for name, file in modules.items():
        if file.parent not in TEST_ROOTS or not file.name.startswith("test_"):
            continue
        relative = str(file.relative_to(REPO))
        if name in changed_modules:
            selected.setdefault(relative, "import closure")
            continue
        text = file.read_text(encoding="utf-8")
        if _walker_evidence(file):
            selected.setdefault(relative, "walks the repository or imports dynamically")
            continue
        if any(dotted in text for dotted in changed_dotted):
            selected.setdefault(relative, "names a changed module")
            continue
        if any(basename in text for basename in changed_basenames):
            selected.setdefault(relative, "names a changed file")

    tests = tuple(sorted(selected))
    total = sum(1 for directory in TEST_ROOTS for _ in directory.glob("test_*.py"))
    if len(tests) >= total:
        return TestSelection(everything=True, reason="every test file is reachable")
    reason = f"{len(tests)} of {total} test files reachable"
    return TestSelection(everything=False, reason=reason, tests=tests)


def pytest_command(
    targets: Sequence[str],
    workers: int,
    *,
    marker: str = "not exhaustive_exact",
    artifact_stem: Path | None = None,
) -> tuple[str, ...]:
    """The pytest invocation for a selection, under `workers` xdist processes.

    Split out from `main` so the distribution can be asserted without running a suite.
    `-n 1` is not asked for, matching `sqpack.cli.validate._xdist_distribution`: one xdist
    worker is a subprocess and a protocol for no concurrency, which is slower than not
    asking.

    `D-488` is what this argument closes. The selector's runner had no distribution at
    all, so the pre-push tier's behavioural step ran in one process at every `--jobs`
    value, including the `--jobs 1` that `_xdist_distribution` documents as the way to
    get four workers on a four-cpu box. The whole-suite fallback is the expensive case:
    other workflow changes or suite configuration select everything, which is
    the quick lane and the slow lane together in a single process.
    """
    distribution = ("-n", str(workers)) if workers > 1 else ()
    receipts = (
        ("-p", "devtools.reachable_progress", f"--junitxml={artifact_stem}.junit.xml")
        if artifact_stem is not None
        else ()
    )
    return (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        *targets,
        "-m",
        marker,
        *distribution,
        "--durations=0",
        "--durations-min=0",
        *receipts,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Select the test files a change can reach, erring toward running too many."
    )
    parser.add_argument("--since", metavar="REF", default="origin/main")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="print one machine-readable line: 'everything' or the selected count",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="run pytest on the selection (the whole non-exhaustive suite when everything)",
    )
    parser.add_argument(
        "-n",
        "--numprocesses",
        metavar="N",
        type=int,
        default=1,
        help=(
            "run the selection under N xdist workers; 1, the default, runs in one process."
            " The caller decides, because the right number depends on how many outer slots"
            " are already busy: `packing-validate` passes `cpus - jobs + 1`."
        ),
    )
    parser.add_argument(
        "--pool-workers",
        metavar="N",
        type=int,
        help=(
            "split the selected tests into disjoint normal and pool_heavy marker lanes; "
            "the latter runs serially with PACK_JOBS=N"
        ),
    )
    namespace = parser.parse_args(argv)
    if namespace.numprocesses < 1:
        parser.error("--numprocesses must be at least 1")
    if namespace.pool_workers is not None and namespace.pool_workers < 1:
        parser.error("--pool-workers must be at least 1")
    if namespace.pool_workers is not None and not namespace.run:
        parser.error("--pool-workers requires --run")

    selection = select_tests(changed_paths(namespace.since))
    if namespace.summary:
        print("everything" if selection.everything else f"narrow {len(selection.tests)}")
        return 0
    if selection.everything:
        print(f"everything: {selection.reason}")
    else:
        print(selection.reason)
        for test in selection.tests:
            print(f"  {test}")
    if not namespace.run:
        return 0

    targets = (
        list(BEHAVIORAL_TEST_ROOTS)
        if selection.everything
        else [os.path.relpath(REPO / test, start=ROOT) for test in selection.tests]
    )
    # `not exhaustive_exact`, which keeps the `slow` lane in. That is deliberate and it
    # is the difference between this tier and the pull-request surface: `--fast` defers
    # every test above the per-test ceiling because it pays for them on every pull
    # request, while `--push` pays only for the tests your own change reaches, and a slow
    # test your change reaches is exactly the one worth waiting for.
    parent_stem_value = os.environ.get("PACKING_REACHABLE_TEST_ARTIFACT_STEM")
    parent_stem: Path | None = None
    child_environment: dict[str, str] | None = None
    if parent_stem_value:
        parent_stem = Path(parent_stem_value)
        if not parent_stem.is_absolute():
            parser.error("reachable-test artifact stem must be absolute")
        parent_stem = parent_stem.resolve()
        if parent_stem.is_relative_to(REPO.resolve()):
            parser.error("reachable-test artifacts must stay outside the source checkout")
        # Each child has its own prefix: a later two-phase run can keep both JUnit and
        # progress receipts without overwriting the first child's partial evidence.
        git_environment = {
            key: value for key, value in os.environ.items() if not key.startswith("GIT_")
        }
        source = subprocess.run(
            ("git", "rev-parse", "HEAD"),
            cwd=REPO,
            check=False,
            capture_output=True,
            text=True,
            env=git_environment,
        )
        source_commit = source.stdout.strip()
        if source.returncode != 0 or re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
            parser.error("cannot identify the reachable-test source commit")
        parent_run_id = os.environ.get("PACKING_REACHABLE_TEST_RUN_ID")
        if not parent_run_id:
            parser.error("reachable-test artifacts need the parent run id")
        child_environment = dict(os.environ)
        child_environment["PACKING_REACHABLE_TEST_RUN_ID"] = parent_run_id
        child_environment["PACKING_REACHABLE_TEST_SOURCE_COMMIT"] = source_commit

    def run_phase(name: str, marker: str, workers: int, pack_jobs: int | None) -> int:
        stem = Path(f"{parent_stem}.{name}") if parent_stem is not None else None
        command = pytest_command(targets, workers, marker=marker, artifact_stem=stem)
        if child_environment is None and pack_jobs is None:
            return subprocess.run(command, cwd=ROOT, check=False).returncode
        environment = dict(os.environ if child_environment is None else child_environment)
        if stem is not None:
            environment["PACKING_REACHABLE_TEST_ARTIFACT_STEM"] = str(stem)
            environment["PACKING_REACHABLE_TEST_WORKERS"] = str(workers)
        if pack_jobs is not None:
            environment["PACK_JOBS"] = str(pack_jobs)
        return subprocess.run(command, cwd=ROOT, check=False, env=environment).returncode

    if namespace.pool_workers is None:
        return run_phase("pytest-all", "not exhaustive_exact", namespace.numprocesses, None)

    def empty_lane(marker: str) -> bool:
        # xdist's exit 5 could hide a collection mismatch. Only a separate serial
        # collection that also finds no tests permits this lane to be omitted.
        probe = (
            sys.executable,
            "-m",
            "pytest",
            "-q",
            *targets,
            "-m",
            marker,
            "--collect-only",
        )
        return subprocess.run(probe, cwd=ROOT, check=False).returncode == 5

    normal_marker = "not exhaustive_exact and not pool_heavy"
    pool_marker = "not exhaustive_exact and pool_heavy"
    normal_status = run_phase("pytest-normal", normal_marker, namespace.numprocesses, 1)
    if normal_status != 0 and (normal_status != 5 or not empty_lane(normal_marker)):
        return normal_status
    pool_status = run_phase("pytest-pool", pool_marker, 1, namespace.pool_workers)
    if pool_status != 0 and (pool_status != 5 or not empty_lane(pool_marker)):
        return pool_status
    return 5 if normal_status == 5 and pool_status == 5 else 0


if __name__ == "__main__":
    raise SystemExit(main())
