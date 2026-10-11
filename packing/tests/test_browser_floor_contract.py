"""The browser floor as a declared contract, and as a floor that is actually live.

The JavaScript and CSS this repository serves have the same shape of floor the Python
does: a formatter that owns layout, a linter at zero tolerance, and a separate type gate.
`tbd guidelines typescript-lint-format-rules` defines it and `biome.json`, the
`tsconfig*.json` set, and the isolated probe-program manifest implement it.

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
from collections import Counter
from collections.abc import Iterable, Mapping
from functools import cache
from pathlib import Path
from typing import Any

import pytest
from nodejs_wheel import node

from devtools import bead_state, render_n11_lower_bounds_explainer
from sqpack.cli import validate
from sqpack.yamlio import safe_load

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
BIOME_CONFIG = REPOSITORY_ROOT / "biome.json"
BIOME = REPOSITORY_ROOT / "node_modules/.bin/biome"
ESLINT = REPOSITORY_ROOT / "node_modules/.bin/eslint"
ESLINT_CONFIG = REPOSITORY_ROOT / "packages/workbench/eslint.config.js"
ESLINT_PROBES = REPOSITORY_ROOT / "eslint.probes.json"
ESLINT_FILE_CONFIGS = PROJECT_ROOT / "devtools/node/eslint-file-configs.mjs"
LEFTHOOK = REPOSITORY_ROOT / "lefthook.yml"
TSC = REPOSITORY_ROOT / "node_modules/.bin/tsc"
TSCONFIG_BASE = REPOSITORY_ROOT / "tsconfig.base.json"
ROOT_PACKAGE = REPOSITORY_ROOT / "package.json"
WORKBENCH_PACKAGE = REPOSITORY_ROOT / "packages/workbench/package.json"
PROBE_TYPECHECK = REPOSITORY_ROOT / "packing/devtools/node/typecheck-probe-groups.mjs"
PROBE_TYPECHECK_MANIFEST = REPOSITORY_ROOT / "packing/devtools/probe-typecheck.json"
WORKFLOWS = (
    REPOSITORY_ROOT / ".github/workflows/packing-validation.yml",
    REPOSITORY_ROOT / ".github/workflows/deep-gate.yml",
)
SCRIPT_ELEMENT = re.compile(r"<script(?:\s[^>]*)?>(.*?)</script>", re.DOTALL)
SCRIPT_PLACEHOLDER = re.compile(r"\s*\{\{([A-Z_]+)\}\}\s*")

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
#: braceless `if` for Biome, a floating Promise for ESLint, type errors for `tsc`, and an
#: undeclared probe result member -- with the exact byte count each must keep. They are test
#: data rather than source, so each source suffix is followed by `.txt`: no tool's scope
#: reaches them and no exclusion has to keep them out. A test hands its tool a copy named as
#: source under `tmp_path`. Declaring the files and their sizes keeps the tree to four minimal
#: violations: a fifth file, or a sample that changes in either direction, fails the contract.
FLOOR_SAMPLES = PROJECT_ROOT / "tests/fixtures/browser-floor"
FLOOR_SAMPLE_BYTES = {
    "braceless-if.js.txt": 36,
    "floating-promise.js.txt": 67,
    "probe-undeclared-member.mjs.txt": 162,
    "type-error.js.txt": 22,
}
PROBE_GROUP_SAMPLES = REPOSITORY_ROOT / "packing/tests/fixtures/probe-typecheck"

#: The only exclusions Biome's `files.includes` may write: what is not ours to hold to a floor,
#: and minified output, of which none is tracked. Any other `!` pattern skips owned code.
#: `packing/resources` is the literature archive. Its JavaScript is other authors' bytes,
#: retained verbatim and hash-bound by each packet's own manifest, so the formatter must not
#: reach it: the pre-commit hook writes Biome's fixes back to staged files, which would edit
#: archived source to look tidy and void the retention. Ruff excludes the same tree for the
#: same reason, and `.flowmarkignore` excludes it for the Markdown beside it.
BIOME_EXCLUSIONS = frozenset(
    {"!**/node_modules", "!vendor", "!packing/resources", "!**/.venv", "!**/*.min.js"}
)

TYPE_ERROR_DIAGNOSTIC = "sample.js(1,12): error TS2345:"

#: Directories whose JavaScript is not ours to hold to a floor: third-party code, vendored,
#: installed, or archived as retained source. Minified files are excluded from Biome too, and
#: none is tracked.
NOT_OURS = ("vendor/", "node_modules/", "packing/resources/")
SCRIPT_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts")
STYLE_SUFFIXES = (".css",)
#: The suffixes the ESLint promise overlay covers: checked JavaScript. Biome's own promise
#: rules hold the TypeScript.
JAVASCRIPT_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs")

#: The language sections of `biome.json` that can switch a tool off for a whole language.
LANGUAGES = ("javascript", "css", "json")

#: Biome's pinned recommended preset includes these rules at `info`, which does not fail
#: `biome ci --error-on-warnings`. Naming them at `error` makes "zero findings" literal.
#: The exact Biome version is pinned and tested below, so a version upgrade must update this
#: declaration together with any changed preset.
RECOMMENDED_INFO_RULES = {
    "complexity": frozenset(
        {
            "noExtraBooleanCast",
            "noFlatMapIdentity",
            "noUselessCatch",
            "noUselessConstructor",
            "noUselessContinue",
            "noUselessEmptyExport",
            "noUselessEscapeInRegex",
            "noUselessFragments",
            "noUselessLabel",
            "noUselessLoneBlockStatements",
            "noUselessRename",
            "noUselessStringRaw",
            "noUselessSwitchCase",
            "noUselessTernary",
            "noUselessThisAlias",
            "noUselessTypeConstraint",
            "noUselessUndefinedInitialization",
            "useFlatMap",
            "useIndexOf",
            "useLiteralKeys",
        }
    ),
    "correctness": frozenset({"useParseIntRadix"}),
    "nursery": frozenset({"noInvalidPropertyInitValue", "useDomNodeTextContent"}),
    "style": frozenset(
        {
            "useArrayLiterals",
            "useExponentiationOperator",
            "useNodejsImportProtocol",
            "useShorthandFunctionType",
            "useTemplate",
        }
    ),
    "suspicious": frozenset({"noDuplicateFields", "noQuickfixBiome"}),
}

#: Per-file suppressions are exceptions to the floor even when no config override exists.
#: The motion exceptions protect reduced-motion accessibility. The publication CSS was
#: previously inline in HTML; its measured vendor overrides and established selector
#: order keep the existing page's cascade after extraction. Exact text is deliberate:
#: a missing reason or broadened rule changes the census and fails.
DECLARED_SUPPRESSIONS = Counter(
    {
        # The site pins its own faces against a font hook an embedding viewer injects;
        # the injected rule may come later at the same specificity, so only !important
        # keeps the pin (`paper-design.md`, Text).
        (
            "packing/devtools/templates/paper-type.css",
            (
                "/* biome-ignore-start lint/complexity/noImportantStyles: the pin must "
                "outrank an injected hook */"
            ),
        ): 1,
        (
            "packing/devtools/templates/paper-type.css",
            (
                "/* biome-ignore-end lint/complexity/noImportantStyles: the pin must "
                "outrank an injected hook */"
            ),
        ): 1,
        (
            "packing/devtools/templates/paper-publication.css",
            (
                "/* biome-ignore lint/style/noDescendingSpecificity: historical selector "
                "order preserves the established KPress publication cascade. */"
            ),
        ): 29,
        (
            "packing/devtools/templates/paper-publication.css",
            (
                "/* biome-ignore lint/complexity/noImportantStyles: this measured KPress "
                "or print override needs to beat a vendor or inline declaration. */"
            ),
        ): 6,
        (
            "packing/devtools/templates/paper-publication.css",
            (
                "/* biome-ignore lint/complexity/noImportantStyles: prepared math reserves "
                "a measured inline box and KPress sets this dimension inline. */"
            ),
        ): 1,
        (
            "packing/devtools/templates/paper-publication.css",
            (
                "/* biome-ignore lint/complexity/noImportantStyles: the paired baseline "
                "correction must override the prepared inline value. */"
            ),
        ): 1,
        (
            "packing/devtools/templates/paper-publication.css",
            (
                "/* biome-ignore lint/style/noDescendingSpecificity: credit emphasis "
                "inherits the shared bold role after the broader support-text rules. */"
            ),
        ): 1,
        (
            "packing/src/sqpack/motion_lab/assets/motion-lab.css",
            (
                "/* biome-ignore lint/complexity/noImportantStyles: `*` has the lowest "
                "specificity, so only !important beats `select, button { transition }` for a "
                "viewer who asked for no motion. */"
            ),
        ): 1,
        (
            "packing/src/sqpack/motion_lab/assets/motion-lab.css",
            (
                "/* biome-ignore lint/complexity/noImportantStyles: as above; without it "
                "the controls still animate under reduced motion. */"
            ),
        ): 1,
        (
            "packing/atlas/rendering/n5-motion-lab.html",
            (
                "/* biome-ignore lint/complexity/noImportantStyles: `*` has the lowest "
                "specificity, so only !important beats `select, button { transition }` for a "
                "viewer who asked for no motion. */"
            ),
        ): 1,
        (
            "packing/atlas/rendering/n5-motion-lab.html",
            (
                "/* biome-ignore lint/complexity/noImportantStyles: as above; without it "
                "the controls still animate under reduced motion. */"
            ),
        ): 1,
        (
            "packing/tests/probes/pdf_math_browser/fault_state.js",
            (
                "// biome-ignore lint/nursery/useDomNodeTextContent: this probe compares "
                "rendered text with raw DOM text, so their different visibility semantics "
                "are the subject of the test."
            ),
        ): 1,
        (
            "packing/devtools/probes/check_site_rendering/report.js",
            (
                "// biome-ignore lint/nursery/useDomNodeTextContent: the gate measures "
                "rendered readable text, excluding hidden content."
            ),
        ): 1,
        (
            "packing/devtools/probes/check_site_rendering/report.js",
            (
                "// biome-ignore lint/nursery/useDomNodeTextContent: a hidden heading "
                "must not pass the reading contract."
            ),
        ): 1,
    }
)
SUPPRESSION_MARKERS = (
    "biome-ignore",
    "eslint-disable",
    "@ts-nocheck",
    "@ts-ignore",
    "@ts-expect-error",
)
SUPPRESSION_SUFFIXES = (*SCRIPT_SUFFIXES, *STYLE_SUFFIXES, ".html")

#: Every package boundary and the module interpretation it is allowed to impose. The only
#: CommonJS subtree is the retained classic slideshow; adding another package boundary is a
#: reviewable floor change rather than an implicit Biome override.
DECLARED_PACKAGE_MODES: dict[str, tuple[str | None, str]] = {
    "package.json": (None, "private tooling workspace root"),
    "packages/workbench/package.json": ("module", "Node and workbench ES modules"),
    "packing/atlas/known-best/video/spikes/v1-slideshow/assets/package.json": (
        "commonjs",
        "retained slideshow page script intentionally runs as a classic script",
    ),
}

#: How every file must be read by `tsc`: in its own scope, so no two files share a name by it.
MODULE_DETECTION = "force"

#: Reads one repository-relative path from the bead store, or None when it is absent. The
#: reader, the state lookup and the fixture store are `devtools.bead_state`: the guard's
#: allowlist resolves its trackers the same way (#175 R2), and one implementation is what
#: keeps the two from drifting.
BeadReader = bead_state.Reader


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


def _floor_configs() -> list[Path]:
    """Every compiler-options program, including ESLint's lint-only probe program."""
    return [*_tsconfigs(), ESLINT_PROBES]


@cache
def _program_files(config: Path) -> frozenset[Path]:
    """The source files TypeScript includes, resolved once per immutable test config."""
    completed = subprocess.run(
        [str(TSC), "-p", str(config), "--listFilesOnly"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    return frozenset(
        Path(line).resolve()
        for line in completed.stdout.splitlines()
        if line.endswith(SCRIPT_SUFFIXES)
    )


def _covered_scripts(configs: list[Path]) -> set[str]:
    _require_tool(TSC)
    tracked = set(_tracked(*(f"*{suffix}" for suffix in SCRIPT_SUFFIXES)))
    covered: set[str] = set()
    for config in configs:
        if config == TSCONFIG_BASE:
            continue
        for path in _program_files(config):
            try:
                relative = path.relative_to(REPOSITORY_ROOT).as_posix()
            except ValueError:
                continue
            if relative in tracked:
                covered.add(relative)
    return covered


def _probe_typecheck_sources() -> set[str]:
    """The scripts the probe manifest assigns to isolated type programs."""
    manifest = json.loads(PROBE_TYPECHECK_MANIFEST.read_text(encoding="utf-8"))
    sources: set[str] = set()
    for specification in manifest["probeRoots"]:
        root = REPOSITORY_ROOT / specification["path"]
        for group in root.iterdir():
            if group.is_dir():
                sources.update(
                    path.relative_to(REPOSITORY_ROOT).as_posix() for path in group.rglob("*.js")
                )
    for program in manifest.get("standalonePrograms", []):
        sources.update(program["sources"])
    return sources


def _probe_typecheck_files() -> set[str]:
    """Every explicit source and declaration input in the isolated programs."""
    manifest = json.loads(PROBE_TYPECHECK_MANIFEST.read_text(encoding="utf-8"))
    files = _probe_typecheck_sources()
    for specification in manifest["probeRoots"]:
        root = REPOSITORY_ROOT / specification["path"]
        files.update(
            path.relative_to(REPOSITORY_ROOT).as_posix()
            for group in root.iterdir()
            if group.is_dir()
            for path in group.rglob("*.d.ts")
        )
        files.update(specification.get("commonDeclarations", []))
        for declarations in specification.get("dependencies", {}).values():
            files.update(declarations)
    for program in manifest.get("standalonePrograms", []):
        files.update(program.get("declarations", []))
    return files


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


def _require_bead_store() -> BeadReader:
    try:
        return bead_state.require_store()
    except bead_state.UnavailableError as error:
        if os.environ.get("CI"):
            pytest.fail(f"{error}; the job must fetch full history to check trackers")
        return pytest.skip(str(error))


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


def _biome_configuration_faults(
    config: Mapping[str, Any], config_paths: Iterable[str]
) -> list[str]:
    """Every configuration layer that can replace the inspected root rules."""
    faults = ["root Biome config declares extends"] if "extends" in config else []
    faults.extend(
        f"nested Biome config: {path}" for path in sorted(set(config_paths) - {"biome.json"})
    )
    return faults


def _suppression_faults(
    files: Mapping[str, str],
    declared: Counter[tuple[str, str]],
) -> list[str]:
    """Every undeclared suppression and every declared suppression no longer present."""
    observed: Counter[tuple[str, str]] = Counter()
    for path, text in files.items():
        for line in text.splitlines():
            stripped = line.strip()
            if any(marker in stripped for marker in SUPPRESSION_MARKERS):
                observed[(path, stripped)] += 1
    faults = [
        f"undeclared suppression ({count}): {path}: {text}"
        for (path, text), count in sorted((observed - declared).items())
    ]
    faults.extend(
        f"declared suppression missing ({count}): {path}: {text}"
        for (path, text), count in sorted((declared - observed).items())
    )
    return faults


def _package_mode_faults(
    packages: Mapping[str, Mapping[str, Any]],
    declared: Mapping[str, tuple[str | None, str]],
) -> list[str]:
    """Every undeclared package boundary, missing boundary, and changed module mode."""
    faults = [
        f"undeclared package boundary: {path}" for path in sorted(set(packages) - set(declared))
    ]
    faults.extend(
        f"declared package boundary missing: {path}"
        for path in sorted(set(declared) - set(packages))
    )
    faults.extend(
        f"{path}: package type {packages[path].get('type')!r}, expected {mode!r} ({reason})"
        for path, (mode, reason) in sorted(declared.items())
        if path in packages and packages[path].get("type") != mode
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
    """Every added or removed `files.includes` exclusion.

    The declaration is exact in both directions: an extra exclusion can skip owned code, while
    a missing exclusion silently puts installed, vendored, or generated code under the floor.
    """
    observed = frozenset(
        pattern
        for pattern in config.get("files", {}).get("includes", [])
        if pattern.startswith("!")
    )
    faults = [f"Biome excludes {pattern}" for pattern in sorted(observed - BIOME_EXCLUSIONS)]
    faults.extend(
        f"Biome exclusion missing: {pattern}" for pattern in sorted(BIOME_EXCLUSIONS - observed)
    )
    return faults


def _floor_sample_faults(tree: Path, declared: Mapping[str, int]) -> list[str]:
    """Every way the samples' tree differs from its declaration: a file it does not name, a
    file it names that is gone, a changed exact byte count, or a file named as source, which
    a tool's scope would reach."""
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
        f"{name} is {size} bytes, expected exactly {declared[name]}"
        for name, size in sorted(held.items())
        if name in declared and size != declared[name]
    )
    faults.extend(
        f"{name} is named as source"
        for name in sorted(held)
        if name.endswith((*SCRIPT_SUFFIXES, *STYLE_SUFFIXES))
    )
    return faults


def _type_liveness_faults(returncode: int, output: str) -> list[str]:
    """Refuse both a clean type-error sample and a nonzero exit for an unrelated reason."""
    if returncode == 0:
        return ["tsc accepted a type error under the floor's own options"]
    if TYPE_ERROR_DIAGNOSTIC not in output:
        return ["tsc failed without the intended sample.js TS2345 type error"]
    return []


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


def _literal_inline_scripts(source: str) -> list[str]:
    """Script bodies that are executable source rather than one asset placeholder."""
    return [
        body.strip().splitlines()[0]
        for body in SCRIPT_ELEMENT.findall(source)
        if SCRIPT_PLACEHOLDER.fullmatch(body) is None
    ]


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
                suite_c=namespace.suite_c,
                suite_d=namespace.suite_d,
                geometry=namespace.geometry,
                typecheck=namespace.typecheck,
                measure_verifier=namespace.measure_verifier,
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
    assert "eslint.probes.json" in includes
    assert "packing/devtools/probe-typecheck.json" in includes


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


def test_the_root_typecheck_script_names_every_root_type_program() -> None:
    """The convenience command covers the same root programs as the official gate."""
    script = _jsonc(ROOT_PACKAGE)["scripts"]["typecheck"]
    observed = set(re.findall(r"\btsc -p (tsconfig(?:\.[a-z0-9-]+)?\.json)\b", script))
    expected = {
        config.name
        for config in _tsconfigs()
        if config.parent == REPOSITORY_ROOT and config != TSCONFIG_BASE
    }
    assert observed == expected
    assert "npm run typecheck:packing-probes" in script
    assert "npm run typecheck --workspace @squares/workbench" in script


def test_biome_has_no_override_and_no_rule_turned_down() -> None:
    """No exceptions: not floor rule 7's scoped kind, and not the global downgrade that rule
    forbids. Every rule Biome enables is at `error` for every file it reaches."""
    config = _jsonc(BIOME_CONFIG)
    assert _biome_override_faults(config) == []
    assert _biome_downgrade_faults(config) == []
    assert _biome_exclusion_faults(config) == []


def test_biome_has_one_literal_root_configuration() -> None:
    """The contract reads the root file literally, so no inherited or nested config may
    change the rules Biome resolves without changing that file."""
    configs = _tracked("biome.json", "**/biome.json", "biome.jsonc", "**/biome.jsonc")
    assert _biome_configuration_faults(_jsonc(BIOME_CONFIG), configs) == []


def test_an_extended_or_nested_biome_configuration_is_refused() -> None:
    config = {**_jsonc(BIOME_CONFIG), "extends": ["./house.jsonc"]}
    assert _biome_configuration_faults(
        config, ["biome.json", "packing/src/sqpack/motion_lab/assets/biome.json"]
    ) == [
        "root Biome config declares extends",
        "nested Biome config: packing/src/sqpack/motion_lab/assets/biome.json",
    ]


def test_every_recommended_biome_info_rule_is_promoted_to_error() -> None:
    """`--error-on-warnings` does not fail on `info`; explicit promotion makes every
    diagnostic from the pinned recommended preset blocking."""
    rules = _jsonc(BIOME_CONFIG)["linter"]["rules"]
    missing = [
        f"{group}.{rule}"
        for group, names in sorted(RECOMMENDED_INFO_RULES.items())
        for rule in sorted(names)
        if rules.get(group, {}).get(rule) != "error"
    ]
    assert not missing, f"recommended Biome rules still report only info: {missing}"


def test_suppressions_are_exactly_the_declared_accessibility_exceptions() -> None:
    paths = _tracked(*(f"*{suffix}" for suffix in SUPPRESSION_SUFFIXES))
    files = {
        path: (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
        for path in paths
        if (REPOSITORY_ROOT / path).is_file()
    }
    assert _suppression_faults(files, DECLARED_SUPPRESSIONS) == []


def test_an_undeclared_or_unreasoned_suppression_is_refused() -> None:
    files = {
        "x.ts": "// @ts-nocheck\n",
        "y.js": "// eslint-disable-next-line no-undef: generated host global\ny();\n",
    }
    assert _suppression_faults(files, Counter()) == [
        "undeclared suppression (1): x.ts: // @ts-nocheck",
        (
            "undeclared suppression (1): y.js: // eslint-disable-next-line no-undef: "
            "generated host global"
        ),
    ]


def test_package_boundaries_are_exactly_the_declared_module_modes() -> None:
    paths = _tracked("package.json", "**/package.json")
    packages = {path: _jsonc(REPOSITORY_ROOT / path) for path in paths}
    assert _package_mode_faults(packages, DECLARED_PACKAGE_MODES) == []


def test_an_undeclared_commonjs_boundary_is_refused() -> None:
    packages = {path: _jsonc(REPOSITORY_ROOT / path) for path in DECLARED_PACKAGE_MODES}
    packages["packing/devtools/probes/zz/package.json"] = {"type": "commonjs"}
    assert _package_mode_faults(packages, DECLARED_PACKAGE_MODES) == [
        "undeclared package boundary: packing/devtools/probes/zz/package.json"
    ]


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


def test_a_declared_biome_exclusion_cannot_silently_disappear() -> None:
    config = json.loads(json.dumps(_jsonc(BIOME_CONFIG)))
    config["files"]["includes"].remove("!vendor")
    assert _biome_exclusion_faults(config) == ["Biome exclusion missing: !vendor"]


def test_the_floor_samples_are_exactly_the_declared_data() -> None:
    assert _floor_sample_faults(FLOOR_SAMPLES, FLOOR_SAMPLE_BYTES) == []


def test_a_changed_or_sourced_sample_tree_is_refused(tmp_path: Path) -> None:
    """The negative control: a tree with an added file, a missing file, samples changed in
    both byte-count directions, and one sample named as source."""
    for name in FLOOR_SAMPLE_BYTES:
        shutil.copyfile(FLOOR_SAMPLES / name, tmp_path / name)
    shutil.copyfile(FLOOR_SAMPLES / "type-error.js.txt", tmp_path / "type-error.js")
    declared = {
        "braceless-if.js.txt": 35,
        "floating-promise.js.txt": 68,
        "gone.js.txt": 1,
        "probe-undeclared-member.mjs.txt": 162,
    }
    assert _floor_sample_faults(tmp_path, declared) == [
        "holds type-error.js, which is not declared",
        "holds type-error.js.txt, which is not declared",
        "declares gone.js.txt, which is not held",
        "braceless-if.js.txt is 36 bytes, expected exactly 35",
        "floating-promise.js.txt is 67 bytes, expected exactly 68",
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
    for config in _floor_configs():
        if config.name == "tsconfig.base.json":
            continue
        extends = _jsonc(config).get("extends")
        assert isinstance(extends, str)
        assert (config.parent / extends).resolve() == TSCONFIG_BASE.resolve(), (
            f"{config.relative_to(REPOSITORY_ROOT)} does not extend the shared base"
        )


def test_no_program_relaxes_a_flag_outside_the_ratchet() -> None:
    """Only the declared ratchet flags may be off, tracker or no tracker."""
    for config in _floor_configs():
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
    relaxed = {config: _relaxed_flags(config) for config in _floor_configs()}
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
        assert bead_state.dead_trackers(aliases, read) == [], (
            f"{source} names a tracker that is not open"
        )


def test_a_closed_or_unknown_tracker_is_refused(tmp_path: Path) -> None:
    """The negative control for the tracker check, on a fixture store, so it runs wherever
    the real store does not."""
    read = bead_state.fixture_store({"aaaa": "open", "bbbb": "in_progress", "cccc": "closed"})
    assert bead_state.dead_trackers(["think-aaaa", "think-bbbb"], read) == []
    assert bead_state.dead_trackers(["think-aaaa", "think-cccc", "think-zzzz"], read) == [
        "think-cccc: closed",
        "think-zzzz: no such bead",
    ]
    config = tmp_path / "tsconfig.json"
    config.write_text(
        '{\n  // Tracked as think-cccc.\n  "compilerOptions": {"strictNullChecks": false}\n}\n',
        encoding="utf-8",
    )
    assert _relaxed_flags(config) == ["strictNullChecks"]
    named = TRACKER.findall(config.read_text(encoding="utf-8"))
    assert bead_state.dead_trackers(named, read) == ["think-cccc: closed"]


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
    covered = _covered_scripts(_tsconfigs()) | _probe_typecheck_files()
    tracked = _tracked(*(f"*{suffix}" for suffix in SCRIPT_SUFFIXES))
    uncovered = sorted(set(tracked) - covered)
    assert not uncovered, f"tracked JavaScript in no type-check program: {uncovered}"


def test_the_probe_checker_and_contract_name_the_same_sources() -> None:
    """A new group is discovered automatically, while a stale manifest/tool join cannot
    make the coverage contract claim a source the executable gate never reads."""
    _require_tool(TSC)
    completed = node(
        [str(PROBE_TYPECHECK), "--list-sources"],
        return_completed_process=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert set(json.loads(completed.stdout)) == _probe_typecheck_sources()


def test_a_probe_cannot_see_a_foreign_groups_ambient_types(tmp_path: Path) -> None:
    """Negative control: the old monolithic program accepted this exact dependency."""
    _require_tool(TSC)
    alpha = tmp_path / "probes/alpha"
    beta = tmp_path / "probes/beta"
    alpha.mkdir(parents=True)
    beta.mkdir(parents=True)
    shutil.copyfile(PROBE_GROUP_SAMPLES / "alpha-types.txt", alpha / "types.d.ts")
    shutil.copyfile(PROBE_GROUP_SAMPLES / "alpha-read.txt", alpha / "read.js")
    shutil.copyfile(PROBE_GROUP_SAMPLES / "beta-read.txt", beta / "read.js")
    (tmp_path / "manifest.json").write_text(
        json.dumps({"probeRoots": [{"path": "probes"}]}), encoding="utf-8"
    )
    (tmp_path / "tsconfig.json").write_text(
        json.dumps(
            {
                "compilerOptions": {
                    "allowJs": True,
                    "checkJs": True,
                    "noEmit": True,
                    "strict": True,
                    "target": "ES2022",
                    "lib": ["ES2022", "DOM"],
                }
            }
        ),
        encoding="utf-8",
    )
    completed = node(
        [
            str(PROBE_TYPECHECK),
            "--root",
            str(tmp_path),
            "--manifest",
            "manifest.json",
            "--config",
            "tsconfig.json",
        ],
        return_completed_process=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0
    stderr = completed.stderr
    assert isinstance(stderr, str)
    assert "probes/beta/read.js" in stderr
    assert "Cannot find name 'AlphaOnly'" in stderr


def test_the_explainer_shell_owns_no_inline_programs() -> None:
    """HTML is not a Biome/ESLint/tsc input, so every executable body comes from a file."""
    source = render_n11_lower_bounds_explainer.TEMPLATE.read_text(encoding="utf-8")
    assert _literal_inline_scripts(source) == []
    placeholders = {
        match.group(1)
        for body in SCRIPT_ELEMENT.findall(source)
        if (match := SCRIPT_PLACEHOLDER.fullmatch(body)) is not None
    }
    assert placeholders == {
        "THEME_BOOTSTRAP",
        "KATEX_JS",
        *render_n11_lower_bounds_explainer.INLINE_SCRIPT_ASSETS,
    }


def test_a_literal_explainer_program_is_refused() -> None:
    """Negative control: a program written back into the HTML cannot escape the floor."""
    source = render_n11_lower_bounds_explainer.TEMPLATE.read_text(encoding="utf-8")
    planted = source.replace("{{NATIVE_MATH_METRICS}}", "literal program", 1)
    assert _literal_inline_scripts(planted) == ["literal program"]


def test_the_package_program_is_required_for_package_typescript() -> None:
    source = "packages/workbench/src/index.ts"
    configs = _tsconfigs()
    assert source in _covered_scripts(configs)
    assert source not in _covered_scripts(
        [config for config in configs if config.parent == REPOSITORY_ROOT]
    )


def test_type_coverage_respects_effective_exclusions(tmp_path: Path) -> None:
    """A raw include glob must not conceal a file that TypeScript actually excludes."""
    _require_tool(TSC)
    included = tmp_path / "included.ts"
    excluded = tmp_path / "excluded.ts"
    included.write_text("interface Included { value: number }\n", encoding="utf-8")
    excluded.write_text("interface Excluded { value: number }\n", encoding="utf-8")
    config = tmp_path / "tsconfig.json"
    config.write_text(
        json.dumps(
            {
                "compilerOptions": {"noEmit": True},
                "include": ["*.ts"],
                "exclude": ["excluded.ts"],
            }
        ),
        encoding="utf-8",
    )
    resolved = _program_files(config)
    assert included.resolve() in resolved
    assert excluded.resolve() not in resolved


def test_every_job_running_the_liveness_tests_installs_node() -> None:
    """The frontend owner of browser liveness installs the pinned Node toolchain."""
    for workflow in WORKFLOWS:
        document = safe_load(workflow.read_text(encoding="utf-8"))
        assert _jobs_without_node(document, "browser floor liveness tests") == [], workflow.name


def test_a_frontend_job_without_node_is_detected() -> None:
    """The negative control: liveness cannot move to a runner without its toolchain."""
    document = safe_load(WORKFLOWS[0].read_text(encoding="utf-8"))
    document["jobs"]["frontend"]["steps"] = [
        step
        for step in document["jobs"]["frontend"]["steps"]
        if "setup-node" not in str(step.get("uses", ""))
        and "npm ci" not in str(step.get("run"))
    ]
    assert _jobs_without_node(document, "browser floor liveness tests") == ["frontend"]


def test_suite_c_does_not_claim_browser_liveness_without_node() -> None:
    document = safe_load(WORKFLOWS[0].read_text(encoding="utf-8"))
    assert "suite-c" not in _jobs_without_node(document, "browser floor liveness tests")


def test_suite_d_does_not_claim_browser_liveness_without_node() -> None:
    document = safe_load(WORKFLOWS[0].read_text(encoding="utf-8"))
    assert "suite-d" not in _jobs_without_node(document, "browser floor liveness tests")


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


def test_biome_rejects_a_floating_promise_in_typescript(tmp_path: Path) -> None:
    """Biome's type-domain rule needs a project root. A scratch project keeps the known
    violation out of the source tree while exercising the pinned root configuration."""
    _require_tool(BIOME)
    for source in (BIOME_CONFIG, ROOT_PACKAGE, TSCONFIG_BASE, REPOSITORY_ROOT / ".gitignore"):
        shutil.copyfile(source, tmp_path / source.name)
    sample = tmp_path / "sample.ts"
    shutil.copyfile(FLOOR_SAMPLES / "floating-promise.js.txt", sample)
    done = subprocess.run(
        [str(BIOME), "check", f"--config-path={tmp_path}", str(sample)],
        check=False,
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    output = done.stdout + done.stderr
    assert done.returncode != 0, "Biome accepted a floating Promise in TypeScript"
    assert "noFloatingPromises" in output, (
        "Biome complained, but not about the promise rule:\n" + output
    )


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
    assert _type_liveness_faults(done.returncode, done.stdout + done.stderr) == []


def test_an_unrelated_tsc_failure_does_not_satisfy_the_type_liveness_control() -> None:
    assert _type_liveness_faults(2, "error TS18003: No inputs were found in config file") == [
        "tsc failed without the intended sample.js TS2345 type error"
    ]


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


def test_the_probe_loader_refuses_an_undeclared_member(tmp_path: Path) -> None:
    """A probe result stays unknown until its caller states the exact shape it consumes."""
    _require_tool(TSC)
    loader = REPOSITORY_ROOT / "packing/tests/node/probe.mjs"
    shutil.copyfile(FLOOR_SAMPLES / "probe-undeclared-member.mjs.txt", tmp_path / "sample.mjs")
    shutil.copyfile(loader, tmp_path / "probe.mjs")
    (tmp_path / "tsconfig.json").write_text(
        json.dumps(
            {
                "extends": str(REPOSITORY_ROOT / "tsconfig.devtools-node.json"),
                "compilerOptions": {
                    "typeRoots": [str(REPOSITORY_ROOT / "node_modules/@types")]
                },
                "include": ["sample.mjs"],
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
    output = done.stdout + done.stderr
    assert done.returncode != 0, "tsc accepted an undeclared member on a narrowed probe"
    assert "Property 'undeclared' does not exist on type '{ declared: number; }'" in output
