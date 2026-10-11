---
type: is
id: is-01m3qknj2hpeb1d7tyv4kvqgh5
title: Make CI wall recent-run sampling aware of gate event surfaces
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T22:13:22.127Z
updated_at: 2026-10-06T08:34:51.665Z
closed_at: 2026-10-06T08:34:51.665Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): Event-aware sampling integrated at 902b959b4 (on origin/main): check_ci_gate_walls.py maps post-merge to push/schedule/workflow_dispatch; PR #246 MERGED with published CI green
resolution: null
duplicate_of: null
---
Post-merge live wall reporting and explicit --run-id work, but --sample --recent discovers successful pull_request runs only. Add event-aware discovery for push/schedule/workflow_dispatch while preserving exact declared-job/source-topology admission. Until then use explicit run IDs for post-merge baseline measurements; do not claim automatic recent sampling works for this surface.

## Notes

Integrated at 902b959b4 and independently reviewed through a2b8e696c. Recent sampling has gate-specific event surfaces, globally deduplicated bounded discovery, exact successful current-topology admission, retained payload reuse, and explicit insufficiency refusal. Focused evidence: 29 tests passed; Ruff/format and BasedPyright clean; native_sol review found no blocker. Ordinary explicit run inspection remains available. Keep in progress until the integrated tree passes published CI.
