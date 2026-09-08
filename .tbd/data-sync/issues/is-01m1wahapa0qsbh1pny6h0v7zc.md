---
type: is
id: is-01m1wahapa0qsbh1pny6h0v7zc
title: Validate negative-control environment in the isolated full gate
kind: task
status: closed
priority: 1
version: 4
spec_path: packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md
labels: []
dependencies: []
parent_id: is-01m1w140k75zvvqpvj55e8k9my
created_at: 2026-09-06T21:38:34.815Z
updated_at: 2026-09-06T22:06:47.980Z
closed_at: 2026-09-06T22:06:47.979Z
close_reason: Isolated environment cause reproduced and documented. Originala105full1447.15s passed all othersteps; corrected full failed-step replay exited0/all163negativecontrols. No dependency changes or expectation weakening; total replay process cost unavailable.
resolution: null
duplicate_of: null
---
Full gate on a105f729 completed1447.15s with exactly one failed step:67/163negative controls failed on module/pytest import traces inside private negctl worker venvs. All mathematical/exhaustive steps passed. Diagnose environment versus harness bug with focused controls before any source fix; do not rerun the24-minute full suite blindly. Preserve projectPython3.14, do not repoint the shared editable venv, weaken controls, or create a separatePR. Supporting correction/replay remains integrated101.

## Notes

Diagnosis retained cf299e6c. Complete failed-step replay with explicit existing UV_PROJECT_ENVIRONMENT finished: all163negative controls fired; retain exact process completion and cost in next record. Original a105 full invocation remains one failed step; all its other steps passed. Separate workflow-snapshot fix think-lpoq in flight on integrated101.
