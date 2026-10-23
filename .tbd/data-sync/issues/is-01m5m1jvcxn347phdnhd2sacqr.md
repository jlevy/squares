---
type: is
id: is-01m5m1jvcxn347phdnhd2sacqr
title: "Land #750 after T-231 to T-233: merge main, cut the explainer, re-pin"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-land-750-1023
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T09:30:59.357Z
updated_at: 2026-10-23T22:22:18.509Z
started_at: 2026-10-23T22:22:18.508Z
---
PR #750 (branch claude/intake-2026-10-23-lean-sources) registers T-234 to T-236 and cannot merge before T-231 (#753, for issue #719) and T-232, T-233 (#745) are on main: `check_results` requires contiguous register ids, and four register tests and one status test in shards A and B fail on that alone.

Once those land:

1. Merge origin/main into the branch (never rebase), re-render RESULTS.md, INVENTORY.md, STATUS.md, VERIFIERS.md, SYNOPSIS.md, the URL registry and the T-007 consumer audit, and re-run `release_pin --update`.
2. Cut the explainer's successor: it counts the register ("one of N results the framework has registered so far"), 233 on the branch and 230 on main on 23 October, so `check_release_impact` asks for an owning successor of v0.4.21 (or of whatever #753 and #745 cut). `cut_release vX --component paper:n11-lower-bounds-explainer --impact patch --scope "..."` after the merge, with the count measured by rendering twice from each tree, as the 5f8c45a47 cut did.
3. The other three papers (optimality review v0.1.11, threshold-bound review v0.1.4, methods survey v0.2.7) already have a fresh no-public-change record on the branch: rendered twice from each tree against main c1115c095, byte-identical. Re-measure only if their versions moved on main.

Hosted CI should then be green.
