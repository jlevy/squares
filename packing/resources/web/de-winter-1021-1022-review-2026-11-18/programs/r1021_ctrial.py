"""Run the controls on synthetic files with each broken copy of the self-test patched in.

Usage: python -I -B r1021_ctrial.py SYNTH_DIR OUT.json

Reads only r1021_synth.py's files.  For the intact programs every control must come out
as stated; for each broken copy (r1021_selftest.MUTANTS) at least one control must not,
or the original must be refused, which shows the controls are not vacuous.  M9 breaks
only the identity measurement, which no control exercises (the self-test catches it).
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

import json
import time

import r1021_controls as ctl
import r1021_selftest as st


def run_controls(kind: str, raws: dict) -> dict:
    plan = json.load(open(ctl.PLAN))
    ids = {c["id"] for c in plan["controls"] if kind in c["applies"]}
    try:
        o = ctl.Original(kind, raws)
    except SystemExit as exc:
        return {"original": f"refused: {exc}", "not_as_stated": ["(original refused)"]}
    except Exception as exc:  # a broken copy that crashes
        return {"original": f"raised {type(exc).__name__}", "not_as_stated": ["(raised)"]}
    try:
        res = ctl.reader_controls(o, ids) + ctl.geometry_controls(o, ids) + ctl.pair_controls(o, ids)
        res.append(ctl.constant_checkers(res))
    except Exception as exc:
        return {"original": "accepted", "not_as_stated": [f"(raised {type(exc).__name__})"]}
    return {"original": "accepted", "ran": len(res), "not_as_stated": [r["id"] for r in res if not r["as_stated"]]}


def main(argv: list[str]) -> int:
    d, out = argv
    raws = {
        "report": {"J": open(_os.path.join(d, "synth_exact.json"), "rb").read(),
                   "C": open(_os.path.join(d, "synth_witness.yaml"), "rb").read()},
        "house": {"H": open(_os.path.join(d, "synth_house.yaml"), "rb").read()},
    }
    rec: dict = {}
    t0 = time.process_time()
    for kind in ("report", "house"):
        rec[f"intact {kind}"] = run_controls(kind, raws[kind])
    for name, apply, undo in st.MUTANTS:
        saved = apply()
        try:
            for kind in ("report", "house"):
                rec[f"{name} / {kind}"] = run_controls(kind, raws[kind])
        finally:
            undo(saved)
    rec["cpu"] = round(time.process_time() - t0, 1)
    intact_ok = all(not rec[f"intact {k}"]["not_as_stated"] for k in ("report", "house"))
    caught = {name: any(rec[f"{name} / {k}"]["not_as_stated"] for k in ("report", "house")) for name, _a, _u in st.MUTANTS}
    # M9 breaks the identity measurement, which decides nothing and which no control exercises;
    # the self-test catches it.  Every broken copy of the checker must be caught here.
    checker = {name: v for name, v in caught.items() if not name.startswith("M9 ")}
    rec["verdict"] = "PASSED" if intact_ok and all(checker.values()) else "FAILED"
    rec["not_a_checker_mutant"] = [name for name in caught if name.startswith("M9 ")]
    rec["caught"] = caught
    with open(out, "w") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    for k, v in rec.items():
        if isinstance(v, dict) and "not_as_stated" in v:
            print(k, "->", v["original"], len(v["not_as_stated"]), v["not_as_stated"][:6])
    print(rec["verdict"], "cpu", rec["cpu"])
    return 0 if rec["verdict"] == "PASSED" else 1


if __name__ == "__main__":
    _sys.exit(main(_sys.argv[1:]))
