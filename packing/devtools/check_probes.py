#!/usr/bin/env python3
"""Every probe tree in the repository: each probe parses as a function, and is used.

    uv run --frozen --all-extras --group dev python -m devtools.check_probes

A probe is a `.js` file under a directory named `probes`, holding one JavaScript expression
that a Python tool loads through `sqpack.probes` and hands to a page. Moving browser code
out of Python strings bought one thing above all: the text can be read by something other
than a browser. This is that something, and it asks three questions of every probe tree:

1. **Does each probe parse, and is it a function?** A probe that does not parse used to
   reach the page as a runtime error at the far end of a slow browser check. One that
   evaluates to a string or an object is handed to `page.evaluate` and silently returned
   unevaluated. `devtools/node/inspect-probes.mjs` answers both, in Node, without running
   any probe's body.
2. **Is each probe named by a caller?** A probe nothing names is dead weight that someone
   will edit believing it runs.
3. **Does every name a caller uses have a file?** A name no file answers is a
   `FileNotFoundError` at the far end of that same slow check.

A tree's callers are the Python files beside its `probes` directory, at any depth: for
`packing/devtools/probes` that is `packing/devtools/`, and for the workbench package's
`packages/workbench/probes` it is the package. No list of callers is kept by hand, so a
new checker is covered the day it is written.

**Used** means any string literal in a caller equals the name, so a name that reaches the
loader through a tuple, a loop or a helper still counts. That is also why a probe name is
always written out whole: a name assembled at run time is one this cannot see, and the
probe it names reads as dead.

**Missing** is checked two ways, and a name either way catches fails:

- A string literal handed straight to a *loader* must name a file, whatever its group. A
  loader is `probe` as imported from `sqpack.probes` or `workbench_tools.probes`, or any
  function or method beside the tree that passes one of its own parameters straight to a
  loader -- the workbench checkers' `look` and `_look`, the Animate view's `session.look`.
  Before this rule a name was checked only when its first segment was an existing group,
  so `probe("newgroup/zz_missing")` passed (#125 F9, fixed in the workbench checker by
  #160 and applied here).
- A string that only *looks* like a probe -- it contains a `/` and its first segment is a
  group the tree has -- must name a file too, when it is in a file that uses a loader.
  This is how a name in a tuple is caught. A file that uses no loader is left out, because
  a build script beside the workbench's probes names `atlas/known-best/...` paths that are
  files, not probes.

This replaced `packages/workbench/tools/workbench_tools/check_probes.py`, which asked the
same questions of the workbench tree alone from a hand-kept list of fourteen callers.
"""

from __future__ import annotations

import ast
import json
import sys
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from nodejs_wheel import node as run_node

from devtools.check_no_embedded_js import LOADER_MODULES, repository_files

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
INSPECTOR = ROOT / "devtools" / "node" / "inspect-probes.mjs"
DIRECTORY = "probes"
SUFFIX = ".js"
#: The loader's own name, in both modules that export it.
LOADER = "probe"


def probe_trees(files: Iterable[str]) -> dict[str, list[str]]:
    """Each probe root, repository-relative, with the probe files under it.

    The root is the path through the first `probes` segment, so
    `packing/devtools/probes/tool/name.js` belongs to `packing/devtools/probes`.
    """
    trees: dict[str, list[str]] = {}
    for path in files:
        parts = PurePosixPath(path).parts
        if DIRECTORY not in parts[:-1]:
            continue
        cut = parts.index(DIRECTORY) + 1
        trees.setdefault(PurePosixPath(*parts[:cut]).as_posix(), []).append(path)
    return trees


def probe_name(root: str, path: str) -> str:
    return PurePosixPath(path).relative_to(root).with_suffix("").as_posix()


def callers(root: str, python: Iterable[str]) -> list[str]:
    """The Python files beside a probe root, at any depth."""
    base = PurePosixPath(root).parent
    return [path for path in python if PurePosixPath(path).is_relative_to(base)]


@dataclass
class Caller:
    """What one Python file says about probes."""

    #: Every string literal in the file.
    literals: set[str] = field(default_factory=set[str])
    #: The names the file imports the loader under: `probe`, an alias, or `module.probe`.
    imported: set[str] = field(default_factory=set[str])
    #: Every name the file calls, as `_called` spells it.
    called: set[str] = field(default_factory=set[str])
    #: Each call with string literals among its positional arguments: the name, the literals.
    literal_calls: list[tuple[str, tuple[str, ...]]] = field(
        default_factory=list[tuple[str, tuple[str, ...]]]
    )
    #: Each function that passes one of its own parameters to a call: its name, the callee.
    forwards: set[tuple[str, str]] = field(default_factory=set[tuple[str, str]])


def read_caller(source: str, filename: str = "<caller>") -> Caller:
    """One parse of a caller: its literals, its loader imports, its calls and forwards."""
    tree = ast.parse(source, filename=filename)
    caller = Caller()
    for node in ast.walk(tree):
        match node:
            case ast.Constant(value=str() as value):
                caller.literals.add(value)
            case ast.ImportFrom(module=str() as module, names=names):
                for alias in names:
                    local = alias.asname or alias.name
                    if module in LOADER_MODULES and alias.name == LOADER:
                        caller.imported.add(local)
                    elif f"{module}.{alias.name}" in LOADER_MODULES:
                        caller.imported.add(f"{local}.{LOADER}")
            case ast.Import(names=names):
                caller.imported.update(
                    f"{alias.asname or alias.name}.{LOADER}"
                    for alias in names
                    if alias.name in LOADER_MODULES
                )
            case ast.FunctionDef() | ast.AsyncFunctionDef():
                parameters = {a.arg for a in (*node.args.posonlyargs, *node.args.args)}
                caller.forwards.update(
                    (node.name, _called(inner))
                    for inner in ast.walk(node)
                    if isinstance(inner, ast.Call)
                    and any(isinstance(a, ast.Name) and a.id in parameters for a in inner.args)
                )
            case ast.Call():
                name = _called(node)
                caller.called.add(name)
                literals = tuple(
                    a.value
                    for a in node.args
                    if isinstance(a, ast.Constant) and isinstance(a.value, str)
                )
                if literals:
                    caller.literal_calls.append((name, literals))
            case _:
                pass
    return caller


def _called(call: ast.Call) -> str:
    """The name a call reaches: `probe`, `look`, or `probes.probe` for a module alias."""
    match call.func:
        case ast.Name(id=name):
            return name
        case ast.Attribute(value=ast.Name(id=owner), attr=attr):
            return f"{owner}.{attr}"
        case ast.Attribute(attr=attr):
            return attr
        case _:
            return ""


def wrappers(files: Mapping[str, Caller]) -> set[str]:
    """Every function beside a tree that passes one of its parameters to a loader.

    Found to a fixed point, so a wrapper of a wrapper counts, and matched across the tree's
    files by bare name, so `session.look` in one file is the `look` another file's
    `Session` defines. The workbench's own `probe(name)`, which forwards to the shared
    loader, is one of these.
    """
    found: set[str] = set()
    while True:
        more = {
            function
            for caller in files.values()
            for function, callee in caller.forwards
            if _loads(callee, caller.imported | found)
        }
        if more <= found:
            return found
        found |= more


def _loads(called: str, loaders: set[str]) -> bool:
    """Whether a call reaches a loader: by its full name, or a method by its bare name."""
    return called in loaders or called.rsplit(".", 1)[-1] in loaders


def name_faults(files: Mapping[str, Caller], have: set[str]) -> tuple[list[str], list[str]]:
    """Names a caller uses that no file answers, and files no caller names."""
    forwarding = wrappers(files)
    groups = {name.split("/")[0] for name in have if "/" in name}
    wanted: set[str] = set()
    used: set[str] = set()
    for caller in files.values():
        used |= caller.literals
        loaders = caller.imported | forwarding
        # Handed straight to a loader: must resolve, whatever its group.
        wanted.update(
            literal
            for called, literals in caller.literal_calls
            if _loads(called, loaders)
            for literal in literals
        )
        # Looks like a probe, in a file that loads probes: must resolve too.
        if caller.imported or any(_loads(called, loaders) for called in caller.called):
            wanted.update(s for s in caller.literals if "/" in s and s.split("/")[0] in groups)
    return sorted(wanted - have), sorted(have - used)


def inspect(repo: Path, paths: list[str]) -> dict[str, dict[str, str]]:
    """What Node makes of each file: `{"type": ...}` or `{"error": ...}`, by path."""
    if not paths:
        return {}
    done = run_node(
        [str(INSPECTOR), *paths],
        return_completed_process=True,
        capture_output=True,
        text=True,
        cwd=repo,
        check=False,
    )
    if done.returncode != 0:
        stderr = str(done.stderr).strip() or "(no stderr)"
        raise RuntimeError(f"node exited {done.returncode}: {stderr}")
    verdicts = json.loads(str(done.stdout))
    if not isinstance(verdicts, dict) or set(verdicts) != set(paths):
        # A partial answer would let an unread probe pass as a clean one.
        raise RuntimeError("the probe inspector did not report on every probe it was given")
    return verdicts


def faults(repo: Path) -> tuple[list[str], int, int]:
    """Every fault, the number of probes read, and the number of trees they are in."""
    trees = probe_trees(repository_files(repo, SUFFIX))
    python = repository_files(repo, ".py")
    parsed: dict[str, Caller] = {}
    found: list[str] = []
    count = 0
    for root, files in sorted(trees.items()):
        count += len(files)
        for path, verdict in sorted(inspect(repo, files).items()):
            if "error" in verdict:
                found.append(f"{path}: does not evaluate -- {verdict['error']}")
            elif verdict.get("type") != "function":
                found.append(f"{path}: evaluates to a {verdict.get('type')}, not a function")
        for path in callers(root, python):
            if path not in parsed:
                parsed[path] = read_caller((repo / path).read_text(encoding="utf-8"), path)
        beside = {path: parsed[path] for path in callers(root, python)}
        have = {probe_name(root, path) for path in files}
        missing, unnamed = name_faults(beside, have)
        found.extend(
            f"{root}/{name}{SUFFIX}: named by a Python file beside {root}, and no such file"
            for name in missing
        )
        found.extend(
            f"{root}/{name}{SUFFIX}: no Python file beside {root} names it" for name in unnamed
        )
    return found, count, len(trees)


def main() -> int:
    found, count, trees = faults(REPO)
    if count == 0:
        # The repository has probes by construction; finding none means the scan broke.
        found.append(f"no probe files found under {REPO}")
    for fault in found:
        print(f"FAIL  {fault}")
    if found:
        print(f"\n{len(found)} fault(s) over {count} probes in {trees} tree(s)")
        return 1
    print(
        f"OK: {count} probes in {trees} tree(s), every one a function that evaluates and is "
        "named by a Python file beside it"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
