---
type: is
id: is-01m5qjf1f2nwwdmeanpfwt5vd4
title: "PR #795 (merge): dedicated correctness review B of the walk's data path (push-publications, release_at, _walk_groups, declared_rows, intake_ledger's first-commit tie-break)"
kind: task
status: closed
priority: 1
version: 4
delegate: c-rev-795b-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T18:23:43.586Z
updated_at: 2026-10-24T18:43:54.332Z
started_at: 2026-10-24T18:23:49.028Z
closed_at: 2026-10-24T18:43:54.332Z
close_reason: "Review B (correctness) posted https://github.com/jlevy/squares/pull/795#issuecomment-6388080390: approve with fixes (B1 Medium credit wording at 364/450/874, B2 Medium loosened same-time gate, B3 Low push_publications credit); 185 rows, tie-break and every existing ledger verified."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-795b-1024: Review B (correctness, round 1) published at https://github.com/jlevy/squares/pull/795#issuecomment-6388080390 against head 28508bdb9, base 3480b5fd3. Verdict: approve with fixes; no Blocker or High. B1 Medium: 364/450/874 still left to the owner in source-coverage.yaml:10650/10744/10925/11032, the packet README:435-439 and the PR body, against the coordinator's runbook decision; Measured Identity says 'nothing stated' though the manifest names previous_source there. B2 Medium: intake_ledger problems() no longer refuses a same-instant tie when one claim lacks first_committed; walk sorts it first. B3 Low: push_publications files non-notebook, non-Couzo credit (efef7d1 994, Polkovskyi) under publisher. Independent re-derivation: 40/90/60 claims, 185 recorded + 5 restatements (efef7d1 633 791 856 919 994); all other ledgers byte-identical through release-sources, gather and render; A1-A3 dispositions hold. Scratch: /tmp/claude-0/-home-user-squares/d57983cc-21aa-53cd-a24f-c90463a5a3c0/scratchpad/rev-795b/. Not synced (coordinator syncs).
