#!/usr/bin/env python3
"""The probes are files, and this is what keeps them honest.

    packing/.venv/bin/python3 check_probes.py

Moving the checkers' JavaScript out of Python string literals bought one thing above all:
the text can now be read by something other than a browser. This is that something. It
asks three questions of every file under `probes/`, and each of them is a failure the old
arrangement could not even express:

1. **Does it parse?** `node` is already a build dependency, for KaTeX. A probe that does
   not parse used to reach the page as a runtime error in a checker step that had already
   spent a minute getting there.

2. **Is it a function?** The contract in `probes.py` is that a probe is one JavaScript
   expression, almost always an arrow function, because Playwright calls it with one
   argument. A probe that evaluates to a string or an object is a probe that will be
   handed to `page.evaluate` and silently returned unevaluated.

3. **Is it reached, and does everything reached exist?** A probe nothing names is dead
   weight that will be edited by someone who thinks it runs; a name no file answers is a
   `FileNotFoundError` at the far end of a slow checker. Both are cheap to find here.

The third question is answered by scanning the checkers for quoted strings rather than by
importing them: the loader is `probe()` today and `look()` wraps it in `check_animate_view`,
and a scan that does not care which helper is used keeps working when a fourth appears.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBES = Path(__file__).resolve().parents[2] / "probes"

#: Every file that may name a probe. Anything scanning for orphans has to read all of
#: them, or a probe used by one checker looks dead to a run that only knew about another.
CALLERS = (
    "animate_view_contract.py",
    "benchmark.py",
    "check_accessibility.py",
    "check_animate_view.py",
    "check_animation_editor.py",
    "check_pack_panel.py",
    "check_page_policy.py",
    "check_search_panel.py",
    "check_stage_resize.py",
    "check_revision6.py",
    "check_candidate.py",
    "capture_stills.py",
    "capture_video.py",
    "smoke_capture.py",
)

#: Asks node to parse each probe and say what it evaluates to. The file is wrapped in
#: parentheses because an arrow function is an expression: `(o) => o` on its own line is a
#: syntax error as a *statement*, which is what a bare `node --check` would read it as.
#:
#: The trailing semicolon is trimmed first, because the formatter puts one there -- the file
#: IS a statement on disk, however it is used -- and a statement terminator inside the
#: wrapping parentheses is a syntax error. Playwright itself does not care either way; it is
#: only this wrapper that has to.
INSPECT = """
const fs = require('fs');
const out = {};
for (const path of process.argv.slice(1)) {
  const source = fs.readFileSync(path, 'utf8').trimEnd().replace(/;$/, '');
  try {
    out[path] = { type: typeof eval('(' + source + ')') };
  } catch (e) {
    out[path] = { error: String(e && e.message ? e.message : e) };
  }
}
process.stdout.write(JSON.stringify(out));
"""


def probe_files() -> list[Path]:
    """Every probe, in a stable order."""
    return sorted(PROBES.rglob("*.js"))


#: The loader. A function whose body hands one of its own parameters to it -- `look` in
#: `check_animate_view`, `_look` in `check_accessibility` -- is found and treated the same.
LOADER = "probe"


def _loaders(tree: ast.Module) -> set[str]:
    """`probe`, and every function in the file that passes a parameter straight to it."""
    loaders = {LOADER}
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        parameters = {a.arg for a in (*node.args.posonlyargs, *node.args.args)}
        for inner in ast.walk(node):
            if (
                isinstance(inner, ast.Call)
                and _called(inner) == LOADER
                and any(isinstance(a, ast.Name) and a.id in parameters for a in inner.args)
            ):
                loaders.add(node.name)
    return loaders


def _called(call: ast.Call) -> str | None:
    match call.func:
        case ast.Name(id=name) | ast.Attribute(attr=name):
            return name
        case _:
            return None


def names_used(callers: Iterable[Path]) -> tuple[set[str], set[str]]:
    """Every quoted string in the checkers, and the ones handed to the probe loader.

    Parsing rather than grepping, so a name inside a comment does not count as a use and a
    name split across an implicit concatenation still does.
    """
    used: set[str] = set()
    loaded: set[str] = set()
    for path in callers:
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        loaders = _loaders(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                used.add(node.value)
            elif isinstance(node, ast.Call) and _called(node) in loaders:
                loaded.update(
                    a.value
                    for a in node.args
                    if isinstance(a, ast.Constant) and isinstance(a.value, str)
                )
    return used, loaded


def name_faults(used: set[str], loaded: set[str], have: set[str]) -> list[str]:
    """Every name a checker uses that no file answers, and every file no checker names.

    A name handed to the loader must resolve, whatever its group: before this, a name was
    checked only when its first segment was an existing probe directory, so a typo in the
    group (`newgroup/zz_missing`) passed here and failed at the far end of a slow checker.
    A string that only *looks* like a probe -- it has a `/` and names an existing group --
    is also checked, because names reach the loader through tuples and loops too; a bare
    word or a file path that no loader call receives is far more often a label.
    """
    groups = {name.split("/")[0] for name in have}
    looks_like = {s for s in used if "/" in s and s.split("/")[0] in groups}
    missing = (loaded | looks_like) - have
    faults = [f"{name}: named by a checker, no such file" for name in sorted(missing)]
    faults.extend(f"{name}: no checker names it" for name in sorted(have - used))
    return faults


def inspect(paths: list[Path]) -> dict[str, dict[str, str]]:
    """What node makes of each file: its type, or the error it raised."""
    if not paths:
        return {}
    done = subprocess.run(
        ["node", "-e", INSPECT, "--", *[str(p) for p in paths]],
        check=False,
        capture_output=True,
        text=True,
    )
    if done.returncode != 0:
        msg = f"node exited {done.returncode}: {done.stderr.strip() or '(no stderr)'}"
        raise RuntimeError(msg)
    return json.loads(done.stdout)


def main() -> int:
    files = probe_files()
    if not files:
        print(f"no probes under {PROBES}")
        return 1

    faults: list[str] = []

    # 1 and 2: it parses, and it is a function.
    for path, verdict in inspect(files).items():
        name = str(Path(path).relative_to(PROBES).with_suffix(""))
        if "error" in verdict:
            faults.append(f"{name}: does not parse -- {verdict['error']}")
        elif verdict["type"] != "function":
            faults.append(f"{name}: evaluates to a {verdict['type']}, not a function")

    # 3: every name resolves, and every file is named.
    have = {str(p.relative_to(PROBES).with_suffix("")) for p in files}
    faults.extend(name_faults(*names_used(HERE / c for c in CALLERS), have))

    for fault in faults:
        print(f"FAIL  {fault}")
    if faults:
        print(f"\n{len(faults)} fault(s) over {len(files)} probes")
        return 1
    print(
        f"OK: {len(files)} probes, every one a function that parses and is named by a checker"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
