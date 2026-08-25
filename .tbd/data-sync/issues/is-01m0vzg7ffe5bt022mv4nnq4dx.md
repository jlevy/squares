---
type: is
id: is-01m0vzg7ffe5bt022mv4nnq4dx
title: Correct false R6 blocker caused by omitted dx4 coordinate
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-037-h-023-n5-tangent-inventory.md
labels:
  - packing
  - measurement
dependencies: []
parent_id: is-01m0vyht9k2p9mahn03w8c1kbx
created_at: 2026-08-25T08:10:02.606Z
updated_at: 2026-08-25T08:10:02.606Z
---
A delegated diagnostic omitted dx4=-1/2 when constructing R6, then reported exact negative contact residuals and a hard source/formula inconsistency. Coordinator replay of the complete vector showed all six matrices feasible with only the two x-upper slacks positive. Correct constructor and retain physical support checks.
