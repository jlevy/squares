---
type: is
id: is-01m24pz39950gnrrvnhsp0d9aj
title: "PR139 R4: correct the invalid generic thin-strip stacking capacity"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
labels: []
dependencies: []
parent_id: is-01m24nswnk9b76cq0hdgenfceq
created_at: 2026-09-10T03:49:44.360Z
updated_at: 2026-09-10T06:58:13.399Z
closed_at: 2026-09-10T04:36:14.156Z
close_reason: Fixed in d21c27b9; coordinator and separate Astra Max scope review passed, Sol mechanical review passed. Active accounts, source records and historical corrections preserve exact domains, quantifiers, finite-search limits and original scoped negative results. R1 full combined checkpoint remains open separately.
resolution: null
duplicate_of: null
---
Retained lane-x3-box-sweep.py.txt capacity() claims short side below2B implies floor(long/B), false for four strictly separated45degree unit squares in1.99x3.95. Counterexample in publishedreview. Correct/archive-annotate before reuse; area bound remainsvalid and old no-exceedance observations need not become invalid. Does not affect T024-T026. ReviewR4: https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994
