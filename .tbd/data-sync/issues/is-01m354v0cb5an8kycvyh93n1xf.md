---
type: is
id: is-01m354v0cb5an8kycvyh93n1xf
title: Cross-fade the facts column so the text does not flicker between records
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T18:07:52.202Z
updated_at: 2026-09-22T18:07:52.202Z
---
The owner (2026-09-22): 'can we make sure there's a clean transition on the text as well? It should be fast and smooth. We just don't want it to flicker because we're changing a lot of text between each record.' Every step rewrites most of the facts column at once -- the n heading, the bounds, the citation lines -- and the swap lands on one frame, which reads as a flicker at 60 fps. Give the changed text a short transition (fast, on the order of the desaturation phase, not a slow dissolve), driven off the same clock as the rest so a capture is deterministic and the cadence check still sees a clean CFR stream.
