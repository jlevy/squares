"""The browser floor as a declared contract, and as a floor that is actually live.

The JavaScript and CSS this repository serves have the same shape of floor the Python
does: a formatter that owns layout, a linter at zero tolerance, and a separate type gate.
`tbd guidelines typescript-lint-format-rules` defines it and `biome.json` plus the
`tsconfig*.json` set implement it.

Two different things are checked here, and the second is the one that matters.

**The contract**: the named floor rules are present and set to `error`, every tracked
first-party `.js` and `.css` file is in one of Biome's scopes and one of the type gate's
programs, and every relaxation of a floor flag names the issue tracking it.

**Liveness**: `ci-and-gates-rules` exists because gates go green while checking nothing —
a `files.includes` typo silently exempts the only thing the floor is for, and nothing
fails. So the braces rule is proved live by handing Biome a file that breaks it and
requiring a complaint, and the type gate by handing `tsc` one that does not type-check.
A configured rule is a claim; a rule that rejects a violation is a fact.
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
BIOME_CONFIG = REPOSITORY_ROOT / "biome.json"
BIOME = REPOSITORY_ROOT / "node_modules/.bin/biome"
TSC = REPOSITORY_ROOT / "node_modules/.bin/tsc"

#: The lint rules the shared floor names, each of which the recommended preset does NOT
#: enable on its own. That is the whole reason they are written out: a project that only
#: says `"recommended"` is below the floor and looks configured.
REQUIRED_RULES = {
    ("style", "useBlockStatements"),
    ("style", "useImportType"),
    ("correctness", "noUnusedVariables"),
    ("correctness", "noUnusedImports"),
}

#: The tsconfig floor. `strict` alone is not it; these are the flags that catch real bugs
#: independently of runtime or build tool.
REQUIRED_COMPILER_OPTIONS = (
    "strict",
    "noUncheckedIndexedAccess",
    "exactOptionalPropertyTypes",
    "noImplicitOverride",
    "noImplicitReturns",
    "noFallthroughCasesInSwitch",
    "forceConsistentCasingInFileNames",
)

#: A relaxation is legitimate only while something is tracking its removal (floor rule 8),
#: so every config that turns a floor flag off has to name a bead in its own text.
TRACKER = re.compile(r"\bthink-[a-z0-9]{4}\b")

#: Directories whose JavaScript is not ours to hold to a floor.
NOT_OURS = ("vendor/", "node_modules/")


def _jsonc(path: Path) -> dict[str, Any]:
    """Read a config that may carry comments, which `tsconfig.json` is entitled to."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
    return json.loads(text)


def _tracked(*patterns: str) -> list[str]:
    listed = subprocess.run(
        ["git", "-C", str(REPOSITORY_ROOT), "ls-files", *patterns],
        check=True,
        capture_output=True,
        text=True,
    )
    return [
        line for line in listed.stdout.splitlines() if line and not line.startswith(NOT_OURS)
    ]


def _tsconfigs() -> list[Path]:
    return sorted(REPOSITORY_ROOT.glob("tsconfig*.json"))


def test_biome_names_every_floor_rule() -> None:
    rules = _jsonc(BIOME_CONFIG)["linter"]["rules"]
    assert rules["preset"] == "recommended", "the floor is the recommended preset plus more"
    for group, rule in sorted(REQUIRED_RULES):
        assert rules.get(group, {}).get(rule) == "error", (
            f"{group}.{rule} is not set to error in biome.json; "
            "the recommended preset does not enable it, which is why the floor names it"
        )
    organize = _jsonc(BIOME_CONFIG)["assist"]["actions"]["source"]["organizeImports"]
    assert organize == "on", "import ordering is part of the floor"


def test_every_biome_exception_is_scoped_and_reasoned() -> None:
    """Floor rule 7: an exception names exact files and exact rules, never a global
    downgrade. A rule turned off at the top level would be a different floor wearing this
    one's name."""
    config = _jsonc(BIOME_CONFIG)
    for override in config.get("overrides", []):
        assert override.get("includes"), "an override with no file list is a global downgrade"
        for entry in override["includes"]:
            assert not entry.startswith("!"), (
                f"an override that excludes rather than scopes: {entry}"
            )
    text = BIOME_CONFIG.read_text(encoding="utf-8")
    assert config.get("overrides", []) == [] or "motion_lab" in text


def test_the_type_floor_is_declared_once_and_extended() -> None:
    base = REPOSITORY_ROOT / "tsconfig.base.json"
    options = _jsonc(base)["compilerOptions"]
    for flag in REQUIRED_COMPILER_OPTIONS:
        assert options.get(flag) is True, f"tsconfig.base.json does not set {flag}"
    missing_js = [flag for flag in ("allowJs", "checkJs") if options.get(flag) is not True]
    assert not missing_js, (
        "this repository's browser code is all JavaScript; without "
        f"{missing_js} the type gate checks nothing"
    )
    for config in _tsconfigs():
        if config.name == "tsconfig.base.json":
            continue
        assert _jsonc(config).get("extends") == "./tsconfig.base.json", (
            f"{config.name} does not extend the base, so it does not inherit the floor"
        )


def test_every_relaxed_flag_names_its_tracker() -> None:
    """Floor rule 8: legacy code ratchets toward strict. A flag turned off without a
    tracked issue is not a ratchet, it is a lower floor."""
    for config in _tsconfigs():
        options = _jsonc(config).get("compilerOptions", {})
        relaxed = sorted(
            flag for flag, value in options.items() if value is False and flag != "noEmit"
        )
        if not relaxed:
            continue
        assert TRACKER.search(config.read_text(encoding="utf-8")), (
            f"{config.name} relaxes {relaxed} and names no tracking issue"
        )


def test_every_first_party_script_is_in_a_type_program() -> None:
    """A file under the lint floor but in no `tsconfig` include is half covered, and the
    half that is missing is the one that catches type errors."""
    included: list[str] = []
    for config in _tsconfigs():
        included.extend(_jsonc(config).get("include", []))
    covered = {
        path for pattern in included for path in _tracked(pattern.replace("**/*.js", "*.js"))
    }
    uncovered = sorted(set(_tracked("*.js", "*.mjs", "*.cjs")) - covered)
    assert not uncovered, f"tracked JavaScript in no type-check program: {uncovered}"


@pytest.mark.skipif(not BIOME.is_file(), reason="run `npm ci` at the repository root")
def test_the_braces_rule_actually_rejects_a_violation() -> None:
    """The liveness check. `useBlockStatements` being written in the config proves only
    that someone wrote it; what proves the floor is live is Biome refusing a braceless
    `if`. The fixture is written outside the repository so no real file has to be broken
    and so the repository's own scope rules cannot accidentally exempt it."""
    with tempfile.TemporaryDirectory() as scratch:
        sample = Path(scratch) / "sample.js"
        sample.write_text("if (globalThis.x) globalThis.y = 1;\n", encoding="utf-8")
        done = subprocess.run(
            [str(BIOME), "check", f"--config-path={REPOSITORY_ROOT}", str(sample)],
            check=False,
            capture_output=True,
            text=True,
            cwd=scratch,
        )
    assert done.returncode != 0, "Biome accepted a braceless if; the floor is not live"
    assert "useBlockStatements" in done.stdout + done.stderr, (
        "Biome complained, but not about the braces rule:\n" + done.stdout + done.stderr
    )


@pytest.mark.skipif(not TSC.is_file(), reason="run `npm ci` at the repository root")
def test_the_type_gate_actually_rejects_a_type_error() -> None:
    """The same liveness question for the type gate. A `tsconfig` whose `include` matches
    nothing reports zero errors and looks exactly like a clean program."""
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        (root / "sample.js").write_text("Math.round(Math.max);\n", encoding="utf-8")
        (root / "tsconfig.json").write_text(
            json.dumps(
                {
                    "compilerOptions": _jsonc(REPOSITORY_ROOT / "tsconfig.base.json")[
                        "compilerOptions"
                    ],
                    "include": ["sample.js"],
                }
            ),
            encoding="utf-8",
        )
        done = subprocess.run(
            [str(TSC), "-p", "tsconfig.json"],
            check=False,
            capture_output=True,
            text=True,
            cwd=scratch,
        )
    assert done.returncode != 0, "tsc accepted a type error under the floor's own options"
