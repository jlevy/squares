---
type: is
id: is-01m5pwb2kmk5xd6tfkzyhh4h3y
title: "Import the 99 Kaggle-credited sides franciscouzo/square-packing published at 964ee2b (pushed 2026-10-23T23:38:42Z): 87 certificates and 12 recipes at 325-1024, each 1.46e-4 to 6.60e-2 below main's record, credited to notebook authors (no issue)"
kind: task
status: open
priority: 1
version: 3
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m5pjxq31vpw03t0emgwnvhfe
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T11:57:05.011Z
updated_at: 2026-10-24T11:57:23.422Z
---

## Notes

2026-10-24 coord-intake-1024, from #789 review B (B1, High, deferred here as the review allows): https://github.com/jlevy/squares/pull/789#issuecomment-6383901035. The 23:38:42Z push that published 964ee2b also put into Couzo's repository sides credited to Kaggle notebook authors at 99 counts in 325-1024: 87 certificates, 12 recipes, 1.46e-4 to 6.60e-2 below main's record at e5c1c64e3, disjoint from #763's counts. A certificate in a watched repository is a report from its first commit (the owner, 2026-10-14), so each is a report at 23:38:42Z, ahead of 43f666c (46 of the 99 overlap 43f666c's 126 counts, where think-cncq assumed 964ee2b's side stands). The list: scratchpad rev-789b/others-below-main-964ee2b.tsv (n327 and n994 checked against GitHub). Next: stage 1 triage of credit (notebook authors, the parents manifest), then import before think-gn29's walk; recipes wait on the D2 checker.
blocked_on: think-ptkk
