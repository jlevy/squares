---
type: is
id: is-01m3te12ggz7rn0gbt5aafsd5v
title: Replace borrowed T-060 unchanged-job timing with its first direct observation
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-10-01T00:32:31.241Z
updated_at: 2026-10-05T23:55:00.304Z
closed_at: 2026-10-05T23:55:00.304Z
close_reason: "The job it measured, n11-optimality-review-unchanged, was removed when #374 folded the *-unchanged placeholder jobs into scope's notices (merged 2026-10-05)."
resolution: null
duplicate_of: null
---
PR259 adds optimality-unchanged, a scope-reason-only notice identical to existing unchanged jobs. gate-budgets.yaml honestly borrows4s measured on run35039355763 for an8s ceiling. When the first unrelated PR exercises this new job successfully, replace the proxy with its actual job/run/time and record any justified ceiling update. No new workflow run is needed solely for this calibration.
