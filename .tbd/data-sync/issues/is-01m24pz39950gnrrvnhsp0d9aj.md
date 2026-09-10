---
type: is
id: is-01m24pz39950gnrrvnhsp0d9aj
title: "PR139 R4: correct the invalid generic thin-strip stacking capacity"
kind: task
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m24nswnk9b76cq0hdgenfceq
created_at: 2026-09-10T03:49:44.360Z
updated_at: 2026-09-10T04:10:40.538Z
---
Retained lane-x3-box-sweep.py.txt capacity() claims short side below2B implies floor(long/B), false for four strictly separated45degree unit squares in1.99x3.95. Counterexample in publishedreview. Correct/archive-annotate before reuse; area bound remainsvalid and old no-exceedance observations need not become invalid. Does not affect T024-T026. ReviewR4: https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994
