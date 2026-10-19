"""The two walk defects the review of 2026-10-14 reproduced, run against today's module.

1. Two pending register bounds that overlap each other: at 1dc253e5e `lowered` returned
   the unlowered record and a claim above both bounds was recorded. The start is now the
   minimal set (`intake_ledger.minimal`), and the claim is not recorded.
2. A frozen lane relation read in one order only: at 1dc253e5e `compare(record, claim)`
   ignored a relation that `compare(claim, record)` used, so a record a claim is decidably
   below stayed in the standing set. `compare` now reads it in both orders.

`bug_demos-output.txt` is what this program prints against the module; the module's tests
hold both cases. The review's own program exercised `lowered`, which no longer exists; the
review (its M4) says what that program printed. From `packing/`, with the project
interpreter::

    python campaign/issue-intake/upper-bounds-20261014/review/bug_demos.py \
        > campaign/issue-intake/upper-bounds-20261014/review/bug_demos-output.txt
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

#: The repository root: this file is packing/campaign/issue-intake/<directory>/review/.
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "packing"))

from devtools import check_standing  # noqa: E402
from devtools import intake_ledger as ledger  # noqa: E402


def entry(label: str, printed: str, rounding: str, when: str, **more: Any) -> ledger.Side:
    claim = cast("ledger.Claim", {"n": 100, "printed": printed, "rounding": rounding, **more})
    report = cast(
        "ledger.Report",
        {
            "report": label,
            "url": "https://github.com/jlevy/squares/issues/1",
            "kind": "issue",
            "holders": f"H {label}",
            "reported_at": when,
            "bead": "",
            "claims": [claim],
        },
    )
    return ledger.entry_side(report, claim)


def overlapping_pending() -> None:
    print("## 1. two pending register bounds that overlap each other")
    record = ledger.record_side(100, {"value": "10.5", "exact_form": "21/2"}, ["T-001"])
    first = ledger.pending_side(
        {"id": "T-901"}, check_standing.Stated(Fraction("10.40"), Fraction(1, 100))
    )
    second = ledger.pending_side(
        {"id": "T-902"}, check_standing.Stated(Fraction("10.405"), Fraction(1, 1000))
    )
    start = [record, first, second]
    print("start:", [side.label for side in ledger.minimal(start)])
    walk = ledger.walk(100, start, [entry("#1", "10.45", "exact", "2026-10-12T01:00:00Z")])
    step = walk.steps[0]
    print(
        "claim #1 = 10.45 (above both pending bounds):",
        step.verdict,
        "against",
        ledger.held_by(step),
    )
    print("expected by the rule: not recorded (above T-901 and T-902)")


def frozen_relation() -> None:
    print("## 2. a frozen relation, read in both orders")
    form = "2 + (1/2)sqrt(2)"
    record = ledger.record_side(5, {"value": "2.70710678118654", "exact_form": form}, ["T-005"])
    relation = {
        "lane": "reported",
        "relation": "below",
        "value": "2.70710678118654",
        "exact_form": form,
        "read_from": "lane",
    }
    claim = entry(
        "#2",
        "2.7071067811865475244008443621048490392848",
        "unstated",
        "2026-10-12T02:00:00Z",
        record_relations=[relation],
    )
    other = entry("#1", "2.70710678118655", "nearest", "2026-10-12T01:00:00Z")
    print("compare(#2, record) =", ledger.compare(claim, record))
    print("compare(record, #2) =", ledger.compare(record, claim))
    walk = ledger.walk(5, record, [other, claim])
    print("verdicts:", [(step.side.label, step.verdict) for step in walk.steps])
    print("standing after the walk:", [side.label for side in walk.standing])
    print("expected by the rule: the record leaves the standing set, since #2 is below it")


if __name__ == "__main__":
    overlapping_pending()
    frozen_relation()
