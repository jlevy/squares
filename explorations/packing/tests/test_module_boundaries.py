"""Architecture contracts for the packing project's code-maturity layers."""

from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src" / "sqpack"


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
