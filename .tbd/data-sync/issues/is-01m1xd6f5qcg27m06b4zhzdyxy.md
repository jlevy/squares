---
type: is
id: is-01m1xd6f5qcg27m06b4zhzdyxy
title: "Phase 1: parameterize build_known_best_atlas and the figure-data tool by range and composite list; 1-100 byte-identical"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md
labels: []
dependencies:
  - type: blocks
    target: is-01m1xd6ffzyzddb7by875t49z4
  - type: blocks
    target: is-01m1xd6g45jsz4p8735rteqyfy
parent_id: is-01m1xd517vezdmp4hrmvs5c8bp
created_at: 2026-09-07T07:44:19.127Z
updated_at: 2026-09-07T08:18:14.319Z
closed_at: 2026-09-07T08:18:14.318Z
close_reason: Builder, figure-data tool and PDF renderer parameterized by CorpusRange and CompositeSpec; 1-100 family byte-identical (git status empty over the family, renderings, witnesses and frontier); 26 tests, atlas/figure/PDF checks and schemas pass.
resolution: null
duplicate_of: null
---
Replace the ~34 hard-coded range/layout sites in devtools/build_known_best_atlas.py (SUMMARY_FIRST_N/LAST_N/COLUMNS/ROWS, canvas, absolute legend/footer baselines, range(1,101), filename sets, manifest checks) with a corpus range and a list of composite specifications (first_n, last_n, columns, stem). Same for build_composite_figure_data.py and render_composite_pdf.py. Schema constants become per-collection values. Regression: the known-best-1-100 svg/png/pdf family is byte-identical before and after.
