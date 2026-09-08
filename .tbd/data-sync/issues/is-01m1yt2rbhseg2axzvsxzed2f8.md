---
type: is
id: is-01m1yt2rbhseg2axzvsxzed2f8
title: Exclude raised footnote ink from the list-marker line measurement
kind: bug
status: closed
priority: 2
version: 2
labels:
  - defect-class:validity
dependencies: []
parent_id: is-01m1yaa0ggca9jacn9cv4y0y6f
created_at: 2026-09-07T20:48:43.363Z
updated_at: 2026-09-07T21:08:46.881Z
closed_at: 2026-09-07T21:08:46.881Z
close_reason: Completed the requested attribution and clarity follow-up in PR115, commit7108dc1a, after PR112 merged. Narrative uses surnames; source history, contribution details, and the intervening-improvement qualification are in footnotes. The new eleven-square bound is stated directly and the MemoIII page10 link is retained. Fixed D480 with a browser-derived regression;22 focused tests and45 final pre-push steps passed (80.08seconds). Screen/print layout and PDF visual/link checks passed, all required PR CI and the paper build passed, and the local preview/PDF were refreshed. The existing research handoff and think-0krc remain in force.
resolution: null
duplicate_of: null
---
The explainer attribution pass added footnotes to single-line reading-list items. The maintained print-layout check reported +2.44px screen and +4.89px print bullet offsets, while PDF inspection showed centered bullets. Diagnose firstLineBox treating raised footnote-reference ink as the ordinary text line; repair the measurement with a regression and retain displaced-marker and mixed-math controls. Also keep the separate real orphan-footnote repair in the paper. This is a bounded W7 validation repair within PR112; no mathematical claim changes.
