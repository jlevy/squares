---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: open
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: null
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-14T05:34:39.468Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

Merged origin/main aeef99ef0 into successor PR578 at eee90ffa5, repinned c855228e6, pushed and clean. Five conflicts resolved; Astra reviewed and accepted. Citation/results regenerated, two Daniel spans joined, stale empty, URLs1020zero failures. Focused309passed; the single precommit HEAD-tree test then passed after commit, plus ceiling check (2passed). Final push prereqs66/66passed. Broad local test phase interrupted for external scratch capacity at about500MBfree (exit130), not a passing full local gate. Hosted exacthead c855228e6/base aeef99ef0:31passed26skipped0failed0pending. Packing38516257725, Pages38516257747, mergeability38516256278. Current requested integration complete; release bead for future main landings. PR remains draft, not merged.
