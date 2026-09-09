---
type: is
id: is-01m23fn82bcsk9rdnpfh30j43s
title: "Fix D-489: corner-dual salvage screen refuses any mass-n source"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T16:22:47.115Z
updated_at: 2026-09-09T16:22:47.115Z
---
D-489. `devtools/screen_corner_dual_salvage.py:_source_receipt` requires the source
family's `verify_ceiling` receipt to carry `failures == ["K3 total weight at least n"]`
exactly (`DEPTH_FAILURE`, lines 253-254). That is the failure a family records when its
total weight is BELOW n, so the predicate accepts only a family short of mass n and
refuses every proved ceiling family, whose `failures` list is empty.

The screen's whole purpose is weak duality: delete from a depth-one family the members
meeting a class's guaranteed patch, and read the survivor weight as a lower bound on that
class's residual cover value. That bound is only as strong as the source family's mass, so
the predicate hard-wires the instrument to produce a weak bound while reading like a
soundness guard.

Cost already paid: exp-137, exp-138 and exp-141 all screened
`.../results/agenda-025/bc-232-leg-01-family.json` of mass `10.384212`, `0.6158` short of
eleven. Their reported shortfalls (`0.582567` one-corner, `0.482906` four-corner) are both
SMALLER than that deficit, so `obstructs: false` on all 48 rows was the source's missing
mass rather than a fact about conditioning. Re-run on the mass-eleven ceiling family, the
same `screen_footprint` reads survivor weight exactly 10 at four of the sixteen classes --
which is the measurement that reversed the campaign's direction, and it could have been
made a day earlier with the instrument as built.

The fix:

1. Keep the clauses deletion-only inheritance actually needs: exact `max_depth == "1"`,
   `regime == "net"`, `symmetric_only is True`, and total weight agreeing with the
   placements.
2. Drop the equality on `failures`. A family that PASSES the mass threshold is the
   strictly better source for this instrument, not a disqualified one. If any filtering is
   wanted at all, refuse only failures that bear on depth.
3. Record the source's total weight in the receipt beside each class's survivor weight,
   and derive the deficit `n - total`. A reader could then see at a glance how much of a
   reported shortfall is the source's rather than the conditioning's -- the arithmetic
   that would have caught this in the receipt itself.
4. Regression: a test that screens a mass-`n` source and asserts it is ACCEPTED (there is
   none today in `packing/tests/test_screen_corner_dual_salvage.py`), plus a control that
   a survivor weight is never reported without its source's total beside it.

Re-run exp-137 and exp-138 against the mass-eleven family once the predicate admits it,
and register the results; lane X1 replayed `screen_footprint` directly rather than through
the CLI, so there is no receipt for the corrected numbers.

Narrative: agenda-033 lane X1
(packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-x1-corner-conditioning-is-mass-neutral.md).
Register entry: D-489 in `packing/defects.yaml`.
