---
type: is
id: is-01m354ty99aychrjcyq62qvwyn
title: Print every figure bound at six decimals
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T18:07:50.052Z
updated_at: 2026-09-22T18:07:50.052Z
---
The owner (2026-09-22): 'use of decimals is okay, just use 6 like we do elsewhere, for consistency. The underlying records should be fully precise and cited.' Stripping trailing zeros made the 324 displays disagree about their precision -- 137 upper/equality displays at six decimals, 8 at five, 2 at four -- so s(17) <= 4.675531 stood beside s(23) <= 5.43689 with no visible reason. _side_text, _upper_text and _lower_text in packing/devtools/build_composite_figure_data.py now share a _six helper that keeps the six decimals as written and leaves a whole number whole (s(100) = 10, never 10.000000). Rounding directions are unchanged. Regenerate the composite record, bound-citations.json, the atlas and the page, extend tests/test_composite_figure_displays.py to hold the width, and re-pin DATA_REVISION.
