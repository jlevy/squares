"""The controls against two constant checkers, after the freeze (lane r127b-1118).

Written after the findings were frozen. Usage:

    python -I -B rb127_constant.py LABEL EXACT.json WITNESS.yaml CLAIM CONTROLS.json OUT.json

It runs the frozen controls of the geometry, side, extent and contraction groups with the
decision replaced by two constant checkers: one that accepts everything and one that
refuses everything. Each wraps the frozen ``rb127_decide.decide``, keeps its rows and
overrides only its verdict and problems, so a control fails under a constant checker
exactly when its stated verdict is the other one. ``CONTROLS.json`` is the real run's
receipt, from which each control's real verdict is read. The plan works when the
accept-everything checker fails every control whose real verdict is a refusal, and the
refuse-everything checker every control whose real verdict is an acceptance. It decides
nothing about a certificate.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rb127_controls as CT  # noqa: E402
import rb127_decide as D  # noqa: E402

GROUPS = ("geometry_controls", "side_controls", "extent_controls", "contraction_controls")


def run_with(kind: str, jb: bytes, cb: bytes, claim: str) -> list[str]:
    real = D.decide

    def constant(*args, **kw):
        dec = real(*args, **kw)
        full = kw.get("squares") is None and kw.get("pairs") is None
        if kind == "always-accept":
            dec["verdict"] = "ACCEPT" if full else "PARTIAL"
            dec["problems"] = []
        else:
            dec["verdict"] = "REFUSE"
            dec["problems"] = ["refused by the constant checker"]
        return dec

    D.decide = constant
    try:
        run = CT.Runner("constant", "pair", jb, cb, claim)
        for g in GROUPS:
            getattr(run, g)()
    finally:
        D.decide = real
    return sorted(r["control"] for r in run.results if not r["as_stated"])


def main(argv: list[str]) -> int:
    if len(argv) != 7:
        print(__doc__)
        return 2
    label, jp, cp, claim, receipt, out = argv[1:7]
    jb, cb = Path(jp).read_bytes(), Path(cp).read_bytes()
    real = json.loads(Path(receipt).read_text(encoding="utf-8"))
    verdicts = {r["control"]: r["outcome"].get("verdict") for r in real["results"]
                if isinstance(r.get("outcome"), dict) and "verdict" in r["outcome"]}
    group_ids = {"G1", "G2", "G3", "G4", "G5", "G6", "G7", "S1a", "S1b", "S1c", "S1d", "S1e", "S1f",
                 "E1c", "E1p", "K1c", "K1p", "K1s"}
    must_refuse = sorted(c for c, v in verdicts.items() if c in group_ids and v == "REFUSE")
    must_accept = sorted(c for c, v in verdicts.items() if c in group_ids and v in ("ACCEPT", "PARTIAL"))
    acc = run_with("always-accept", jb, cb, claim)
    ref = run_with("always-refuse", jb, cb, claim)
    rec = {
        "program": "rb127_constant.py",
        "label": label,
        "must_refuse_by_real_verdict": must_refuse,
        "must_accept_by_real_verdict": must_accept,
        "always_accept_fails": acc,
        "always_refuse_fails": ref,
        "always_accept_fails_every_must_refuse": set(must_refuse) <= set(acc),
        "always_refuse_fails_every_must_accept": set(must_accept) <= set(ref),
    }
    rec["plan_catches_both"] = rec["always_accept_fails_every_must_refuse"] and rec["always_refuse_fails_every_must_accept"]
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(label, "always-accept fails", len(acc), "of", len(must_refuse), "must-refuse;",
          "always-refuse fails", len(ref), "of", len(must_accept), "must-accept;", "both caught:", rec["plan_catches_both"])
    return 0 if rec["plan_catches_both"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
