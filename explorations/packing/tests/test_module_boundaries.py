"""Architecture contracts for the packing project's code-maturity layers."""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest
import yaml

from devtools.check_readme import meaningful_top_level_entries
from sqpack.project import ProjectLayoutError, require_project_root

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src" / "sqpack"
VALIDATION_WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "packing-validation.yml"
PYTHON_VERSION = PROJECT_ROOT / ".python-version"


def _mapping(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return cast("dict[str, object]", value)


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    return imported


def _assert_imports_exclude(paths: list[Path], forbidden: tuple[str, ...]) -> None:
    violations = [
        f"{path.relative_to(PROJECT_ROOT)} imports {imported}"
        for path in paths
        for imported in sorted(_imports(path))
        if imported.startswith(forbidden)
    ]
    assert violations == []


def _process_module_references(path: Path) -> set[str]:
    """Literal Python modules named across a subprocess boundary."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance((value := node.value), str)
        and re.fullmatch(r"(?:cases|devtools)(?:\.[a-zA-Z_][a-zA-Z0-9_]*)+", value)
    }


def test_code_is_segregated_by_maturity_and_dependencies_flow_one_way() -> None:
    required = [
        SOURCE_ROOT,
        SOURCE_ROOT / "research",
        SOURCE_ROOT / "campaign",
        SOURCE_ROOT / "cli",
        PROJECT_ROOT / "cases",
        PROJECT_ROOT / "devtools",
    ]
    assert [path.relative_to(PROJECT_ROOT) for path in required if not path.is_dir()] == []

    reusable = list(SOURCE_ROOT.glob("*.py"))
    research = list((SOURCE_ROOT / "research").glob("*.py"))
    campaign = list((SOURCE_ROOT / "campaign").glob("*.py"))
    cli = list((SOURCE_ROOT / "cli").glob("*.py"))

    _assert_imports_exclude(
        reusable,
        ("sqpack.research", "sqpack.campaign", "cases", "devtools"),
    )
    _assert_imports_exclude(research, ("sqpack.campaign", "cases", "devtools"))
    _assert_imports_exclude(campaign, ("cases", "devtools"))
    _assert_imports_exclude(cli, ("cases", "devtools"))

    assert {
        reference
        for path in reusable + research + campaign
        for reference in _process_module_references(path)
    } == set()
    cli_process_edges = {
        reference for path in cli for reference in _process_module_references(path)
    }
    assert any(reference.startswith("cases.") for reference in cli_process_edges)
    assert any(reference.startswith("devtools.") for reference in cli_process_edges)


def test_repository_applications_fail_clearly_without_a_project_checkout(
    tmp_path: Path,
) -> None:
    with pytest.raises(ProjectLayoutError, match="PACKING_PROJECT_ROOT"):
        require_project_root(tmp_path)


@pytest.mark.parametrize(
    ("module", "arguments"),
    [
        ("sqpack.cli.validate", ["--list"]),
        ("sqpack.cli.witness", ["inspect", "missing.yaml"]),
        ("sqpack.campaign.runner", ["status"]),
        ("sqpack.campaign.ledger", ["check"]),
    ],
)
def test_repository_application_entrypoints_reject_an_invalid_explicit_root(
    tmp_path: Path, module: str, arguments: list[str]
) -> None:
    environment = os.environ.copy()
    environment["PACKING_PROJECT_ROOT"] = str(tmp_path)

    completed = subprocess.run(
        [sys.executable, "-m", module, *arguments],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode != 0
    assert "packing project checkout not found" in completed.stderr
    assert "PACKING_PROJECT_ROOT" in completed.stderr


def test_no_python_implementation_remains_in_ambiguous_legacy_locations() -> None:
    legacy = [
        *PROJECT_ROOT.glob("*.py"),
        *(PROJECT_ROOT / "tools").glob("*.py"),
        *(PROJECT_ROOT / "campaign").glob("*.py"),
        *(PROJECT_ROOT / "sqpack").rglob("*.py"),
    ]
    assert [path.relative_to(PROJECT_ROOT) for path in legacy] == []


def test_no_bash_or_shell_entry_points_remain() -> None:
    scripts = [
        path
        for pattern in ("*.sh", "*.bash")
        for path in PROJECT_ROOT.rglob(pattern)
        if not any(part.startswith(".") for part in path.relative_to(PROJECT_ROOT).parts)
    ]
    assert [path.relative_to(PROJECT_ROOT) for path in scripts] == []


def test_readme_inventory_ignores_cache_only_legacy_directories(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    (repository / "README.md").write_text("# Example\n", encoding="utf-8")
    (repository / "current").mkdir()
    (repository / "current" / "module.py").write_text("", encoding="utf-8")
    cache = repository / "tools" / "__pycache__"
    cache.mkdir(parents=True)
    (cache / "removed.cpython-314.pyc").write_bytes(b"ignored")

    assert meaningful_top_level_entries(repository) == {"README.md", "current"}


def test_ci_jobs_fetch_provenance_history_and_key_the_uv_cache_from_the_lock() -> None:
    document: object = yaml.safe_load(VALIDATION_WORKFLOW.read_text(encoding="utf-8"))
    jobs = _mapping(_mapping(document)["jobs"])

    assert PYTHON_VERSION.read_text(encoding="utf-8").strip() == "3.14.7"

    for job_name in ("validate", "macos-portability"):
        raw_steps = _mapping(jobs[job_name])["steps"]
        assert isinstance(raw_steps, list)
        steps = [_mapping(step) for step in raw_steps]

        checkout = next(
            step for step in steps if str(step.get("uses", "")).startswith("actions/checkout@")
        )
        assert _mapping(checkout["with"])["fetch-depth"] == 0

        setup_uv = next(
            step
            for step in steps
            if str(step.get("uses", "")).startswith("astral-sh/setup-uv@")
        )
        setup_options = _mapping(setup_uv["with"])
        assert setup_options["python-version"] == "3.14.7"
        assert setup_options["working-directory"] == "explorations/packing"
        assert setup_options["cache-dependency-glob"] == "uv.lock"

        environment_commands = [
            str(step["run"])
            for step in steps
            if isinstance(step.get("run"), str)
            and str(step["run"]).startswith(("uv sync", "uv run"))
        ]
        assert environment_commands
        assert all("--all-extras" in command for command in environment_commands)

    triggers = _mapping(_mapping(document)["on"])
    assert "workflow_dispatch" in triggers
    assert "schedule" in triggers
    assert triggers["pull_request"] == {}

    validate_steps = _mapping(jobs["validate"])["steps"]
    assert isinstance(validate_steps, list)
    required_step = next(
        _mapping(step)
        for step in validate_steps
        if _mapping(step).get("name") == "Run the required pull-request surface"
    )
    assert required_step["if"] == "github.event_name == 'pull_request'"
    assert " ".join(str(required_step["run"]).split()) == (
        "uv run --frozen --all-extras --group dev packing-validate --fast "
        "--jobs 2 --inner-jobs 1"
    )
    full_step = next(
        _mapping(step)
        for step in validate_steps
        if _mapping(step).get("name") == "Run the complete integration surface"
    )
    assert full_step["if"] == "github.event_name != 'pull_request'"
    assert " ".join(str(full_step["run"]).split()) == (
        "uv run --frozen --all-extras --group dev packing-validate --jobs 2 --inner-jobs 2"
    )

    required_job = _mapping(jobs["packing-required"])
    assert required_job["needs"] == "validate"
    assert required_job["if"] == ("always() && github.event_name == 'pull_request'")
    assert "continue-on-error" not in required_job
    required_job_steps = required_job["steps"]
    assert isinstance(required_job_steps, list)
    required_command = " ".join(str(_mapping(required_job_steps[0])["run"]).split())
    assert required_command == 'test "$VALIDATE_RESULT" = "success"'

    mac_steps = _mapping(jobs["macos-portability"])["steps"]
    assert isinstance(mac_steps, list)
    mac_job = _mapping(jobs["macos-portability"])
    assert mac_job["if"] == "github.event_name != 'pull_request'"
    assert "continue-on-error" not in mac_job
    assert all("continue-on-error" not in _mapping(step) for step in mac_steps)
    mac_full_step = next(
        _mapping(step)
        for step in mac_steps
        if _mapping(step).get("name")
        == "Run the complete packing validation surface on a second architecture"
    )
    assert " ".join(str(mac_full_step["run"]).split()) == (
        "uv run --frozen --all-extras --group dev packing-validate --jobs 2 --inner-jobs 2"
    )
    deep_probes = [
        _mapping(step)
        for step in mac_steps
        if _mapping(step).get("name") == "Run the focused deep-golden portability check"
    ]
    assert len(deep_probes) == 1
    deep_command = " ".join(str(deep_probes[0]["run"]).split())
    assert deep_command == (
        "uv run --frozen --all-extras --group dev packing-validate --deep "
        '--only "golden basin maps" --jobs 1 --inner-jobs 1'
    )
    assert all(
        "check_known_macos_golden_drift" not in str(_mapping(step).get("run", ""))
        for step in mac_steps
    )


def test_exhaustive_exact_marker_is_declared_only_by_measured_slow_nodes() -> None:
    expected = {
        "test_exact_jets.py": {
            "test_n5_wall_and_contact_gradients_match_authoritative_source_rows",
        },
        "test_minus_w_row_jets.py": {
            "test_owner_rows_match_complete_authoritative_inventory",
            "test_active_rows_expose_both_owner_alternatives",
            "test_sat_row_retains_exact_center_angle_cross_curvature",
        },
        "test_minus_w_sheet.py": {
            "test_positive_sheet_path_checks_all_seventeen_rows_for_both_owners",
            "test_bad_center_correction_is_rejected_by_same_row_evaluator",
        },
        "test_minus_w_stress.py": {
            "test_w_curvature_is_even_nonzero_and_quadratically_scaled",
            "test_real_production_weight_perturbation_breaks_cancellation",
            "test_uniform_weight_rescaling_fails_exact_normalization",
        },
    }
    declared: dict[str, set[str]] = {}
    marker = "pytest.mark.exhaustive_exact"
    for path in (PROJECT_ROOT / "tests").glob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        marked: set[str] = set()
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(
                ast.unparse(decorator) == marker for decorator in node.decorator_list
            ):
                marked.add(node.name)
            if isinstance(
                node, (ast.Assign, ast.AnnAssign)
            ) and "exhaustive_exact" in ast.unparse(node):
                marked.add("<module-level assignment>")
        if marked:
            declared[path.name] = marked

    assert declared == expected


def test_devtools_use_public_package_interfaces() -> None:
    violations: list[str] = []
    path = PROJECT_ROOT / "devtools" / "check_canonical.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        if node.module.startswith("sqpack"):
            violations.extend(
                f"{path.relative_to(PROJECT_ROOT)} imports {alias.name}"
                for alias in node.names
                if alias.name.startswith("_")
            )
    assert violations == []
