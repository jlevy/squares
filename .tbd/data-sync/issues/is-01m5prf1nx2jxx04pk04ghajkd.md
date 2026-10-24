---
type: is
id: is-01m5prf1nx2jxx04pk04ghajkd
title: "PR #790 (merge): senior review"
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-rev-790-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T10:49:20.829Z
updated_at: 2026-10-24T11:13:22.590Z
started_at: 2026-10-24T10:49:28.083Z
---

## Notes

2026-10-24 c-rev-790-1024: Review A (senior, round 1) of #790 at b4fe44df2 posted as PR comment https://github.com/jlevy/squares/pull/790#issuecomment-6383513133. Verdict: approve after A1. A1 Medium: packet README lines 140 and 145 carry TAB+'imes' for \times. A2 Low: README:146 'part of the way' overstates the geometry. A3 Low: evand read omits 8b2f214; franciscouzo read omits that 797 and 847 restate #763 by print. A4 Low: PR body Release row says 8f48cc11, head pins 3ec97505. Suggestions A5 (read/pin the source's certificates/parents/manifest.json entry for cdd08485 before the #672 final asks how it was made), A6 (control-character check in Markdown math; main's review-2026-10-03-sqverify-fast-soundness.md:357,378,402 has the same bug for \tan), A7 (cite exact_finish.py:68-70 at 1c17153 for the call). Records tier 53/53, focused tests 314 passed 1 skipped.
