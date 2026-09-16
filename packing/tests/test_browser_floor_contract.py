"""The browser floor as a declared contract, and as a floor that is actually live.

The JavaScript and CSS this repository serves have the same shape of floor the Python
does: a formatter that owns layout, a linter at zero tolerance, and a separate type gate.
`tbd guidelines typescript-lint-format-rules` defines it and `biome.json` plus the
`tsconfig*.json` set implement it.

Two different things are checked here, and the second is the one that matters.

**The contract**: the named floor rules are present and set to `error`, every tracked
first-party script and stylesheet is inside the scope Biome actually resolves and inside
one of the type gate's programs, Biome has no override and no rule turned down, ESLint
resolves one configuration for every owned script, `tsc` gives every file its own scope,
no program relaxes a flag outside the declared ratchet, and every relaxation
names an open bead tracking its removal. The floor has no exceptions (owner, 2026-09-14):
the overrides and the file-specific ESLint blocks it once carried went in think-6o9n.

**Liveness**: `ci-and-gates-rules` exists because gates go green while checking nothing —
a `files.includes` typo silently exempts the only thing the floor is for, and nothing
fails. So the braces rule is proved live by handing Biome a file that breaks it and
requiring a complaint, and the type gate by handing `tsc` one that does not type-check.
A configured rule is a claim; a rule that rejects a violation is a fact.

The liveness tests need the pinned Node tools. Locally, a checkout without `npm ci` skips
them; under `CI` a missing tool fails, because a liveness test that skips on the surface
that runs it proves nothing (#125 F20, #160 R19). A workflow check below keeps a Node
toolchain on every job that runs this file.

The samples those tests hand their tools are checked in, under
`packing/tests/fixtures/browser-floor/`, as `.js.txt` data rather than source: each must
fail the floor, so no tool's scope may reach one, and a name that is not a script's keeps
them out with no exclusion, which is what lets the floor have none. The contract holds the
tree to exactly those samples at their sizes. No test writes into the source tree: the
ESLint probe reads its sample on stdin under an in-scope `--stdin-filename`, and Biome and
`tsc` read a copy named as JavaScript under pytest's `tmp_path`, so nothing here can race a
test that lists the tree (#160 R18).
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from typing import Any

import pytest
from nodejs_wheel import node

from devtools.check_bead_tree import ISSUES, MAPPINGS, REFS, parse_aliases
from sqpack.cli import validate
from sqpack.yamlio import safe_load

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
BIOME_CONFIG = REPOSITORY_ROOT / "biome.json"
BIOME = REPOSITORY_ROOT / "node_modules/.bin/biome"
ESLINT = REPOSITORY_ROOT / "node_modules/.bin/eslint"
ESLINT_CONFIG = REPOSITORY_ROOT / "packages/workbench/eslint.config.js"
ESLINT_FILE_CONFIGS = PROJECT_ROOT / "devtools/node/eslint-file-configs.mjs"
LEFTHOOK = REPOSITORY_ROOT / "lefthook.yml"
TSC = REPOSITORY_ROOT / "node_modules/.bin/tsc"
TSCONFIG_BASE = REPOSITORY_ROOT / "tsconfig.base.json"
ROOT_PACKAGE = REPOSITORY_ROOT / "package.json"
WORKBENCH_PACKAGE = REPOSITORY_ROOT / "packages/workbench/package.json"
WORKFLOWS = (
    REPOSITORY_ROOT / ".github/workflows/packing-validation.yml",
    REPOSITORY_ROOT / ".github/workflows/deep-gate.yml",
)

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

#: What `strict: true` turns on. A program that sets one of these false has relaxed the
#: floor as surely as one that sets `strict` itself false.
STRICT_FAMILY = (
    "alwaysStrict",
    "noImplicitAny",
    "noImplicitThis",
    "strictBindCallApply",
    "strictBuiltinIteratorReturn",
    "strictFunctionTypes",
    "strictNullChecks",
    "strictPropertyInitialization",
    "useUnknownInCatchVariables",
)

#: Every flag a program could set false to lower the floor. `allowJs` and `checkJs` are
#: in it because the retained programs are checked JavaScript: without them `tsc` reads
#: those files as nothing and reports a clean program.
FLOOR_FLAGS = frozenset({"allowJs", "checkJs", *REQUIRED_COMPILER_OPTIONS, *STRICT_FAMILY})

#: Options that lower the floor by being true. `noCheck` skips type checking outright.
FORBIDDEN_TRUE = frozenset({"noCheck"})

#: The only flags a program may relax, and only while an open bead tracks their removal
#: (floor rule 8). This is the ratchet `tsconfig.json`, `tsconfig.probes.json` and
#: `tsconfig.motion-lab.json` adopted. Any other floor flag set false fails whatever the
#: comment beside it says: naming a tracker is not a licence to turn off `checkJs`
#: (#125 F19b).
RATCHET_FLAGS = frozenset(
    {
        "noImplicitAny",
        "strictNullChecks",
        "noUncheckedIndexedAccess",
        "exactOptionalPropertyTypes",
    }
)

#: A relaxation is legitimate only while something is tracking its removal (floor rule 8),
#: so every config that turns a floor flag off has to name a bead in its own text.
TRACKER = re.compile(r"\bthink-[a-z0-9]{4}\b")

#: The bead states that still track work. A closed bead tracks nothing, which is how the
#: relaxations came to name the closed `think-4cwy` with every check green (#160 R24).
LIVE_BEAD_STATES = frozenset({"open", "in_progress", "blocked"})

#: The Biome overrides the floor carried until think-6o9n, exactly as `biome.json` wrote them:
#: the motion-lab assets' unused-symbol rules and the classic scripts' strict-mode directive.
#: They went when those files became modules. They are kept here only as reintroductions the
#: negative control must refuse, beside a broad one such as `packing/**` with a floor rule
#: off (#125 F19a): an override is a fault however narrow, and no declaration licenses one.
REMOVED_BIOME_OVERRIDES: tuple[dict[str, Any], ...] = (
    {
        "includes": ["packing/src/sqpack/motion_lab/assets/**/*.js"],
        "linter": {
            "rules": {
                "correctness": {
                    "noUnusedVariables": "off",
                    "noUnusedFunctionParameters": "off",
                }
            }
        },
    },
    {
        "includes": [
            "packing/src/sqpack/motion_lab/assets/**/*.js",
            "packages/workbench/src/application.js",
        ],
        "linter": {"rules": {"suspicious": {"noRedundantUseStrict": "off"}}},
    },
)

#: The liveness samples: code that breaks the floor on purpose, one for each tool -- a
#: braceless `if` for Biome, a floating Promise for ESLint, a type error for `tsc` -- with the
#: most bytes each may grow to. They are test data rather than source, so each is named
#: `.js.txt`: no tool's scope reaches it and no exclusion has to keep it out, which is what
#: lets the floor have no exceptions. A test hands its tool a copy named as JavaScript under
#: `tmp_path`, or its text on stdin. Declaring the files and their sizes keeps the tree to three
#: minimal violations: a fourth file, or a sample that stops being minimal, fails the contract.
FLOOR_SAMPLES = PROJECT_ROOT / "tests/fixtures/browser-floor"
FLOOR_SAMPLE_BYTES = {
    "braceless-if.js.txt": 36,
    "floating-promise.js.txt": 67,
    "type-error.js.txt": 22,
}

#: The only exclusions Biome's `files.includes` may write: what is not ours to hold to a floor,
#: and minified output, of which none is tracked. Any other `!` pattern skips owned code.
BIOME_EXCLUSIONS = frozenset({"!**/node_modules", "!vendor", "!**/.venv", "!**/*.min.js"})

#: Directories whose JavaScript is not ours to hold to a floor: third-party code, vendored
#: or installed. Minified files are excluded from Biome too, and none is tracked.
NOT_OURS = ("vendor/", "node_modules/")
SCRIPT_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts")
STYLE_SUFFIXES = (".css",)
#: The suffixes the ESLint promise overlay covers: checked JavaScript. Biome's own promise
#: rules hold the TypeScript.
JAVASCRIPT_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs")

#: The language sections of `biome.json` that can switch a tool off for a whole language.
LANGUAGES = ("javascript", "css", "json")

#: How every file must be read by `tsc`: in its own scope, so no two files share a name by it.
MODULE_DETECTION = "force"

#: Reads one repository-relative path from the bead store, or None when it is absent.
BeadReader = Callable[[str], str | None]


def _jsonc(path: Path) -> dict[str, Any]:
    """Read a config that may carry comments, which `tsconfig.json` is entitled to."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
    return json.loads(text)


def _git(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(REPOSITORY_ROOT), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def _tracked(*patterns: str) -> list[str]:
    listed = _git("ls-files", "--cached", "--others", "--exclude-standard", "--", *patterns)
    listed.check_returncode()
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
    """Every option the config sets that lowers the type floor."""
    options = _jsonc(config).get("compilerOptions", {})
    return sorted(
        flag
        for flag, value in options.items()
        if (value is False and flag in FLOOR_FLAGS)
        or (value is True and flag in FORBIDDEN_TRUE)
        # A program that reads its files as scripts lets them share top-level names, which
        # is how two motion-lab files once passed every tool while calling each other.
        or (flag == "moduleDetection" and value != MODULE_DETECTION)
    )


def _require_tool(tool: Path) -> None:
    """Skip a liveness test without its pinned tool locally; fail it under `CI`.

    A skip is honest on a laptop that never ran `npm ci`. On a CI surface it is a green
    lane in which the floor's proof silently did not run, which is the defect this replaces.
    """
    if tool.is_file():
        return
    message = (
        f"{tool.relative_to(REPOSITORY_ROOT)} is missing; run `npm ci` at the repository root"
    )
    if os.environ.get("CI"):
        pytest.fail(f"{message}. CI must install the Node toolchain on this job.")
    pytest.skip(message)


# ---------------------------------------------------------------------------------------
# Bead store


def _bead_store() -> BeadReader | None:
    """A reader over the bead store: the local sync worktree, else the sync branch.

    Read straight from the store rather than through the `tbd` binary, which CI does not
    install. Every CI job that clones full history fetches `origin/tbd-sync`.
    """
    common = _git("rev-parse", "--path-format=absolute", "--git-common-dir")
    if common.returncode == 0:
        worktree = Path(common.stdout.strip()) / "tbd" / "data-sync-worktree"
        if (worktree / MAPPINGS).is_file():

            def from_worktree(path: str) -> str | None:
                target = worktree / path
                return target.read_text(encoding="utf-8") if target.is_file() else None

            return from_worktree
    for ref in REFS:
        if _git("cat-file", "-e", f"{ref}:{MAPPINGS}").returncode == 0:

            def from_ref(path: str, ref: str = ref) -> str | None:
                shown = _git("show", f"{ref}:{path}")
                return shown.stdout if shown.returncode == 0 else None

            return from_ref
    return None


def _bead_state(alias: str, read: BeadReader) -> str | None:
    """The status of the bead a `think-xxxx` alias names, or None if there is no such bead."""
    tail = parse_aliases(read(MAPPINGS) or "").get(alias.removeprefix("think-"))
    if tail is None:
        return None
    text = read(f"{ISSUES}/is-{tail}.md")
    if text is None or not text.startswith("---\n"):
        return None
    front = safe_load(text[4 : text.index("\n---", 4)])
    return str(front.get("status")) if isinstance(front, dict) else None


def _dead_trackers(aliases: Iterable[str], read: BeadReader) -> list[str]:
    """Each named tracker that is not a live bead, with what it is instead."""
    faults: list[str] = []
    for alias in sorted(set(aliases)):
        state = _bead_state(alias, read)
        if state is None:
            faults.append(f"{alias}: no such bead")
        elif state not in LIVE_BEAD_STATES:
            faults.append(f"{alias}: {state}")
    return faults


def _require_bead_store() -> BeadReader:
    read = _bead_store()
    if read is not None:
        return read
    message = "no bead store is reachable (no tbd sync worktree, no tbd-sync branch)"
    if os.environ.get("CI"):
        pytest.fail(f"{message}; the job must fetch full history to check trackers")
    pytest.skip(message)


def _fixture_store(states: Mapping[str, str]) -> BeadReader:
    """A bead store holding one bead per alias, in the given state."""
    files = {MAPPINGS: "".join(f"{alias}: tail{alias}\n" for alias in states)}
    for alias, state in states.items():
        files[f"{ISSUES}/is-tail{alias}.md"] = (
            f"---\nid: is-tail{alias}\nstatus: {state}\n---\n"
        )
    return files.get


# ---------------------------------------------------------------------------------------
# Biome


def _biome_override_faults(config: Mapping[str, Any]) -> list[str]:
    """Every override in `config`, each a fault: a rule is on for every file Biome reaches."""
    return [
        f"Biome override: {json.dumps(override, sort_keys=True)}"
        for override in config.get("overrides", [])
    ]


def _biome_downgrade_faults(config: Mapping[str, Any]) -> list[str]:
    """Every rule turned below `error` or off, and every tool or language switched off.

    The global form of an override, and a worse one: floor rule 7 forbids it outright. A rule
    is set to a severity string or to an object carrying a `level`.
    """
    faults: list[str] = []
    for group, rules in config.get("linter", {}).get("rules", {}).items():
        if not isinstance(rules, Mapping):
            continue
        for rule, setting in rules.items():
            level = setting.get("level") if isinstance(setting, Mapping) else setting
            if level != "error":
                faults.append(f"{group}.{rule} is {level!r}")
    sections = {"": config, **{f"{name}.": config.get(name, {}) for name in LANGUAGES}}
    faults.extend(
        f"{prefix}{tool}.enabled is false"
        for prefix, section in sections.items()
        for tool in ("linter", "formatter", "assist")
        if section.get(tool, {}).get("enabled") is False
    )
    return faults


# ---------------------------------------------------------------------------------------
# ESLint


def _eslint_file_configs(
    paths: Iterable[str], block: Path | None = None
) -> list[dict[str, Any]]:
    """What ESLint resolves for each path, read through ESLint's own API.

    `block`, a JSON configuration object, is applied after the config file's own, which is how
    the negative control reintroduces a relaxed block without writing one into the tree.
    """
    done = node(
        [str(ESLINT_FILE_CONFIGS), str(ESLINT_CONFIG), *([str(block)] if block else [])],
        return_completed_process=True,
        input="\n".join(paths),
        capture_output=True,
        text=True,
        cwd=REPOSITORY_ROOT,
    )
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


def _eslint_faults(tracked: Iterable[str], resolved: Iterable[Mapping[str, Any]]) -> list[str]:
    """Every owned script ESLint misses or holds below the promise floor, and every
    configuration that is not the one all of them share.

    "No file-specific block" is checked as what ESLint does rather than how the config reads:
    a block that relaxes a rule for some files, or types them through a different program,
    shows up as those files resolving differently from the rest.
    """
    by_path = {entry["path"]: entry for entry in resolved}
    faults: list[str] = []
    shapes: dict[str, list[str]] = {}
    for path in sorted(tracked):
        entry = by_path.get(path)
        if entry is None or entry["ignored"]:
            faults.append(f"outside ESLint: {path}")
            continue
        below = [rule for rule in PROMISE_RULES if entry["rules"].get(rule) != 2]
        if below:
            faults.append(f"{path}: {below} below error")
        shape = json.dumps(
            {key: entry[key] for key in ("rules", "parser", "parserOptions")}, sort_keys=True
        )
        shapes.setdefault(shape, []).append(path)
    if len(shapes) > 1:
        for shape, paths in sorted(shapes.items(), key=lambda item: -len(item[1]))[1:]:
            faults.append(f"file-specific ESLint configuration for {paths[:3]}: {shape}")
    return faults


def _biome_exclusion_faults(config: Mapping[str, Any]) -> list[str]:
    """Every `files.includes` exclusion beyond what is not ours: an owned tree Biome skips."""
    return [
        f"Biome excludes {pattern}"
        for pattern in config.get("files", {}).get("includes", [])
        if pattern.startswith("!") and pattern not in BIOME_EXCLUSIONS
    ]


def _floor_sample_faults(tree: Path, declared: Mapping[str, int]) -> list[str]:
    """Every way the samples' tree differs from its declaration: a file it does not name, a
    file it names that is gone, a file over its bytes, or a file named as source, which a
    tool's scope would reach."""
    held = {
        path.relative_to(tree).as_posix(): path.stat().st_size
        for path in tree.rglob("*")
        if path.is_file()
    }
    faults = [
        f"holds {name}, which is not declared" for name in sorted(set(held) - set(declared))
    ]
    faults.extend(
        f"declares {name}, which is not held" for name in sorted(set(declared) - set(held))
    )
    faults.extend(
        f"{name} is {size} bytes, over the {declared[name]} declared"
        for name, size in sorted(held.items())
        if name in declared and size > declared[name]
    )
    faults.extend(
        f"{name} is named as source"
        for name in sorted(held)
        if name.endswith((*SCRIPT_SUFFIXES, *STYLE_SUFFIXES))
    )
    return faults


def _biome_listed(command: str) -> set[str]:
    """The files `biome <command>` processes, as it reports them under `--verbose`."""
    done = subprocess.run(
        [str(BIOME), command, "--verbose", "--colors=off", "--max-diagnostics=0", "."],
        check=False,
        capture_output=True,
        text=True,
        cwd=REPOSITORY_ROOT,
    )
    listed = {
        line.removeprefix("  - ").strip()
        for line in (done.stdout + done.stderr).splitlines()
        if line.startswith("  - ")
    }
    assert listed, f"biome {command} --verbose listed no files:\n{done.stdout}{done.stderr}"
    return listed


def _outside_scope(tracked: Iterable[str], processed: set[str]) -> list[str]:
    return sorted(path for path in tracked if path not in processed)


# ---------------------------------------------------------------------------------------
# Workflows


def _jobs_without_node(document: Mapping[str, Any], step_name: str) -> list[str]:
    """Jobs that run `step_name` through `packing-validate` without installing Node first.

    Resolved with the CLI's own parser and selector, so a job counts exactly when the gate
    would run the step there.
    """
    missing: list[str] = []
    for job_name, job in document.get("jobs", {}).items():
        node = npm = False
        for step in job.get("steps", []):
            command = str(step.get("run", ""))
            node = node or str(step.get("uses", "")).startswith("actions/setup-node@")
            npm = npm or "npm ci" in command
            if "packing-validate" not in command:
                continue
            tokens = shlex.split(command)
            # The CLI's own parser and selector, private by name; `test_validation_cli.py`
            # reads the workflow through them the same way, so neither can drift from it.
            parser = validate._parser()  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
            namespace = parser.parse_args(tokens[tokens.index("packing-validate") + 1 :])
            selected = validate._select_steps(  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
                only=namespace.only,
                skip=namespace.skip,
                fast=namespace.fast,
                records=namespace.records,
                edit=namespace.edit,
                checks=namespace.checks,
                frontend=namespace.frontend,
                sweeps=namespace.sweeps,
                suite_a=namespace.suite_a,
                suite_b=namespace.suite_b,
                geometry=namespace.geometry,
            )
            if step_name in {chosen.name for chosen in selected} and not (node and npm):
                missing.append(job_name)
    return missing


# ---------------------------------------------------------------------------------------
# The contract


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
    for suffix in (*SCRIPT_SUFFIXES, *STYLE_SUFFIXES):
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


def test_biome_has_no_override_and_no_rule_turned_down() -> None:
    """No exceptions: not floor rule 7's scoped kind, and not the global downgrade that rule
    forbids. Every rule Biome enables is at `error` for every file it reaches."""
    config = _jsonc(BIOME_CONFIG)
    assert _biome_override_faults(config) == []
    assert _biome_downgrade_faults(config) == []
    assert _biome_exclusion_faults(config) == []


@pytest.mark.parametrize(
    "override",
    [
        *REMOVED_BIOME_OVERRIDES,
        {
            "includes": ["packing/**"],
            "linter": {"rules": {"style": {"useBlockStatements": "off"}}},
        },
    ],
    ids=["unused-symbols", "strict-directive", "broad"],
)
def test_a_reintroduced_biome_override_is_refused(override: dict[str, Any]) -> None:
    """The negative control: each override the floor carried, put back exactly as it was, and
    the broad one from #125 F19a."""
    config = _jsonc(BIOME_CONFIG)
    faults = _biome_override_faults({**config, "overrides": [override]})
    assert faults == [f"Biome override: {json.dumps(override, sort_keys=True)}"]


def test_a_global_downgrade_is_refused() -> None:
    config = json.loads(json.dumps(_jsonc(BIOME_CONFIG)))
    config["linter"]["rules"]["suspicious"] = {"noRedundantUseStrict": "off"}
    config["linter"]["rules"]["style"]["useBlockStatements"] = {"level": "warn"}
    config["css"] = {"linter": {"enabled": False}}
    assert _biome_downgrade_faults(config) == [
        "style.useBlockStatements is 'warn'",
        "suspicious.noRedundantUseStrict is 'off'",
        "css.linter.enabled is false",
    ]


def test_an_owned_tree_excluded_from_biome_is_refused() -> None:
    """The negative control for exclusions: the one the liveness samples briefly had, before
    they became data rather than source."""
    config = json.loads(json.dumps(_jsonc(BIOME_CONFIG)))
    config["files"]["includes"].append("!packing/tests/fixtures/browser-floor")
    assert _biome_exclusion_faults(config) == [
        "Biome excludes !packing/tests/fixtures/browser-floor"
    ]


def test_the_floor_samples_are_exactly_the_declared_data() -> None:
    assert _floor_sample_faults(FLOOR_SAMPLES, FLOOR_SAMPLE_BYTES) == []


def test_a_grown_or_sourced_sample_tree_is_refused(tmp_path: Path) -> None:
    """The negative control: a tree that has grown a file, lost one, let a sample grow past
    its size, and named one as source."""
    for name in FLOOR_SAMPLE_BYTES:
        shutil.copyfile(FLOOR_SAMPLES / name, tmp_path / name)
    shutil.copyfile(FLOOR_SAMPLES / "type-error.js.txt", tmp_path / "type-error.js")
    declared = {"braceless-if.js.txt": 35, "floating-promise.js.txt": 67, "gone.js.txt": 1}
    assert _floor_sample_faults(tmp_path, declared) == [
        "holds type-error.js, which is not declared",
        "holds type-error.js.txt, which is not declared",
        "declares gone.js.txt, which is not held",
        "braceless-if.js.txt is 36 bytes, over the 35 declared",
        "type-error.js is named as source",
    ]


def test_the_type_floor_is_declared_once_and_extended() -> None:
    options = _jsonc(TSCONFIG_BASE)["compilerOptions"]
    for flag in REQUIRED_COMPILER_OPTIONS:
        assert options.get(flag) is True, f"tsconfig.base.json does not set {flag}"
    missing_js = [flag for flag in ("allowJs", "checkJs") if options.get(flag) is not True]
    assert not missing_js, (
        "the retained browser programs are checked JavaScript; without "
        f"{missing_js} their type gates check nothing"
    )
    assert options.get("moduleDetection") == MODULE_DETECTION, (
        "tsconfig.base.json does not give every file its own scope; a program that reads "
        "files as scripts lets them share top-level names by scope"
    )
    for config in _tsconfigs():
        if config.name == "tsconfig.base.json":
            continue
        extends = _jsonc(config).get("extends")
        assert isinstance(extends, str)
        assert (config.parent / extends).resolve() == TSCONFIG_BASE.resolve(), (
            f"{config.relative_to(REPOSITORY_ROOT)} does not extend the shared base"
        )


def test_no_program_relaxes_a_flag_outside_the_ratchet() -> None:
    """Only the declared ratchet flags may be off, tracker or no tracker."""
    for config in _tsconfigs():
        if config == TSCONFIG_BASE:
            continue
        beyond = sorted(set(_relaxed_flags(config)) - RATCHET_FLAGS)
        assert not beyond, (
            f"{config.relative_to(REPOSITORY_ROOT)} relaxes {beyond}, which no tracker can "
            "license; only the ratchet flags may be relaxed"
        )


def test_a_tracked_relaxation_of_checkjs_is_still_refused(tmp_path: Path) -> None:
    """The negative control, on the reproduction from #125 F19b."""
    config = tmp_path / "tsconfig.json"
    config.write_text(
        "{\n  // Tracked as think-n711.\n"
        '  "compilerOptions": {"checkJs": false, "strict": false, "noCheck": true,'
        ' "strictNullChecks": false, "noEmit": false}\n}\n',
        encoding="utf-8",
    )
    assert TRACKER.search(config.read_text(encoding="utf-8"))
    assert sorted(set(_relaxed_flags(config)) - RATCHET_FLAGS) == [
        "checkJs",
        "noCheck",
        "strict",
    ]
    assert "strictNullChecks" in _relaxed_flags(config)


def test_a_program_reading_files_as_scripts_is_refused(tmp_path: Path) -> None:
    """The negative control for module detection: `auto` is `tsc`'s default, and what let the
    motion lab's model and page script share functions by scope while both tools passed."""
    config = tmp_path / "tsconfig.json"
    config.write_text(
        json.dumps({"compilerOptions": {"moduleDetection": "auto"}}), encoding="utf-8"
    )
    assert _relaxed_flags(config) == ["moduleDetection"]
    assert sorted(set(_relaxed_flags(config)) - RATCHET_FLAGS) == ["moduleDetection"]


def test_every_relaxed_flag_names_an_open_tracker() -> None:
    """Floor rule 8: legacy code ratchets toward strict. A flag turned off without a live
    tracked issue is not a ratchet, it is a lower floor."""
    relaxed = {config: _relaxed_flags(config) for config in _tsconfigs()}
    relaxed = {config: flags for config, flags in relaxed.items() if flags}
    for config, flags in relaxed.items():
        assert TRACKER.search(config.read_text(encoding="utf-8")), (
            f"{config.name} relaxes {flags} and names no tracking issue"
        )
    read = _require_bead_store()
    named = {
        config.name: TRACKER.findall(config.read_text(encoding="utf-8")) for config in relaxed
    }
    for source, aliases in named.items():
        assert _dead_trackers(aliases, read) == [], f"{source} names a tracker that is not open"


def test_a_closed_or_unknown_tracker_is_refused(tmp_path: Path) -> None:
    """The negative control for the tracker check, on a fixture store, so it runs wherever
    the real store does not."""
    read = _fixture_store({"aaaa": "open", "bbbb": "in_progress", "cccc": "closed"})
    assert _dead_trackers(["think-aaaa", "think-bbbb"], read) == []
    assert _dead_trackers(["think-aaaa", "think-cccc", "think-zzzz"], read) == [
        "think-cccc: closed",
        "think-zzzz: no such bead",
    ]
    config = tmp_path / "tsconfig.json"
    config.write_text(
        '{\n  // Tracked as think-cccc.\n  "compilerOptions": {"strictNullChecks": false}\n}\n',
        encoding="utf-8",
    )
    assert _relaxed_flags(config) == ["strictNullChecks"]
    assert _dead_trackers(TRACKER.findall(config.read_text(encoding="utf-8")), read) == [
        "think-cccc: closed"
    ]


def test_an_untracked_relaxation_is_detected(tmp_path: Path) -> None:
    config = tmp_path / "tsconfig.json"
    config.write_text(
        json.dumps({"compilerOptions": {"strictNullChecks": False}}), encoding="utf-8"
    )
    assert _relaxed_flags(config) == ["strictNullChecks"]
    assert TRACKER.search(config.read_text(encoding="utf-8")) is None


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


def test_every_job_running_the_liveness_tests_installs_node() -> None:
    """Both behavioral shards may own liveness modules and therefore install Node."""
    for workflow in WORKFLOWS:
        document = safe_load(workflow.read_text(encoding="utf-8"))
        for shard in ("fast behavioral tests, shard A", "fast behavioral tests, shard B"):
            assert _jobs_without_node(document, shard) == [], workflow.name


@pytest.mark.parametrize("job_name", ["suite-a", "suite-b"])
def test_a_behavioral_job_without_node_is_detected(job_name: str) -> None:
    """The negative control: either behavioral job without Node is detected."""
    document = safe_load(WORKFLOWS[0].read_text(encoding="utf-8"))
    document["jobs"][job_name]["steps"] = [
        step
        for step in document["jobs"][job_name]["steps"]
        if "setup-node" not in str(step.get("uses", ""))
        and "npm ci" not in str(step.get("run"))
    ]
    shard = "A" if job_name == "suite-a" else "B"
    assert _jobs_without_node(document, f"fast behavioral tests, shard {shard}") == [job_name]


def test_a_missing_tool_fails_under_ci_and_skips_locally(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    absent = REPOSITORY_ROOT / "node_modules/.bin/not-a-floor-tool"
    assert not absent.exists()
    monkeypatch.setenv("CI", "true")
    with pytest.raises(pytest.fail.Exception, match="CI must install"):
        _require_tool(absent)
    monkeypatch.delenv("CI")
    with pytest.raises(pytest.skip.Exception):
        _require_tool(absent)


# ---------------------------------------------------------------------------------------
# Liveness


def test_every_tracked_script_and_stylesheet_is_in_biome_scope() -> None:
    """Biome's real scope, as Biome resolves it, not as `files.includes` reads (#125 F19c).

    A suffix glob in the config proves only that someone wrote one. An exclusion, a VCS
    ignore or a per-tool `includes` can still take a tracked file out of the linter or the
    formatter while every string comparison passes.
    """
    _require_tool(BIOME)
    tracked = [
        path
        for path in _git("ls-files", "--cached").stdout.splitlines()
        if path.endswith((*SCRIPT_SUFFIXES, *STYLE_SUFFIXES))
        and not path.startswith(NOT_OURS)
        # A tracked file deleted in the working tree is a pending removal, not a file
        # Biome could have scanned.
        and (REPOSITORY_ROOT / path).is_file()
    ]
    assert tracked
    for command in ("lint", "format"):
        outside = _outside_scope(tracked, _biome_listed(command))
        assert outside == [], f"tracked source outside `biome {command}`: {outside}"


def test_a_file_outside_biome_scope_is_detected() -> None:
    tracked = ["packages/workbench/src/index.ts", "packing/src/sqpack/motion_lab/assets/x.css"]
    assert _outside_scope(tracked, {"packages/workbench/src/index.ts"}) == [
        "packing/src/sqpack/motion_lab/assets/x.css"
    ]


def _owned_javascript() -> list[str]:
    return [
        path
        for path in _tracked(*(f"*{suffix}" for suffix in JAVASCRIPT_SUFFIXES))
        if (REPOSITORY_ROOT / path).is_file()
    ]


def test_eslint_holds_every_owned_script_to_one_configuration() -> None:
    """Every tracked JavaScript file is reached, at the promise floor, and resolves exactly as
    every other one does: no file has a block of its own, relaxed or merely different. Read
    from ESLint's own resolution of each file, not from the config's source (#125 F19c)."""
    _require_tool(ESLINT)
    owned = _owned_javascript()
    assert owned
    assert _eslint_faults(owned, _eslint_file_configs(owned)) == []


@pytest.mark.parametrize(
    ("block", "expected"),
    [
        (
            {
                "files": ["packages/workbench/probes/**/*.js"],
                "rules": {"@typescript-eslint/no-floating-promises": "off"},
            },
            "below error",
        ),
        (
            # The shape of the block `application.js` had: the same rules, typed through a
            # program of its own.
            {
                "files": ["packages/workbench/src/application.js"],
                "languageOptions": {"parserOptions": {"project": "./tsconfig.json"}},
            },
            "file-specific ESLint configuration for ['packages/workbench/src/application.js']",
        ),
        ({"ignores": ["packing/src/sqpack/motion_lab/assets/**"]}, "outside ESLint"),
    ],
    ids=["relaxed-rule", "own-program", "ignored"],
)
def test_a_reintroduced_eslint_block_is_refused(
    tmp_path: Path, block: dict[str, Any], expected: str
) -> None:
    """The negative control, live: ESLint resolves the real config with the block added, and
    the faults name what the block did."""
    _require_tool(ESLINT)
    extra = tmp_path / "block.json"
    extra.write_text(json.dumps(block), encoding="utf-8")
    owned = _owned_javascript()
    faults = _eslint_faults(owned, _eslint_file_configs(owned, extra))
    assert faults
    assert any(expected in fault for fault in faults), faults


def test_eslint_faults_name_each_kind_of_gap() -> None:
    floor = dict.fromkeys(PROMISE_RULES, 2)
    shared = {
        "ignored": False,
        "rules": floor,
        "parser": "p",
        "parserOptions": {"project": ["a"]},
    }
    resolved = [
        {**shared, "path": "a.js"},
        {**shared, "path": "b.js"},
        {**shared, "path": "c.js", "rules": {**floor, PROMISE_RULES[1]: 1}},
        {**shared, "path": "d.js", "parserOptions": {"project": ["b"]}},
        {"path": "e.js", "ignored": True},
    ]
    faults = _eslint_faults(["a.js", "b.js", "c.js", "d.js", "e.js", "f.js"], resolved)
    assert faults[:3] == [
        "c.js: ['@typescript-eslint/no-floating-promises'] below error",
        "outside ESLint: e.js",
        "outside ESLint: f.js",
    ]
    configurations = sorted(fault.split(":")[0] for fault in faults[3:])
    assert configurations == [
        "file-specific ESLint configuration for ['c.js']",
        "file-specific ESLint configuration for ['d.js']",
    ]


def test_the_gates_lint_the_whole_repository_with_eslint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A directory list in a gate could only leave a new tree outside the floor, as the old one
    left the video spikes' probes: the config decides what is owned, so both gates pass `.`."""
    _require_tool(ESLINT)
    captured: list[tuple[str, ...]] = []

    def record(_context: validate.Context, commands: Any, **_options: Any) -> str:
        captured.extend(tuple(command) for command in commands)
        return ""

    monkeypatch.setattr(validate, "_commands", record)
    validate._browser_floor(  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        validate.Context(
            deep=False, strict=False, jobs=1, inner_jobs=1, environment=dict(os.environ)
        )
    )
    (eslint,) = [command for command in captured if command[0] == str(ESLINT)]
    expected = (".", "--config", "packages/workbench/eslint.config.js", "--max-warnings", "0")
    assert eslint[1:] == expected
    script = _jsonc(WORKBENCH_PACKAGE)["scripts"]["lint:promises"]
    assert script == f"cd ../.. && eslint {' '.join(expected)}"


def test_the_checked_javascript_overlay_rejects_a_floating_promise() -> None:
    """Linted at an in-scope path through stdin, so the config's own `files` globs decide
    whether the rule applies, and no fixture is ever written into the source tree.

    The path is a real file in a type program, because a file in none fails to parse, which
    is the point. `TSESTREE_SINGLE_RUN=false` is what makes typescript-eslint type the text on
    stdin: detecting a one-shot CLI run, it otherwise builds each program once from the disk
    and lints the file there, and the fixture is never seen."""
    _require_tool(ESLINT)
    done = subprocess.run(
        [
            str(ESLINT),
            "--stdin",
            "--stdin-filename",
            "packages/workbench/src/application.js",
            "--config",
            str(ESLINT_CONFIG),
        ],
        env=os.environ | {"TSESTREE_SINGLE_RUN": "false"},
        input=(FLOOR_SAMPLES / "floating-promise.js.txt").read_text(encoding="utf-8"),
        check=False,
        capture_output=True,
        text=True,
        cwd=REPOSITORY_ROOT,
    )
    assert done.returncode != 0, "ESLint accepted a floating Promise in checked JavaScript"
    assert "@typescript-eslint/no-floating-promises" in done.stdout + done.stderr


def test_the_braces_rule_actually_rejects_a_violation(tmp_path: Path) -> None:
    """The liveness check. `useBlockStatements` being written in the config proves only
    that someone wrote it; what proves the floor is live is Biome refusing a braceless
    `if`. The sample is copied outside the repository, named as JavaScript, so no real file
    has to be broken and the repository's own scope rules cannot exempt it."""
    _require_tool(BIOME)
    sample = tmp_path / "sample.js"
    shutil.copyfile(FLOOR_SAMPLES / "braceless-if.js.txt", sample)
    done = subprocess.run(
        [str(BIOME), "check", f"--config-path={REPOSITORY_ROOT}", str(sample)],
        check=False,
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert done.returncode != 0, "Biome accepted a braceless if; the floor is not live"
    assert "useBlockStatements" in done.stdout + done.stderr, (
        "Biome complained, but not about the braces rule:\n" + done.stdout + done.stderr
    )


def test_the_type_gate_actually_rejects_a_type_error(tmp_path: Path) -> None:
    """The same liveness question for the type gate. A `tsconfig` whose `include` matches
    nothing reports zero errors and looks exactly like a clean program."""
    _require_tool(TSC)
    shutil.copyfile(FLOOR_SAMPLES / "type-error.js.txt", tmp_path / "sample.js")
    (tmp_path / "tsconfig.json").write_text(
        json.dumps(
            {
                "compilerOptions": _jsonc(TSCONFIG_BASE)["compilerOptions"],
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
        cwd=tmp_path,
    )
    assert done.returncode != 0, "tsc accepted a type error under the floor's own options"


# ---------------------------------------------------------------------------------------
# Formatting


def test_the_commit_hook_fixes_every_owned_suffix() -> None:
    """Floor rule 6: the hook formats and fixes each staged script and stylesheet with Biome
    and stages the result. The glob is matched against the whole path, so `*.js` reaches a
    probe four directories down (measured with lefthook 2.1.10 on a nested `.ts`, `.js` and
    `.css` for think-6o9n)."""
    hook = safe_load(LEFTHOOK.read_text(encoding="utf-8"))["pre-commit"]
    assert hook["parallel"] is False, "stage_fixed commands race on the index when parallel"
    biome = hook["commands"]["biome"]
    globbed = re.fullmatch(r"\*\.\{([a-z,]+)\}", biome["glob"])
    assert globbed, f"the Biome hook's glob is not one suffix set: {biome['glob']}"
    covered = {f".{suffix}" for suffix in globbed.group(1).split(",")}
    missing = sorted({*SCRIPT_SUFFIXES, *STYLE_SUFFIXES} - covered)
    assert not missing, f"the commit hook does not format {missing}"
    command = shlex.split(biome["run"])
    assert command[:2] == ["./node_modules/.bin/biome", "check"]
    assert {"--write", "--unsafe"} <= set(command)
    assert command[-1] == "{staged_files}"
    assert biome["stage_fixed"] is True


@pytest.mark.parametrize(
    "source",
    [
        "packages/workbench/src/core/geometry.ts",
        "packages/workbench/probes/animate/scope.js",
        "packing/src/sqpack/motion_lab/assets/motion-lab.css",
    ],
)
def test_the_gate_rejects_an_unformatted_file(tmp_path: Path, source: str) -> None:
    """The verify half of floor rule 6: `biome ci`, the pull-request gate's command, fails a
    file the formatter would change. The fixture is a real source file with its indentation
    doubled, so what is proved is the formatter's verdict and not a lint rule's."""
    _require_tool(BIOME)
    text = (REPOSITORY_ROOT / source).read_text(encoding="utf-8")
    unformatted = re.sub(r"^( +)", r"\1\1", text, flags=re.MULTILINE)
    assert unformatted != text
    sample = tmp_path / Path(source).name
    sample.write_text(unformatted, encoding="utf-8")
    done = subprocess.run(
        [
            str(BIOME),
            "ci",
            "--error-on-warnings",
            f"--config-path={REPOSITORY_ROOT}",
            sample.name,
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    output = done.stdout + done.stderr
    assert done.returncode != 0, f"biome ci accepted an unformatted {source}"
    assert "format" in output, f"biome ci failed, but not on formatting:\n{output}"
