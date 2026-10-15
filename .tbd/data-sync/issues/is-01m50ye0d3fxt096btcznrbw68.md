---
type: is
id: is-01m50ye0d3fxt096btcznrbw68
title: "PR #627 A7: suggestion: records-tier check that frozen claim records' houses match the case record"
kind: bug
status: open
priority: 2
version: 4
delegate: ecstatic-edison-address-627
labels: []
dependencies: []
parent_id: is-01m50gnwbxd5kxbynyx9nd162p
hold: null
hold_until: null
created_at: 2026-10-15T23:30:20.707Z
updated_at: 2026-10-15T23:58:14.735Z
started_at: 2026-10-15T23:30:47.486Z
---
Suggestion. PR #627, review A (https://github.com/jlevy/squares/pull/627#pullrequestreview-5541077630). A main merge that moves a house should fail instead of leaving stale prose. Implement only if small; otherwise a bead under think-wnsv.

## Notes

Deferred from PR #627 review A (A7 suggestion). Not small: upper_bound_reports.live_problems already holds a declaration's houses to the case records, but only when a claim record is written, and frozen records keep the houses they read by design, so a records-tier check needs a rule for which frozen records it holds (for example, only packets whose register entries are still pending adoption, or a read_at_main no older than the last change to the case record at an in-horizon count). Waits on that design decision. The PR #627 instance (A1) was fixed by refreezing at main 22a67ce4a.
