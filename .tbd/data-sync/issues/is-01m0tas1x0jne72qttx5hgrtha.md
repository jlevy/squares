---
type: is
id: is-01m0tas1x0jne72qttx5hgrtha
title: Derive basin-event admissibility from complete fixed-point receipts
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0t4phe1905yy2jk7czp1391
created_at: 2026-08-24T16:48:37.279Z
updated_at: 2026-08-24T16:50:47.772Z
closed_at: 2026-08-24T16:50:47.771Z
close_reason: Fixed by 8f20908 and retained in exp-021 at badb9cb. Every quench-bracket fixed-point evaluation now enters one audited receipt; BasinEvent/v3 derives all-probes, blockers, and scientific admissibility from balanced counts, producer convergence, and independent geometry. The supervised n=3 event retains 2,037/2,037 settled evaluations, independently verifies, replays, and rejects a forged claim. Full 30-step gate passed in 21s. Historical v2 events remain unchanged.
resolution: null
duplicate_of: null
---
D-165. Route every quench-bracket fixed-point evaluation through one audited typed path and derive BasinEvent admissibility from a balanced retained receipt, producer convergence, and independent geometry. Acceptance: a supervised event is scientifically admissible only when all counts balance and no evaluation is unsettled; a forged all-probes claim fails replay; historical v2 events remain unchanged.
