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
ESLINT = REPOSITORY_ROOT / "node_modules/.bin/eslint"
ESLINT_CONFIG = REPOSITORY_ROOT / "packages/workbench/eslint.config.js"
TSC = REPOSITORY_ROOT / "node_modules/.bin/tsc"
ROOT_PACKAGE = REPOSITORY_ROOT / "package.json"
WORKBENCH_PACKAGE = REPOSITORY_ROOT / "packages/workbench/package.json"

#: The lint rules the shared floor names, each of which the recommended preset does NOT
#: enable on its own. That is the whole reason they are written out: a project that only
#: says `"recommended"` is below the floor and looks configured.
REQUIRED_RULES = {
    ("style", "useBlockStatements"),
    ("style", "useImportType"),
    ("correctness", "noUnusedVariables"),
    ("correctness", "noUnusedImports"),
    ("nursery", "noFloatingPromises"),
    ("nursery", "noMisusedPromises"),
    ("nursery", "useAwaitThenable"),
}

PROMISE_RULES = (
    "@typescript-eslint/await-thenable",
    "@typescript-eslint/no-floating-promises",
    "@typescript-eslint/no-misused-promises",
)

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
SCRIPT_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts")


def _jsonc(path: Path) -> dict[str, Any]:
    """Read a config that may carry comments, which `tsconfig.json` is entitled to."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
    return json.loads(text)


def _tracked(*patterns: str) -> list[str]:
    listed = subprocess.run(
        [
            "git",
            "-C",
            str(REPOSITORY_ROOT),
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            *patterns,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return [
        line for line in listed.stdout.splitlines() if line and not line.startswith(NOT_OURS)
    ]


def _tsconfigs() -> list[Path]:
    return sorted(REPOSITORY_ROOT.glob("tsconfig*.json")) + sorted(
        (REPOSITORY_ROOT / "packages/workbench").glob("tsconfig*.json")
    )


def _include_pattern(config: Path, pattern: str) -> str:
    parent = config.parent.relative_to(REPOSITORY_ROOT).as_posix()
    rooted = f"{parent}/{pattern}" if parent != "." else pattern
    return rooted.replace("**/*", "*")


def _covered_scripts(configs: list[Path]) -> set[str]:
    return {
        path
        for config in configs
        for pattern in _jsonc(config).get("include", [])
        for path in _tracked(_include_pattern(config, pattern))
    }


def _relaxed_flags(config: Path) -> list[str]:
    options = _jsonc(config).get("compilerOptions", {})
    return sorted(
        flag for flag, value in options.items() if value is False and flag != "noEmit"
    )


def test_biome_names_every_floor_rule() -> None:
    config = _jsonc(BIOME_CONFIG)
    rules = config["linter"]["rules"]
    assert rules["preset"] == "recommended", "the floor is the recommended preset plus more"
    for group, rule in sorted(REQUIRED_RULES):
        assert rules.get(group, {}).get(rule) == "error", (
            f"{group}.{rule} is not set to error in biome.json; "
            "the recommended preset does not enable it, which is why the floor names it"
        )
    organize = _jsonc(BIOME_CONFIG)["assist"]["actions"]["source"]["organizeImports"]
    assert organize == "on", "import ordering is part of the floor"
    includes = config["files"]["includes"]
    for suffix in (*SCRIPT_SUFFIXES, ".css"):
        assert f"**/*{suffix}" in includes, f"Biome does not include {suffix} source"
    assert "packages/workbench/**/*.json" in includes


def test_the_node_toolchain_is_exactly_pinned_and_runtime_bounded() -> None:
    root = _jsonc(ROOT_PACKAGE)
    workbench = _jsonc(WORKBENCH_PACKAGE)
    assert root["engines"]["node"] == workbench["engines"]["node"] == ">=24.18.0 <25"
    assert (REPOSITORY_ROOT / ".node-version").read_text(encoding="utf-8").strip() == "24.18.0"
    assert root["devDependencies"]["typescript"] == "6.0.2"
    assert workbench["devDependencies"] == {
        "@types/node": "24.13.3",
        "esbuild": "0.28.2",
        "eslint": "10.9.0",
        "typescript": "6.0.2",
        "typescript-eslint": "8.68.0",
    }


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
        "the retained browser programs are checked JavaScript; without "
        f"{missing_js} their type gates check nothing"
    )
    for config in _tsconfigs():
        if config.name == "tsconfig.base.json":
            continue
        extends = _jsonc(config).get("extends")
        assert isinstance(extends, str)
        assert (config.parent / extends).resolve() == base.resolve(), (
            f"{config.relative_to(REPOSITORY_ROOT)} does not extend the shared base"
        )


def test_every_relaxed_flag_names_its_tracker() -> None:
    """Floor rule 8: legacy code ratchets toward strict. A flag turned off without a
    tracked issue is not a ratchet, it is a lower floor."""
    for config in _tsconfigs():
        relaxed = _relaxed_flags(config)
        if not relaxed:
            continue
        assert TRACKER.search(config.read_text(encoding="utf-8")), (
            f"{config.name} relaxes {relaxed} and names no tracking issue"
        )


def test_every_first_party_script_is_in_a_type_program() -> None:
    """A file under the lint floor but in no `tsconfig` include is half covered, and the
    half that is missing is the one that catches type errors."""
    covered = _covered_scripts(_tsconfigs())
    tracked = _tracked(*(f"*{suffix}" for suffix in SCRIPT_SUFFIXES))
    uncovered = sorted(set(tracked) - covered)
    assert not uncovered, f"tracked JavaScript in no type-check program: {uncovered}"


def test_the_package_program_is_required_for_package_typescript() -> None:
    source = "packages/workbench/src/index.ts"
    configs = _tsconfigs()
    assert source in _covered_scripts(configs)
    assert source not in _covered_scripts(
        [config for config in configs if config.parent == REPOSITORY_ROOT]
    )


def test_an_untracked_relaxation_is_detected() -> None:
    with tempfile.TemporaryDirectory() as scratch:
        config = Path(scratch) / "tsconfig.json"
        config.write_text(
            json.dumps({"compilerOptions": {"strictNullChecks": False}}), encoding="utf-8"
        )
        assert _relaxed_flags(config) == ["strictNullChecks"]
        assert TRACKER.search(config.read_text(encoding="utf-8")) is None


@pytest.mark.skipif(not ESLINT.is_file(), reason="run `npm ci` at the repository root")
def test_the_checked_javascript_promise_overlay_is_effective() -> None:
    representatives = (
        "packing/atlas/known-best/video/spikes/v2-transitions/assets/workbench.js",
        "packing/atlas/known-best/video/spikes/v2-transitions/probes/api/apply.js",
        "packing/src/sqpack/motion_lab/assets/free-quench.js",
        "packing/atlas/known-best/video/spikes/v1-slideshow/timeline_harness.js",
    )
    for source in representatives:
        configured = subprocess.run(
            [
                str(ESLINT),
                "--print-config",
                source,
                "--config",
                str(ESLINT_CONFIG),
            ],
            check=True,
            capture_output=True,
            text=True,
            cwd=REPOSITORY_ROOT,
        )
        rules = json.loads(configured.stdout)["rules"]
        for rule in PROMISE_RULES:
            assert rules[rule][0] == 2, f"{source}: {rule} is below error severity"


@pytest.mark.skipif(not ESLINT.is_file(), reason="run `npm ci` at the repository root")
def test_the_checked_javascript_overlay_rejects_a_floating_promise() -> None:
    assets = REPOSITORY_ROOT / "packing/atlas/known-best/video/spikes/v2-transitions/assets"
    with tempfile.TemporaryDirectory(dir=assets) as scratch:
        sample = Path(scratch) / "floating-promise.js"
        sample.write_text(
            "/** @returns {Promise<void>} */\nasync function later() {}\nlater();\n",
            encoding="utf-8",
        )
        done = subprocess.run(
            [str(ESLINT), str(sample), "--config", str(ESLINT_CONFIG)],
            check=False,
            capture_output=True,
            text=True,
            cwd=REPOSITORY_ROOT,
        )
    assert done.returncode != 0, "ESLint accepted a floating Promise in checked JavaScript"
    assert "@typescript-eslint/no-floating-promises" in done.stdout + done.stderr


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
