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
importing them: the loader is `probe()` today and `look()` wraps it in `check_workbench`,
and a scan that does not care which helper is used keeps working when a fourth appears.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBES = HERE / "probes"

#: Every file that may name a probe. Anything scanning for orphans has to read all of
#: them, or a probe used by one checker looks dead to a run that only knew about another.
CALLERS = (
    "check_workbench.py",
    "check_revision6.py",
    "check_revision7.py",
    "check_legend.py",
    "test_candidate.py",
)

#: Asks node to parse each probe and say what it evaluates to. The file is wrapped in
#: parentheses because an arrow function is an expression: `(o) => o` on its own line is a
#: syntax error as a *statement*, which is what a bare `node --check` would read it as.
INSPECT = """
const fs = require('fs');
const out = {};
for (const path of process.argv.slice(1)) {
  try {
    out[path] = { type: typeof eval('(' + fs.readFileSync(path, 'utf8') + ')') };
  } catch (e) {
    out[path] = { error: String(e && e.message ? e.message : e) };
  }
}
process.stdout.write(JSON.stringify(out));
"""


def probe_files() -> list[Path]:
    """Every probe, in a stable order."""
    return sorted(PROBES.rglob("*.js"))


def names_used() -> set[str]:
    """Every probe name any checker mentions, as a quoted string.

    Parsing rather than grepping, so a name inside a comment does not count as a use and a
    name split across an implicit concatenation still does.
    """
    used: set[str] = set()
    for caller in CALLERS:
        path = HERE / caller
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                used.add(node.value)
    return used


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
    used = names_used()
    # A string is a probe reference when a probe answers it; a name nothing answers is
    # only a fault if it *looks* like one, which is the one heuristic here -- a bare word
    # in a checker is far more often a label than a missing probe.
    groups = {name.split("/")[0] for name in have}
    missing = {s for s in used if "/" in s and s not in have and s.split("/")[0] in groups}
    faults.extend(f"{name}: named by a checker, no such file" for name in sorted(missing))
    faults.extend(f"{name}: no checker names it" for name in sorted(have - used))

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
