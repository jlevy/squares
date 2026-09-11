---
type: is
id: is-01m26vjmtsxx4gdy8j8b95bhfq
title: The terminal-unmeasured state is invisible in the coverage view it was built for
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-10T23:48:48.087Z
updated_at: 2026-09-10T23:48:48.087Z
---
The terminal-unmeasured state landed with #150 and works: session-099 is `status: stopped` with
`resource_usage_unmeasured: {reason: native_harness_data_unavailable}`, and `campaign record` is
green again for commits after 13:50Z. What did not land is the reader-facing half.

`SYNOPSIS.md`'s generated coverage block still reports one number:

```
| Coverage | sessions |
| measured | 80 |
| unmeasured | 45 |
| **total** | **125** |
```

and the prose beside it still names two categories: "Unmeasured sessions include live work
awaiting a retained receipt and older closed sessions whose harness logs were not retained."

That sentence is not false -- "include" is not a claim of exhaustiveness -- but it no longer
names what one of the 45 now is. Session-099 is neither live nor older: it sits above
`GRANDFATHERED_BEFORE = "session-045"` and was deliberately terminalised with an explicit
marker. The whole purpose of that marker is to make a missing measurement visible rather than
silent, and the view a reader actually reads does not show it. The total stayed 45 across the
transition, so nothing in the rendered output changed when the state did.

Underneath, `devtools/close_session.py` emits `sessions_unmeasured` as one integer now carrying
three distinct facts (44 pre-field, any live session awaiting a receipt, and terminal sessions
with an explicit marker), and its generated reason string falls through to
`"declares no rollups"` for a marker-bearing session -- indistinguishable from the silent
omission the marker exists to rule out.

The fix is a split in the generator, not a sentence: a third counter and a third Coverage row,
with the marker's own `reason` and `detail` carried into the per-session entry instead of the
fallback string. Do it in the generator because the prose route was already tried and failed:
bead `is-01m1w3nwm3vpjys7r8mxy2kf06` was the same defect one category earlier, closed
2026-09-06 in PR 103 by rewording SYNOPSIS, which is why it recurred here.

Predicted before #150 landed (see think-7erf) and confirmed against main at e0c2583e.
Nothing is wrong with the arithmetic: every consumer either refuses or skips a missing rollup,
and `close_session.sum_rollups` totals receipts on disk rather than summing sessions, so no
session is ever counted as zero cost. This is a labelling gap only.
