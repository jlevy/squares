---
type: is
id: is-01m1t2x0hrpqkjjzfvapmrwdbq
title: Time the BC-233 inset screen before launch
kind: task
status: closed
priority: 2
version: 2
labels:
  - research
dependencies: []
parent_id: is-01m1t2sgqmantgyx59knjxqheg
created_at: 2026-09-06T00:46:40.183Z
updated_at: 2026-09-06T01:02:20.071Z
closed_at: 2026-09-06T01:02:20.071Z
close_reason: "Recorded on PR 89 in commit c0db25cf: the inset-1/2 screen converged in 191 s wall on the reviewer's host (receipt in agenda-025), the BC-240 duration reads 105 minutes, and agenda-024 tells a fresh worktree to init vendor/kpress before uv runs."
resolution: null
duplicate_of: null
---
BC-233's three inset screens run one column round each under a 540-second deadline and are eligible only if the row loop converges and a candidate is emitted, but the launch spike's zero-budget probes stopped before the first LP round, so no measurement says a 25,34,41-grid one-round screen at 3.82 finishes inside 540 s. Run the inset-1/2 screen once outside the reserved output root and record the wall time and stopping class in agenda-025's launch receipts.
