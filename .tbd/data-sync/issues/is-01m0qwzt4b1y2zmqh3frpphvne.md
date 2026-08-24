---
type: is
id: is-01m0qwzt4b1y2zmqh3frpphvne
title: "Engine anchors: sqsearch must recover s(n) at the trivial n, and budget must be monotone"
kind: task
status: in_progress
priority: 0
version: 10
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: unknown@spud10.local
labels:
  - focus-correctness
dependencies:
  - type: blocks
    target: is-01m0pw8698kc2bqm7d7fy0xydy
parent_id: is-01m0rkz14t04yjme92gnfncfv7
hold: null
hold_until: null
created_at: 2026-08-23T18:09:09.771Z
updated_at: 2026-08-24T18:48:19.842Z
started_at: 2026-08-24T18:39:12.483Z
---
Anchor sqsearch against proved instances and verify budget accounting. Existing selftests cover n=4 and n=5; add the missing proved ladder cases appropriate to their mechanism, including the proved n=16 not-below-4 guard, and reconcile the recorded n=10 control.

For budget behavior, distinguish two claims. Exact best-so-far monotonicity is valid only for deterministic prefix-coupled runs whose schedule and RNG stream do not depend on the terminal budget. Otherwise compare declared pair-test spend and distributions rather than demanding per-seed monotonicity. Acceptance: the test proves prefix coupling before asserting best(4B) <= best(B), detects move-budget overshoot, records tolerance and seed policy, and never treats lack of improvement as a correctness failure.

## Notes

2026-08-24 BC-008 now explicitly gates the size ladder after exp-030: random-start BasinEvent/v3 is validated through complete blocks n=3..8 and one n=9 performance event. Before n=10, add a source-bound seeded-pose entry that perturbs the proved n=10 witness, retain the full start and endpoint, replay independent validity, and distinguish return-to-known-answer from random-search performance. Do not substitute another blind random-start block.

2026-08-24 source-start checkpoint: `gobel10-svg-v1` reconstructs the published Göbel n=10 witness and binds URL plus SHA-256; BasinEvent/v3 retains deterministic perturbations and rejects source/start tampering. All 36 prior events replay. A one-second real smoke run reached a valid endpoint at the proved side and retained a typed time-budget stop. BC-008 is ready, not complete: preregister and run four 15-second perturbations under the 90-second cap.
