"""The lint and type floors as declared contracts: one runtime, the rule families the
project has argued for, and every tracked Python file under a gate or on a named list.

`pyproject.toml` is read rather than trusted, and the file inventory comes from git, so a
new directory of Python that neither ruff nor basedpyright reaches fails here before it
fails by surprise.
"""

from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path
from typing import cast

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
PYPROJECT = PROJECT_ROOT / "pyproject.toml"

#: Rule families the floor enables, each argued for in `pyproject.toml` beside its entry.
REQUIRED_FAMILIES = {
    "F", "E", "W", "I", "UP", "B", "A", "ARG", "BLE", "C4", "C90", "DTZ", "EM", "ERA",
    "FBT", "FLY", "FURB", "ICN", "ISC", "LOG", "N", "PERF", "PIE", "PL", "PT", "PTH",
    "PYI", "RET", "RSE", "RUF", "SIM", "SLF", "T20", "TID", "TRY",
}  # fmt: skip

#: Tracked Python that is deliberately outside both gates, with the reason it stays out.
NAMED_EXCLUSIONS = {
    # The literature archive holds other authors' verifier scripts as downloaded.
    "packing/resources/": "archived third-party source, never edited to look tidy",
    # An independent reviewer's file, retained verbatim as evidence.
    "packing/cases/n12_fractional_certificate/independent_verify.py": (
        "independent reviewer's verifier, checked by being run"
    ),
    # A byte-identical mirror of `.agents/skills`, kept by `make skills-sync` and
    # compared by `make skills-check`; linting the source copy covers it.
    ".claude/skills/": "mirror of .agents/skills",
}


def _mapping(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return cast("dict[str, object]", value)


def _config() -> dict[str, object]:
    return tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))


def _tool(name: str) -> dict[str, object]:
    return _mapping(_mapping(_config()["tool"])[name])


def _tracked_python() -> list[str]:
    listing = subprocess.run(
        ["git", "ls-files", "--", "*.py", "*.pyi"],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in listing.stdout.splitlines() if line]


def _handwritten_skills() -> list[str]:
    text = (REPOSITORY_ROOT / "Makefile").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("HANDWRITTEN_SKILLS"):
            return line.split(":=", 1)[1].split()
    raise AssertionError("Makefile does not declare HANDWRITTEN_SKILLS")


def test_one_runtime_is_declared_everywhere() -> None:
    project = _mapping(_config()["project"])
    pyright = _tool("basedpyright")
    assert project["requires-python"] == ">=3.14,<3.15"
    assert _tool("ruff")["target-version"] == "py314"
    assert pyright["pythonVersion"] == "3.14"
    assert pyright["typeCheckingMode"] == "standard"
    pinned = (PROJECT_ROOT / ".python-version").read_text(encoding="utf-8").strip()
    assert pinned.startswith("3.14")


def test_the_rule_families_are_enabled_and_print_is_a_checked_boundary() -> None:
    lint = _mapping(_tool("ruff")["lint"])
    select = lint["select"]
    ignore = lint["ignore"]
    assert isinstance(select, list)
    assert isinstance(ignore, list)
    assert set(select) >= REQUIRED_FAMILIES
    assert "T201" not in ignore
    # Every place printing is allowed is a tool, named one directory or module at a time.
    waived = {
        path
        for path, rules in _mapping(lint["per-file-ignores"]).items()
        if isinstance(rules, list) and "T201" in rules
    }
    assert waived == {
        "devtools/*",
        "cases/*",
        "tests/*",
        "benchmarks/*",
        "frankensim-probe/*",
        "src/sqpack/cli/*",
        "src/sqpack/campaign/runner.py",
        "src/sqpack/campaign/ledger.py",
    }
    ceiling = _mapping(lint["mccabe"])["max-complexity"]
    assert isinstance(ceiling, int)
    assert ceiling <= 57


def test_every_tracked_python_file_is_under_a_gate_or_named() -> None:
    """Ruff walks `packing/` and the hand-written skills; basedpyright walks its
    `include` list. Anything tracked that neither reaches must be on the named list."""
    ruff = _tool("ruff")
    pyright = _tool("basedpyright")
    ruff_exclude = ruff["extend-exclude"]
    include = pyright["include"]
    exclude = pyright["exclude"]
    assert isinstance(ruff_exclude, list)
    assert isinstance(include, list)
    assert isinstance(exclude, list)
    ruff_excluded = [f"packing/{entry}" for entry in ruff_exclude]
    pyright_included = [
        str((PROJECT_ROOT / entry).resolve().relative_to(REPOSITORY_ROOT)) for entry in include
    ]
    pyright_excluded = [
        f"packing/{entry}" for entry in exclude if not entry.startswith((".", "**"))
    ]
    skills = [f".agents/skills/{name}" for name in _handwritten_skills()]

    def under(path: str, roots: list[str]) -> bool:
        return any(path == root or path.startswith(root.rstrip("/") + "/") for root in roots)

    unreached: list[str] = []
    for path in _tracked_python():
        if path.startswith("vendor/"):
            continue  # submodules carry their own tooling
        named = under(path, list(NAMED_EXCLUSIONS))
        linted = (path.startswith("packing/") and not under(path, ruff_excluded)) or under(
            path, skills
        )
        typed = under(path, pyright_included) and not under(path, pyright_excluded)
        if not named and not (linted and typed):
            unreached.append(path)
    assert unreached == []

    # A named exclusion that names nothing tracked is a stale entry, not a contract.
    tracked = _tracked_python()
    for exclusion in NAMED_EXCLUSIONS:
        assert any(under(path, [exclusion]) for path in tracked), exclusion
    for exclusion in ruff_excluded + pyright_excluded:
        assert any(under(path, [exclusion]) for path in tracked), exclusion
    # And every named exclusion is also an exclusion or non-target of both gates.
    for exclusion in NAMED_EXCLUSIONS:
        assert not (
            exclusion.startswith("packing/") and not under(exclusion, ruff_excluded)
        ) or (exclusion in ruff_excluded), exclusion
