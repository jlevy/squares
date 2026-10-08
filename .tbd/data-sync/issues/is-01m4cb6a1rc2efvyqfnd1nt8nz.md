---
type: is
id: is-01m4cb6a1rc2efvyqfnd1nt8nz
title: "PR #427 A3 — Medium: all nine rigidity fields disagree with their owning producer."
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
hold: null
hold_until: null
created_at: 2026-10-07T23:29:16.855Z
updated_at: 2026-10-08T00:20:40.427Z
started_at: 2026-10-08T00:20:31.517Z
closed_at: 2026-10-08T00:20:40.427Z
close_reason: Source fixes9ff422a/6c615115 at f1d7 are independently reviewed E/F/G/H with0newfindings and hosted final-head CI30SUCCESS26documentedSKIP. Focused379+190+3+11owner checks passed; selected broad assertions completed with original capability failure retained and unchanged supported profiler/heavy completions. Actual broad allowance1800 is unchanged. These source findings are fixed; parent422 intake/confirmation/deployment remain open until atomic stack merge and publication.
resolution: null
duplicate_of: null
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
