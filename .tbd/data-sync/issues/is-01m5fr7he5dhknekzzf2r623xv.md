---
type: is
id: is-01m5fr7he5dhknekzzf2r623xv
title: Link credit evidence to GitHub issues and pull requests
kind: task
status: in_progress
priority: 2
version: 3
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T17:30:33.796Z
updated_at: 2026-10-21T17:40:37.804Z
started_at: 2026-10-21T17:30:43.351Z
---
Where existing credit/contribution evidence has GitHub issue or PR URLs, render navigable number references with canonical GitHub issue and pull-request branch icons; share component, preserve repository context/accessibility, do not infer unsupported references.

## Notes

Safe exact GitHub issue/PR URL parser, dedupe, typed Octicons and explicit source/registration/supporting evidence joins implemented. Shared helper suites: 37 passed; Ruff and BasedPyright clean; Astra read-only helper review found no blockers. Renderer integration remains in progress.
