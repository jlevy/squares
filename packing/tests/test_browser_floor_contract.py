"""The browser floor as a declared contract, and as a floor that is actually live.

The JavaScript and CSS this repository serves have the same shape of floor the Python
does: a formatter that owns layout, a linter at zero tolerance, and a separate type gate.
`tbd guidelines typescript-lint-format-rules` defines it and `biome.json` plus the
`tsconfig*.json` set implement it.

Two different things are checked here, and the second is the one that matters.

**The contract**: the named floor rules are present and set to `error`, every tracked
first-party script and stylesheet is inside the scope Biome actually resolves and inside
one of the type gate's programs, every Biome exception is one this file declares, no
program relaxes a flag outside the declared ratchet, and every relaxation names an open
bead tracking its removal.

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
`packing/tests/fixtures/browser-floor/`, and they are the floor's one declared exception:
each must fail the floor, so Biome skips their tree and no type program includes it, and
the contract holds that tree to exactly those samples at their sizes. No test writes into
the source tree, and none hands a tool the checked-in path, which the tree's own scope rules
would exempt: the ESLint probe reads its sample on stdin under an in-scope
`--stdin-filename`, and Biome and `tsc` read a copy under pytest's `tmp_path`, so nothing
here can race a test that lists the tree (#160 R18).
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

from devtools.check_bead_tree import ISSUES, MAPPINGS, REFS, parse_aliases
from sqpack.cli import validate
from sqpack.yamlio import safe_load

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
BIOME_CONFIG = REPOSITORY_ROOT / "biome.json"
BIOME = REPOSITORY_ROOT / "node_modules/.bin/biome"
ESLINT = REPOSITORY_ROOT / "node_modules/.bin/eslint"
ESLINT_CONFIG = REPOSITORY_ROOT / "packages/workbench/eslint.config.js"
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

#: Every Biome override the floor tolerates, exactly as `biome.json` writes it, with the
#: bead that removes it. An override is floor rule 7's scoped exception only if it is one of
#: these. Any other override fails until it is declared here, where a reviewer reads it --
#: above all a broad one such as `packing/**` with a floor rule off, which the old test
#: accepted because `biome.json` mentioned `motion_lab` somewhere (#125 F19a).
DECLARED_BIOME_OVERRIDES: tuple[dict[str, Any], ...] = (
    {
        "tracker": "think-6o9n",
        "reason": "the motion-lab assets are fragments concatenated into one page, so a "
        "symbol one fragment defines is used by another",
        "override": {
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
    },
    {
        "tracker": "think-6o9n",
        "reason": "the motion-lab assets and the legacy application script are classic "
        "scripts that declare their own strict mode",
        "override": {
            "includes": [
                "packing/src/sqpack/motion_lab/assets/**/*.js",
                "packages/workbench/src/application.js",
            ],
            "linter": {"rules": {"suspicious": {"noRedundantUseStrict": "off"}}},
        },
    },
)

#: Every tree of first-party source Biome is told to skip, exactly as `biome.json`'s
#: `files.includes` writes the exclusion, with why, and with every file the tree may hold and
#: the most bytes each may grow to. There is one, and it is permanent rather than tracked:
#: the liveness samples below must be rejected by the tool each proves live, so no tool may
#: be configured to accept them. Declaring the files as well as the tree is what keeps the
#: exception from growing -- a fourth file, or a sample that stops being minimal, fails the
#: contract before it can carry anything but a violation.
DECLARED_BIOME_EXCLUSIONS: tuple[dict[str, Any], ...] = (
    {
        "reason": "the liveness samples break the floor on purpose: a braceless `if` for "
        "Biome, a floating Promise for ESLint, and a type error for `tsc`",
        "exclusion": "!packing/tests/fixtures/browser-floor",
        "files": {"braceless-if.js": 36, "floating-promise.js": 67, "type-error.js": 22},
    },
)
FLOOR_SAMPLES = REPOSITORY_ROOT / DECLARED_BIOME_EXCLUSIONS[0]["exclusion"].removeprefix("!")

#: Directories whose JavaScript is not ours to hold to a floor.
NOT_OURS = ("vendor/", "node_modules/")
SCRIPT_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts")
STYLE_SUFFIXES = (".css",)

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


def _biome_override_faults(
    config: Mapping[str, Any], declared: Iterable[Mapping[str, Any]]
) -> list[str]:
    """Every override in `config` that is not exactly one of the declared exceptions."""
    allowed = [entry["override"] for entry in declared]
    return [
        f"undeclared Biome override: {json.dumps(override, sort_keys=True)}"
        for override in config.get("overrides", [])
        if override not in allowed
    ]


def _declared_exclusion_faults(
    config: Mapping[str, Any], declared: Iterable[Mapping[str, Any]]
) -> list[str]:
    """Every declared exclusion `config` does not write, and every way its tree differs from
    the declaration: a file it does not name, a file it names that is gone, or a file over
    the bytes it allows."""
    faults: list[str] = []
    includes = config.get("files", {}).get("includes", [])
    for entry in declared:
        exclusion = entry["exclusion"]
        if exclusion not in includes:
            faults.append(f"declared Biome exclusion not in biome.json: {exclusion}")
        tree = REPOSITORY_ROOT / exclusion.removeprefix("!")
        held = {
            path.relative_to(tree).as_posix(): path.stat().st_size
            for path in tree.rglob("*")
            if path.is_file()
        }
        allowed: Mapping[str, int] = entry["files"]
        faults.extend(
            f"{exclusion}: holds {name}, which the exception does not declare"
            for name in sorted(set(held) - set(allowed))
        )
        faults.extend(
            f"{exclusion}: declares {name}, which the tree does not hold"
            for name in sorted(set(allowed) - set(held))
        )
        faults.extend(
            f"{exclusion}: {name} is {size} bytes, over the {allowed[name]} declared"
            for name, size in sorted(held.items())
            if name in allowed and size > allowed[name]
        )
    return faults


def _declared_excluded(path: str) -> bool:
    """Whether a repository-relative path lies in a tree a declared exclusion skips."""
    return any(
        path.startswith(entry["exclusion"].removeprefix("!") + "/")
        for entry in DECLARED_BIOME_EXCLUSIONS
    )


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


def test_every_biome_exception_is_declared() -> None:
    """Floor rule 7: an exception names exact files and exact rules, never a global
    downgrade. A rule turned off at the top level, or over a whole tree, would be a
    different floor wearing this one's name."""
    assert _biome_override_faults(_jsonc(BIOME_CONFIG), DECLARED_BIOME_OVERRIDES) == []
    assert _declared_exclusion_faults(_jsonc(BIOME_CONFIG), DECLARED_BIOME_EXCLUSIONS) == []
    tracked = _tracked(*(f"*{suffix}" for suffix in (*SCRIPT_SUFFIXES, *STYLE_SUFFIXES)))
    for entry in DECLARED_BIOME_OVERRIDES:
        for pattern in entry["override"]["includes"]:
            assert not pattern.startswith("!"), f"an override that excludes: {pattern}"
            assert _tracked(pattern.replace("**/*", "*")), (
                f"a declared override names no tracked file: {pattern}"
            )
    assert tracked


def test_a_broad_or_undeclared_biome_override_is_refused() -> None:
    """The negative control for the test above, on the reproduction from #125 F19a."""
    config = _jsonc(BIOME_CONFIG)
    broad = {
        "includes": ["packing/**"],
        "linter": {"rules": {"style": {"useBlockStatements": "off"}}},
    }
    faults = _biome_override_faults(
        {**config, "overrides": [*config.get("overrides", []), broad]},
        DECLARED_BIOME_OVERRIDES,
    )
    assert len(faults) == 1
    assert "packing/**" in faults[0]

    widened = json.loads(json.dumps(config))
    widened["overrides"][0]["includes"].append("packages/**/*.js")
    assert len(_biome_override_faults(widened, DECLARED_BIOME_OVERRIDES)) == 1

    # The exclusion's own controls: dropped from `biome.json`, and a tree that has grown a
    # file, lost one, and let a sample grow past its size.
    dropped = json.loads(json.dumps(config))
    dropped["files"]["includes"].remove(DECLARED_BIOME_EXCLUSIONS[0]["exclusion"])
    assert len(_declared_exclusion_faults(dropped, DECLARED_BIOME_EXCLUSIONS)) == 1
    narrowed = [
        {**entry, "files": {"braceless-if.js": 35, "type-error.js": 22, "gone.js": 1}}
        for entry in DECLARED_BIOME_EXCLUSIONS
    ]
    faults = _declared_exclusion_faults(config, narrowed)
    assert len(faults) == 3, faults
    assert "holds floating-promise.js, which the exception does not declare" in faults[0]
    assert "declares gone.js, which the tree does not hold" in faults[1]
    assert "braceless-if.js is 36 bytes, over the 35 declared" in faults[2]


def test_the_type_floor_is_declared_once_and_extended() -> None:
    options = _jsonc(TSCONFIG_BASE)["compilerOptions"]
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
    named["biome.json overrides"] = [entry["tracker"] for entry in DECLARED_BIOME_OVERRIDES]
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
    uncovered = sorted(path for path in set(tracked) - covered if not _declared_excluded(path))
    assert not uncovered, f"tracked JavaScript in no type-check program: {uncovered}"
    typed_samples = sorted(path for path in covered if _declared_excluded(path))
    assert not typed_samples, f"a program type-checks a sample that must fail: {typed_samples}"


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
    held = [path for path in tracked if not _declared_excluded(path)]
    samples = [path for path in tracked if _declared_excluded(path)]
    for command in ("lint", "format"):
        listed = _biome_listed(command)
        outside = _outside_scope(held, listed)
        assert outside == [], f"tracked source outside `biome {command}`: {outside}"
        linted = sorted(set(samples) & listed)
        assert linted == [], f"`biome {command}` reaches a declared exclusion: {linted}"


def test_a_file_outside_biome_scope_is_detected() -> None:
    tracked = ["packages/workbench/src/index.ts", "packing/src/sqpack/motion_lab/assets/x.css"]
    assert _outside_scope(tracked, {"packages/workbench/src/index.ts"}) == [
        "packing/src/sqpack/motion_lab/assets/x.css"
    ]


def test_the_checked_javascript_promise_overlay_is_effective() -> None:
    _require_tool(ESLINT)
    representatives = (
        "packages/workbench/src/application.js",
        "packages/workbench/probes/api/apply.js",
        "packing/devtools/probes/check_published_site/startup.js",
        "packing/devtools/node/inspect-probes.mjs",
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


def test_the_checked_javascript_overlay_rejects_a_floating_promise() -> None:
    """Linted at an in-scope path through stdin, so the config's own `files` globs decide
    whether the rule applies, whatever tree the sample is checked in under."""
    _require_tool(ESLINT)
    done = subprocess.run(
        [
            str(ESLINT),
            "--stdin",
            "--stdin-filename",
            "packages/workbench/src/floor-liveness-probe.js",
            "--config",
            str(ESLINT_CONFIG),
        ],
        input=(FLOOR_SAMPLES / "floating-promise.js").read_text(encoding="utf-8"),
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
    `if`. The sample is copied outside the repository so no real file has to be broken and
    so the repository's own scope rules, which skip the samples' tree, cannot exempt it."""
    _require_tool(BIOME)
    sample = tmp_path / "sample.js"
    shutil.copyfile(FLOOR_SAMPLES / "braceless-if.js", sample)
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
    shutil.copyfile(FLOOR_SAMPLES / "type-error.js", tmp_path / "sample.js")
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
