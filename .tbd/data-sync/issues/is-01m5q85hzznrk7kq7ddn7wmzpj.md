---
type: is
id: is-01m5q85hzznrk7kq7ddn7wmzpj
title: "PR #793 (merge): senior review of W7, the code slice for rows above 1024"
kind: task
status: closed
priority: 1
version: 4
delegate: c-rev-793-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T15:23:47.071Z
updated_at: 2026-10-24T15:47:30.883Z
started_at: 2026-10-24T15:23:52.269Z
closed_at: 2026-10-24T15:47:30.882Z
close_reason: "Review A posted https://github.com/jlevy/squares/pull/793#issuecomment-6386210280: approve once A1, A3, A4 (Medium) are fixed or dispositioned; A2, A5-A10 Low; A11-A13 suggestions; correctness review recommended (focus listed) and a security pass on hosted_shards.py."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-793-1024: Review A (senior, round 1) of PR #793 at 6d44159 published as a PR comment: https://github.com/jlevy/squares/pull/793#issuecomment-6386210280. Verdict: approve after A1, A3, A4 (Medium) are fixed or dispositioned; no Blocker or High; 7 Low (A2, A5-A10), 3 suggestions (A11-A13). Tests: 529 passed, 1 skipped; --records 53/53; 16 of 18 in-memory guard mutations fail their tests (Göbel-receipt and claims-record byte checks have no refusal test, A5). Recommended Review B focus: checker lemma and write_out geometry, Göbel exactness, window/walk_of semantics once a release is lifted, recipe-row certificate_n and dating (A8), and the hosted fast-path custody chain (A3, A6, A7).
