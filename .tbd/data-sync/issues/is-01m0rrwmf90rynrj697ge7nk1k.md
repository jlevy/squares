---
type: is
id: is-01m0rrwmf90rynrj697ge7nk1k
title: quench_bracket's budget is wall-clock, so results depend on machine load
kind: bug
status: open
priority: 2
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:16:45.800Z
updated_at: 2026-08-30T10:37:37.222Z
---
quench_bracket and _free_sweep take time_budget in seconds and stop on a wall-clock deadline. Host speed, load, pool width, and contention therefore change how many LP solves and angle probes a nominally identical quench performs, making convergence a property of the machine as well as the mathematics.

D-036 already covers an incomplete free sweep returned as complete. On 2026-08-24 this broader risk became observed rather than benign: a 10-wide strict deep gate and a separately isolated one-worker deep golden step both changed the n=4 convergence total and left n=10 at a typed post-check rejection. The isolated step consumed 109 seconds and reproduced the same D-162 golden drift; no tolerance was weakened and no regenerated map was accepted.

Express the scientific budget as work (LP solves or bracket iterations), retain wall time only as an outer recorded safety deadline, and mark any deadline hit censored. Also separate load sensitivity from solver-residual nondeterminism under D-162. Acceptance requires identical retained work and outcomes across declared pool widths and a stable known-answer response at n=4 and n=10.

## Notes

2026-08-30 session-045: BC-017 advanced, not closed. The first sentence of its next_evidence was already discharged before the slice started -- the source-free n=3 full-cell control retains a target-free tagged execution plan with every wall and pair role visible, and its execution-plan forged-count, omitted-row, replay and role-swap controls all pass. Its own promotion_boundary says passing authorizes exactly a BC-016 or BC-017 readiness decision, so the slice produced that decision's input instead of another receipt. Measured on the same three-square subject: the structural plan reports 4 seated-wall equalities and 8 open-wall inequalities against 2 contact equalities and 1 non-edge inequality; solve_cell builds 12 containment rows and 3 pair rows. The same twelve and the same three -- every total agrees and every composition does not. Exactly one unit survives all three vocabularies, the LP solve attempt, and it is the unit this commitment's exit names, so the LP-solve half is reachable now. pair_tests does not transfer: compiled rows in the structural plan, dynamic overlap tests in sqsearch, so the exit's pair-test total is not one number until which sense is meant is decided, and that is a judgement rather than a measurement. Target-free throughout; no stratum is priced. Evidence: devtools/audit_work_accounting.py, campaign/series/series-000-smoke-and-calibration/results/bc-017-work-accounting.json, tests/test_work_accounting.py. Next action: someone takes the readiness decision the n=3 control's promotion_boundary authorizes; then freeze the numerical semantics; then real n=5 and n=10 counted executions agreeing across pool width and host load. An unattended runner may not take that decision alone.
