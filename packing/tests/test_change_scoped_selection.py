"""Change-scoped gate selection, and the two ways it must refuse to under-select.

`BC-084`. `D-355` measured a two-file edit to the rigidity assessor verified by a 979.79s
full gate whose two reachable steps run together in 12.06s. Selecting fewer steps is only
admissible when the unselected ones provably cannot fail on the change, so the design is
conservative on both sides and these assertions are where that is held:

- a changed path no step claims selects the **whole gate**, never the steps that happened
  to match, because a partial answer derived from an admittedly incomplete map is worse
  than no answer;
- a step that declares nothing is claimed by everything.

The one failure that costs coverage is a pattern set too narrow for its step. Two
contracts stand between that and a check that silently stops running:
`test_every_step_is_reachable_from_a_declared_pattern` against a mistyped glob, and
`test_every_attributed_step_claims_the_modules_it_runs` against a step that imports a
module its patterns do not claim.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import inspect
import os
import re
import subprocess
import types
from collections import deque
from collections.abc import Mapping
from pathlib import Path

import pytest

from devtools import reachable_tests
from devtools.reachable_tests import PACKAGE_ROOTS, ROOT, _imports_of, _mapped_files
from sqpack.cli import validate
from sqpack.cli.validate import STEPS, Step, select_for_paths
from workbench_tools.build_site import RENDER_INPUTS, REPO

WORKBENCH_STEP = "workbench browser behavior in Chromium"
BROWSER_FLOOR_STEP = "browser floor (biome, eslint, tsc, node:test)"
KATEX_STEP = "X-027 mathematics parses with pinned KaTeX"

# One representative path per source region. Every step must be selected by at least one
# of these; a step selected by none has a pattern set that matches nothing real, which is
# indistinguishable from having been switched off.
PATTERN_PROBES = (
    "packing/src/sqpack/verify.py",
    "packing/src/sqpack/research/canonical.py",
    "packing/sqsearch/src/main.rs",
    "packing/sqverify_exact/src/lib.rs",
    "packing/sqverify_fast/src/rotated.rs",
    "packing/cases/small_n/optimal_moduli.py",
    "packing/devtools/render_defects.py",
    "packing/devtools/assess_frontier_rigidity.py",
    "packing/devtools/build_n5_identity_pair.py",
    "packing/devtools/render_agenda_map.py",
    "packing/devtools/render_packing_svg.py",
    "packing/devtools/check_soundness_perimeter.py",
    "packing/devtools/wand125_fn1_bindings.py",
    "packing/devtools/render_research_tables.py",
    "packing/tests/test_verify.py",
    "packing/tests/test_browser_floor_contract.py",
    "packing/campaign/agendas/agenda-008-x.md",
    "packing/campaign/schemas/agenda.schema.yaml",
    "packing/campaign/series/series-000-smoke-and-calibration/results/bc-083-n5-identity-pair.json",
    "packing/frontier/STATUS.md",
    "packing/atlas/n-003-optimal-moduli.svg",
    "packing/defects.yaml",
    "packing/pyproject.toml",
    "AGENTS.md",
    "operating-rules.md",
    "defects.md",
    "SYNOPSIS.md",
    "Makefile",
    ".claude/skills/experiment-loop/SKILL.md",
    "packing/witnesses/known-best/n-011.yaml",
    "packing/golden/basin-maps.yaml",
    "packing/atlas/known-best/manifest.json",
    "packing/atlas/prospective/manifest.json",
    "packing/atlas/enumerated/contact-scaffolds-size5.json",
    "packages/workbench/src/application.js",
    "packages/workbench/probes/atlas-transitions.d.ts",
    "packing/cases/trump11/packing.py",
    "packing/cases/stromquist/printed_cover.py",
    "packing/resources/papers/kingbird-square-29-provenance.svg",
    "docs/project/research/research-2026-08-22-packing-11-unit-squares.md",
    ".tbd/config.yml",
)


def test_every_step_is_reachable_from_a_declared_pattern() -> None:
    """No step may be unreachable from every probe.

    An attributed step whose patterns match nothing that exists has been switched off
    without anyone deciding to switch it off, and the gate would keep reporting green.
    """
    unreachable = [
        step.name
        for step in STEPS
        if not any(step.reachable_from(path) for path in PATTERN_PROBES)
    ]
    assert unreachable == [], (
        f"these steps match no probe path and would never be selected: {unreachable}"
    )


def test_an_unclaimed_path_selects_the_whole_gate() -> None:
    """The escape hatch, which is the whole soundness argument.

    A path nobody attributed means the map is incomplete for this change. Returning the
    steps that happened to match would be an answer computed from a map known to be
    wrong, so the only safe answer is everything.
    """
    selection = select_for_paths(["packing/some/file/nobody/attributed.xyz"])
    assert selection.is_whole_gate
    assert selection.unattributed_paths == ("packing/some/file/nobody/attributed.xyz",)


def test_exact_rust_source_selects_its_own_gate_without_search_engine_build() -> None:
    selection = select_for_paths(["packing/sqverify_exact/src/lib.rs"])
    assert not selection.is_whole_gate
    names = {step.name for step in selection.steps}
    assert "exact rectangle Rust geometry" in names
    assert "search engine (sqsearch)" not in names
    assert "lint floor (rust)" not in names


def test_one_unclaimed_path_poisons_an_otherwise_narrow_selection() -> None:
    """Not "mostly attributed, so mostly narrow" -- one unknown path widens everything.

    This is the case a plausible implementation gets wrong: it is tempting to union the
    matched steps and treat the unknown path as contributing nothing.
    """
    narrow = select_for_paths(["packing/devtools/assess_frontier_rigidity.py"])
    assert not narrow.is_whole_gate

    poisoned = select_for_paths(
        ["packing/devtools/assess_frontier_rigidity.py", "some/unknown/thing.xyz"]
    )
    assert poisoned.is_whole_gate
    assert len(poisoned.steps) > len(narrow.steps)


def test_no_paths_is_not_nothing_changed() -> None:
    """An empty path list means "nothing was determined", not "nothing changed"."""
    assert select_for_paths([]).is_whole_gate


def test_an_unattributed_step_is_selected_by_everything() -> None:
    """The safe default: forgetting to attribute a step costs time, never coverage."""
    unattributed = Step("synthetic", lambda _c: "")
    claimed = Step("claimed", lambda _c: "", touches=("packing/frontier/*",))
    universe = (unattributed, claimed)

    selection = select_for_paths(["packing/frontier/STATUS.md"], universe)
    assert {step.name for step in selection.steps} == {"synthetic", "claimed"}


def test_a_narrow_change_does_not_select_the_whole_gate() -> None:
    """The point of the feature, stated as a measurement rather than a hope.

    `D-355`'s case: an edit to the rigidity assessor alone. It must reach the frontier
    steps and the Python floors, and must not reach steps that provably cannot see that
    file -- here the Rust ones, which read only `packing/sqsearch/`.

    It does still reach every unattributed step, and most steps are unattributed today.
    That is the safe direction and not a defect, but it does mean this test measures the
    mechanism rather than the saving; the saving grows as attribution does.
    """
    selection = select_for_paths(["packing/devtools/assess_frontier_rigidity.py"])
    assert not selection.is_whole_gate
    names = {step.name for step in selection.steps}
    assert "frontier rigidity assessed here" in names
    assert "lint floor (ruff)" in names
    # `frontier corpus` runs `cases.kingbird29.verify_svg`, not the assessor, so it is
    # correctly excluded -- attribution is per step's actual inputs, not per topic. It
    # first claimed `check_source_coverage.py`, which a different step runs; that was an
    # under-selection and is fixed.
    assert "frontier corpus" not in names
    assert "lint floor (rust)" not in names
    assert "search engine (sqsearch)" not in names


def test_a_markdown_only_change_skips_the_python_floors() -> None:
    """The cheapest real win, and the one that shows attribution is doing work.

    Editing only prose cannot change what `ruff` or `basedpyright` say, so neither should
    run. If this ever fails, either a floor gained a Markdown input or its patterns drifted.
    """
    selection = select_for_paths(["operating-rules.md", "AGENTS.md"])
    names = {step.name for step in selection.steps}
    assert "lint floor (ruff)" not in names
    assert "type floor (basedpyright)" not in names
    assert "AGENTS.md mirrors the operating rules" in names


def test_results_register_runs_for_its_open_ended_path_dependencies() -> None:
    for path in (
        "packing/cases/stromquist/repaired_cover.py",
        "packing/tests/test_falsify.py",
        "packing/witnesses/known-best/n-011.yaml",
        "packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md",
        "docs/project/document-map.yaml",
    ):
        names = {step.name for step in select_for_paths([path]).steps}
        assert "results rungs are earned and the view agrees" in names


def test_the_five_under_selections_an_adversarial_review_found() -> None:
    """Each of these was a real hole: a file that changes a step's verdict, unclaimed.

    They matter more than they look, because `*.py` and `*.md` cross separators and so
    claim every Python and Markdown file in the repository. No change to either extension
    can reach the whole-gate escape, which leaves each narrow step's own patterns as the
    only thing standing between an edit and a check that does not run.
    """
    cases = {
        # check_svg_rendering pins examples in TUTORIAL.md and walks REPO.rglob("*.md").
        "TUTORIAL.md": "deterministic SVG rendering",
        # render_research_tables diffs the n=11 report cell by cell.
        "docs/project/research/research-2026-08-22-packing-11-unit-squares.md": (
            "generated tables in sync with frontier/"
        ),
        # assess_frontier_rigidity derives its verdict from this screen.
        "packing/atlas/known-best/translation-escape-screen.json": (
            "frontier rigidity assessed here"
        ),
        # _frontier_corpus runs cases.kingbird29.verify_svg.
        "packing/cases/kingbird29/verify_svg.py": "frontier corpus",
        # Both registry renderers parse through sqpack.yamlio.
        "packing/src/sqpack/yamlio.py": "defect log",
    }
    for path, step_name in cases.items():
        names = {step.name for step in select_for_paths([path]).steps}
        assert step_name in names, f"changing {path} must select {step_name!r}"


def test_a_narrowed_tier_reports_its_own_universe() -> None:
    """`--since` narrows whatever tier preceded it, so "everything" is that tier.

    Comparing against the full step list made a whole-tier selection report itself as a
    partial one, which is the wrong way round for a field a reader uses to decide whether
    anything was skipped.
    """
    fast = [step for step in STEPS if step.fast]
    selection = select_for_paths(["nobody/claims/this.xyz"], fast)
    assert selection.is_whole_gate
    assert len(selection.steps) == len(fast)


def test_an_explicitly_empty_universe_is_not_the_whole_gate() -> None:
    """An empty list passed on purpose meant "all steps", which reads backwards."""
    assert select_for_paths(["packing/frontier/STATUS.md"], []).steps == ()


def _selects(path: str, step_name: str, patterns: tuple[str, ...] | None = None) -> bool:
    if patterns is None:
        return step_name in {step.name for step in select_for_paths([path]).steps}
    return Step(step_name, lambda _c: "", touches=patterns).reachable_from(path)


def _render_input_probe(declared: Path) -> str:
    """A repository-relative path that stands for one declared render input."""
    relative = declared.relative_to(REPO).as_posix()
    return f"{relative}/__render_input__" if declared.is_dir() else relative


def test_every_workbench_render_input_selects_the_workbench_check() -> None:
    """`_WORKBENCH_INPUTS` is a hand list beside the builder's own declaration.

    Compared here rather than trusted: it omitted
    `packing/devtools/render_n11_lower_bounds_explainer.py`, which the builder runs for the
    KaTeX stylesheet, so a `--since` run over that file skipped the page check (#160 R26).
    """
    unselected = [
        _render_input_probe(declared)
        for declared in RENDER_INPUTS
        if not _selects(_render_input_probe(declared), WORKBENCH_STEP)
    ]
    assert unselected == [], f"render inputs that do not select {WORKBENCH_STEP!r}"


def test_a_motion_lab_probe_selects_the_workbench_check() -> None:
    assert _selects(
        "packing/devtools/probes/check_motion_lab_pages/remove_element.js",
        WORKBENCH_STEP,
    )


def test_the_motion_lab_golden_selects_its_browser_replay() -> None:
    assert _selects("packing/tests/golden/motion-lab-pages.json", WORKBENCH_STEP)


def test_an_omitted_workbench_input_is_detected() -> None:
    """The negative control: the step's patterns without the explainer renderer.

    The renderer hub's `packing/devtools/*` claims the explainer too since PR 496 G1, so
    the control removes both; what it shows is that the builder's declaration is checked
    against the gate's copy and not merely that some wide pattern happens to cover it.
    """
    (step,) = [step for step in STEPS if step.name == WORKBENCH_STEP]
    without = tuple(
        pattern
        for pattern in step.touches
        if "render_n11_lower_bounds_explainer" not in pattern
        and pattern != "packing/devtools/*"
    )
    explainer = REPO / "packing/devtools/render_n11_lower_bounds_explainer.py"
    assert explainer in RENDER_INPUTS
    assert not _selects(_render_input_probe(explainer), WORKBENCH_STEP, without)


def test_the_node_katex_checker_selects_the_x027_math_check() -> None:
    assert _selects("packing/devtools/node/check-katex.mjs", KATEX_STEP)


def test_an_omitted_node_katex_checker_is_detected() -> None:
    """The negative control: remove the executable the Python driver invokes.

    The renderer hub's `packing/devtools/*` covers the checker's directory too since
    PR 496 G1, so the control removes both patterns: it is the explicit claim on the
    executable that is under test, not a wide pattern that happens to reach it.
    """
    (step,) = [step for step in STEPS if step.name == KATEX_STEP]
    without = tuple(
        pattern
        for pattern in step.touches
        if pattern not in {"packing/devtools/node/check-katex.mjs", "packing/devtools/*"}
    )
    assert not _selects(
        "packing/devtools/node/check-katex.mjs",
        KATEX_STEP,
        without,
    )


def test_browser_floor_inputs_select_the_browser_floor() -> None:
    """Declarations, scripts, nested manifests and the workbench's JSON are browser-floor
    inputs (#125 F36, PR 496 G2): editing one must select the floor on a `--since` run.

    The JSON matters because `*.json` is claimed by `retained JSON`, so a fixture edit
    that breaks a `node:test` file, or one Biome would reformat, has no whole-gate
    fallback to fall through to.
    """
    for path in (
        "eslint.probes.json",
        "packing/devtools/probe-typecheck.json",
        "packages/workbench/probes/atlas-transitions.d.ts",
        "packing/atlas/known-best/video/spikes/v1-slideshow/node-harness.d.ts",
        "packing/atlas/known-best/video/spikes/v1-slideshow/assets/package.json",
        "packing/devtools/node/inspect-probes.mjs",
        "packages/workbench/tools/render-katex.ts",
        "packages/workbench/assets/workbench.css",
        "packages/workbench/tests/fixtures/corpus.json",
        "packages/workbench/tests/fixtures/benchmark-foundation/manifest.json",
        "packages/workbench/design-allowlist.json",
    ):
        assert (REPO / path).is_file(), path
        assert _selects(path, BROWSER_FLOOR_STEP), path


_RUN_MODULE = re.compile(r"^(?:devtools|cases|sqpack|benchmarks|workbench_tools)(?:\.\w+)+$")
_RUN_SCRIPT = re.compile(r"^(?:tests|devtools|cases|benchmarks)/[\w/.-]+\.py(?:::.*)?$")
#: Where pytest targets live; a target under it loads every `conftest.py` from here down.
TESTS = (ROOT / "tests").resolve()
#: The subprocess runners. Their own constants name the two modules they treat specially
#: (`devtools.reachable_tests`, `devtools.run_negative_controls`), which are not modules
#: every step runs, so the walk through the gate's helpers stops at them.
_RUNNERS = frozenset(
    {"_run", "_run_command", "_module", "_commands", "_command_groups", "_concurrent_commands"}
)
#: Attributed steps that run no mapped Python: external tools, Rust, or an in-process
#: check of a record. A step whose action the derivation cannot see is a step the
#: closure contract does not hold, so the set is pinned rather than tolerated.
_RUNS_NO_MAPPED_PYTHON = frozenset(
    {
        "lint floor (ruff)",
        "type floor (basedpyright)",
        BROWSER_FLOOR_STEP,
        "search engine (sqsearch)",
        "strategy catalogues",
        "skills mirrored between .agents and .claude",
        "provenance: recorded commits are reachable",
    }
)


def _strings_and_names(code: types.CodeType) -> tuple[set[str], set[str]]:
    """String constants and referenced names of a code object, nested functions included.
    The compiler folds a literal tuple of constants into one constant, so a command
    written as `("pytest", "tests/x.py")` is read through it."""
    strings: set[str] = set()
    names = set(code.co_names)
    for constant in code.co_consts:
        if isinstance(constant, str):
            strings.add(constant)
        elif isinstance(constant, tuple | frozenset):
            strings.update(item for item in constant if isinstance(item, str))
        elif isinstance(constant, types.CodeType):
            inner_strings, inner_names = _strings_and_names(constant)
            strings |= inner_strings
            names |= inner_names
    return strings, names


def _module_files(name: str, files: Mapping[str, Path]) -> set[Path]:
    """The mapped file of a dotted module and of every package above it, which Python
    executes on the way down."""
    parts = name.split(".")
    prefixes = (".".join(parts[: depth + 1]) for depth in range(len(parts)))
    return {files[prefix] for prefix in prefixes if prefix in files}


def _conftests_loaded_for(target: Path) -> set[Path]:
    """The `conftest.py` files pytest loads for a target under `packing/tests/`: the one
    in its directory and in each directory above it up to the tests root. pytest loads
    them without an import edge, so the closure cannot reach them from the target."""
    if TESTS not in target.parents:
        return set()
    found: set[Path] = set()
    directory = target.parent
    while True:
        conftest = directory / "conftest.py"
        if conftest.is_file():
            found.add(conftest)
        if directory == TESTS:
            return found
        directory = directory.parent


def _run_targets(step: Step) -> set[Path]:
    """The mapped Python files `step.action` runs.

    Read from the string constants of the action and of the gate helpers it calls: the
    `-m` modules, the pytest targets, and the scripts, whether written whole or joined
    from `PROJECT_ROOT / "devtools" / "x.py"`. Module-level strings and tuples of strings
    the action names count too, which is how the site tests' list is seen. A pytest
    target brings the `conftest.py` files pytest loads for it (PR 507 review A6).
    """
    strings: set[str] = set()
    seen: set[types.FunctionType] = set()
    pending: deque[types.FunctionType] = deque()
    if isinstance(step.action, types.FunctionType):
        pending.append(step.action)
    while pending:
        function = pending.popleft()
        if function in seen:
            continue
        seen.add(function)
        found, names = _strings_and_names(function.__code__)
        strings |= found
        for name in names:
            value: object = getattr(validate, name, None)
            if isinstance(value, types.FunctionType):
                if value.__module__ == validate.__name__ and name not in _RUNNERS:
                    pending.append(value)
            elif isinstance(value, str):
                strings.add(value)
            elif isinstance(value, tuple):
                strings.update(item for item in value if isinstance(item, str))
    files = _mapped_files()
    targets: set[Path] = set()
    for text in strings:
        if _RUN_MODULE.match(text):
            targets |= _module_files(text, files)
        elif _RUN_SCRIPT.match(text):
            targets.add((ROOT / text.partition("::")[0]).resolve())
        elif re.fullmatch(r"\w+\.py", text):
            scripts = [
                directory / text
                for _package, directory in PACKAGE_ROOTS
                if (directory / text).is_file()
            ]
            if len(scripts) == 1:
                targets.add(scripts[0].resolve())
    for target in tuple(targets):
        targets |= _conftests_loaded_for(target)
    return targets


def _import_closure(start: set[Path]) -> set[Path]:
    """`start` and every mapped file reachable from it through the static import graph,
    function-local imports included, as `reachable_tests` builds it."""
    files = _mapped_files()
    reached = set(start)
    pending = deque(start)
    while pending:
        path = pending.popleft()
        imported = _imports_of(path)
        assert imported is not None, f"{path} did not parse"
        for name in imported:
            for target in _module_files(name, files):
                if target not in reached:
                    reached.add(target)
                    pending.append(target)
    return reached


def _unclaimed_closure(step: Step) -> list[str] | None:
    """Repo-relative files in the import closure of what `step` runs that none of its
    patterns claim, or None when the derivation sees no Python the step runs."""
    targets = _run_targets(step)
    if not targets:
        return None
    relative = (
        path.relative_to(reachable_tests.REPO).as_posix() for path in _import_closure(targets)
    )
    return sorted(path for path in relative if not step.reachable_from(path))


def test_every_attributed_step_claims_the_modules_it_runs() -> None:
    """A step's patterns must claim every module it runs and everything those import.

    PR 496 review G1: `*.py` is claimed by the lint floor, so a Python change never
    reaches the whole-gate escape and each narrow step's own patterns are the only thing
    that selects it. Fifteen edit-tier steps imported a file they did not claim -- the
    retained-JSON check parsed through `sqpack.yamlio` and claimed only `retained_json.py`
    -- and a change to that file ran the pre-push floor green without them.

    The closure is the static one `devtools.reachable_tests` builds, lazy imports
    included, so it over-approximates what a run executes; that is the conservative
    side, and the one the attribution policy chooses. The counterpart of
    `test_every_step_is_reachable_from_a_declared_pattern`: that one guards a pattern
    that matches nothing, this one a pattern set that misses an input the step reads.
    """
    silent: set[str] = set()
    unclaimed: dict[str, list[str]] = {}
    for step in STEPS:
        if not step.touches:
            continue
        missing = _unclaimed_closure(step)
        if missing is None:
            silent.add(step.name)
        elif missing:
            unclaimed[step.name] = missing
    assert silent == _RUNS_NO_MAPPED_PYTHON, (
        "a step whose run modules the derivation cannot see is one this contract does "
        f"not hold; derive them or pin the step: {sorted(silent ^ _RUNS_NO_MAPPED_PYTHON)}"
    )
    report = "\n".join(
        f"  {name}: {', '.join(files[:8])}"
        + (f" (+{len(files) - 8} more)" if len(files) > 8 else "")
        for name, files in unclaimed.items()
    )
    assert unclaimed == {}, f"steps whose `touches` miss a module they run or import:\n{report}"


def test_the_run_derivation_sees_modules_pytest_targets_and_scripts() -> None:
    """The positive controls for the derivation: one of each way a step names Python."""
    expected = {
        # `-m` modules in a concurrent command list, a `sqpack` entry point among them.
        "exact verification": {
            "packing/cases/gobel_strip/verify_exact.py",
            "packing/devtools/dilation_corollary.py",
            "packing/src/sqpack/cli/witness.py",
        },
        # A module named through a helper function the action calls.
        "finer-net dilation-limit record, 720 steps": {
            "packing/devtools/dilation_corollary.py"
        },
        # A module held in a local variable.
        "basin event record and replay": {"packing/cases/campaign_smoke/basin_events.py"},
        # pytest targets from a module-level tuple, and the conftest pytest loads for them.
        "site table layout in Chromium": {
            "packing/tests/test_site_homepage.py",
            "packing/tests/conftest.py",
        },
        # A script joined from path parts.
        "lint floor (rust)": {"packing/devtools/check_rust_floor.py"},
    }
    for name, files in expected.items():
        (step,) = [step for step in STEPS if step.name == name]
        targets = {
            path.relative_to(reachable_tests.REPO).as_posix() for path in _run_targets(step)
        }
        assert files <= targets, f"{name}: {sorted(files - targets)} not derived"


def test_an_unclaimed_import_is_detected() -> None:
    """The negative control: the retained-JSON check, claiming only the records it reads."""
    step = Step(
        "synthetic",
        lambda context: validate._module(context, "devtools.check_retained_json"),  # noqa: SLF001
        touches=("*.json",),
    )
    unclaimed = _unclaimed_closure(step)
    assert unclaimed is not None
    assert {
        "packing/devtools/__init__.py",
        "packing/devtools/check_retained_json.py",
        "packing/src/sqpack/yamlio.py",
    } <= set(unclaimed)
    claimed = Step(
        "synthetic", step.action, touches=("packing/devtools/*", "packing/src/sqpack/*")
    )
    assert _unclaimed_closure(claimed) == []


def test_every_step_that_runs_pytest_claims_the_conftests_pytest_loads() -> None:
    """pytest loads `conftest.py` without an import edge, so the closure could not see
    it from a test target: the three steps that run pytest targets did not claim it, and
    a change to it selected none of them (PR 507 review A6). `_run_targets` now adds each
    conftest pytest loads for a target, which the closure contract holds; this is the
    readable statement of what that covers, with its negative control."""
    conftest = "packing/tests/conftest.py"
    assert (REPO / conftest).is_file()
    running_pytest = {
        step.name
        for step in STEPS
        if step.touches and any(TESTS in target.parents for target in _run_targets(step))
    }
    assert running_pytest >= {
        "browser floor liveness tests",
        "site table layout in Chromium",
        "n17 branch-and-bound native (Rust)",
    }
    selected = {step.name for step in select_for_paths([conftest]).steps}
    assert running_pytest <= selected, sorted(running_pytest - selected)
    # The negative control: a step that claims its test file and not the conftest.
    step = Step(
        "synthetic",
        lambda context: validate._run(context, ("pytest", "tests/test_site_homepage.py")),  # noqa: SLF001
        touches=("packing/tests/test_site_homepage.py",),
    )
    targets = {path.relative_to(reachable_tests.REPO).as_posix() for path in _run_targets(step)}
    assert targets == {"packing/tests/test_site_homepage.py", conftest}
    assert conftest in (_unclaimed_closure(step) or [])
    claimed = Step("synthetic", step.action, touches=("packing/tests/*",))
    assert conftest not in (_unclaimed_closure(claimed) or [])


def _defined_in(step: Step) -> str:
    """The repository-relative file of the module `step.action` is defined in."""
    action: object = getattr(step.action, "func", step.action)  # a partial's function
    module = inspect.getmodule(action)
    assert module is not None, f"{step.name}: its action has no module"
    assert module.__file__, f"{step.name}: its action's module has no file"
    return Path(module.__file__).resolve().relative_to(reachable_tests.REPO).as_posix()


def test_every_attributed_step_claims_the_module_that_defines_its_action() -> None:
    """An edit to a step's action -- its command list, what it requires of the output --
    must select the step, so every attributed step claims the module its action is
    defined in. The steps that run mapped Python reach `validate.py` through `_CORE` or
    `*.py`; the four that run none claimed only their inputs, and an edit to
    `_browser_floor`'s command list passed `--push` without running it (PR 507 review A7).
    """
    unclaimed = {
        step.name: _defined_in(step)
        for step in STEPS
        if step.touches and not step.reachable_from(_defined_in(step))
    }
    assert unclaimed == {}, (
        f"steps whose `touches` miss the module defining their action: {unclaimed}"
    )
    # The negative control: the browser floor's action, claiming only an input.
    step = Step("synthetic", validate._browser_floor, touches=("biome.json",))  # noqa: SLF001
    assert _defined_in(step) == "packing/src/sqpack/cli/validate.py"
    assert not step.reachable_from(_defined_in(step))
    claimed = Step("synthetic", step.action, touches=("biome.json", *validate._GATE))  # noqa: SLF001
    assert claimed.reachable_from(_defined_in(claimed))


def test_the_three_under_selections_review_g_reproduced() -> None:
    """PR 496 review G1's reproductions, each a step dropped by a file it imports."""
    cases = {
        "packing/src/sqpack/yamlio.py": {
            "retained JSON is one record per line",
            "published URL registry and historical compatibility",
        },
        "packing/devtools/audit_wand125_declared_net.py": {"FN1 original-input bindings"},
        "packing/devtools/__init__.py": {
            "FN1 original-input bindings",
            "class records do not claim the unconditional bound",
            "retained JSON is one record per line",
        },
    }
    for path, expected in cases.items():
        selection = select_for_paths([path])
        assert not selection.is_whole_gate, path
        names = {step.name for step in selection.steps}
        assert expected <= names, f"changing {path} must select {sorted(expected - names)}"


def test_push_paths_include_committed_and_worktree_renames_deletions_and_additions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An attributed source moved out of its subtree must still select its old consumers."""
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }

    def git(*args: str) -> str:
        return subprocess.run(
            ("git", "-c", "commit.gpgsign=false", "-c", f"core.hooksPath={os.devnull}", *args),
            cwd=tmp_path,
            env=environment,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    git("init", "-q")
    for name in ("old.py", "staged-old.py", "deleted.py", "edited.py"):
        (tmp_path / name).write_text(name)
    git("add", ".")
    git(
        "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "base"
    )
    base = git("rev-parse", "HEAD")
    (tmp_path / "old.py").rename(tmp_path / "renamed.py")
    git("add", "-A")
    git(
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "rename",
    )
    (tmp_path / "staged-old.py").rename(tmp_path / "staged-new.py")
    git("add", "-A")
    (tmp_path / "deleted.py").unlink()
    (tmp_path / "edited.py").write_text("changed")
    (tmp_path / "untracked é\n.py").write_text("new")
    monkeypatch.setattr(validate, "REPOSITORY_ROOT", tmp_path)
    for key in tuple(os.environ):
        if key.startswith("GIT_"):
            monkeypatch.delenv(key)
    assert validate.changed_paths(base) == sorted(
        [
            "old.py",
            "renamed.py",
            "staged-old.py",
            "staged-new.py",
            "deleted.py",
            "edited.py",
            "untracked é\n.py",
        ]
    )
    with pytest.raises(validate.UsageError, match="failed"):
        validate.changed_paths("edited.py")
