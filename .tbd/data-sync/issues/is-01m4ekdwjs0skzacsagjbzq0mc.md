---
type: is
id: is-01m4ekdwjs0skzacsagjbzq0mc
title: "PR #456: scope Pages workflow changes to publication tests in the local push cycle"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e2d5gyj7m218hm9f5g01xd
hold: null
hold_until: null
created_at: 2026-10-08T20:31:42.653Z
updated_at: 2026-10-08T20:32:24.680Z
started_at: 2026-10-08T20:32:24.679Z
---
An edit to seven Pages publication job dependencies selected all640 test files through a generic .github fallback; the local push attempt reached its1800s ceiling. Introduce an explicit defensible Pages workflow input/contract closure for local change-reachable selection. Preserve whole-suite fallback for Packing and unknown workflow changes, keep every existing fast CI partition and gate, and prove the selected closure with positive/negative contract controls and an actual final push run. Record this as an efficiency block in the active site plan; no budget increases or waived checks.
