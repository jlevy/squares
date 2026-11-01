#!/usr/bin/env python3
"""Which of the checker's checks each of its eleven per-row controls exercises (stage 4
review of the filled-end lemma, PR #870).

This program runs the code under review, `devtools.filled_end_checker`, and never edits
it: it parses the module's source, and for each ``_refuse(...)`` call in `decide`,
`band` and `_stated` compiles an in-memory variant with that one call deleted. At each
sampled row it decides the row's controls (`mutants`) with every variant. A control
*exercises* a check when deleting the check makes the control accepted (or makes the
checker raise something other than its refusal). A check no control exercises is one a
deletion would leave every control refused.

With ``--baseline-all`` it also decides every control of every V2.0 row with the
unmodified checker and classifies each change's refusal by the message's check, so the
receipt shows whether each control is refused, at every row, by the check it names
(the lane's receipts keep only a boolean per control). It also probes a candidate
control for 0 < t, each tilt negated, with and without the tilt check.

    python -I fe_checker_mutation.py PACKING_DIR OUT.json [--baseline-all] N...
"""

from __future__ import annotations

import ast
import hashlib
import json
import platform
import re
import sys
import time
import types
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path

#: Each refusal message's check, by the message's own words.
REASONS = (
    ("kind", r"not a filled-end packing"),
    ("n >= 1", r"no squares to pack"),
    ("S > 0", r"is not positive"),
    ("2 <= K <= MAX_K", r"the checker decides 2 <= K"),
    ("S <= K", r"is above K = "),
    ("0 < t < 1", r"tan\(theta/2\) must lie in"),
    ("1 <= b <= K - 1", r"a band is 1 to K - 1"),
    ("layers of all four ends or none", r"all four band ends or of none"),
    ("V fit", r"passes the right wall"),
    ("H fit", r"passes the top wall"),
    ("h <= L", r"deep, is longer than its length"),
    ("y >= 0", r" lift .* is negative"),
    ("y <= F", r"lift passes its free length"),
    ("m_i >= 0", r"-end layer \d+ holds -\d+ squares"),
    ("m_i <= W - a_i", r"crosses the band's end row"),
    ("n <= capacity", r"is above the capacity"),
)
#: The check each control names.
NAMED = {
    "count above the capacity": "n <= capacity",
    "side below the binding fit": "V fit",
    "V lift past its free length": "y <= F",
    "H lift past its free length": "y <= F",
    "a V near-end layer one over": "m_i <= W - a_i",
    "a V far-end layer one over": "m_i <= W - a_i",
    "an H near-end layer one over": "m_i <= W - a_i",
    "an H far-end layer one over": "m_i <= W - a_i",
    "no tilt": "0 < t < 1",
    "a right angle": "0 < t < 1",
    "unknown kind": "kind",
}


def reason(message: str) -> str:
    found = [name for name, pattern in REASONS if re.search(pattern, message)]
    return found[0] if len(found) == 1 else f"unclassified: {message[:80]}"


def sites(tree: ast.Module) -> list[tuple[str, int, int, str]]:
    found = []
    for function in tree.body:
        if isinstance(function, ast.FunctionDef) and function.name in ("decide", "band", "_stated"):
            for node in ast.walk(function):
                if (
                    isinstance(node, ast.Expr)
                    and isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and node.value.func.id == "_refuse"
                ):
                    found.append((function.name, node.lineno, node.col_offset, ast.unparse(node.value.args[0])))
    return found


class Drop(ast.NodeTransformer):
    def __init__(self, line: int, column: int) -> None:
        self.line, self.column = line, column

    def visit_Expr(self, node: ast.Expr):  # noqa: N802
        if node.lineno == self.line and node.col_offset == self.column:
            return ast.copy_location(ast.Pass(), node)
        return node


def variant(source: str, path: Path, line: int | None, column: int | None, name: str) -> types.ModuleType:
    tree = ast.parse(source, filename=str(path))
    if line is not None:
        tree = ast.fix_missing_locations(Drop(line, column).visit(tree))
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(tree, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


def outcomes(module: types.ModuleType, row) -> dict[str, dict]:
    """Each control's changes decided by one variant: refused (with each change's check),
    accepted, or crashed."""
    found = {}
    try:
        controls = module.mutants(row)
    except Exception as error:  # noqa: BLE001
        return {"(mutants)": {"verdict": "crashed", "checks": {type(error).__name__: 1}}}
    for control, changes in controls:
        kinds: Counter = Counter()
        for changed in changes:
            try:
                module.decide(changed)
            except module.FilledEndRefusedError as error:
                kinds[reason(str(error))] += 1
            except Exception as error:  # noqa: BLE001
                kinds[f"crashed: {type(error).__name__}"] += 1
            else:
                kinds["accepted"] += 1
        verdict = "refused"
        if kinds["accepted"]:
            verdict = "accepted"
        elif any(key.startswith("crashed") for key in kinds):
            verdict = "crashed"
        found[control] = {"verdict": verdict, "checks": dict(kinds)}
    return found


def negative_tilt(checker, source: str, path: Path, found_sites, rows, counts) -> dict:
    """A candidate control for 0 < t: each tilt negated in turn, decided by the unmodified
    checker and by the variant without the tilt check. It isolates that check where the
    variant accepts it."""
    line, column = next((s[1], s[2]) for s in found_sites if "tilt" in s[3])
    module = variant(source, path, line, column, "fe_mut_tilt")
    tally: Counter = Counter()
    for n in counts:
        row = rows[n]
        for name, changed in (
            ("tH -> -tH", replace(row, tilt_h=-row.tilt_h)),
            ("tV -> -tV", replace(row, tilt_v=-row.tilt_v)),
        ):
            try:
                checker.decide(changed)
                unmodified = "accepted"
            except checker.FilledEndRefusedError as error:
                unmodified = reason(str(error))
            try:
                module.decide(changed)
                without = "accepted"
            except module.FilledEndRefusedError as error:
                without = reason(str(error))
            except Exception as error:  # noqa: BLE001
                without = f"crashed: {type(error).__name__}"
            tally[f"{name} | unmodified: {unmodified} | without the tilt check: {without}"] += 1
    del sys.modules["fe_mut_tilt"]
    return dict(sorted(tally.items()))


def main() -> int:
    packing = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2])
    rest = sys.argv[3:]
    baseline_all = "--baseline-all" in rest
    counts = [int(a) for a in rest if a != "--baseline-all"]
    sys.path.insert(0, str(packing))
    from devtools import filled_end_checker as checker  # noqa: PLC0415

    path = Path(checker.__file__)
    source = path.read_text(encoding="utf-8")
    found_sites = sites(ast.parse(source))
    rows = {row.n: row for row in checker.records(checker.V2)}
    started = time.process_time()
    base = variant(source, path, None, None, "fe_mut_base")
    baseline = {n: outcomes(base, rows[n]) for n in counts}
    by_site = []
    for index, (function, line, column, condition) in enumerate(found_sites):
        module = variant(source, path, line, column, f"fe_mut_{index}")
        flipped: dict[str, Counter] = defaultdict(Counter)
        refused_by: dict[str, Counter] = defaultdict(Counter)
        for n in counts:
            for control, item in outcomes(module, rows[n]).items():
                flipped[control][item["verdict"]] += 1
                if item["verdict"] == "refused":
                    for check in item["checks"]:
                        refused_by[control][check] += 1
        by_site.append(
            {
                "function": function,
                "line": line,
                "condition": condition,
                "controls_no_longer_refused": {
                    control: dict(tally) for control, tally in flipped.items() if tally["refused"] != len(counts)
                },
                "refused_instead_by": {
                    control: dict(refused_by[control])
                    for control in flipped
                    if NAMED[control] not in refused_by[control] and refused_by[control]
                },
            }
        )
        del sys.modules[f"fe_mut_{index}"]
    summary_baseline = {
        control: dict(Counter(check for n in counts for check in baseline[n][control]["checks"]))
        for control in checker.CONTROLS
    }
    negative = negative_tilt(checker, source, path, found_sites, rows, counts)
    every = None
    if baseline_all:
        tally: dict[str, Counter] = defaultdict(Counter)
        verdicts: dict[str, Counter] = defaultdict(Counter)
        for row in rows.values():
            for control, item in outcomes(base, row).items():
                verdicts[control][item["verdict"]] += 1
                for check, times in item["checks"].items():
                    tally[control][check] += times
        every = {
            "rows": len(rows),
            "verdicts": {control: dict(verdicts[control]) for control in checker.CONTROLS},
            "changes_by_check": {control: dict(tally[control]) for control in checker.CONTROLS},
            "every_change_refused_by_the_check_named": all(
                set(tally[control]) == {NAMED[control]} for control in checker.CONTROLS
            ),
        }
    receipt = {
        "program": "fe_checker_mutation.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "environment": {"python": platform.python_version(), "machine": platform.machine()},
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rows": counts,
        "baseline_checks_over_sample": summary_baseline,
        "negative_tilt_probe": negative,
        "baseline_all_v2": every,
        "sites": by_site,
        "unexercised_checks": [
            f"{site['function']}:{site['line']} {site['condition']}"
            for site in by_site
            if not site["controls_no_longer_refused"]
        ],
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"unexercised_checks": receipt["unexercised_checks"], "cpu": receipt["cpu_seconds"]}, indent=1))
    for site in by_site:
        print(site["function"], site["line"], site["condition"][:60], "->", site["controls_no_longer_refused"], site["refused_instead_by"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
