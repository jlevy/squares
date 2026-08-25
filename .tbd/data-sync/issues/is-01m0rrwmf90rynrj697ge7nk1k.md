---
type: is
id: is-01m0rrwmf90rynrj697ge7nk1k
title: quench_bracket's budget is wall-clock, so results depend on machine load
kind: bug
status: open
priority: 2
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:16:45.800Z
updated_at: 2026-08-25T04:30:00.983Z
---
quench_bracket and _free_sweep take time_budget in seconds and stop on a wall-clock deadline. Host speed, load, pool width, and contention therefore change how many LP solves and angle probes a nominally identical quench performs, making convergence a property of the machine as well as the mathematics.

D-036 already covers an incomplete free sweep returned as complete. On 2026-08-24 this broader risk became observed rather than benign: a 10-wide strict deep gate and a separately isolated one-worker deep golden step both changed the n=4 convergence total and left n=10 at a typed post-check rejection. The isolated step consumed 109 seconds and reproduced the same D-162 golden drift; no tolerance was weakened and no regenerated map was accepted.

Express the scientific budget as work (LP solves or bracket iterations), retain wall time only as an outer recorded safety deadline, and mark any deadline hit censored. Also separate load sensitivity from solver-residual nondeterminism under D-162. Acceptance requires identical retained work and outcomes across declared pool widths and a stable known-answer response at n=4 and n=10.

## Notes

Observed again on merged main 1244634 during the 2026-08-24 readiness audit: with several other full gates active across worktrees, the 30-step normal gate took 118s and the real n=10 D-168 control did not exercise adjacent-cell closure, so the historical-regression step failed. An immediate isolated PACK_JOBS=1 replay passed all 8 regression groups, including D-168, in 43.7s. No threshold changed. This is direct evidence that wall-clock-bounded quench work and host oversubscription can make the gate verdict load-dependent; scientific runs and performance receipts must use work units and declared host load.
