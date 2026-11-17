---
type: is
id: is-01m6njad7kd4rxmaye77mf39nt
title: "T-257's bibliography credit names the 260 start's finder by handle (kirilltym), F10 of the #895 review"
kind: task
status: open
priority: 3
version: 1
labels:
  - attribution
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-05T09:58:24.755Z
updated_at: 2026-11-05T09:58:24.755Z
---
F10 of the 5 November 2026 stage 4 review of #895 (docs/project/reviews/review-2026-11-05-yim-895-260.md), repeating M-1 of the 31 October review of T-257: the bibliography's credit for `[Daniel issue 845 2026-10-29]` (`packing/resources/bibliography.yaml`, the `credit` line, "Daniel after Chaoweeraprasit, Gupta, Ostashev, kirilltym, Friedman") still names the 260 start's finder by the handle "kirilltym", where the register and the newer key `[Yim s260 upper bound 2026-11-05]` write "Tymchishin" (attribution.md, one identity under several labels).

Not a one-line change, so lane L48 left it out of PR #911: the credit line has six spans in `packing/contributors/occurrences.yaml` (expected_text and offsets), five of them resolved, and "Friedman"'s offsets move with the longer name; `contributor_census --reconcile` would drop and re-propose the resolved joins for re-review. The short credit, the bound citations and the atlas metadata that read the line may move too.

Done when: the credit reads "Tymchishin" (or whatever the owner's identity review decides), the six spans are carried over with their resolved joins kept, and `contributor_census --stale`, `build_bound_citations --check` and the atlas check pass.
