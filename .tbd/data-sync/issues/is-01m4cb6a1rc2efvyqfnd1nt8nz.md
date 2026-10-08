---
type: is
id: is-01m4cb6a1rc2efvyqfnd1nt8nz
title: "PR #427 A3 — Medium: all nine rigidity fields disagree with their owning producer."
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
hold: null
hold_until: null
created_at: 2026-10-07T23:29:16.855Z
updated_at: 2026-10-08T00:20:31.517Z
started_at: 2026-10-08T00:20:31.517Z
---
Review https://github.com/jlevy/squares/pull/427#pullrequestreview-5449633758 head83748.

**A3 — Medium: all nine rigidity fields disagree with their owning producer.**
`packing/devtools/squish_second_update_packets.py` clears the selected records’
`rigidity` fields, while `packing/devtools/assess_frontier_rigidity.py:313` requires the
assessment derived from the current inputs.
The actual full-gate run `aa80c2ea572c4151887f38c5cad0a25b` records all nine counts as
stale. This is a consistency failure; it does not justify asserting positive rigidity.

**Fix:** refresh the nine fields through `assess_frontier_rigidity`, preserving the
exact scope and strength of its assessment.
Reconcile report redrafting with that producer so a later record regeneration does not
erase the owned assessment.
Check both redraft stability and the producer’s check mode.
