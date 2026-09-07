---
type: is
id: is-01m1yt2rbhseg2axzvsxzed2f8
title: Exclude raised footnote ink from the list-marker line measurement
kind: bug
status: open
priority: 2
version: 1
labels:
  - defect-class:validity
dependencies: []
parent_id: is-01m1yaa0ggca9jacn9cv4y0y6f
created_at: 2026-09-07T20:48:43.363Z
updated_at: 2026-09-07T20:48:43.363Z
---
The explainer attribution pass added footnotes to single-line reading-list items. The maintained print-layout check reported +2.44px screen and +4.89px print bullet offsets, while PDF inspection showed centered bullets. Diagnose firstLineBox treating raised footnote-reference ink as the ordinary text line; repair the measurement with a regression and retain displaced-marker and mixed-math controls. Also keep the separate real orphan-footnote repair in the paper. This is a bounded W7 validation repair within PR112; no mathematical claim changes.
