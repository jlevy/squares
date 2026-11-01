---
type: is
id: is-01m6ah2k5saw21a8r8hycw869k
title: "Answer beads closed before the records PR merges break check_bead_tree on main and every branch (31 Oct: twice)"
kind: bug
status: closed
priority: 2
version: 3
delegate: bold-ritchie-l12
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-01T03:05:01.369Z
updated_at: 2026-11-01T17:35:12.105Z
started_at: 2026-11-01T15:39:39.758Z
closed_at: 2026-11-01T17:35:12.105Z
close_reason: Fixed in https://github.com/jlevy/squares/pull/869 (merged 83a2b9132), senior review A addressed, hosted CI green.
resolution: null
duplicate_of: null
---
On 2026-10-31 lanes closed answer beads (think-3xn9/-big9/-n61j/-17wo, then think-3oi5) as soon as their issue was answered on GitHub, while main's result-requests.yaml still listed the issue open with that answer_bead. check_bead_tree reads the live tracker, so every branch's records tier and hosted CI failed until the coordinator reopened them. Options: have check_bead_tree treat an answer bead whose issue is closed on GitHub (or closed in an open PR's record) as satisfied; or have tbd close / the runbook's stage 7 refuse closing a bead an open entry names; or document 'close the answer bead in the same step as the merge' in result-import.md stage 7.
