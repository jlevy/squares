---
type: is
id: is-01m5q9h14az2vh0xkmmxf98vca
title: "PR #793 (merge): dedicated correctness review B of W7 (checker lemma and write_out, Göbel exactness, window semantics, recipe and deletion rows, hosted custody chain)"
kind: task
status: closed
priority: 1
version: 4
delegate: c-rev-793b-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T15:47:31.593Z
updated_at: 2026-10-24T16:06:57.755Z
started_at: 2026-10-24T15:47:50.118Z
closed_at: 2026-10-24T16:06:57.754Z
close_reason: "Review B (correctness) posted https://github.com/jlevy/squares/pull/793#issuecomment-6386415527: approve after B1 (Medium: lifting #666 breaks the frozen #719 walk's sources; fix verified in scratch); B2-B4 Low; checker, Göbel module and window lift verified against independent oracles."
resolution: null
duplicate_of: null
---

## Notes

c-rev-793b-1024, 2026-10-24: Review B (correctness, round 1) published at https://github.com/jlevy/squares/pull/793#issuecomment-6386415527 against head 6d44159fc. Verdict: approve after B1 is fixed or dispositioned. Findings: B1 Medium (ledger_sources reads held_claims(#666), so lifting #666's window breaks the frozen #719 walk's sources.yaml rebuild); B2 Low (release_sides has no recipe rule; A8's fix as written gives a side one layer low); B3 Low (blob_of skips the digest-to-pin check); B4 Low (later_commits reads only the own walk). Scratch: /tmp/claude-0/-home-user-squares/d57983cc-21aa-53cd-a24f-c90463a5a3c0/scratchpad/rev-793b/. Not synced.
