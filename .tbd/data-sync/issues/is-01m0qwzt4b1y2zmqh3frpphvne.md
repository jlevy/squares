---
type: is
id: is-01m0qwzt4b1y2zmqh3frpphvne
title: "Engine anchors: sqsearch must recover s(n) at the trivial n, and budget must be monotone"
kind: task
status: open
priority: 0
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-correctness
dependencies:
  - type: blocks
    target: is-01m0pw8698kc2bqm7d7fy0xydy
parent_id: is-01m0rkz14t04yjme92gnfncfv7
created_at: 2026-08-23T18:09:09.771Z
updated_at: 2026-08-24T01:00:52.960Z
---
Anchor sqsearch against proved instances and verify budget accounting. Existing selftests cover n=4 and n=5; add the missing proved ladder cases appropriate to their mechanism, including the proved n=16 not-below-4 guard, and reconcile the recorded n=10 control.

For budget behavior, distinguish two claims. Exact best-so-far monotonicity is valid only for deterministic prefix-coupled runs whose schedule and RNG stream do not depend on the terminal budget. Otherwise compare declared pair-test spend and distributions rather than demanding per-seed monotonicity. Acceptance: the test proves prefix coupling before asserting best(4B) <= best(B), detects move-budget overshoot, records tolerance and seed policy, and never treats lack of improvement as a correctness failure.
