---
type: is
id: is-01m3nqe6bqy3bx879h33d7qycd
title: Generate README's 'Recent Results, All Sources' table from the records (render_recent_results) with typed lineage, a rung rule, and a README count check
kind: feature
status: closed
priority: 1
version: 3
labels:
  - packing
  - documentation
  - wand125-update
dependencies: []
parent_id: is-01m3neehm7hq4apdvzg9925738
created_at: 2026-09-29T04:40:46.199Z
updated_at: 2026-10-06T08:35:44.275Z
closed_at: 2026-10-06T08:35:44.275Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): 8b4488561 (2026-09-29) 'tools: render README's recent results from the register and case records (think-ti71)'; packing/devtools/render_recent_results.py now feeds the site overview that replaced README's table, from the records
resolution: null
duplicate_of: null
---
OR-1: the recent-results listing and its counts have drifted three times by hand. Render README's 'Recent Results, All Sources' table from the results register once it holds others' results (think-z9wy; depends on think-gntk), not from the case files: per n <= 100, both lanes' lower bounds, holder as the bibliography credit prints it, lineage, published date, V/C, case link; splice between BEGIN/END GENERATED markers with --check; guard the README prose counts in check_readme in the shape of check_nagamochi_bounds._README_COUNT.
