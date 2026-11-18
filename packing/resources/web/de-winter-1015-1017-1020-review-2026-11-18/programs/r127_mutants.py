"""Run the self-test against broken copies of the programs: each must fail it.

Lane r127-1118.  Written for this review.

    python -I -B r127_mutants.py --work SCRATCH_DIR --out OUT.json

Each mutant copies every r127_*.py into its own new directory under SCRATCH_DIR,
applies its stated textual replacements (each old text must occur exactly once), runs
the copied r127_selftest.py with the same interpreter, and records its exit status and
the number of failed checks it printed.  The verdict is ALL_MUTANTS_FAIL when every
mutant's self-test fails at least one check, and the unmutated copy passes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

MUTANTS = [
    ("A uses only the first square's axes", "r127_axes.py",
     [("return max(_sep_on(a, 0, b), _sep_on(a, 1, b), _sep_on(b, 0, a), _sep_on(b, 1, a))",
       "return max(_sep_on(a, 0, b), _sep_on(a, 1, b))")]),
    ("A measures the separation on one side only", "r127_axes.py",
     [("s = max(lo_b - hi_a, lo_a - hi_b)", "s = lo_b - hi_a")]),
    ("A's unit test without perpendicularity", "r127_axes.py",
     [("        and E[0][0] * E[1][0] + E[0][1] * E[1][1] == 0\n", "")]),
    ("A takes the right clearance from the least x", "r127_axes.py",
     [("side - Fraction(max(xs), a.D),", "side - Fraction(min(xs), a.D),")]),
    ("A counts a zero margin as apart", "r127_axes.py",
     [('return "apart" if m > 0 else', 'return "apart" if m >= 0 else')]),
    ("B with open point-in-polygon and crossing tests", "r127_area.py",
     [("cross(poly[i], poly[(i + 1) % k], p) >= 0", "cross(poly[i], poly[(i + 1) % k], p) > 0"),
      ("if 0 <= t <= 1 and 0 <= u <= 1:", "if 0 < t < 1 and 0 < u < 1:")]),
    ("B skips the edge crossings", "r127_area.py",
     [("cand += seg_intersections(P, Q)", "cand += []")]),
    ("B's unit test by its sides alone", "r127_area.py",
     [("ok = ok and d2(pts[0], pts[2]) == 2 and d2(pts[1], pts[3]) == 2", "ok = ok"),
      ("ok = ok and (s == 2 or s == -2)", "ok = ok")]),
    ("B calls a zero-area intersection apart", "r127_area.py",
     [("    if area == 0:\n        return \"contact\", ZERO", "    if area == 0:\n        return \"apart\", ZERO")]),
    ("B's wall test calls a touch clear", "r127_area.py",
     [('out.append("clear" if npts == 0 else', 'out.append("clear" if area == 0 else')]),
    ("the closed form's half-extent doubled", "r127_frame.py",
     [("return (abs(u[0]) + abs(u[1])) / 2", "return abs(u[0]) + abs(u[1])")]),
    ("the closed form's threshold without the sine", "r127_frame.py",
     [("return (1 + abs(cosd) + abs(sind)) / 2", "return (1 + abs(cosd)) / 2")]),
    ("the YAML reader lets a duplicate key through", "r127_read.py",
     [("if value in top:", "if False:")]),
    ("the readers ignore the stated count", "r127_read.py",
     [('if len(squares) != w["n"]:', "if False:"),
      ("if not isinstance(sq, list) or len(sq) != n:", "if not isinstance(sq, list):")]),
    ("the readers allow a leading plus", "r127_read.py",
     [('RATIONAL = re.compile(r"(-?)(0|', 'RATIONAL = re.compile(r"([-+]?)(0|')]),
    ("the decision ignores wall crossings", "r127_decide.py",
     [('if ca == "cross" or cb == "cross":', "if False:"),
      ("if d.insideB[i] != 1:", "if False:")]),
    ("the contraction takes the least factor", "r127_contract.py",
     [("if best is None or lam > best:", "if best is None or lam < best:")]),
    ("the twin comparison reads only the first corner", "r127_twin.py",
     [("if set(a) != set(b):", "if a[0] not in b:")]),
]


def run_copy(work: str, name: str, edits) -> dict:
    d = os.path.join(work, name)
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for f in os.listdir(HERE):
        if f.startswith("r127_") and f.endswith(".py"):
            shutil.copy(os.path.join(HERE, f), d)
    for fname, pairs in edits:
        path = os.path.join(d, fname)
        t = open(path).read()
        for old, new in pairs:
            if t.count(old) != 1:
                return {"error": f"{fname}: replacement text occurs {t.count(old)} times: {old[:60]}"}
            t = t.replace(old, new)
        open(path, "w").write(t)
    proc = subprocess.run([sys.executable, "-I", "-B", os.path.join(d, "r127_selftest.py")],
                          capture_output=True, text=True, timeout=1800)
    m = re.search(r"failures=(\d+)", proc.stdout)
    return {"exit": proc.returncode, "failures": int(m.group(1)) if m else None,
            "first_lines": proc.stdout.strip().split("\n")[:4] + proc.stderr.strip().split("\n")[-2:]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    base = run_copy(a.work, "m00-unmutated", [])
    rows = []
    for k, (what, fname, pairs) in enumerate(MUTANTS, 1):
        r = run_copy(a.work, f"m{k:02d}", [(fname, pairs)])
        failed = r.get("exit", 0) != 0 and (r.get("failures") or 0) >= 1
        rows.append({"mutant": k, "what": what, "file": fname,
                     "replacements": [[o, n] for o, n in pairs], **r, "fails_selftest": failed})
        print(f"m{k:02d} {what}: exit={r.get('exit')} failures={r.get('failures')} {r.get('error', '')}")
    ok = base.get("exit") == 0 and all(r["fails_selftest"] for r in rows)
    out = {"program": "r127_mutants.py", "unmutated": base, "mutants": rows,
           "verdict": "ALL_MUTANTS_FAIL" if ok else "SOME_MUTANT_PASSES"}
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"unmutated: exit={base.get('exit')} failures={base.get('failures')}; verdict {out['verdict']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
